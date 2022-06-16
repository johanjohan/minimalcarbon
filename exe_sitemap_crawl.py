# https://www.thepythoncode.com/article/extract-all-website-links-python
# https://www.thepythoncode.com/code/extract-all-website-links-python
# pip3 install requests bs4 colorama
# thank you!

import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
#import mimetypes
# pip install python-magic
# pip install python-magic-bin # win
import magic
import time

# init the colorama module
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
RED = colorama.Fore.RED

#-----------------------------------------
# 
#-----------------------------------------

# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()

total_urls_visited = 0

headers  = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    #'X-Mashape-Key': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    }
data_folder="data"
mime_types_allowed = ["text/html", "text/plain"]

# args defaults
def_url = "https://1001suns.com/sitemap_post/" # for args
def_url = "https://1001suns.com/universe_bochum21/" # for args
def_url = "https://karlsruhe.digital/"
def_max_urls = 1000

#-----------------------------------------
# 
#-----------------------------------------

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_content_type(url):
    # seems to be incorrect many times
    try:
        r = requests.head(url, allow_redirects=True)
        ### {'Date': 'Thu, 16 Jun 2022 16:03:31 GMT', 'Server': 'Apache/2.4.54 (Unix)', 'X-Powered-By': 'PHP/7.4.30', 'Allow': 'GET, POST, PUT', 'Cache-Control': 'no-store, no-cache, must-revalidate', 'Expires': 'Sat, 26 Jul 1997 05:00:00 GMT', 'Pragma': 'no-cache', 'Vary': 'User-Agent,Accept-Encoding', 'Content-Encoding': 'gzip', 'Content-Type': 'text/html; charset=UTF-8', 'Set-Cookie': 'PHPSESSID=8bss92l8og8s789ldp0p3u5uvr; path=/', 'Keep-Alive': 'timeout=3, max=100', 'Connection': 'Keep-Alive'}
        return r.headers["content-type"] # "text/html; charset=UTF-8"
    except Exception as e:
        print(f"{RED}[!] {url} Exception: {e}{RESET}")
        return None
    
def get_content_part(url, index):
    ct = get_content_type(url)
    if ct:
        subs = ct.split(';') # "text/html; charset=UTF-8"
        if len(subs) >= (index+1):
            return subs[index]

    return None

def get_encoding(url):
    return get_content_part(url, 1)
    
def get_mime_type(url):
    try:
        import urllib.request
        import ssl
        req = urllib.request.Request(url, data=None, headers=headers) # user agent
        # https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
        context = ssl._create_unverified_context()
        contentType = None
        with urllib.request.urlopen(req, context=context) as response:
            contentType   = response.headers.get_content_type()
            contentLength = response.headers.get('content-length')         
        return contentType
    except Exception as e:
        print(f"{RED}[!] {url} Exception: {e}{RESET}")
        return None
    
def get_all_website_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url,headers=headers).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        href = href.rstrip('/')
        if not is_valid(href):
            # not a valid URL
            print(f"{RED}[!] bad url: {href}{RESET}")
            continue
        if href in internal_urls:
            # already in the set
            continue
        
        # issue: https://www.facebook.com/karlsruhe.digital
        href_netloc = urlparse(href).netloc                 
        if domain_name not in href_netloc:  #  in href
            # external link
            if href not in external_urls:
                print(f"{GRAY}[!] External: {href}{RESET}")
                external_urls.add(href)
            continue
        
        mime_type =  get_mime_type(href)
        if not mime_type in mime_types_allowed:
            print(f"{RED}[!] skipped mime_type: {mime_type}{RESET}")
            continue
        
        if not href in internal_urls:
            print(
                f"{total_urls_visited}/{def_max_urls}", 
                mime_type, 
                f"{GREEN}[*] Internal: {href}{RESET}"
            )
            internal_urls.add(href)
        
        urls.add(href)
        
    return urls

def crawl(url, max_urls=30):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    global total_urls_visited
    total_urls_visited += 1
    print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)

#-----------------------------------------
# main
#-----------------------------------------
if __name__ == "__main__":
    start_secs = time.time()
    
    import argparse
    parser = argparse.ArgumentParser(description="Link Extractor Tool with Python")
    parser.add_argument("--url",        default=def_url,        type=str,   help="The URL to extract links from.")
    parser.add_argument("--max-urls",   default=def_max_urls,   type=int,   help="Number of max URLs to crawl.")
    
    #args = parser.parse_args()
    args, _unknown_args = parser.parse_known_args()
    url = args.url
    max_urls = args.max_urls
    print("url     :", url)
    print("max_urls:", max_urls)

    crawl(url, max_urls=max_urls)

    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total External links:", len(external_urls))
    print("[+] Total URLs:", len(external_urls) + len(internal_urls))
    print("[+] Total crawled URLs:", max_urls)

    domain_name = urlparse(url).netloc
    print("domain_name:", domain_name)

    # skip http
    print("before http replace:", len(internal_urls))
    internal_urls = [s.replace('http://', 'https://') for s in internal_urls]
    print("after http replace:", len(internal_urls))
    
    internal_urls = sorted(set(internal_urls))
    external_urls = sorted(set(external_urls))
    
    # save the internal links to a file
    print("save the internal links to a file...")
    with open(f"{data_folder}/{domain_name}_internal_links.csv", "w", encoding="utf-8") as f:
        for internal_link in internal_urls:
            f.write(internal_link.strip() + "\n")

    # save the external links to a file
    print("save the external links to a file...")
    with open(f"{data_folder}/{domain_name}_external_links.csv", "w", encoding="utf-8") as f:
        for external_link in external_urls:
            f.write(external_link.strip() + "\n")
            
    print("all done:", "duration:", round(time.time() - start_secs, 1), "s")