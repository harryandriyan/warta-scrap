import scrapy
import sys
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http.request import Request
from republika.items import RepublikaItem


class RepublikaSpider(scrapy.Spider):
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
        print "Crawling list of news"
        indeks = Selector(response).xpath('//div[@class="wp-indeks"]')
        indeks_length = len(indeks)
        if float(indeks_length) > 0:
            for indek in indeks:
                item = RepublikaItem()
                news_link = indek.xpath('a/@href').extract_first()
                item['title'] = indek.xpath('a/div[@class="item3"]/text()').extract_first()
                item['link'] = news_link
                item['images'] = indek.xpath('a/div[@class="item2"]/div[@class="img-ct"]/img/@src').extract_first()
                item['category'] = ""
                item['date'] = indek.xpath('a/div[@class="item1"]/div[@class="date"]/text()').extract_first()
                detail_request = Request(news_link, callback=self.parse_detail)
                detail_request.meta['item'] = item
                yield detail_request

        else:
            sys.exit()

        # get the true next pagination link
        next_page_text = Selector(response).xpath('//div[@class="pagination"]/section/nav/a/text()').extract_first()
        if next_page_text == "Next":
            next_page_link = Selector(response).xpath('//div[@class="pagination"]/section/nav/a/@href').extract_first()
        else:
            next_page_link = Selector(response).xpath('//div[@class="pagination"]/section/nav/a[2]/@href').extract_first()

        if next_page_link:
            yield scrapy.Request(
                response.urljoin(next_page_link),
                callback=self.parse
            )

    def parse_detail(self, response):
        print "Crawling detail news"
        item = response.meta['item']
        selector = Selector(response)
        description = selector.xpath('//div[@class="content-detail"]').extract_first()
        item['desc'] = BeautifulSoup(description).text
        return item