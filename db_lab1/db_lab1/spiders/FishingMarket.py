import scrapy
from db_lab_1.items import ProdItem


class FishMarktUaSpider(scrapy.Spider):
    name = "fishmarkt"
    custom_settings = {
        'ITEM_PIPELINES': {
            'db_lab1.pipelines.Task2XmlPipeline': 300,
        },
        'CLOSESPIDER_PAGECOUNT': 0,
        'CLOSESPIDER_ITEMCOUNT': 20
    }
    fields = {
        'product': '//div[@class="product-container"]',
        'img': './div[@class="left-block"]/div[@class="product-image-container"]/a/img/@src',
        'name': './div[@class="right-block"]/h5/a/text()',
        'link': './div[@class="right-block"]/h5/a/@href',
        'price': './div[@class="right-block"]/div[@class="content_price"]/span/text()',
    }
    start_urls = [
        'https://fishing-mart.com.ua'
    ]
    allowed_domains = [
        'fishing-mart.com.ua'
    ]

    def parse(self, response):
        for product in response.xpath(self.fields["product"]):
            prod = ProdItem()
            prod['prodImage'] = product.xpath(self.fields['img']).extract()
            prod['prodPrice'] = product.xpath(self.fields['price']).extract()
            prod['prodName'] = product.xpath(self.fields['name']).extract()
            prod['prodLink'] = product.xpath(self.fields['link']).extract()
            yield prod
