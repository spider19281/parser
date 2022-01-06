import os
import asyncio
from aiogram import Bot, Dispatcher



class ParseBot:
    token = os.environ['TOKEN']
    bot = Bot(token=token)
    dp = Dispatcher(bot)
    loop = asyncio.get_event_loop()

    @classmethod
    def send_message(cls, *args, **kwargs):
        cls.loop.run_until_complete(cls.bot.send_message(*args, **kwargs), )

    @classmethod
    def send_video(cls, *args, **kwargs):
        cls.loop.run_until_complete(cls.bot.send_video(*args, **kwargs))
