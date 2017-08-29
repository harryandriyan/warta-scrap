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

        indeks = Selector(response).xpath('//div[@class="wp-indeks"]')

        for indek in indeks:
            item = RepublikaItem()
            item['title'] = indek.xpath('a/div[@class="item3"]/text()').extract()[0]
            item['link'] = indek.xpath('a/@href').extract()[0]
            item['images'] = indek.xpath('a/div[@class="item2"]/div[@class="img-ct"]/img/@src').extract()[0]
            item['category'] = ""
            item['date'] = indek.xpath('a/div[@class="item1"]/div[@class="date"]/text()').extract()[0]
            item['desc'] = ""

            yield item
