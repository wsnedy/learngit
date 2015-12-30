# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
from twisted.enterprise import adbapi
from scrapy import log
import MySQLdb
import MySQLdb.cursors

class SinaNewsPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = ["images/" + x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

class MySQLStorePipelin(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                            host = '127.0.0.1',
                                            db = 'newsdb',
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
        if item.get('news_id'):
            conn.execute("select * from sinanews where news_id = %s", (item['news_id']))
            result = conn.fetchone()
            if result:
                log.msg("Item already stored in db: %s" % item, level=log.DEBUG)
            else:
                conn.execute("""insert into sinanews (news_id, news_url, news_title, news_pubtime, news_media, news_content, news_commentnum,
                  news_commenturl, image_urls, image_paths) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                             (item['news_id'], item['news_url'][0], item['news_title'][0], item['news_pubtime'][0], item['news_media'], item['news_content'][0], item['news_commentnum'], item['news_commenturl'], item['image_urls'][0], item['image_paths'][0]))
                log.msg("Item stored in db: %s" % item, level=log.DEBUG)

    def _handle_error(self, e, item, spider):
        log.err(e)