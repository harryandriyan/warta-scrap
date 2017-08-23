from scrapy.item import Item, Field


class PropertiesItem(Item):
    # List of fields
    title = Field()
    images = Field()
    category = Field()
    date = Field()
    desc = Field()
