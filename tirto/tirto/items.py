from scrapy.item import Item, Field


class MerdekaItem(Item):
    # List of fields
    title = Field()
    link = Field()
    images = Field()
    category = Field()
    date = Field()
    desc = Field()
