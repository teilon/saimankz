# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3
from itemadapter import ItemAdapter

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
        self.c.execute(INSERT_PRODUCT, (
            item.get('title'),
            item.get('category'),
            item.get('price'),
            item.get('product_url')
        ))
        self.connection.commit()
        return item
