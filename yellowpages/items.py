# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YellowpagesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Address(scrapy.Item):
    street_address = scrapy.Field()
    locality = scrapy.Field()
    region = scrapy.Field()
    zipcode = scrapy.Field()


class Business(scrapy.Item):
    name = scrapy.Field()
    address_text = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
