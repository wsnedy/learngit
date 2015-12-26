__author__ = 'Jon_chen'
from scrapy.spiders import Spider
from scrapy.selector import Selector
from test_pic.items import TestPicItem

class MyImageSpider(Spider):
    name = "image_spider"
    allowed_domains = ["sina.com.cn"]
    start_urls = [
        "http://search.sina.com.cn/?q=mh370&c=news&from=channel&col=&range=all&source=&country=&size=&time=&a=&sort=time&t=3_5_6",
    ]

    def parse(self, response):
        sel = Selector(response)
        news = sel.xpath('//div[@class="box-result clearfix"]')
        items = []
        for eachnews in news:
            item = TestPicItem()
            item['title'] = eachnews.xpath('h2/a/text()').extract()
            item['image_urls'] = eachnews.xpath('div/a/img/@src').extract()
            items.append(item)

        return items