import asyncio
import logging

from vkbottle import Bot
from vkbottle.bot import Message

from bin.dialogflow import get_intent_answer
from bin.log_handler import setup_tg_logger
from bin.settings import settings
from bin.utils import split_message

logger = logging.getLogger(__name__)


def run_bot(token: str):
    vk_bot = Bot(token=token)
    vk_bot.on.message()(send_echo_with_dialogflow)
    vk_bot.run_forever()


async def send_echo_with_dialogflow(message: Message):
    logger.debug(f'Got message: {message}')
    texts = split_message(message.text)
    logger.debug(f'After split: {texts}')
    if not texts:
        return

    responses = get_intent_answer(
        project_id=settings.project_id,
        session_id=f'vk-{message.from_id}',
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


if __name__ == '__main__':
    logging.basicConfig(level=settings.log_level, format=settings.log_format)
    setup_tg_logger(settings.log_bot_token, settings.admin_id)

    while True:
        try:
            run_bot(settings.vk_token)
        except Exception as e:
            logging.critical(e, exc_info=True)
            asyncio.run(asyncio.sleep(settings.restart_delay))
