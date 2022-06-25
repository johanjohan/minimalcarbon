# https://www.jcchouinard.com/create-xml-sitemap-with-python/
# https://stackoverflow.com/questions/46446457/generating-a-sitemap-using-python

import xml.etree.cElementTree as ET
from xml.dom import minidom
import datetime
import config
import helpers_web as wh


def create_xml_sitemap(links, out_xmlpath='sitemap.xml'):
    print("registerSiteMaps:", out_xmlpath)
    #print("registerSiteMaps", *links, sep="\n\t")
    
    root = ET.Element('urlset')
    root.attrib['xmlns:xsi']="http://www.w3.org/2001/XMLSchema-instance"
    root.attrib['xsi:schemaLocation']="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"
    root.attrib['xmlns']="http://www.sitemaps.org/schemas/sitemap/0.9"

    for link in links:
        print("\t\t xml:", link)
        dt = datetime.datetime.now().strftime ("%Y-%m-%d")
        doc = ET.SubElement(root, "url")
        ET.SubElement(doc, "loc").text = link
        ET.SubElement(doc, "lastmod").text = dt
        ET.SubElement(doc, "changefreq").text = "weekly"
        ET.SubElement(doc, "priority").text = "1.0"

    # not pretty
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0) # pretty
    tree.write(out_xmlpath, encoding='utf-8', xml_declaration=True)
    
import requests
from bs4 import BeautifulSoup
import re

def make_soup(url):
    try:
        r = requests.get(url, headers=wh.headers) # needs user agent
        text = r.text
    except:
        # try a local file
        print("trying as a local file:", url)
        with open(url, encoding='utf-8') as file:
            text = file.read()
    #print("text:", text)  
    
    soup = BeautifulSoup(text, features='lxml-xml')
    print(soup.prettify())
    return soup

# put urls in a list
def get_xml_urls(soup):
    urls = [loc.string for loc in soup.find_all('loc')]
    return urls

# get the img urls
def get_src_contain_str(soup, string):
    srcs = [img['src'] for img in soup.find_all('img', src=re.compile(string))]
    return srcs

if __name__ == '__main__':
    xmlpath = 'http://www.adidas.it/on/demandware.static/-/Sites-adidas-IT-Library/it_IT/v/sitemap/product/adidas-IT-it-it-product.xml'
    xmlpath = 'https://1001suns.com/sitemap.xml'
    xmlpath = config.sitemap_xml_path # a local file
    print("xmlpath:", xmlpath)
    
    soup = make_soup(xmlpath)
    
    urls = get_xml_urls(soup)
    
    # # loop through the urls
    # for url in urls:
    #     url_soup = make_soup(url)
    #     srcs = get_src_contain_str(url_soup, 'zoom')
    #     print(srcs)
    
    print("urls:", *urls, sep="\n\t")
        

if False and __name__ == "__main__":
    with open(config.sitemap_links_internal) as file:
        links = file.readlines()
        links = [line.rstrip() for line in links]
        create_xml_sitemap(links)
        
    
exit(0)


# # # import pandas as pd
# # # import os
# # # import datetime 
# # # from jinja2 import Template
# # # import gzip

# # # # Set-Up Maximum Number of URLs (recommended max 50,000)
# # # n = 50000

# # # # Create a Sitemap Template to Populate
 
# # # sitemap_template='''<?xml version="1.0" encoding="UTF-8"?>
# # # <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
# # #     {% for page in pages %}
# # #     <url>
# # #         <loc>{{page[1]|safe}}</loc>
# # #         <lastmod>{{page[3]}}</lastmod>
# # #         <changefreq>{{page[4]}}</changefreq>
# # #         <priority>{{page[5]}}</priority>        
# # #     </url>
# # #     {% endfor %}
# # # </urlset>'''
 
# # # template = Template(sitemap_template)
 
# # # # Get Today's Date to add as Lastmod
# # # lastmod_date = datetime.datetime.now().strftime('%Y-%m-%d')




""" 
https://stackoverflow.com/questions/41781054/how-do-i-create-a-list-from-a-sitemap-xml-file-to-extract-the-url-in-python
import requests
from bs4 import BeautifulSoup
import re

def make_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup
# put urls in a list
def get_xml_urls(soup):
    urls = [loc.string for loc in soup.find_all('loc')]
    return urls
# get the img urls
def get_src_contain_str(soup, string):
    srcs = [img['src']for img in soup.find_all('img', src=re.compile(string))]
    return srcs
if __name__ == '__main__':
    xml = 'http://www.adidas.it/on/demandware.static/-/Sites-adidas-IT-Library/it_IT/v/sitemap/product/adidas-IT-it-it-product.xml'
    soup = make_soup(xml)
    urls = get_xml_urls(soup)
    # loop through the urls
    for url in urls:
        url_soup = make_soup(url)
        srcs = get_src_contain_str(url_soup, 'zoom')
        print(srcs)


"""