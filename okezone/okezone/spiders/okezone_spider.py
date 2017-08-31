import scrapy
import time
from scrapy.selector import Selector
from okezone.items import OkezoneItem


class RepublikaSpider(scrapy.Spider):
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
            item['title'] = indek.xpath('h4/a/text()').extract()[0].strip()
            item['link'] = indek.xpath('h4/a/@href').extract()[0].strip()
            item['images'] = ""
            item['category'] = indek.xpath('h6/a/text()').extract()[0].strip()
            item['date'] = time.strftime("%d/%m/%Y")
            item['desc'] = ""

            yield item
