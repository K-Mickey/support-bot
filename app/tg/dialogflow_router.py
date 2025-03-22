import logging

from aiogram import Router
from aiogram.types import Message

from app.dialogflow import get_intent_answer
from app.settings import settings
from app.utils import split_message

router = Router()
logger = logging.getLogger(__name__)


@router.message()
async def dialogflow(message: Message):
    logger.debug(f'Got message: {message}')
    texts = split_message(message.text)
    logger.debug(f'After split: {texts}')
    if not texts:
        return

    responses = get_intent_answer(
        project_id=settings.project_id,
        session_id=str(message.from_user.id),
        texts=texts,
        language_code=settings.language_code,
    )

    logger.debug(f'Got responses: {responses}')
    answers = [response.fulfillment_text for response in responses]
    logger.info(f'Answers: {answers}')
    await message.answer('\n\n'.join(answers))
