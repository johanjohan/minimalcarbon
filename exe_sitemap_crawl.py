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
import urllib.request
import ssl
import datetime
        
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
start_secs = time.time()
args    = None

date_time  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

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

def get_status_code(url, fast=True, timeout=5):
    try:
        if fast:
            r = requests.head(url,verify=True,timeout=timeout) # it is faster to only request the header
            return (r.status_code)
        else:
            req = urllib.request.Request(url, timeout=timeout, data=None, headers=headers) # user agent
            context = ssl._create_unverified_context()
            with urllib.request.urlopen(req, context=context) as response:
                return response.getcode()
    except Exception as e:
        print(f"{RED}[!] {url} Exception: {e}{RESET}")
        return -1

def get_all_website_links(url, max_urls):
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
                print(
                    f"{total_urls_visited}/{max_urls}", 
                    f"{GRAY}[!] External: {href}{RESET}"
                )
                external_urls.add(href)
            continue
        
        mime_type =  get_mime_type(href)
        if not mime_type in mime_types_allowed:
            print(f"{RED}[!] skipped mime_type: {mime_type}{RESET}")
            continue
        
        if not href in internal_urls:
            print(
                f"{total_urls_visited}/{max_urls}", 
                mime_type, 
                f"{GREEN}[*] Internal: {href}{RESET}"
            )
            internal_urls.add(href)
        
        urls.add(href)
        
    return urls

def crawl(url, max_urls):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    global total_urls_visited
    total_urls_visited += 1
    print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    links = get_all_website_links(url, max_urls)
    for link in links:
        
        if (args.timeout > 0) and (time.time() - start_secs > args.timeout): # timeout
            print(f"{RED}[*] TIMEOUT: {args.timeout}s {RESET}")
            break
        
        if total_urls_visited > max_urls:
            print(f"{RED}[*] max_urls: {max_urls} {RESET}")
            break
        
        crawl(link, max_urls=max_urls)


#-----------------------------------------
# main
#-----------------------------------------
if __name__ == "__main__":

    # args defaults
    def_url = "https://1001suns.com/sitemap_post/" # for args
    # def_url = "https://1001suns.com/universe_bochum21/" # for args
    # def_url = "https://karlsruhe.digital/"
    
    import argparse
    parser = argparse.ArgumentParser(description="Link Extractor Tool with Python")
    parser.add_argument("--url",        default=def_url,    type=str,   help="The URL to extract links from.")
    parser.add_argument("--max-urls",   default=5000,       type=int,   help="Number of max URLs to crawl.")
    parser.add_argument("--crawl",      default=True,       type=bool,  help="crawl True or False")
    parser.add_argument("--timeout",    default=-1,         type=float, help="timeout. -1 means no timeout")
    
    #args = parser.parse_args()
    args, _unknown_args = parser.parse_known_args()
    for arg in vars(args):
        print(str(arg).rjust(15) + ':', getattr(args, arg))
            
    #-----------------------------------------
    # crawl
    #-----------------------------------------
    domain_name = urlparse(args.url).netloc
    file_internal_path = f"{data_folder}/{domain_name}_{date_time}_internal_links.csv"
    file_external_path = f"{data_folder}/{domain_name}_{date_time}_external_links.csv"
    print("domain_name       :", domain_name)
    print("file_internal_path:", file_internal_path)
    print("file_external_path:", file_external_path)
 
    if args.crawl:
        crawl(args.url, max_urls=args.max_urls)

        # print("[+] Total Internal links:", len(internal_urls))
        # print("[+] Total External links:", len(external_urls))
        # print("[+] Total URLs:", len(external_urls) + len(internal_urls))
        # print("[+] Total crawled URLs:", args.max_urls)

        # skip http
        print("before http replace:", len(internal_urls))
        internal_urls = [s.replace('http://', 'https://') for s in internal_urls]
        internal_urls = sorted(set(internal_urls))
        external_urls = sorted(set(external_urls))
        print("after http replace :", len(internal_urls))
        
        # save the internal links to a file
        print("save the internal links to a file...")
        with open(file_internal_path, "w", encoding="utf-8") as f:
            for internal_link in internal_urls:
                #check response
                status = get_status_code(internal_link)
                if status in [200, 301]:
                    #print(status, internal_link)
                    f.write(internal_link.strip() + "\n")
                else:
                    print(f"{RED}[*] status: {status} {internal_link} {RESET}")

        # save the external links to a file
        print("save the external links to a file...")
        with open(file_external_path, "w", encoding="utf-8") as f:
            for external_link in external_urls:
                f.write(external_link.strip() + "\n")

        print("[+] Total Internal links:", len(internal_urls))
        print("[+] Total External links:", len(external_urls))
        print("[+] Total URLs:", len(external_urls) + len(internal_urls))
        print("[+] Total crawled URLs:", args.max_urls)
                        
        print("all done:", "duration:", round(time.time() - start_secs, 1), "s")
    
    exit(0)
    #-----------------------------------------
    # pywebcopy
    #-----------------------------------------
    from pywebcopy import save_webpage

    with open(file_internal_path, "r") as f:
        internal_urls = f.readlines()
        
    for internal_link in internal_urls:
        print(f"{YELLOW}[*] save_webpage: {internal_link}{RESET}")
        # save_webpage(
        #     url=internal_link,
            
        #     project_folder="scraped_pywebcopy/",
        #     project_name=urlparse(args.url).netloc,
            
        #     debug=True,
        #     open_in_browser=True,
        #     delay=None,
        #     bypass_robots= True,
            
        #     threaded=False,
        # )  
    
    exit(0)  
    
    # https://stackoverflow.com/questions/31205497/how-to-download-a-full-webpage-with-a-python-script
    
    import urllib.request as urllib2
    from bs4 import *
    from urllib.parse  import urljoin


    def crawl(pages, depth=None):
        indexed_url = [] # a list for the main and sub-HTML websites in the main website
        for i in range(depth):
            for page in pages:
                if page not in indexed_url:
                    indexed_url.append(page)
                    try:
                        c = urllib2.urlopen(page)
                    except:
                        print( "Could not open %s" % page)
                        continue
                    soup = BeautifulSoup(c.read())
                    links = soup('a') #finding all the sub_links
                    for link in links:
                        if 'href' in dict(link.attrs):
                            url = urljoin(page, link['href'])
                            if url.find("'") != -1:
                                    continue
                            url = url.split('#')[0] 
                            if url[0:4] == 'http':
                                    indexed_url.append(url)
            pages = indexed_url
        return indexed_url


    pagelist=["https://en.wikipedia.org/wiki/Python_%28programming_language%29"]
    urls = crawl(pagelist, depth=1)
    print( urls )
    
    exit(0)    
    
    # wget -E -H -k -K -p -e robots=off https://karlsruhe.digital
    # wget -E --span-hosts -k -K -p -e robots=off https://karlsruhe.digital
    # wget --mirror -nH -np -p -k -E -e robots=off https://karlsruhe.digital
    # wget --mirror -nH -np -p -k -E -e robots=off -i "../data/karlsruhe.digital_internal_links.csv" 
    
    # https://stackoverflow.com/questions/31205497/how-to-download-a-full-webpage-with-a-python-script
    
