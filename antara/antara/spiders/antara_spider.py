import scrapy
import time
from scrapy.selector import Selector
from antara.items import AntaraItem


class AntaraSpider(scrapy.Spider):
    name = "antara"
    allowed_domains = ["antaranews.com"]
    start_urls = [
        "http://www.antaranews.com/terkini",
    ]

    def parse(self, response):
        """ This function parses a property page.

        @url http://www.antaranews.com/terkini
        @returns items
        """

        indeks = Selector(response).xpath('//ul[@class="ul_rubrik"]/li')

        for indek in indeks:
            item = AntaraItem()
            item['title'] = indek.xpath('div/div[@class="bxpd"]/h3/a/text()').extract_first()
            item['link'] = response.urljoin(indek.xpath('div/div[@class="bxpd"]/h3/a/@href').extract_first())
            item['images'] = indek.xpath('div/div[@class="imgpg"]/a/img/@src').extract_first()
            item['category'] = ""
            item['date'] = time.strftime("%d/%m/%Y")
            item['desc'] = ""

            yield item
