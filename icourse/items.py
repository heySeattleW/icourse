# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IcourseItem(scrapy.Item):
    # define the fields for your item here like:
    video_title = scrapy.Field()
    video_code = scrapy.Field()
    video_img = scrapy.Field()
    video_time = scrapy.Field()
    pan_url = scrapy.Field()
    video_type = scrapy.Field()
    video_desc = scrapy.Field()
