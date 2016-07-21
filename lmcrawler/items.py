# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LmcrawlerItem(scrapy.Item):
    title = scrapy.Field()
    photographer = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    reviewer = scrapy.Field()
    site = scrapy.Field()

    ## image
    image_url = scrapy.Field()
    
    ## score
    overall = scrapy.Field()
    score = scrapy.Field()

    ## captions
    general_impression = scrapy.Field()
    subject_of_photo = scrapy.Field()
    composition = scrapy.Field()
    depth_of_field = scrapy.Field()
    color_lighting = scrapy.Field()
    focus = scrapy.Field()
    use_of_camera = scrapy.Field()
    
    pass
