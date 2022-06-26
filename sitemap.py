# https://www.jcchouinard.com/create-xml-sitemap-with-python/
# https://stackoverflow.com/questions/46446457/generating-a-sitemap-using-python

import xml.etree.cElementTree as ET
from xml.dom import minidom
import datetime
import config
import helpers_web as wh

#-----------------------------------------
# 
#-----------------------------------------
def sitemap_xml_from_list(links, out_xml_path='sitemap.xml'):
    print("sitemap_xml_from_list:", out_xml_path)
    #print("sitemap_xml_from_list", *links, sep="\n\t")
    
    root = ET.Element('urlset')
    root.attrib['xmlns:xsi']="http://www.w3.org/2001/XMLSchema-instance"
    root.attrib['xsi:schemaLocation']="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"
    root.attrib['xmlns']="http://www.sitemaps.org/schemas/sitemap/0.9"

    dt = datetime.datetime.now().strftime ("%Y-%m-%d")
    for link in links:
        print("\t\t xml:", link)
        doc = ET.SubElement(root, "url")
        ET.SubElement(doc, "loc").text = link
        ET.SubElement(doc, "lastmod").text = dt
        ET.SubElement(doc, "changefreq").text = "weekly"
        ET.SubElement(doc, "priority").text = "1.0"

    # not pretty
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0) # pretty
    tree.write(out_xml_path, encoding='utf-8', xml_declaration=True)
    
    return out_xml_path

def sitemap_xml_from_file(in_list_path, out_xml_path='sitemap.xml'):
    with open(in_list_path) as file:
        links = file.readlines()
        links = [link.rstrip() for link in links]
        xmlpath = sitemap_xml_from_list(links, out_xml_path)
        
#-----------------------------------------
# 
#-----------------------------------------
    
import requests
from bs4 import BeautifulSoup
import re

def _make_soup(url):
    print("make_soup:", "trying as an online file:", url)
    try:
        r = requests.get(url, headers=wh.headers) # needs user agent
        text = r.text
    except: # try a local file
        print("make_soup:", "trying as a local file:", url)
        with open(url, encoding='utf-8') as file:
            text = file.read()
    #print("text:", text)  
    return BeautifulSoup(text, features='lxml-xml')

# put urls in a list
def _get_xml_urls(soup):
    #print(soup.prettify())
    return [loc.string for loc in soup.find_all('loc')]

# get the img urls
def __get_src_contain_str(soup, string):
    return [img['src'] for img in soup.find_all('img', src=re.compile(string))]

def read_sitemap_xml_to_list(xmlpath):
    print("read_sitemap_xml_to_list: xmlpath:", xmlpath)
    soup = _make_soup(xmlpath)
    #print(soup.prettify())
    urls = _get_xml_urls(soup)
    #print("urls:", *urls, sep="\n\t")
    return urls
        
#-----------------------------------------
# 
#-----------------------------------------
if __name__ == "__main__":
    
    #-----------------------------------------
    # write sitemap.xml
    #-----------------------------------------

    sitemap_xml_from_file(in_list_path=config.sitemap_links_internal_path, out_xml_path=config.sitemap_xml_path)
        
if __name__ == '__main__':
    
    #-----------------------------------------
    # read sitemap.xml
    #-----------------------------------------
    
    # xmlpath = 'http://www.adidas.it/on/demandware.static/-/Sites-adidas-IT-Library/it_IT/v/sitemap/product/adidas-IT-it-it-product.xml'
    # xmlpath = 'https://1001suns.com/sitemap.xml'
    xmlpath = config.sitemap_xml_path # a local file or url
    
    urls = read_sitemap_xml_to_list(xmlpath)
    print("urls:", *urls, sep="\n\t")
    
    # # loop through the urls
    # for url in urls:
    #     url_soup = make_soup(url)
    #     srcs = get_src_contain_str(url_soup, 'zoom')
    #     print(srcs)
    
        