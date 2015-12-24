# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    sex = scrapy.Field()
    agree_count = scrapy.Field()
    thanks_count = scrapy.Field()
    fans_count = scrapy.Field()
    as_fans_count = scrapy.Field()
    province = scrapy.Field()
    #image_urls = scrapy.Field()
    #images = scrapy.Field()
    #image_paths = scrapy.Field()
