import scrapy
from scrapy import Spider
from scrapy.selector import Selector

from detik.items import DetikItem


class DetikSpider(scrapy.Spider):
    name = "detik"
    allowed_domains = ["detik.com"]
    start_urls = [
        "http://news.detik.com/indeks",
    ]

    def parse(self, response):
        """ This function parses a property page.

        @url http://news.detik.com/indeks
        @returns items
        @scrapes title link server date
        """

        indeks = Selector(response).xpath('//*[@id="indeks-container"]')

        for indek in indeks:
            item = DetikItem()
            item['title'] = indek.xpath('li[1]/article/div/a/h2').extract()[0]
            item['link'] = indek.xpath('li[1]/article/div/a').extract()[0]
            item['images'] = ""
            item['category'] = ""
            item['date'] = indek.xpath('li[1]/article/div/span').extract()[0]
            item['desc'] = ""
            
            yield item
