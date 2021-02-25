# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

#import scrapy
from scrapy import Item, Field
from scrapy.loader.processors import TakeFirst


class SaimanItem(Item):
    image_urls = Field()
    images = Field()
    product_name = Field(
        output_processor = TakeFirst()
    )

class ProductItem(Item):
    title = Field()
    category = Field()
    price = Field()
    product_url = Field()
