# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliPlanItem(scrapy.Item):

    name = scrapy.Field()
    media_id = scrapy.Field()
    play_href = scrapy.Field()
    cover_url = scrapy.Field()
    pub_time = scrapy.Field()
    watch_number = scrapy.Field()
    followed_number = scrapy.Field()
    bilibili_score = scrapy.Field()
    detail_url = scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass