from aiogram import Router
from aiogram.types import Message

from app.dialogflow import get_intent_answer
from app.settings import settings

router = Router()


@router.message()
async def dialogflow(message: Message):
    texts = message.text.split('.')
    answers = get_intent_answer(
        project_id=settings.project_id,
        session_id=str(message.from_user.id),
        texts=texts,
        language_code=settings.language_code,
    )
    await message.answer('\n\n'.join(answers))
