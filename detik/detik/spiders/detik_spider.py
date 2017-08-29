import scrapy
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
        """

        indeks = Selector(response).xpath('//*[@id="indeks-container"]/li[1]')

        for indek in indeks:
            item = DetikItem()
            item['title'] = indek.xpath('article/div/a/h2/text()').extract()[0]
            item['link'] = indek.xpath('article/div/a/@href').extract()[0]
            item['images'] = ""
            item['category'] = ""
            item['date'] = indek.xpath('article/div/span/text()').extract()[0]
            item['desc'] = ""
            
            yield item
