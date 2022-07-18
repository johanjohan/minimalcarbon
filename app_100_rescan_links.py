
from helpers_web import links_make_absolute, links_remove_externals, links_strip_query_and_fragment, sq as sq, strip_query_and_fragment, url_path
from helpers_web import dq as dq
from helpers_web import pa as pa
from helpers_web import qu as qu
from helpers_web import add_trailing_slash as ats
from bs4 import BeautifulSoup, Comment
import time
import helpers_web as wh
import os
import requests
import lxml.html
import lxml
import chromedriver_binary  # pip install chromedriver-binary-auto
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver  # pip install selenium
from selenium.webdriver.chrome.options import Options

from app_050_sitemap_crawl import rectify

import jsbeautifier
import cssbeautifier

from urllib.parse import urlparse
import pyautogui as pag

import image_sizes
import urllib.parse

import config
GREEN = config.GREEN
GRAY = config.GRAY
RESET = config.RESET
YELLOW = config.YELLOW
RED = config.RED
CYAN = config.CYAN
MAGENTA = config.MAGENTA

# -----------------------------------------
#
# -----------------------------------------
start_secs              = time.time()
# images_written          = []
# assets_written          = []
# verbose                 = True

# image_size_tuples       = []
# urls_visited            = []

b_extend_rescan_urls    = True

valid_exts      = [".html", ".htm", ".php", ""] # ""!!!
# -----------------------------------------
#
# -----------------------------------------
def force_replace_karlsruhe_digital(url):
    url = wh.link_replace_pair(url, "http://karlsruhe.digital",     "https://karlsruhe.digital")
    url = wh.link_replace_pair(url, "http://www.karlsruhe.digital", "https://karlsruhe.digital")
    return url
    
def rectify_links(urls):
    urls = wh.links_remove_comments(urls, '#')
    urls = wh.links_replace(urls, config.replacements_pre)
    urls = wh.links_remove_externals(urls, config.base)
    urls = wh.links_remove_excludes(urls, config.protocol_excludes)
    urls = wh.links_remove_excludes(urls, config.sitemap_links_ignore)
    urls = wh.links_strip_query_and_fragment(urls)
    urls = wh.links_make_absolute(urls, config.base)
    urls = wh.links_sanitize(urls)
    return urls


