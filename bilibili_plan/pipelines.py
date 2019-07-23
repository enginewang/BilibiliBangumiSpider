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
        media_id = str(item['media_id'])
        name = str(item['name'])
        play_href = str(item['play_href'])
        cover_url = str(item['cover_url'])
        pub_time = str(item['pub_time'])
        watch_number = str(item['watch_number'])
        followed_number = str(item['followed_number'])
        bilibili_score = str(item['bilibili_score'])
        detailed_url = str(item['detail_url'])
        desc = str(item['desc'])
        tags = str(item['tags'])
        cv = str(item['cv'])
        staff = str(item['staff'])
        # 写和执行sql语句，这里交代表表名
        sql_command = "insert ignore into bilibili_index values ( '{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}' );".format(media_id, name, play_href, cover_url, pub_time, watch_number, followed_number, bilibili_score, detailed_url, desc, tags, cv, staff)
        self.cursor.execute(sql_command)
        self.connect.commit()
        print("sql_command = " + sql_command)
        return item
