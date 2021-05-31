from scrapy import cmdline
import os
import lxml.etree


def xslt_parse():
    dom = lxml.etree.parse('results/fishmarket.xml')
    xslt = lxml.etree.parse('fishmarket.xslt')
    transform = lxml.etree.XSLT(xslt)
    newdom = transform(dom)
    with open('results/fishmarket.html', 'wb') as f:
        f.write(lxml.etree.tostring(newdom, pretty_print=True))


#cmdline.execute("scrapy crawl fishmarkt".split())
#with open('results/fishmarket.xml', 'r') as file:
    #root = lxml.etree.parse(file)
xslt_parse()
