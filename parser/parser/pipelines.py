# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from ..parser.bot import bot
from itemadapter import ItemAdapter
import requests

API_KEY_TOKEN = bot._token

class ParserPipeline:
    async def process_item(self, item, spider):
        if spider.chat_id:
            res = requests.post("https://api.telegram.org/bot" + API_KEY_TOKEN + "/sendMessage",
                                {"text": item["title"], "chat_id": spider.chat_id, "parse_mode": "html"})

            '''res = requests.post("https://api.telegram.org/bot" + API_KEY_TOKEN + "/sendDocument",
                                {"document": "./files/" + item["file"] + ".mp4", "chat_id": spider.chat_id})'''
            with open('C:\\Users\\efimov-sv\\parser\\parser\\files\\' + item['file'] + '.mp4', 'rb') as video:
                await bot.answer_video(video)
            #bot.send_video()
        return item
