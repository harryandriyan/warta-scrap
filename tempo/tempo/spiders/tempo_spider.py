import scrapy
from scrapy.selector import Selector
from tempo.items import TempoItem


class VivaSpider(scrapy.Spider):
    name = "tempo"
    allowed_domains = ["tempo.co"]
    start_urls = [
        "https://www.tempo.co/indeks",
    ]

    def parse(self, response):
        """ This function parses a property page.

        @url https://www.tempo.co/indeks
        @returns items
        """

        indeks = Selector(response).xpath('//ul[@class="wrapper"]/li')

        for indek in indeks:
            item = TempoItem()
            item['title'] = indek.xpath('div/div/a[2]/h2/text()').extract()[0]
            item['link'] = indek.xpath('div/div/a[2]/@href').extract()[0]
            item['images'] = indek.xpath('div/div/a[1]/img/@src').extract()[0]
            item['category'] = ""
            item['date'] = indek.xpath('div/div/a[2]/span/text()').extract()[0]
            item['desc'] = ""

            yield item
