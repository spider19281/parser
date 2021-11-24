from __future__ import absolute_import


import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from ..items import ParserItem



from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token="2045834896:AAFJ_d3GVABZNd9fhFh652m0bAeFhKM3ZIE")
dp = Dispatcher(bot)

class ParserSpider(scrapy.Spider):
    name = "ParserSpider"
    def __init__(self, chat_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat_id = chat_id

    def start_requests(self):
        urls = [
            'https://05.xn--b1aew.xn--p1ai/news',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        elements = response.css('.sl-item')
        for el in elements:
            date = el.css('.sl-item-date::text').get()            
            if el.css('.t_vid::text').get():
                title_url = el.css('a::attr(href)').get()
                yield scrapy.Request(url=response.url.replace('news', title_url), callback=self.parse_post)

    def parse_post(self, response):
        title = response.css('h1::text').get()
        item1 = ParserItem()
        item1['title'] = title
        yield item1
        '''download_url = response.css('.sl-item-video').css('iframe::attr(src)').get()
        file = requests.get(download_url)
        f = open('test', 'wb')
        f.write(file)'''

    def download_video(self, response):
        return response.body

@dp.message_handler(commands="/start")
async def cmd_test1(message: types.Message):
    process = CrawlerProcess()
    process.crawl(ParserSpider(chat_id=message.chat))
    process.start()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)