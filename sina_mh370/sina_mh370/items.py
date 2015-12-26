# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaMh370Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    time = scrapy.Field()
    media = scrapy.Field()
    content = scrapy.Field()
    comment = scrapy.Field()
    cmt_num = scrapy.Field()
