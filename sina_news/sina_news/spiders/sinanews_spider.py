__author__ = 'Jon_chen'
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
import json

from sina_news.items import SinaNewsItem

class SinaNewsSpider(CrawlSpider):
    name = "sinanews"
    allowed_domains = ["sina.com.cn"]
    start_urls = [
        "http://search.sina.com.cn/?q=mh370&c=news&from=channel&col=&range=all&source=&country=&size=&time=&a=&sort=time&t=3_5_6",
    ]

    rules = [
        Rule(LinkExtractor(allow=(r'&page=(\d+)')), callback= 'parse_search')
    ]

    def parse_search(self,response):
        sel = Selector(response)
        news = sel.xpath('//div[@class="box-result clearfix"]')
        for eachnews in news:
            item = SinaNewsItem()
            item['image_urls'] = eachnews.xpath('div/a/img/@src').extract()
            item['news_url'] = eachnews.xpath('h2/a/@href').extract()
            if(item['news_url']):
                yield Request(url=item['news_url'][0],callback=self.parse_news, meta={'item': item})


    def parse_news(self,response):
        item = response.meta['item']
        sel = Selector(response)
        item['news_title'] = sel.xpath('//title/text()').extract()
        news_media = sel.xpath('//meta[@name="mediaid"]/@content').extract()
        if news_media:
            item['news_media'] = news_media[0]
        else:
            item['news_media'] = "NoMedia"
        timelist1 = sel.xpath('//span[@class="time-source"]/text()').re('\d+')[0:3]
        timelist2 = sel.xpath('//span[@id="pub_date"]/text()').re('\d+')[0:3]
        timelist3 = sel.xpath('//span[@class="time"]/text()').re('\d+')[0:3]
        timelist = timelist1 + timelist2 + timelist3
        # print timelist
        item['news_pubtime'] = ['-'.join(map(str,timelist))]
        news_content1 = sel.xpath('//div[@id="artibody"]').extract()
        news_content2 = sel.xpath('//div[@class="mainContent"]').extract()
        item['news_content'] = news_content1 + news_content2
        channel1 = sel.xpath('//script').re('channel:.*\'(.*)\'')
        channel2 = sel.xpath('//script').re('channel:.*\"(.*)\"')
        channel = channel1 + channel2
        newsid1 = sel.xpath('//script').re('newsid:.*\'(.*)\'')
        newsid2 = sel.xpath('//script').re('newsid:.*\"(.*)\"')
        newsid = newsid1 + newsid2
        item['news_id'] = newsid[0]
        cmturl = "http://comment5.news.sina.com.cn/page/info?format=json&channel=%s&newsid=%s&page_size=200"%(channel[0],newsid[0])
        item['news_commenturl'] = cmturl
        yield Request(url=cmturl,callback=self.parse_commentnum,meta={'item': item})

    def parse_commentnum(self,response):
        data = json.loads(response.body_as_unicode())
        item = response.meta['item']
        item['news_commentnum'] = data['result']['count']['total']
        return item



