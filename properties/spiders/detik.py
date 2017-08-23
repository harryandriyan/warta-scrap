import datetime
import urlparse
import socket
import scrapy

from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader

from properties.items import PropertiesItem


class DetikSpider(scrapy.Spider):
    name = "detik"

    # Start on a property page
    start_urls = (
        'http://news.detik.com/indeks',
    )

    def parse(self, response):
        """ This function parses a property page.

        @url http://news.detik.com/indeks
        @returns items
        @scrapes title link server date
        """

        # Create the loader using the response
        l = ItemLoader(item=PropertiesItem(), response=response)

        return l.load_item()
