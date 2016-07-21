# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import re
import scrapy
import json
from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from scrapy.exporters import BaseItemExporter
from scrapy import signals

class LmcrawlerPipeline(object):
  def file_path(self, request, response=None, info=None):
    image_name = request.meta['title']
    #image_name = request.url.split('/')[-1]
    return 'full/%s' %(image_name)

  def get_media_requests(self, item, info):
   # for image_url in item['image_url']:
    if item['image_url']:
      yield scrapy.Request(item['image_url'], meta=item)
  
  def item_completed(self, results, item, info):
    image_paths = [x['path'] for ok, x in results if ok]
    if not image_paths:
      raise DropItem("Item contains no images")
      item['image_paths'] = image_paths
      return item

class JsonWriterPipeline(BaseItemExporter):

  def __init__(self, **kwargs):
    self._configure(kwargs)
    self.files = {} 
    self.encoder = json.JSONEncoder(ensure_ascii=False, **kwargs)
 
  @classmethod
  def from_crawler(cls, crawler):
    pipeline = cls()
    crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
    crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
    return pipeline

  def spider_opened(self, spider):
    file = codecs.open('item.json', 'wb', encoding="utf-8")
    self.files[spider] = file
    self.exporter = JsonItemExporter(file)
    self.exporter.start_exporting()

  def spider_closed(self, spider):
    self.exporter.finish_exporting()
    file = self.files.pop(spider)
    file.close() 

  def process_item(self, item, spider):

    if item['title']: # and item['image_url'] :
      item['description'] = re.sub("\r|\n","", item['description'])
      item['general_impression'] = re.sub("\r|\n","", item['general_impression'])
      item['subject_of_photo'] = re.sub("\r|\n","", item['subject_of_photo'])
      item['composition'] = re.sub("\r|\n","", item['composition'])
      item['use_of_camera'] = re.sub("\r|\n","", item['use_of_camera'])
      item['depth_of_field'] = re.sub("\r|\n","", item['depth_of_field'])
      item['color_lighting'] = re.sub("\r|\n","", item['color_lighting'])
      item['focus'] = re.sub("\r|\n","", item['focus'])

      ##line = json.dumps(dict(item)) + '\n'
      ##self.file.write(line)
      self.exporter.export_item(item)
    return item   
