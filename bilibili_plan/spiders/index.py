# -*- coding: utf-8 -*-
import scrapy
from bilibili_plan.items import BilibiliPlanItem
import json
import time
import requests
import re
from scrapy import Request
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

class VideoSpider(scrapy.Spider):
    # scrapy默认配置
    name = 'index'
    allowed_domains = ['bilibili.com']
    start_urls = [
                'https://bangumi.bilibili.com/media/web_api/search/result?order=3&st=1&sort=0&page=1&season_type=1&pagesize=20'
    ]

    def parse(self, response):
        page = 1
        # 内容为api页面的json格式
        content = str(response.body, "utf-8")
        result = json.loads(content)['result']
        bangumi_content = result['data']
        for bangumi_data in bangumi_content:
            name = bangumi_data["title"]
            media_id = bangumi_data['media_id']
            play_href = bangumi_data['link']
            cover_url = bangumi_data['cover']
            pub_time = bangumi_data['order']['pub_date']
            watch_number = bangumi_data['order']['play'][:-3]
            followed_number = bangumi_data['order']['follow'][:-3]
            # 可能有未评分番剧
            try:
                bilibili_score = bangumi_data['order']['score'][:-1]
            except:
                bilibili_score = "null"
            detail_url = "https://www.bilibili.com/bangumi/media/md" + str(media_id)
            yield scrapy.Request(url=detail_url, meta={"name": name, "media_id": media_id, "play_href": play_href,
                                                       "cover_url": cover_url, "pub_time": pub_time, "watch_number": watch_number,
                                                       "followed_number": followed_number, "bilibili_score": bilibili_score,
                                                       "detail_url": detail_url}, callback=self.parse_detail)
        # 翻页
        while page < 147:
            page = page + 1
            next_url = 'https://bangumi.bilibili.com/media/web_api/search/result?order=3&st=1&sort=0&page=' + str(page) \
                   + '&season_type=1&pagesize=20'
            # 把新的页面url加入待爬取页面
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)

    def parse_detail(self, response):
        bangumi_item = BilibiliPlanItem()
        bangumi_item["name"] = response.meta["name"]
        bangumi_item["media_id"] = response.meta["media_id"]
        bangumi_item["play_href"] = response.meta["play_href"]
        bangumi_item["cover_url"] = response.meta["cover_url"]
        bangumi_item["pub_time"] = response.meta["pub_time"]
        bangumi_item["watch_number"] = response.meta["watch_number"]
        bangumi_item["followed_number"] = response.meta["followed_number"]
        bangumi_item["bilibili_score"] = response.meta["bilibili_score"]
        bangumi_item["detail_url"] = response.meta["detail_url"]
        tag_list = response.xpath('//span[@class="media-tag"]/text()').extract()
        divider = ','
        bangumi_item["tags"] = divider.join(tag_list)
        desc = re.findall('"evaluate":"(.*?)","long_review"', response.text)[0]
        bangumi_item["desc"] = desc.replace('\\n', '').replace('\\', '')
        cv_raw = re.findall('"actors":(.*?),"alias"', response.text)
        cv_list = clean_array(re.findall('：(.*?)n', str(cv_raw)))
        bangumi_item["cv"] = clean_string(divider.join(cv_list).replace('\\', '').replace('、', ',').replace('u002F', ','))
        staff_raw = re.findall('"staff":"(.*?)","stat"', response.text)
        staff_list = clean_array(re.findall('：(.*?)n', str(staff_raw)))
        bangumi_item["staff"] = clean_string(divider.join(staff_list).replace('\\', '').replace('、', ',').replace('u002F', ','))
        yield bangumi_item


def clean_array(arr):
    for i in range(len(arr)):
        arr[i] = clean_item(arr[i])
    return arr


def clean_item(str):
    str = str.replace(' ', '').replace('\'', '')
    if str.find('（') != -1:
        pos = str.find("（")
        new_str = str[:int(pos)]
        return new_str
    else:
        return str


def clean_string(str):
    new_list = str.split(',')
    new_list[:] = list(set(new_list))

    if len(new_list) > 10:
        new_list[:] = new_list[:10]
    new_str = ','.join(new_list)
    return new_str
