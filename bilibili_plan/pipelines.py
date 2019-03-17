# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from bilibili_plan import settings


class BilibiliPlanPipeline(object):
    # 连接信息配置
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        name = item['name']
        media_id = item['media_id']
        play_href = item['play_href']
        cover_url = item['cover_url']
        pub_time = item['pub_time']
        watch_number = item['watch_number']
        followed_number = item['followed_number']
        bilibili_score = item['bilibili_score']
        detail_url = item['detail_url']
        # 写和执行sql语句，这里交代表表名
        sql_command = "insert ignore into bilibili_index(name, media_id, play_href, cover_url, pub_time, watch_number, followed_number, bilibili_score, detailed_url) values ('" + \
                            name + "','" + str(media_id) + "','" + play_href + "','" + cover_url + "','" + str(pub_time) + "','" + watch_number + "','" + followed_number + "','" + \
                            str(bilibili_score) + "','" + detail_url + "');"
        self.cursor.execute(sql_command)
        self.connect.commit()
        return item
