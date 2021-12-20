from __future__ import absolute_import
import os

import urllib.parse
import requests
from twisted.internet import reactor, defer
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
import logging
import datetime
from ..strdate import CustomDate
from ..items import ParserItem

# Parse Depth in days
PARSE_DEPTH = 4

logging.getLogger("requests").setLevel(logging.WARNING)

class ParserSpider(scrapy.Spider):
    name = "ParserSpider"
    def __init__(self, chat_id=None, region=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat_id = chat_id
        self.region = region
    def start_requests(self):
        
        urls = [
            f'https://0{x}.xn--b1aew.xn--p1ai/news' if x < 10 
            else
            f'https://{x}.xn--b1aew.xn--p1ai/news' for x in range(1, 100)
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        elements = response.css('.sl-item')
        last_date = elements[-1].css('.sl-item-date::text').get()
        if (datetime.date.today() - CustomDate(last_date)).days <= PARSE_DEPTH:
             yield scrapy.Request(url=response.url + '/2/', callback=self.parse)
        for el in elements:
            parse_date = el.css('.sl-item-date::text').get()
            if el.css('.t_vid::text').get() and (datetime.date.today() - CustomDate(parse_date)).days <= PARSE_DEPTH:
                title_url = el.css('a::attr(href)').get()
                date = el.css('.sl-item-date').get()
                parse_url = urllib.parse.urlsplit(response.url)
                yield scrapy.Request(url=urllib.parse.urljoin(f'{parse_url.scheme}://{parse_url.netloc}', title_url[1:]), callback=self.parse_post)

    def parse_post(self, response):
        title = response.css('h1::text').get()
        item = ParserItem()
        item['title'] = title
        item['link'] = response.url
        embed = response.css('iframe::attr(src)').get()
        url = embed.split('?')[0].replace('embed', 'video')
        fname =  url.rsplit('/')[-1] 
        item['file'] = fname
        r = requests.get(url, stream=True)
        item['size'] = int(r.headers['Content-Length'])
        if (item['size'] < 52428800):
            f = open('C:\\Users\\Slint\\parser\\parser\\' + fname + ".mp4", 'wb')
            f.write(requests.get(url).content)
            f.close()
        yield item


