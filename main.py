import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from app.settings import settings
from app.support_router import router as support_router


class SupportBot:
    def __init__(self, bot_token: str, log_format: str, log_level: str):
        self.bot_token = bot_token

        self.log_format = log_format
        self.log_level = log_level

    async def run(self):
        async with Bot(token=self.bot_token).context() as bot:
            logging.basicConfig(level=self.log_level, format=self.log_format)

            await bot.set_my_commands(
                commands=[
                    BotCommand(command='start', description='Запустить бота'),
                ]
            )

            dp = Dispatcher()
            dp.include_router(support_router)
            await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(
        SupportBot(
            bot_token=settings.bot_token,
            log_format=settings.log_format,
            log_level=settings.log_level,
        ).run()
    )
