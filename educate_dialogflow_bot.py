import json

from environs import env
import requests

env.read_env()
PROJECT_ID = env.str("Project_ID")
LANGUAGE_CODE = "en-US"


def get_data_json_from_url(url: str) -> dict:
    data = requests.get(url).content
    data_json = json.loads(data)
    return data_json


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

    data_url = 'https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json'
    data = get_data_json_from_url(data_url)
    train_bot(data)


if __name__ == '__main__':
    main()