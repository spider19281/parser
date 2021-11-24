# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import requests

API_KEY_TOKEN = "2045834896:AAFJ_d3GVABZNd9fhFh652m0bAeFhKM3ZIE"

class ParserPipeline:
    def process_item(self, item, spider):
        res = requests.post("https://api.telegram.org/bot" + API_KEY_TOKEN + "/sendMessage",
                            {"text": item["text"], "chat_id": spider.chat_id, "parse_mode": "html"})
        return item
