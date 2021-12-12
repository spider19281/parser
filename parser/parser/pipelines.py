# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import aiogram
from ..parser.bot import bot, Dispatcher
from itemadapter import ItemAdapter
import requests
import functools
import json
import os
import sqlite3

API_KEY_TOKEN = bot._token




class ParserPipeline(object):
    def __init__(self):
        self.connection = sqlite3.connect('./database.db')
        self.cursor = self.connection.cursor()

    def send_message(spider, item, method):
        pass

    def insert_item(self, item):
            self.cursor.execute(
                "insert into posts (title, file, link) values (?, ?, ?)",
                    (item['title'], item['file'], item['link']))
            self.connection.commit()
            self.connection.close()

    def process_item(self, item, spider):
        if spider.chat_id:
            link = item['link']
            title = item['title']
            file = item['file']
            #self.insert_item(item)
            data_video = {'chat_id': str(spider.chat_id), 'caption': f'<a href="{link}">{title}</a>', 'parse_mode': 'html'}
            data_text = {'chat_id': str(spider.chat_id), 'text': f'<a href="{link}">{title}</a>', 'parse_mode': 'html'}
            if (item['size'] < 52428800):
                fvideo = open(file + '.mp4', 'rb')
                video = {'video': fvideo}
                res = requests.post("https://api.telegram.org/bot" + API_KEY_TOKEN + "/sendVideo",
                data=data_video, files=video)
                fvideo.close()
                os.remove(file + '.mp4')
            else:
                res = requests.post("https://api.telegram.org/bot" + API_KEY_TOKEN + "/sendMessage",
                data=data_text)
            print(res)
        return item

