# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Learner1Item(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    content = scrapy.Field()
    language = scrapy.Field()
