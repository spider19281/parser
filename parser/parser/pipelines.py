# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from parser.parser.bot import ParseBot
from parser.parser.database import Database
from  aiogram import exceptions, types
import requests


class ParserPipeline:
    def open_spider(self, spider):
        self.database = Database()

    def close_spider(self, spider):
        self.database.close()

    def process_item(self, item, spider):
        if spider.chat_id:
            self.database.insert_item(item)
            r = requests.get(item['file'], stream=True)
            if int(r.headers['Content-Length']) < 52428800:
                try:
                    ParseBot.send_video(chat_id=spider.chat_id, video=item['file'],
                        caption=f"<a href=\"{item['link']}\">{item['title']}</a>", parse_mode="html")
                except (exceptions.WrongFileIdentifier, exceptions.InvalidHTTPUrlContent):
                    ParseBot.send_video(chat_id=spider.chat_id, 
                        video=types.InputFile.from_url(item['file']),
                        caption=f"<a href=\"{item['link']}\">{item['title']}</a>", parse_mode="html")
            else:
                ParseBot.send_message(chat_id=spider.chat_id, 
                    text=f"<a href=\"{item['link']}\">{item['title']}</a>", parse_mode="html")
        return item

