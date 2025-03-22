import logging

from app.settings import settings
from app.vk.bot import VKBot

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    VKBot(vk_token=settings.vk_token).run()
