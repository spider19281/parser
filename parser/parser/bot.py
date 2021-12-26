from __future__ import absolute_import
import os 
from twisted.internet import reactor, defer
from multiprocessing import Process
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from parser.parser.spiders.parser_spider import ParserSpider
from parser.parser.parsebot import ParseBot
from aiogram import types, executor
import logging

logging.basicConfig(level=logging.INFO)



class ParseBotWithHandlers(ParseBot):
    @ParseBot.dp.message_handler(commands="parse")
    async def cmd_test1(message: types.Message):
        scraper = Scraper()
        p = Process(target=scraper.run_spiders, args=(message.chat.id,))
        p.start()
        p.join


class Scraper:
    def __init__(self):
        settings_file_path = 'parser.parser.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        settings = get_project_settings()
        configure_logging(settings)
        self.spider = ParserSpider 

    def run_spiders(self, chat_id=None):
        self.process = CrawlerProcess(get_project_settings())
        p = self.process.crawl(ParserSpider, chat_id=chat_id)
        reactor.run()



if __name__ == "__main__":
    bot = ParseBotWithHandlers()
    executor.start_polling(bot.dp)