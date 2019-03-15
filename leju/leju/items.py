# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LejuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AgentItem(scrapy.Item):
    name = scrapy.Field()
    tel = scrapy.Field()
    source = scrapy.Field()
    area = scrapy.Field()

