import logging
from typing import Iterable, MutableSequence

from google.cloud import dialogflow
from google.cloud.dialogflow_v2 import DetectIntentResponse, Intent
from google.cloud.dialogflow_v2.services.intents.pagers import ListIntentsPager

logger = logging.getLogger(__name__)


def get_intent_answer(
    project_id: str, session_id: str, texts: Iterable[str], language_code: str
) -> list[DetectIntentResponse]:
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    responses = []
    for text in texts:
        text_input = dialogflow.TextInput(
            text=text, language_code=language_code
        )
        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={'session': session, 'query_input': query_input}
        )

        logger.debug('Query text: {}'.format(response.query_result.query_text))
        logger.debug(
            'Detected intent: {} (confidence: {})\n'.format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )
        logger.debug(
            'Fulfillment text: {}\n'.format(
                response.query_result.fulfillment_text
            )
        )
        responses.append(response)
    return responses


def create_intent(
    project_id: str,
    display_name: str,
    training_phrases_parts: Iterable[str],
    message_texts: MutableSequence[str],
) -> Intent:
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part
        )
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message],
    )
    response = intents_client.create_intent(
        request={'parent': parent, 'intent': intent}
    )

    logger.info('Intent created: {}'.format(response.display_name))
    return response


def list_intents(project_id: str) -> ListIntentsPager:
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    intents = intents_client.list_intents(request={'parent': parent})

    logging.info('Intents:')
    for intent in intents:
        logging.debug('=' * 20)
        logging.info('Intent display_name: {}'.format(intent.display_name))
        logging.debug('Action: {}\n'.format(intent.action))
        logging.debug(
            'Root followup intent: {}'.format(intent.root_followup_intent_name)
        )
        logging.debug(
            'Parent followup intent: {}\n'.format(
                intent.parent_followup_intent_name
            )
        )

        logging.debug('Input contexts:')
        for input_context_name in intent.input_context_names:
            logging.debug('\tName: {}'.format(input_context_name))

        logging.debug('Output contexts:')
        for output_context in intent.output_contexts:
            logging.debug('\tName: {}'.format(output_context.name))

    return intents


def delete_intent(project_id: str, intent_name: str):
    intent_id = intent_name.split('/')[-1]
    intents_client = dialogflow.IntentsClient()
    intent_path = intents_client.intent_path(project_id, intent_id)
    intents_client.delete_intent(request={'name': intent_path})
    logger.info('Intent deleted: {}'.format(intent_name))
