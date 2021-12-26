# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from aiogram.types import video
from parser.parser.bot import ParseBot
from parser.parser.database import Database
from itemadapter import ItemAdapter
import requests






class ParserPipeline(object):
    def __init__(self):
        self.database = Database()
       
    def insert_item(self, item):
            cur = self.database.cursor.execute(
                "insert into posts (title, file, link) values (?, ?, ?)",
                    (item['title'], item['file'], item['link']))
            self.database.connection.commit()
            self.database.connection.close()

    def process_item(self, item, spider):
        if spider.chat_id:
            link = item['link']
            title = item['title']
            file = item['file']
            #self.insert_item(item)
            r = requests.get(item['file'], stream=True)
            if (int(r.headers['Content-Length']) < 52428800):
                r = requests.get(item['file'])
                ParseBot.send_video(chat_id=spider.chat_id, video=item['file'],
                    caption=f'<a href="{link}">{title}</a>', parse_mode='html')
            else:
                ParseBot.send_message(chat_id=spider.chat_id, 
                    text=f'<a href="{link}">{title}</a>', parse_mode='html')
        return item

