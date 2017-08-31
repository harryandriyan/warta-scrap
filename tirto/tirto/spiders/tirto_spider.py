import scrapy
import time
from scrapy.selector import Selector
from tirto.items import TirtoItem


class TirtoSpider(scrapy.Spider):
    name = "tirto"
    allowed_domains = ["tirto.co.id"]
    start_urls = [
        "https://tirto.id/indeks",
    ]

    def parse(self, response):
        """ This function parses a property page.

        @url https://tirto.id/indeks
        @returns items
        """

        indeks = Selector(response).xpath('//div[@class="media-body"]')

        for indek in indeks:
            item = TirtoItem()
            item['title'] = indek.xpath('h4/a/text()').extract()[0]
            item['link'] = indek.xpath('h4/a/@href').extract()[0]
            item['images'] = ""
            item['category'] = indek.xpath('span/text()').extract()[0]
            item['date'] = time.strftime("%d/%m/%Y")
            item['desc'] = ""

            yield item
