import scrapy
import time
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http.request import Request
from tirto.items import TirtoItem


class TirtoSpider(scrapy.Spider):
    name = "tirto"
    allowed_domains = ["tirto.co.id"]
    date_today = time.strftime("%Y-%m-%d")
    indeks_url = ''.join(["https://tirto.id/indeks?date=", date_today])
    start_urls = [
        indeks_url,
    ]

    def parse(self, response):
        """ This function parses a property page.

        @url https://tirto.id/indeks
        @returns items
        """

        indeks = Selector(response).xpath('//div[@class="media-body"]')

        for indek in indeks:
            item = TirtoItem()
            news_link = ''.join(['https:', indek.xpath('h4/a/@href').extract_first()])
            item['title'] = indek.xpath('h4/a/text()').extract_first()
            item['link'] = news_link
            item['category'] = indek.xpath('span/text()').extract_first()
            item['date'] = time.strftime("%d/%m/%Y")

            detail_request = Request(news_link, callback=self.parse_detail)
            detail_request.meta['item'] = item
            yield detail_request

    def parse_detail(self, response):
        print "Crawling detail news"
        item = response.meta['item']
        selector = Selector(response)
        description = selector.xpath('//div[@class="content-text-editor"]').extract_first()
        item['images'] = selector.xpath('//article/figure/img/@src').extract_first()
        item['desc'] = BeautifulSoup(description).text
        return item