from scrapy.item import Item, Field


class AntaraItem(Item):
    # List of fields
    title = Field()
    link = Field()
    images = Field()
    category = Field()
    date = Field()
    desc = Field()
