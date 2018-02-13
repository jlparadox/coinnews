# -*- coding: utf-8 -*-
import scrapy
from scrapy.item import Item, Field

class Article(scrapy.Item):
    request_url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field(serializer=str)
    content = scrapy.Field()

class CointelegraphNewsSpider(scrapy.Spider):
    name = 'cointelegraph_news'
    start_urls = ['https://cointelegraph.com/tags/bitcoin/',
                  'https://cointelegraph.com/tags/ethereum',
                  'https://cointelegraph.com/tags/altcoin',
                  'https://cointelegraph.com/tags/blockchain',
                  'https://cointelegraph.com/tags/bitcoin-regulation',
                  'https://cointelegraph.com/tags/bitcoin-scams',]

    def parse(self, response):
        links = response.css('.results figure h2.header a::attr(href)')
        for link in links:
            url = response.urljoin(link.extract())
            yield scrapy.Request(url, callback=self.parse_content)
    
    def parse_content(self, response):
        item = Article()
        for result in response.css('div.post-container'):
            item['request_url'] = response.request.url
            item['title'] = result.css('.post-header h1.header::text').extract_first()
            item['author'] = result.css('.post-header .staff .user .name a::text').extract_first()
            item['date'] = result.css('.post-header div.date::attr(datetime)').extract_first()
            item['content'] = response.xpath('//div[@id="post"]/node()').extract()
            yield item
