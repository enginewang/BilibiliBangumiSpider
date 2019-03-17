# -*- coding: utf-8 -*-
import scrapy
from bilibili_plan.items import BilibiliPlanItem
import json
import time
import request
import re
from scrapy import Request


class VideoSpider(scrapy.Spider):
    # scrapy默认配置
    name = 'index'
    allowed_domains = ['bilibili.com']
    start_urls = [
                'https://bangumi.bilibili.com/media/web_api/search/result?order=3&st=1&sort=0&page=1&season_type=1&pagesize=20'
    ]

    #count = 0
    def parse(self, response):
        #print(response.body)
        bangumi_item = BilibiliPlanItem()
        page = 1
        # 内容为api页面的json格式
        content = str(response.body, "utf-8")
        result = json.loads(content)['result']
        bangumi_content = result['data']
        for bangumi_data in bangumi_content:
            bangumi_item["name"] = bangumi_data["title"]
            bangumi_item['media_id'] = bangumi_data['media_id']
            bangumi_item['play_href'] = bangumi_data['link']
            bangumi_item['cover_url'] = bangumi_data['cover']
            bangumi_item['pub_time'] = bangumi_data['order']['pub_date']
            bangumi_item['watch_number'] = bangumi_data['order']['play'][:-3]
            bangumi_item['followed_number'] = bangumi_data['order']['follow'][:-3]
            try:
                bangumi_item['bilibili_score'] = bangumi_data['order']['score'][:-1]
            except:
                bangumi_item['bilibili_score'] = "null"
            bangumi_item['detail_url'] = "https://www.bilibili.com/bangumi/media/md" + str(bangumi_item['media_id'])
            yield bangumi_item
        # 翻页
        while page < 255:
            page = page + 1
            next_url = 'https://bangumi.bilibili.com/media/web_api/search/result?order=3&st=1&sort=0&page=' + str(page) \
                   + '&season_type=1&pagesize=20'
            # 把新的页面url加入待爬取页面
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)
