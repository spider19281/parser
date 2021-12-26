import asyncio
from aiogram import Bot, Dispatcher


class ParseBot:
    token = "2045834896:AAHdxAfzv01yNMzebHa1nQa7RCXB99iGzew"
    bot = Bot(token=token)
    dp = Dispatcher(bot)

    @classmethod
    def send_message(cls, *args, **kwargs):
        asyncio.run(cls.bot.send_message(*args, **kwargs), )

    @classmethod
    def send_video(cls, *args, **kwargs):
        asyncio.run(cls.bot.send_video(*args, **kwargs))
