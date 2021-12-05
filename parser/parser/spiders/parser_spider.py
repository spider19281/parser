from __future__ import absolute_import
import os

import requests
from twisted.internet import reactor, defer
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
import logging

from ..items import ParserItem


logging.getLogger("requests").setLevel(logging.WARNING)

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
        print(os.path)
        title = response.css('h1::text').get()
        item = ParserItem()
        item['title'] = title
        embed = response.css('.sl-item-video').css('iframe::attr(src)').get()
        url = embed.split('?')[0].replace('embed', 'video')
        fname =  url.rsplit('/')[-1] 
        item['file'] = fname
        f = open('..//..//files//' + fname + ".mp4", 'wb')
        f.write(requests.get(url).content)
        f.close()
        yield item


