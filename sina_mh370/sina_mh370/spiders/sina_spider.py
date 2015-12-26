__author__ = 'Jon_chen'
from scrapy.spiders import Spider
from sina_mh370.items import SinaMh370Item
from scrapy.http import Request
import json

class SinaMh370Spider(Spider):
    name = "mh370"
    allow_domain = ['news.sina.com.cn']
    start_urls = ['http://news.sina.com.cn/2015-12-25/doc-ifxmxxst0424605.shtml']

    def parse(self, response):
        item = SinaMh370Item()
        item['title'] = response.xpath('//div[@class="page-header"]/h1/text()').extract()
        timelist = response.xpath('//div[@class="page-info"]/span/text()').re('\d+')[0:3]
        item['time'] = ['-'.join(map(str,timelist))]
        item['media'] = response.xpath('//div[@class="page-info"]/span/span/span/a/text()').extract()
        item['content'] = [','.join(response.xpath('//div[@id="artibody"]/p').extract())]
        cmtinfo = response.xpath('//meta[@name="comment"]/@content').extract()[0].split(':')
        channel = cmtinfo[0]
        newsid = cmtinfo[1]
        cmturl = "http://comment5.news.sina.com.cn/page/info?format=json&channel=%s&newsid=%s&page_size=200"%(channel,newsid)
        yield Request(url=cmturl, callback=self.parse_comment, meta={'item': item})

    def parse_comment(self,response):
        data = json.loads(response.body_as_unicode())
        item = response.meta['item']
        item['cmt_num'] = data['result']['count']['total']
        cmntlist = data['result']['cmntlist']
        cmnt = [eachcmnt['content'] for eachcmnt in cmntlist]
        item['comment'] = [','.join(cmnt)]
        return item



