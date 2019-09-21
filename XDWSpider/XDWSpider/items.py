# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from user.models import Movie


class XdwspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MovieItem(DjangoItem):
    django_model = Movie
    # cate_name = scrapy.Field()
    # movie_name = scrapy.Field()
    # img = scrapy.Field()
    # movie_down_url = scrapy.Field()
