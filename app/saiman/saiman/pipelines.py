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

from saiman.items import SaimanItem

CREATE_TABLE_PRODUCTS = '''
    CREATE TABLE products(
        title TEXT,
        category TEXT,
        price TEXT,
        product_url TEXT
        )
'''
INSERT_PRODUCT = '''
    INSERT INTO products (title, category, price, product_url) VALUES (?, ?, ?, ?)
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
            ))
            self.connection.commit()

        return item
    
    # def file_path(self, request, response=None, info=None):
    #     url = request if not isinstance(request, Request) else request.url
    #     media_guid = hashlib.sha1(to_bytes(url)).hexdigest()
    #     path, media_ext = os.path.splitext(url)
    #     media_name = os.path.split(path)[1]
    #     return '%s_%s%s' % (media_name, media_guid, media_ext)

    
    # {'image_urls': ['https://www.saiman.kz/i/Products/51.png'],
    #  'images': [
    #      {'checksum': 'cb67361adebb53cd9355e96a290e7453',
    #          'path': 'full/0e159089cec6d787796077e12da708e971b7f021.jpg',
    #          'status': 'downloaded',
    #          'url': 'https://www.saiman.kz/i/Products/51.png'}
    #          ],
    #  'product_name': '140325830074'
    #  }

class CustomImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        adapter = ItemAdapter(item)
        adapter['image_paths'] = image_paths
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        return 'files/' + os.path.basename(urlparse(request.url).path)

        #image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        #return f'fuller/{image_guid}.jpg'

        #url = request if not isinstance(request, Request) else request.url
        #media_guid = hashlib.sha1(to_bytes(url)).hexdigest()
        #path, media_ext = os.path.splitext(url)
        #media_name = os.path.split(path)[1]
        #return '%s_%s%s' % (media_name, media_guid, media_ext)



    # {'image_urls': ['https://www.saiman.kz/i/Products/80.png'],
    # 'images': [],
    # 'product_name': '154056874683'}