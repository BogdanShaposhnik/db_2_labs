from scrapy import cmdline
from lxml import etree

cmdline.execute("scrapy crawl kpi".split())
root = None
print('Average count of text fragments per p')
with open('results/kpi.xml', 'r') as file:
    root = etree.parse(file)
#root = tree.getroot()
#urls = root.findall("page")
#for url in urls:
    #print(url.get('url'))



