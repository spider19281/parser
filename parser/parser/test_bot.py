from aiogram import Bot, Dispatcher, types, executor
import logging

token = "2045834896:AAHdxAfzv01yNMzebHa1nQa7RCXB99iGzew"
bot = Bot(token=token)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(lambda message: message.text == 'test')
async def test(message: types.Message):
    await bot.send_video(678501296, video=types.InputFile.from_url('https://media.mvd.ru/files/video/2299661'))
    #await bot.send_video(678501296, video='https://media.mvd.ru/files/video/2298542')

if __name__ == '__main__':
    executor.start_polling(dp)