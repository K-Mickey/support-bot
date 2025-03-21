from typing import Iterable

from google.cloud import dialogflow
import logging

logger = logging.getLogger(__name__)


def get_indent_answer(project_id: str, session_id: str, texts: Iterable[str], language_code: str) -> list[str]:
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    answers = []
    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        logger.debug("Query text: {}".format(response.query_result.query_text))
        logger.debug(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )
        logger.debug("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
        answers.append(response.query_result.fulfillment_text)
    return answers
