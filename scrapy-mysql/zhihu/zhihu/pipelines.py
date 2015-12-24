# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#from scrapy.pipelines.images import ImagesPipeline
#from scrapy.exceptions import DropItem
#from scrapy.http import Request
import json
import codecs
from twisted.enterprise import adbapi
from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy import log
import MySQLdb
import MySQLdb.cursors

class ZhihuPipeline(object):

    def __init__(self):
        self.file = codecs.open('zhihu.json', 'w', encoding = 'utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self,spider):
        self.file.close()


class MySQLStorePipelin(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                            host = '127.0.0.1',
                                            db = 'zhihudb',
                                            user = 'root',
                                            passwd = '314159',
                                            cursorclass = MySQLdb.cursors.DictCursor,
                                            charset = 'utf8',
                                            use_unicode = False
                                            )

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item, spider)

        query.addErrback(self._handle_error, item, spider)

        query.addBoth(lambda _: item)
        return query

    def _conditional_insert(self, conn, item, spider):
        if item.get('url'):
            conn.execute("select * from zhihuinfo where url = %s", (item['url']))
            result = conn.fetchone()
            if result:
                log.msg("Item already stored in db: %s" % item, level=log.DEBUG)
            else:
                conn.execute("""insert into zhihuinfo (url, nickname, sex, agree_count, thanks_count, fans_count, as_fans_count, province)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s) """, (item['url'], item['name'][0], item['sex'][0], item['agree_count'][0], item['thanks_count'][0], item['fans_count'][0], item['as_fans_count'][0], item['province'][0]))
                log.msg("Item stored in db: %s" % item, level=log.DEBUG)

    def _handle_error(self,e, item, spider):
        log.err(e)



#class MyZhihuPipeline(ImagesPipeline):
#   def get_media_requests(self, item, info):
#        for image_url in item['image_urls']:
#           yield Request(image_url)

#    def item_completed(self, results, item, info):
#        image_paths = [x['path'] for ok, x in results if ok]
#        if not image_paths:
#            raise DropItem("Item contains no images")
#        item['image_paths'] = image_paths
#       return item

