import scrapy
import sys
from scrapy.selector import Selector
from scrapy.http.request import Request
from republika.items import RepublikaItem


class RepublikaSpider(scrapy.Spider):
    name = "republika"
    allowed_domains = ["republika.co.id"]
    start_urls = [
        "http://www.republika.co.id/indeks",
    ]
    detail_url = []

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
                news_link = indek.xpath('a/@href').extract()[0]
                item['title'] = indek.xpath('a/div[@class="item3"]/text()').extract()[0]
                item['link'] = news_link
                detail_request = Request(news_link, callback=self.parse_detail)
                item['images'] = indek.xpath('a/div[@class="item2"]/div[@class="img-ct"]/img/@src').extract()[0]
                item['category'] = ""
                item['date'] = indek.xpath('a/div[@class="item1"]/div[@class="date"]/text()').extract()[0]
                item['desc'] = detail_request

                yield item
        else:
            sys.exit()

        # get the true next pagination link
        next_page_text = Selector(response).xpath('//div[@class="pagination"]/section/nav/a/text()').extract()[0]
        if next_page_text == "Next":
            next_page_link = Selector(response).xpath('//div[@class="pagination"]/section/nav/a/@href').extract()[0]
        else:
            next_page_link = Selector(response).xpath('//div[@class="pagination"]/section/nav/a[2]/@href').extract()[0]

        if next_page_link:
            yield scrapy.Request(
                response.urljoin(next_page_link),
                callback=self.parse
            )

    def parse_detail(self, response):
        print "Crawling detail news"
        selector = Selector(response)
        description = selector.xpath('//div[@class="content-detail"]/p/text()').extract()[0]

        return description