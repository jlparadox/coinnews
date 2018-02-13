# -*- coding: utf-8 -*-
import scrapy
from scrapy.item import Item, Field

class Event(scrapy.Item):
    title = scrapy.Field()
    location = scrapy.Field()
    date = scrapy.Field(serializer=str)
    content = scrapy.Field()

class CointelegraphEventSpider(scrapy.Spider):
    name = 'cointelegraph_events'
    start_urls = ['https://cointelegraph.com/events',]

    def parse(self, response):
        item = Event()
        for result in response.xpath('//div[@id="post"]') :
            item['title'] = result.css('.event a h3::text').extract_first()
            item['location'] = result.css('.event div h4 span.location::text').extract_first()
            item['date'] = result.css('.event div h4 span.time::text').extract_first()
            item['content'] = result.css('.event div p span::text').extract()
            yield item