# -----------------------------------------
#
# -----------------------------------------
if __name__ == "__main__":
    
    wh.logo_filename(__file__)
    wh.log("__file__", __file__, filepath=config.path_log_params)
    wh.log("re-scanning for new links in given urls...", filepath=config.path_log_params)

    # -----------------------------------------
    # 
    # -----------------------------------------     
    wh.file_make_unique(config.path_sitemap_links_internal, True)
    urls = wh.list_from_file(config.path_sitemap_links_internal)
    
    # # # # # urls = wh.links_remove_comments(urls, '#')
    # # # # # urls = wh.links_replace(urls, config.replacements_pre)
    # # # # # urls = wh.links_remove_externals(urls, config.base)
    # # # # # urls = wh.links_strip_query_and_fragment(urls)
    # # # # # urls = wh.links_make_absolute(urls, config.base)
    # # # # # urls = wh.links_sanitize(urls)
    urls = rectify_links(urls)
    urls_len_orig   = len(urls)    
    urls_orig       = urls.copy()
    links_a_href    = []
    for count, url in enumerate(urls):
        
        url = force_replace_karlsruhe_digital(url)
        url = rectify(url, config.base)
        
        print()
        wh.progress(count / len(urls), verbose_string="TOTAL", VT=CYAN, n=16, prefix="\t")
        print()
        wh.sleep_random(config.wait_secs, verbose_string=url, n=16, prefix="\t") 
        
        protocol, loc, path = wh.url_split(url)
        name, ext = os.path.splitext(path) # also splits the domain
        #print("\t", "name", name, "ext", ext)
        if not ext in valid_exts:
            print("\t\t", YELLOW, "skipping:", RED, wh.dq(ext), RESET)
            continue

        n = 15
        if response := wh.get_response(url, pre="\t"):
            
            content = response.read().decode('utf-8')
            url     = rectify(response.url, config.base)  # may be redirected
            
            if url in links_a_href:
                continue
            
            links_a_href.append(url)
            
            tree  = lxml.html.fromstring(content)
            hrefs = tree.xpath('//a/@href') # //a[@href and not(@disabled)]
            for href in hrefs:
                
                ###href = href.strip()
                href = wh.link_replace(href, config.replacements_pre) # some are bad like "http:// http://www.xxx.com"
                href = force_replace_karlsruhe_digital(href)
                href = rectify(href, config.base)
                
                if any(ex in href for ex in config.protocol_excludes): # exclude whatsapp: etc
                    #print("\t\t", "exclude:".ljust(n), YELLOW, href, RESET)
                    continue
                
                if wh.url_is_external(href, config.base):
                    #print("\t\t", "external:".ljust(n), RED, href, RESET )
                    continue
                
                if href in links_a_href:
                    continue

                href, is_redirected = wh.get_redirected_url(href)
                href = rectify(href, config.base)
                
                if href in links_a_href:
                    continue

                # proven status above: get_redirected_url  
                protocol, loc, path = wh.url_split(href)
                name, ext = os.path.splitext(path)
                if ext in valid_exts:
                    print("\t\t", "append:".ljust(n), GREEN, href, RESET)
                    links_a_href.append(href)
                        
                                        
                # status = wh.get_status_code(href)
                # if status and status < 400:
                #     name, ext = os.path.splitext(href)
                #     if ext in valid_exts:
                #         print("\t\t", "append:".ljust(n), GREEN, href, RESET)
                #         links_a_href.append(href)
                # else:
                #     print("\t\t", "bad status:".ljust(n), RED, status, href, RESET)
                    
        else:
            print(RED, "error logged:".ljust(n), config.path_links_errors)
            wh.string_to_file(url + "\n", config.path_links_errors, mode="a")                
        ###break # debug
    ### for />
    
    # errs
    if os.path.isfile(config.path_links_errors):
        wh.file_make_unique(config.path_links_errors, sort=True)    

    # add to urls
    print("len(links_a_href):", len(links_a_href))
    #urls.extend(links_a_href)
    urls = links_a_href
    # # # urls = wh.links_remove_externals(urls, config.base)
    # # # urls = wh.links_remove_excludes(urls, config.protocol_excludes)
    # # # urls = wh.links_remove_excludes(urls, config.sitemap_links_ignore) # NEW
    # # # urls = wh.links_replace(urls, config.replacements_pre)
    # # # urls = wh.links_strip_query_and_fragment(urls)
    # # # urls = wh.links_make_absolute(urls, config.base)
    # # # urls = wh.links_sanitize(urls)   
    urls = rectify_links(urls)
    print("len(urls) after:", len(urls), "added:", len(urls) - urls_len_orig)  
    time.sleep(3)
    
    # save back to file 
    wh.list_to_file(urls, config.path_sitemap_links_internal)             

    #print("urls:", GREEN, *urls, RESET, sep="\n\t")
    print("len(urls):", len(urls))
    
    urls_no_frag = urls.copy()
    urls_no_frag = wh.links_strip_query_and_fragment(urls_no_frag)
    urls_no_frag = wh.links_sanitize(urls_no_frag)   
    print("len(urls_no_frag):", len(urls_no_frag))
    
    urls_diff = list(set(urls) - set(urls_orig))
    urls_diff = wh.links_sanitize(urls_diff)   
    print("len(urls_diff):", len(urls_diff))
    
    print("", "additions:", wh.GREEN, *urls_diff, wh.RESET, sep="\n\t")
    wh.log("additions:", urls_diff, filepath=config.path_log_params, echo=False)

      
    # all done
    wh.log("all done: duration: {:.1f}m".format((time.time() - start_secs)/60.0), filepath=config.path_log_params)

    exit(0)
