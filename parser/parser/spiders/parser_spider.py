from __future__ import absolute_import

import urllib.parse
import scrapy
from scrapy import signals
import logging
import datetime
from parser.parser.strdate import CustomDate
from parser.parser.items import ParserItem
from parser.parser.database import Database
from parser.parser.parsebot import ParseBot


# Parse Depth in days
PARSE_DEPTH = 2

logging.getLogger("requests").setLevel(logging.WARNING)


class ParserSpider(scrapy.Spider):
    name = "ParserSpider"
    def __init__(self, chat_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat_id = chat_id

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ParserSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_opened(self, spider):
        ParseBot.send_message(chat_id=spider.chat_id, text="Парсер запущен")

    def spider_closed(self, spider):
        stats = spider.crawler.stats.get_stats() 
        try:
            count = stats['item_scraped_count']
        except KeyError:
            count = 0
        ParseBot.send_message(chat_id=spider.chat_id, 
            text=f"Парсер закончил работу. Найдено {count} новых постов")

    def start_requests(self):
        self.database = Database()
        urls = [
            f"https://0{x}.xn--b1aew.xn--p1ai/news" if x < 10 
            else
            f"https://{x}.xn--b1aew.xn--p1ai/news" for x in range(1, 10)
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def is_exists(self, url):
        cur = self.database.cursor.execute(
                "select id from posts where link = ?", (url,))
        rows = cur.fetchall()
        return True if rows else False


    def parse_url(self, url, loc):
        parse_url = urllib.parse.urlsplit(url)
        return urllib.parse.urljoin(f"{parse_url.scheme}://{parse_url.netloc}", loc)

    def parse(self, response):
        elements = response.css('.sl-item')
        last_date = elements[-1].css('.sl-item-date::text').get()
        if (datetime.date.today() - CustomDate(last_date)).days <= PARSE_DEPTH:
            next = response.css('.next::attr(href)').get()
            url = self.parse_url(response.url, next)
            yield scrapy.Request(url=url, callback=self.parse)
        for el in elements:
            parse_date = el.css('.sl-item-date::text').get()
            if el.css('.t_vid::text').get() and (datetime.date.today() - CustomDate(parse_date)).days <= PARSE_DEPTH:
                title_url = el.css('a::attr(href)').get()
                date = el.css('.sl-item-date').get()
                url = self.parse_url(response.url, title_url[1:])
                if not self.is_exists(url):
                    yield scrapy.Request(url=url, callback=self.parse_post)

    def parse_post(self, response):
        title = response.css('h1::text').get()
        item = ParserItem()
        item['title'] = title
        item['link'] = response.url
        embed = response.css('iframe::attr(src)').get()
        try:
            url = embed.split('?')[0].replace('embed', 'video')
        except:
            url = embed
        item['file'] = url
        yield item
