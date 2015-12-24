__author__ = '2YANG'
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request, FormRequest
from zhihu.items import ZhihuItem

class ZhihuSpider(CrawlSpider):
    name = "zhihu"
    allowed_domains = ["zhihu.com"]
    start_urls = [
        "http://www.zhihu.com"
    ]
    rules = [
        Rule(LinkExtractor(allow=(r'/question/\d+'))),
        Rule(LinkExtractor(allow=(r'/people/(\w+-?)+$')), callback= 'parse_item')
    ]

    num_users = 0
    headers = {
    #"Accept": "*/*",
    #"Accept-Encoding": "gzip,deflate",
    #"Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
    #"Connection": "keep-alive",
    #"Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0",
    #"Referer": "http://www.zhihu.com/"
    }

    def start_requests(self):
        return [Request("http://www.zhihu.com/#signin", meta = {'cookiejar': 1},callback= self.post_login)]

    def post_login(self,response):
        print 'Preparing login'
        xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]
        print xsrf
        return [FormRequest.from_response(response,
                                          meta = {'cookiejar': response.meta['cookiejar']},
                                          headers = self.headers,
                                          formdata={
                                              '_xsrf' : xsrf,
                                              'email': '974922865@qq.com',
                                              'password': '314159SQ0903'
                                              },
                                          callback = self.after_login,
                                          dont_filter = True
                                          )]

    def after_login(self,response):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse_item(self,response):
        self.num_users = self.num_users + 1
        problem = Selector(response)
        item = ZhihuItem()
        sex = []
        place = []
        item['url'] = response.url
        item['name'] = problem.xpath('//div[@class="title-section ellipsis"]/span[@class="name"]/text()').extract()
        sex = problem.xpath('/html/body/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/span[1]/span[3]/i/@class').re(r'icon icon-profile-(.*)')
        if len(sex) != 0:
            item['sex'] = sex
        else:
            item['sex'] = ['morf']
        item['agree_count'] = problem.xpath('//span[@class="zm-profile-header-user-agree"]/strong/text()').extract()
        item['thanks_count'] = problem.xpath('//span[@class="zm-profile-header-user-thanks"]/strong/text()').extract()
        item['fans_count'] = problem.xpath('//div[@class="zm-profile-side-following zg-clear"]/a[2]/strong/text()').extract()
        item['as_fans_count'] = problem.xpath('//div[@class="zm-profile-side-following zg-clear"]/a[1]/strong/text()').extract()
        place = problem.xpath('/html/body/div[3]/div[1]/div/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/span[1]/span[1]/a/text()').extract()
        if len(place) != 0:
            item['province'] = place
        else:
            item['province'] = ['noplace']
        #item['image_urls'] = problem.xpath('//div[@class="body clearfix"]/div[1]/img/@src').extract()
        return item

