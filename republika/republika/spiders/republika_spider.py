import scrapy
from scrapy.selector import Selector
from republika.items import RepublikaItem


class DetikSpider(scrapy.Spider):
    name = "republika"
    allowed_domains = ["republika.co.id"]
    start_urls = [
        "http://www.republika.co.id/indeks",
    ]

    def parse(self, response):
        """ This function parses a property page.

        @url http://www.republika.co.id/indeks
        @returns items
        """

        indeks = Selector(response).xpath('/html/body/div/div[3]/div[3]/div[1]')

        for indek in indeks:
            item = RepublikaItem()
            item['title'] = indek.xpath(
                '/html/body/div/div[3]/div[3]/div[1]/a/div[3]/text()').extract()[0]
            item['link'] = indek.xpath(
                '/html/body/div/div[3]/div[3]/div[1]/a/@href').extract()[0]
            item['images'] = ""
            item['category'] = ""
            item['date'] = ""
            item['desc'] = ""

            yield item
