from aiogram import Router
from aiogram.types import Message

from app.dialogflow import get_indent_answer
from app.settings import settings

router = Router()


@router.message()
async def echo(message: Message):
    answers = get_indent_answer(
        project_id=settings.project_id,
        session_id=str(message.from_user.id),
        texts=[message.text],
        language_code=settings.language_code,
    )
    await message.answer('\n\n'.join(answers))
