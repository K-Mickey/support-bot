import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, Message

from bin.dialogflow import get_intent_answer
from bin.settings import settings
from bin.utils import split_message

logger = logging.getLogger(__name__)


class SupportBot:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token

    async def run(self):
        async with Bot(token=self.bot_token).context() as bot:
            await bot.set_my_commands(
                commands=[
                    BotCommand(command='start', description='Запустить бота'),
                ]
            )

            dp = Dispatcher()
            dp.message.register(self.dialogflow)
            await dp.start_polling(bot)

    @staticmethod
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
        answers = [
            response.query_result.fulfillment_text for response in responses
        ]
        logger.info(f'Answers: {answers}')
        await message.answer('\n\n'.join(answers))


if __name__ == '__main__':
    logging.basicConfig(level=settings.log_level, format=settings.log_format)
    asyncio.run(
        SupportBot(
            bot_token=settings.tg_token,
        ).run()
    )
