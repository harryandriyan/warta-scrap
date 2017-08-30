import scrapy
from scrapy.selector import Selector
from viva.items import VivaItem


class VivaSpider(scrapy.Spider):
    name = "viva"
    allowed_domains = ["viva.co.id"]
    start_urls = [
        "http://www.viva.co.id/indeks",
    ]

    def parse(self, response):
        """ This function parses a property page.

        @url http://www.viva.co.id/indeks
        @returns items
        """

        indeks = Selector(response).xpath('//*[@id="load_segment"]/li')

        for indek in indeks:
            item = VivaItem()
            item['title'] = indek.xpath('div[@class="content_center"]/span/a[2]/h3/text()').extract()[0]
            item['link'] = indek.xpath('div[@class="content_center"]/span/a[2]/@href').extract()[0]
            item['images'] = indek.xpath('div[@class="thumb"]/a/img/@data-original').extract()[0]
            item['category'] = indek.xpath('div[@class="content_center"]/span/a[1]/h5/text()').extract()[0].strip()
            item['date'] = indek.xpath('div[@class="content_center"]/span/div[@class="date"]/text()').extract()[0]
            item['desc'] = ""

            yield item
