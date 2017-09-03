import scrapy
from scrapy.selector import Selector
from scrapy.http.request import Request
from detik.items import DetikItem

# compatibility between python 2 and 3
try:
    from urllib.parse import urlparse
except:
    from urlparse import urlparse

class DetikSpider(scrapy.Spider):
    name = "detik"
    allowed_domains = ["detik.com"]
    start_urls = [
        "http://news.detik.com/",
        "http://news.detik.com/indeks",
    ]

    def parse(self, response):
        """ This function parses a property page.

        @url http://news.detik.com/indeks
        @returns items
        """

        html_selector = Selector(response)

        # get all links only from detik.com
        links = html_selector.xpath('//a/@href').extract()
        links = [link for link in links if 'detik.com' in link]

        # full url
        links = map(response.urljoin, links)

        # follow the next links, so we can crawl recursively
        for link in links:
            yield Request(link, self.parse)

        # now we need to figure out, is the current response
        # is news article or not? I put simple logic here
        # but for the next version we have to identify the
        # structure of news page so we can identify it easier
        url = response.url
        path = urlparse(url).path
        if path.startswith('/berita'):
            # parse the news article
            layout = html_selector.xpath('//article')[0] # May raise exception here. Becareful
            item = DetikItem()
            item['date'] = layout.xpath('//div[@class="jdl"]/div[@class="date"]/text()').extract_first()
            item['title'] = layout.xpath('//div[@class="jdl"]/h1/text()').extract_first()
            item['link'] = response.url
            item['images'] = layout.xpath('//div[@class="pic_artikel"]/img/@src').extract_first()
            # it is not clean. TODO: clean the HTML tag
            item['desc'] = layout.xpath('//div[@class="detail_text"]').extract_first()
            yield item
