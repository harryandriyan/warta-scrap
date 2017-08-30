import scrapy
from scrapy.selector import Selector
from kompas.items import KompasItem


class KompasSpider(scrapy.Spider):
    name = "kompas"
    allowed_domains = ["kompas.com"]
    start_urls = [
        "http://indeks.kompas.com",
    ]

    def parse(self, response):
        """ This function parses a property page.

        @url http://indeks.kompas.com
        @returns items
        """

        indeks = Selector(response).xpath('//div[@class="article__list clearfix"]')

        for indek in indeks:
            item = KompasItem()
            item['title'] = indek.xpath('div[@class="article__list__title"]/h3/a/text()').extract()[0]
            item['link'] = indek.xpath('div[@class="article__list__title"]/h3/a/@href').extract()[0]
            item['images'] = indek.xpath('div[@class="article__list__asset clearfix"]/div/img/@src').extract()[0]
            item['category'] = indek.xpath('div[@class="article__list__info"]/div[@class="article__subtitle article__subtitle--inline"]/text()').extract()[0]
            item['date'] = indek.xpath('div[@class="article__list__info"]/div[@class="article__date"]/text()').extract()[0]
            item['desc'] = ""

            yield item
