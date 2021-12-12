# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParserItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    file = scrapy.Field()
    link = scrapy.Field()
    size = scrapy.Field()
