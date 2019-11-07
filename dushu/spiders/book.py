# -*- coding: utf-8 -*-
from redis import Redis
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from dushu.settings import HOST, PORT


class BookSpider(CrawlSpider):
    name = 'book'
    allowed_domains = ['www.dushu.com']
    start_urls = ['https://www.dushu.com/book/']
    r = Redis(host=HOST, port=PORT)
    rules = (
        # 提取图书的所有分类，如果没有指定callback，默认由parse来解析
        Rule(LinkExtractor(restrict_css='.sub-catalog'), follow=True),
        # 提取分类下的所有页规则
        Rule(LinkExtractor(restrict_css='.pages'), callback='parse_detail', follow=True),
        # 提取详情页面的规则
        # Rule(LinkExtractor(allow=r'/book/\d+/'), callback='parse_item', follow=False)
    )

    def parse_detail(self, response):
        url_list = response.xpath("//div[@class='book-info']/h3/a/@href").extract()
        for url in url_list:
            full_url = 'https://www.dushu.com' + url
            result = self.r.sadd('books_url', full_url)
            if result:
                yield Request(url=full_url, callback=self.parse_item)
            else:
                print(full_url, '已经爬取过了')

    def parse_item(self, response):
        item = {}
        item['name'] = response.css('.book-title').xpath('./h1/text()').get()
        price = response.css('.num').xpath('./text()').get()
        if '¥' in price:
            price = price[1:]
        else:
            price = price
        item['price'] = price
        item['author'] = response.css('.book-details-left').xpath('.//tr[1]/td[2]/text()').get()
        item['publisher'] = response.css('.book-details-left').xpath('.//tr[2]/td[2]/a/text()').get()
        item['publish_date'] = response.css('.book-details').xpath('./table//tr[1]/td[4]/text()').get()
        item['isbn'] = response.css('.book-details').xpath('./table//tr[1]/td[2]/text()').get()
        item['detail_url'] = response.url
        yield item
