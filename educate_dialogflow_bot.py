import json

from environs import env

env.read_env()
PROJECT_ID = env.str("Project_ID")
LANGUAGE_CODE = "en-US"
TRAINING_PHRASES = env.str('TRAINING_PHRASES')


def get_data_json_from_url(url: str) -> dict:
    with open(url, "r", encoding="UTF-8") as my_file:
        file_contents = my_file.read()
    return json.loads(file_contents)


def create_intent(project_id: str, display_name: str, training_phrases_parts: list, message_texts: list) -> None:
    """Create an intent of the given intent type."""
    from google.cloud import dialogflow

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def train_bot(data: dict) -> None:
    for intent in data:
        name = intent
        questions = data[intent]['questions']
        answer = [data[intent]['answer']]
        create_intent(PROJECT_ID, name, questions, answer)


def main():

    data = get_data_json_from_url(TRAINING_PHRASES)
    train_bot(data)


if __name__ == '__main__':
    main()