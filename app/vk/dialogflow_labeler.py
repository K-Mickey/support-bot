from vkbottle.bot import BotLabeler, Message

from app.dialogflow import get_intent_answer
from app.settings import settings

bl = BotLabeler()


@bl.message()
async def echo(message: Message):
    texts = message.text.split('.')
    answers = get_intent_answer(
        project_id=settings.project_id,
        session_id=str(message.from_id),
        texts=texts,
        language_code=settings.language_code,
    )
    await message.answer('\n\n'.join(answers))
