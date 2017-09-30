import scrapy
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http.request import Request
from viva.items import VivaItem


class VivaSpider(scrapy.Spider):
    name = "viva"
    allowed_domains = ["viva.co.id"]
    start_urls = [
        "http://www.viva.co.id/indeks/berita",
    ]

    def parse(self, response):
        """ This function parses a property page.

        @url http://www.viva.co.id/indeks/berita
        @returns items
        """

        indeks = Selector(response).xpath('//*[@id="load_segment"]/li')

        for indek in indeks:
            item = VivaItem()
            news_link = indek.xpath('div[@class="content_center"]/span/a[2]/@href').extract_first()
            item['title'] = indek.xpath('div[@class="content_center"]/span/a[2]/h3/text()').extract_first()
            item['link'] = news_link
            item['images'] = indek.xpath('div[@class="thumb"]/a/img/@data-original').extract_first()
            item['category'] = indek.xpath('div[@class="content_center"]/span/a[1]/h5/text()').extract_first().strip()
            item['date'] = indek.xpath('div[@class="content_center"]/span/div[@class="date"]/text()').extract_first()
            detail_request = Request(news_link, callback=self.parse_detail)
            detail_request.meta['item'] = item
            yield detail_request

    def parse_detail(self, response):
        print("Crawling detail news")
        item = response.meta['item']
        selector = Selector(response)
        description = selector.xpath('//div[@id="article-detail-content"]').extract_first()
        item['desc'] = BeautifulSoup(description).text
        return item