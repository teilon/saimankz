# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import sqlite3
from itemadapter import ItemAdapter
from scrapy.loader import ItemLoader
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request

from saiman.items import ImageItem

CREATE_TABLE_PRODUCTS = '''
    CREATE TABLE products(
        title TEXT,
        category TEXT,
        price TEXT,
        product_url TEXT,
        image_name TEXT
        )
'''
INSERT_PRODUCT = '''
    INSERT INTO products (title, category, price, product_url, image_name) VALUES (?, ?, ?, ?, ?)
'''

MSG_TABLE_ALREADY_EXISTS = "Table already exists"

class SQLlitePipeline:

    def open_spider(self, spider):
        self.connection = sqlite3.connect("imdb.db")
        self.c = self.connection.cursor()
        try:
            self.c.execute(CREATE_TABLE_PRODUCTS)
            self.connection.commit()
        except sqlite3.OperationalError:
            logging.warning(MSG_TABLE_ALREADY_EXISTS)

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):

        if item.get('title'):
            self.c.execute(INSERT_PRODUCT, (
                item.get('title'),
                item.get('category'),
                item.get('price'),
                item.get('product_url'),
                item.get('image_name'),
            ))
            self.connection.commit()

        return item

class CustomImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        return [Request(x, meta={'image_name': item["image_name"]}) 
            for x in item.get('image_urls', [])]

    def file_path(self, request, response=None, info=None, *, item=None):
        # image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        image_name = request.meta['image_name']
        path = f'fuller/{image_name}.jpg'
        return path
        # return '%s.jpg' % request.meta['image_name']
