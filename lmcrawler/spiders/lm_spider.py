import scrapy
from lmcrawler.items import LmcrawlerItem
import re
import logging

class LmcrawlerSpider(scrapy.Spider):
  name = 'lmcrawler'

  allower_domains = [""] # the website domain ex: ptt.cc
  start_urls = [""] # the entry of website that u want to crawl

  _class_map = {
    "adventure-photography" : 1,
    "aerial-photography" : 2,
    "animal-photography" : 3,
    "architectual-photography" : 4,
    "black-and-white-photography" : 5,
    "commercial-photography" : 6,
    "documentry-photography" : 7,
    "event-photography" : 8,
    "family-photography" : 9,
    "fashion-photography" : 10,
    "fine-art-photography" : 11,
    "food-photography" : 12,
    "landscape-photography" : 13,
    "nature-photography" : 14,
    "night-photography" : 15,
    "outdoor-photography" : 16,
    "people-photography" : 17,
    "pet-photography" : 18,
    "photojournalism" : 19,
    "portrait-photography" : 20,
    "sport-photography" : 21,
    "still-life-photography" : 22,
    "street-photography" : 23,
    "travel-photography" : 24,
    "underwater-photography" : 25,
    "wedding-photography" : 26,
    "wildlife-photography" : 27
  }
  #_pages = 0;
 
  #_total = open('url.txt', 'w')

  def parse(self, response):

    #self._pages += 1
    
    for href in response.xpath('/html/body/div/div[3]/div[3]/a/@href')[2:29]: # categories in left side block 
      category = href.extract().rstrip().split('/')[-1]
      print 'category------------{}'.format(category)
      url = 'http://reviews.gurushots.com/scripts/ajax-critiques.php?action_id=1&category={}&start=0&end=10000'.format(category)
      yield scrapy.Request(url, callback = self.parse_tab,  headers={"X-Requested-With":"XMLHttpRequest"})

  def parse_tab(self, response):
    #source = response.url.split('&')[-3].replace('category=','')
    #filename = 'url/' + source + '.txt'
    #f = open(filename, 'w')
    #for href in response.xpath('/html/body/div/div[1]/a/@href'):
    for href in response.xpath('//a[contains(@class, "-button")]/@href'):  
      url = response.urljoin(href.extract())
      #f.write(url+'\n')
      #_total.write(url+'\n')
      yield scrapy.Request(url, callback=self.parse_comment)
    

  def parse_comment(self, response):
    item = GurushotsItem()
    
    item['site'] = response.url
    category = response.url.split('/')[-2]
    item['category'] = category.encode('utf-8', "ignore")
    class_id = self._class_map.get(category)

    ## title
    item['title'] = '{}_{}'.format(class_id, response.url.split('/')[-1])

    ## image_url
    item['image_url'] = ''
    image_url = response.xpath('//div[contains(@class, "-image")]/a/@href').extract()
    if not image_url:
      image_url = response.xpath('//img[@title="Click to enlarge"]/@src').extract()
    item['image_url'] = image_url[0].encode('utf-8')
    
    item['photographer'] = ''
    text = response.xpath('/html/body/div[1]/div[3]/div[1]/span/text()').extract()
    text = text[0].split(" ")[2:]
    photographer = ' '.join(text)
    if photographer:
      item['photographer'] = photographer.encode('utf-8', "ignore")

    item['reviewer'] = ''
    reviewer = response.xpath('//a[contains(@class, "pro-name")]/text()').extract()
    if reviewer:
      item['reviewer'] = reviewer[0].encode('utf-8', "ignore")
    else:
      logging.warning('----------{} has no reviewer'.format(item['reviewer']))
    
    score = []
    ##---------------  captions -----------------
    item['description'] =''
    description = \
      response.xpath('//div[contains(@class, "image-info-description")]/text()').extract()
    
    if description:
      item['description'] = description[0].encode('utf-8', "ignore")
    else:
      logging.warning('----------{} has no description'.format(item['title']))
    
    item['general_impression'] = ''
    general_impression = \
    response.xpath('//div[@class="full-critique-general-impression"]/parent::node()/following-sibling::div[1]/text()').extract()
    if general_impression:
      item['general_impression'] = general_impression[0]
    score_general = \
    response.xpath('//div[@class="full-critique-general-impression"]/parent::node()/following-sibling::div[2]/text()').extract()
    if not score_general:
      score_general = 'NA'
    score.append(score_general[0])
    
    item['subject_of_photo'] = ''
    subject_of_photo = \
    response.xpath('//div[@class="full-critique-subject-photo"]/parent::node()/following-sibling::div[1]/text()').extract()
    if subject_of_photo:
      item['subject_of_photo'] = subject_of_photo[0].encode('utf-8', "ignore")
    score_subject = \
    response.xpath('//div[@class="full-critique-subject-photo"]/parent::node()/following-sibling::div[2]/text()').extract()
    if not score_subject:
      score_subject = 'NA'
    score.append(score_subject[0])
    
    item['composition'] = ''
    composition = \
    response.xpath('//div[@class="full-critique-composition-perspective"]/parent::node()/following-sibling::div[1]/text()').extract()
    if composition:
      item['composition'] =  composition[0].encode('utf-8', "ignore")
    score_composition= \
    response.xpath('//div[@class="full-critique-composition-perspective"]/parent::node()/following-sibling::div[2]/text()').extract()
    if not score_composition:
      score_composition = 'NA'
    score.append(score_composition[0])

    item['use_of_camera'] = ''
    use_of_camera = \
    response.xpath('//div[@class="full-critique-use-of-camera"]/parent::node()/following-sibling::div[1]/text()').extract()
    if use_of_camera:
      item['use_of_camera'] = use_of_camera[0].encode('utf-8', "ignore")
    score_camera= \
    response.xpath('//div[@class="full-critique-use-of-camera"]/parent::node()/following-sibling::div[2]/text()').extract()
    if not score_camera:
      score_camera = 'NA'
    score.append(score_camera[0])

    
    item['depth_of_field'] = ''
    depth_of_field = \
    response.xpath('//div[@class="full-critique-depth-field"]/parent::node()/following-sibling::div[1]/text()').extract()
    if depth_of_field:
      item['depth_of_field'] = depth_of_field[0].encode('utf-8', "ignore")
    score_depth= \
    response.xpath('//div[@class="full-critique-depth-field"]/parent::node()/following-sibling::div[2]/text()').extract()
    if not score_depth:
      score_depth = 'NA'
    score.append(score_depth[0])

    
    item['color_lighting'] = ''
    color_lighting = \
    response.xpath('//div[@class="full-critique-color-lighting"]/parent::node()/following-sibling::div[1]/text()').extract()
    if color_lighting:
      item['color_lighting'] = color_lighting[0].encode('utf-8', "ignore")
    score_color= \
    response.xpath('//div[@class="full-critique-color-lighting"]/parent::node()/following-sibling::div[2]/text()').extract()
    if not score_color:
      score_color = 'NA'
    score.append(score_color[0])

    item['focus'] = ''
    focus = \
    response.xpath('//div[@class="full-critique-focus"]/parent::node()/following-sibling::div[1]/text()').extract()
    if focus:
      item['focus'] = focus[0].encode('utf-8', "ignore")
    score_focus = \
    response.xpath('//div[@class="full-critique-focus"]/parent::node()/following-sibling::div[2]/text()').extract()
    if not score_focus:
      score_focus = 'NA'
    score.append(score_focus[0])

    ##----------------- score -------------------
    item['overall'] = ''
    overall = response.xpath('//div[@class="full-critique-horizontal-overall"]/div/text()').extract()
    if not overall:
      overall = response.xpath('//div[@class="full-critique-vertical-overall"]/text()').extract()
    item['overall'] = overall[0]

    #t_score = response.xpath('//div[contains(@class, "suggestion-score")]/text()').extract()
    #print '------------:{}'.format(t_score)

    item['score'] = score
    #print '------------:{}'.format(item['score'])
    ##---------------------------------------------------------
    
    yield item