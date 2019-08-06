# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeixinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pic_id = scrapy.Field()
    pic_link = scrapy.Field()
    pic_desc = scrapy.Field()
