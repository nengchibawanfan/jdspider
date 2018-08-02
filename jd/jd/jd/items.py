# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    category = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    remark_count = scrapy.Field()
    descript = scrapy.Field()
    merchant = scrapy.Field()
    second_hand = scrapy.Field()
