import os 
from twisted.internet import reactor, defer
from multiprocessing import Process
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from parser.parser.spiders.parser_spider import ParserSpider
from aiogram import Bot, Dispatcher, executor, types


bot = Bot(token="2045834896:AAFJ_d3GVABZNd9fhFh652m0bAeFhKM3ZIE")
dp = Dispatcher(bot)

COMMAND_TIME = 0

class Scraper:
    def __init__(self):
        settings_file_path = 'parser.parser.settings' # The path seen from root, ie. from main.py
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        settings = get_project_settings()
        configure_logging(settings)
        self.spider = ParserSpider # The spider you want to crawl

    def run_spiders(self, chat_id=None):
        self.process = CrawlerProcess(get_project_settings())
        p = self.process.crawl(ParserSpider, chat_id=chat_id)
        reactor.run()

'''@dp.message_handler(content_types=["text"])
async def cmd_image(message: types.Message):
    with open('C:\\Users\\efimov-sv\\parser\\parser\\files\\2281719.mp4', 'rb') as video:
        await message.answer_video(video)   '''


@dp.message_handler(commands="parse")
async def cmd_test1(message: types.Message):
    scraper = Scraper()
    print(str(message.chat.id))
    p = Process(target=scraper.run_spiders, args=(message.chat.id,))
    p.start()
    p.join


if __name__ == "__main__":
    executor.start_polling(dp)