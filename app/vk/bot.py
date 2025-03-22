from vkbottle import Bot

from app.vk.dialogflow_labeler import bl as dialogflow_bp


class VKBot:
    def __init__(self, vk_token: str):
        self.bot = Bot(token=vk_token, labeler=dialogflow_bp)

    def run(self):
        self.bot.run_forever()
