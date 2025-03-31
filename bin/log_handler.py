import asyncio
import logging

from aiogram import Bot


class TelegramLogsHandler(logging.Handler):
    def __init__(self, bot: Bot, chat_id: str):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        message = self.format(record)
        if len(message) > 1000:
            message = message[:1000] + '...'

        loop = asyncio.get_running_loop()
        loop.create_task(self.bot.send_message(self.chat_id, message))


def setup_tg_logger(bot_token: str, chat_id: str) -> None:
    log_bot = Bot(token=bot_token)
    telegram_handler = TelegramLogsHandler(bot=log_bot, chat_id=chat_id)
    telegram_handler.setFormatter(logging.Formatter('%(message)s'))
    telegram_handler.setLevel(logging.WARNING)
    logging.getLogger().addHandler(telegram_handler)
