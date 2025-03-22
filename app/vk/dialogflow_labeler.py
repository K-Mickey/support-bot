import logging

from vkbottle.bot import BotLabeler, Message

from app.dialogflow import get_intent_answer
from app.settings import settings
from app.utils import split_message

bl = BotLabeler()
logger = logging.getLogger(__name__)


@bl.message()
async def dialogflow(message: Message):
    logger.debug(f'Got message: {message}')
    texts = split_message(message.text)
    logger.debug(f'After split: {texts}')
    if not texts:
        return

    responses = get_intent_answer(
        project_id=settings.project_id,
        session_id=str(message.from_id),
        texts=texts,
        language_code=settings.language_code,
    )

    logger.debug(f'Responses: {responses}')
    answers = [
        response.query_result.fulfillment_text
        for response in responses
        if not response.query_result.intent.is_fallback
    ]
    if answers:
        logger.info(f'Answers: {answers}')
        await message.answer('\n\n'.join(answers))
