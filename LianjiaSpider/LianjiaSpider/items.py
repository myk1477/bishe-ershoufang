# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # 定义爬取的信息
    # 爬取房屋的所在城市
    city = scrapy.Field()
    # 街道的名字
    street = scrapy.Field()
    # 街道的url地址
    street_page_url = scrapy.Field()
    # 房屋的url地址
    detail_url = scrapy.Field()
    # 房屋的详细信息
    house_info_dict = scrapy.Field()

