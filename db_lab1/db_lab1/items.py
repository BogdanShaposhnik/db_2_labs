# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProdItem(scrapy.Item):
    prodName = scrapy.Field()
    prodPrice = scrapy.Field()
    prodImage = scrapy.Field()
    prodLink = scrapy.Field()
