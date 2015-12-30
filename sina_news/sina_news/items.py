# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    news_id = scrapy.Field()
    news_url = scrapy.Field()
    news_title = scrapy.Field()
    news_pubtime = scrapy.Field()
    news_media = scrapy.Field()
    news_content = scrapy.Field()
    news_commentnum = scrapy.Field()
    news_commenturl = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()
