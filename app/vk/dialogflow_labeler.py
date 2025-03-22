from vkbottle.bot import BotLabeler, Message

bl = BotLabeler()


@bl.message()
async def echo(message: Message):
    await message.answer(message.text)
