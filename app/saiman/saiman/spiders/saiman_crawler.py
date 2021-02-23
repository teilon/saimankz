import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import logging


class SaimanCrawlerSpider(CrawlSpider):
    name = 'saiman_crawler'
    allowed_domains = ['www.saiman.kz']
    start_urls = ['http://www.saiman.kz/products/']

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths=r"//div[@class='wrapper blocks']/div/a"), 
            callback='parse_category', 
            follow=True),
    )

    def parse_category(self, response):
        category_name = response.xpath("//h1[@class='title-1']/text()").get()
        meta = {'category_name': category_name}

        products = response.xpath("//div[@class='products-list']/a")
        for product in products:
            url = product.xpath(".//@href").get()
            
            yield response.follow(url=url, callback=self.parse_item, meta=meta)
        
        paginator = response.xpath("//div[@class='paginator']")
        if paginator:
            is_last_page = paginator.xpath(".//a[@class='active' and position() = last()]")
            if not is_last_page:
                next_page = paginator.xpath(".//a[@class='active']/following-sibling::a[1]/@href").get()
                absolute_url = f"{response.url}{next_page}"
                yield scrapy.Request(url=absolute_url, callback=self.parse_category)

    def parse_item(self, response):
        yield {
            'category': response.meta['category_name'],
            'title': response.xpath("normalize-space(//h1[@class='title-1']/text())").get(),
            'price': response.xpath("//div[@class='costs']/span/text()").get(),
        }
