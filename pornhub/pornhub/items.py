# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PornhubItem(scrapy.Item):
    video_title = scrapy.Field()
    image_url = scrapy.Field()
    video_duration = scrapy.Field()
    quality_480p = scrapy.Field()
    video_views = scrapy.Field()
    video_rating = scrapy.Field()
    link_url = scrapy.Field()
