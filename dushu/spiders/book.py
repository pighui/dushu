# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BookSpider(CrawlSpider):
    name = 'book'
    allowed_domains = ['www.dushu.com']
    start_urls = ['http://www.dushu.com/book/']

    rules = (
        # 提取图书的所有分类，如果没有指定callback，默认由parse来解析
        Rule(LinkExtractor(restrict_css='.sub-catalog'), follow=True),
        # 提取分类下的所有页规则
        Rule(LinkExtractor(restrict_css='.pages'), follow=True),
        # 提取详情页面的规则f
        Rule(LinkExtractor(allow=r'/book/\d+/'), callback='parse_item', follow=False)
    )

    def parse_item(self, response):
        item = {}
        item['name'] = response.css('.book-title h1').xpath('./text()').get()
        item['price'] = response.css('.num').xpath('./text()').get()[1:]
        item['author'] = response.css('.book-details-left').xpath('.//tr[1]//a/text()').get()
        item['publisher'] = response.css('.book-details-left').xpath('.//tr[2]//a/text()').get()
        item['publish_date'] = response.css('.book-details').xpath('./table//tr[1]/td[4]/text()').get()
        item['isbn'] = response.css('.book-details').xpath('./table//tr[1]/td[2]/text()').get()
        item['detail_url'] = response.url
        return item
