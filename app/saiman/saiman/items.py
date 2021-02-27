# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

#import scrapy
from scrapy import Item, Field
from scrapy.loader.processors import TakeFirst, MapCompose

def remove_extention(value):
    return os.path.splitext(value)[0]
    

class ImageItem(Item):
    image_urls = Field()
    images = Field()
    image_name = Field(
        # input_processor = MapCompose(remove_extention),
        output_processor = TakeFirst()        
    )
    # image_path = Field()

class ProductItem(Item):
    title = Field()
    category = Field()
    price = Field()
    product_url = Field()
    image_name = Field()
