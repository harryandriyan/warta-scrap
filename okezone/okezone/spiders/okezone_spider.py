import scrapy
import time
import sys
from __future__ import print_function
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http.request import Request
from okezone.items import OkezoneItem


class OkezoneSpider(scrapy.Spider):
    name = "okezone"
    allowed_domains = ["okezone.com"]
    start_urls = [
        "http://index.okezone.com/",
    ]

    def parse(self, response):
        """ This function parses a property page.

        @url http://index.okezone.com/
        @returns items
        """

        indeks = Selector(response).xpath('//*[@id="in"]/ol/li')

        for indek in indeks:
            item = OkezoneItem()
            news_link = indek.xpath('h4/a/@href').extract_first().strip()
            item['title'] = indek.xpath('h4/a/text()').extract_first().strip()
            item['link'] = news_link
            item['category'] = indek.xpath('h6/a/text()').extract_first().strip()
            item['date'] = time.strftime("%d/%m/%Y")
            detail_request = Request(news_link, callback=self.parse_detail)
            detail_request.meta['item'] = item
            yield detail_request

    def parse_detail(self, response):
        print("Crawling detail news")
        item = response.meta['item']
        selector = Selector(response)
        description = selector.xpath('//*[@id="contentx"]').extract_first()
        item['desc'] = BeautifulSoup(description).text.strip()
        item['images'] = selector.xpath('//*[@id="imgCheck"]/@src')
        return item