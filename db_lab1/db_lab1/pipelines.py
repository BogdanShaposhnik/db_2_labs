from lxml import etree


class Task1XmlPipeline:
    def open_spider(self, spider):
        self.root = etree.Element('data')

    def close_spider(self, spider):
        with open('results/kpi.xml', 'wb') as file:
            etree.ElementTree(self.root).write(file, pretty_print=True, encoding="UTF-8")

    def process_item(self, item, spider):
        page = etree.SubElement(self.root, 'page', url=item['url'])
        for text in item['text']:
            etree.SubElement(page, 'fragment', type='text').text = text
        for url in item['images']:
            etree.SubElement(page, 'fragment', type='image').text = url
        return item


class Task2XmlPipeline:
    def open_spider(self, spider):
        self.root = etree.Element('items')

    def close_spider(self, spider):
        with open('results/fishmarket.xml', 'wb') as file:
            etree.ElementTree(self.root).write(file, pretty_print=True, encoding="UTF-8")

    def process_item(self, item, spider):
        item1 = etree.SubElement(self.root, 'item')
        link = etree.SubElement(item1, 'link')
        etree.SubElement(link, 'value').text = item['prodLink'][0]
        etree.SubElement(item1, 'price').text = item['prodPrice'][0]
        image = etree.SubElement(item1, 'img')
        etree.SubElement(image, 'value').text = item['prodImage'][0]
        etree.SubElement(item1, 'name').text = item['prodName'][0]
        return item
