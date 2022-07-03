# https://www.thepythoncode.com/article/extract-all-website-links-python
# https://www.thepythoncode.com/code/extract-all-website-links-python
# pip3 install requests bs4 colorama
# thank you!

"""
    # wget -E -H -k -K -p -e robots=off https://karlsruhe.digital
    # wget -E --span-hosts -k -K -p -e robots=off https://karlsruhe.digital
    # wget --mirror -nH -np -p -k -E -e robots=off https://karlsruhe.digital
    # wget --mirror -nH -np -p -k -E -e robots=off -i "../data/karlsruhe.digital_internal_links.csv" 
    
    # https://stackoverflow.com/questions/31205497/how-to-download-a-full-webpage-with-a-python-script
    
https://www.elegantthemes.com/blog/editorial/the-wordpress-json-rest-api-wp-api-what-it-is-how-it-works-what-it-means-for-the-future-of-wordpress
https://developer.wordpress.org/rest-api/


https://karlsruhe.digital/wp-json/
https://karlsruhe.digital/wp-json/wp/v2
https://karlsruhe.digital/wp-json/wp/v2/routes
routes
_links self

TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
-> link "https://karlsruhe.digital/2022/06/events-termine-in-karlsruhe-kw-25-2022/"
-> guid rendered "https://karlsruhe.digital/?p=5522" ## media makes more sense
https://karlsruhe.digital/wp-json/wp/v2/posts
https://karlsruhe.digital/wp-json/wp/v2/pages
https://karlsruhe.digital/wp-json/wp/v2/media
https://karlsruhe.digital/wp-json/wp/v2/blocks
https://karlsruhe.digital/wp-json/wp/v2/categories


"""

import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
#import mimetypes
# pip install python-magic
# pip install python-magic-bin # win
import magic
import time

import datetime
import helpers_web as wh
import sitemap

import config
        
# init the colorama module
import colorama
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
RED = colorama.Fore.RED
MAGENTA = colorama.Fore.MAGENTA
CYAN = colorama.Fore.CYAN
#-----------------------------------------
# testing...
#-----------------------------------------
# # requests TFFTF vs urllib TFFTF
# print(wh.get_mime_type("http://karlsruhe.digital"))
# print(wh.get_mime_type("https://karlsruhe.digital"))
# print(wh.get_mime_type("https://karlsruhe.digital/"))
# print(wh.get_mime_type("https://karlsruhe.digital//"))
# print(wh.get_mime_type("https://karlsruhe.digital/wp-content/uploads/2022/06/2021.Sesemann_7422.Foto-im-Intranet.jpg"))
# #print(wh.get_mime_type("https://123ddd.cccXXXX"))
# exit(0)

# https://searchfacts.com/url-trailing-slash/
# Should You Have a Trailing Slash at the End of URLs
# The short answer is that the trailing slash does not matter for your root domain or subdomain. 
# Google sees the two as equivalent.
# But trailing slashes do matter for everything else because Google sees the two versions 
# (one with a trailing slash and one without) as being different URLs.
#-----------------------------------------
# 
#-----------------------------------------
# initialize the set of links (unique links)
internal_urls       = set()
external_urls       = set()

total_urls_visited  = 0


data_folder         = config.data_folder
mime_types_allowed  = ["text/html", "text/plain"]
excludes            = ["bunte-nacht-karlsruhe.digital"] # ["/category/", "/author/"]
start_secs          = time.time()
args                = None

date_time_crawler   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

#-----------------------------------------
# 
#-----------------------------------------
def get_all_website_links(url, max_urls, wait_secs=(0.001, 0.002)):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    
    # get content
    for tries in range(10):
        print(MAGENTA + f"[{tries}] tries: {url}", RESET)
        wh.sleep_random(wait_secs, verbose_string=url) # NEW
        response    = wh.get_response(url, timeout=config.timeout)
        url         = response.url
        content     = response.read().decode('utf-8')
        if content:
            break
        else:
            print(RED, "request failed...sleep and try again...", url, RESET)
            time.sleep(3)
            
    internal_urls.add(url)
    soup = BeautifulSoup(content, "html.parser")
    
    for a_tag in soup.findAll("a"):
        
        href = a_tag.attrs.get("href")
        
        #href = wh.replace_all(href, "http:// https://", "https://")
        href = wh.replace_all(href, "http:// ",  "")
        href = wh.replace_all(href, "https:// ", "")        
        
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        
        href        = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        #href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        # keep frag
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path # NEW
        if parsed_href.fragment:
            href += "#" + parsed_href.fragment
            print(YELLOW, "NEW keeping frag:", href, RESET)
        href = href.rstrip('/')
        
        if not wh.url_is_valid(href):
            # not a valid URL
            print(f"{RED}[!] bad url: {href}{RESET}")
            continue

        #-----------------------------------------
        # external link
        #-----------------------------------------       
        #if domain_name not in urlparse(href).netloc :  #  in href # issue: https://www.facebook.com/karlsruhe.digital
        if wh.url_is_external(href, domain_name):
            if href not in external_urls and wh.strip_trailing_slash(href) not in external_urls:
                print(
                    "\t\t",
                    f"{total_urls_visited}/{max_urls}", 
                    f"{GRAY}[!] External: {href}{RESET}"
                )
                external_urls.add(href)
            else:
                #print("\t\t", f"{YELLOW}skipping external_urls: {href}{RESET}")
                pass
            continue
                
        #-----------------------------------------
        # internal link
        #-----------------------------------------     
        if href in internal_urls or wh.strip_trailing_slash(href) in internal_urls:
            # already in the internal_urls
            #print("\t\t", f"{YELLOW}skipping internal_urls: {href}{RESET}")
            continue
          
        # hresponse redirected, mime etc
        for tries in range(3):
            hresponse = wh.get_response(href, timeout=config.timeout, method='HEAD') 
            if hresponse:
                break
            else:
                print(f"{YELLOW}[{tries}] trying again: {href}{RESET}")
                time.sleep(1)
            
        if not hresponse:
            print(f"{RED}[!] not hresponse: {href}{RESET}")
            continue

        # get redirected href NEW
        ####href, _ = wh.get_redirected_url(href, timeout=config.timeout)
        # # # # # # # # # if hresponse.url != href:
        # # # # # # # # #     internal_urls.add(hresponse.url)
            
        #href = hresponse.url
          
        # # # if href in internal_urls:
        # # #     # already in the set
        # # #     continue
        
        ###mime_type =  wh.get_mime_type(href)
        mime_type =  hresponse.headers.get_content_type()
        if not mime_type in mime_types_allowed:
            print("\t\t", f"{RED}[!] skipped mime_type: {mime_type}{RESET}")
            continue
        
        # internel url
        if not href in internal_urls and not wh.strip_trailing_slash(href) in internal_urls:
            print(
                "\t\t",
                f"{total_urls_visited}/{max_urls}", 
                mime_type, 
                f"{CYAN}[*] Internal: {href}{RESET}"
            )
            internal_urls.add(href)
            
            # add redirected as well
            if hresponse.url != href:
                internal_urls.add(hresponse.url)
                
        else:
            #print("\t\t", f"{YELLOW}finally skipping internal_urls: {href}{RESET}")
            pass
            
        urls.add(href) # only store internals
    ### for a_tag
        
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
    
    print("\n" + YELLOW + "-"*88 + RESET)
    print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    print(f"{YELLOW}[*] {round((time.time() - start_secs)/60.0, 1)}m {RESET}")
     
    links = get_all_website_links(url, max_urls)
    for link in links:
        
        # app timeout?
        if (args.app_timeout > 0) and (time.time() - start_secs > args.app_timeout):
            print(f"{RED}[*] app_timeout: {args.app_timeout}s {RESET}")
            break
        
        # max_urls?
        if total_urls_visited > max_urls:
            print(f"{RED}[*] max_urls: {max_urls} {RESET}")
            break
        
        crawl(link, max_urls=max_urls)

#-----------------------------------------
# main
#-----------------------------------------
if __name__ == "__main__":
    
    wh.logo_filename(__file__)

    # args defaults TODO use config
    # def_url = "https://1001suns.com/sitemap_post/" # for args
    # def_url = "https://1001suns.com/universe_bochum21/" # for args
    def_url = config.base # "https://karlsruhe.digital/"
    
    import argparse
    parser = argparse.ArgumentParser(description="Link Extractor Tool with Python")
    parser.add_argument("--url",        default=def_url,    type=str,   help="The URL to extract links from.")
    parser.add_argument("--max-urls",   default=5000,       type=int,   help="Number of max URLs to crawl.")
    parser.add_argument("--crawl",      default=True,       type=bool,  help="crawl True or False")
    parser.add_argument("--app_timeout",default=60*60*2,    type=float, help="app_timeout in secs. -1 means no timeout")
    
    #args = parser.parse_args()
    args, _unknown_args = parser.parse_known_args()
    for arg in vars(args):
        print(str(arg).rjust(15) + ':', getattr(args, arg))
            
    #-----------------------------------------
    # crawl
    #-----------------------------------------
    domain_name = urlparse(args.url).netloc
    file_internal_path = f"{data_folder}/{domain_name}_{date_time_crawler}_internal_links.csv"
    file_external_path = f"{data_folder}/{domain_name}_{date_time_crawler}_external_links.csv"
    
    print("\n"*4, wh.CYAN)
    print("domain_name       :", domain_name)
    print("\n"*4, wh.RESET)
    
    print("file_internal_path:", file_internal_path)
    print("file_external_path:", file_external_path)
 
    if not args.crawl:
        print(wh.RED, "args.crawl:", args.crawl, wh.RESET)
    else:
        crawl(args.url, max_urls=args.max_urls)

        # internal
        internal_urls = [s.replace('http://', 'https://') for s in internal_urls]
        internal_urls = wh.links_remove_similar(internal_urls) # end vs end/
        internal_urls = wh.links_make_unique(internal_urls)
        internal_urls = wh.links_remove_excludes(internal_urls, excludes)
        #internal_urls = wh.links_strip_trailing_slash(internal_urls)
        internal_urls = sorted(internal_urls)
        
        # external
        external_urls = wh.links_remove_similar(external_urls)
        external_urls = wh.links_make_unique(external_urls )
        external_urls = wh.links_strip_trailing_slash(external_urls)
        external_urls = sorted(external_urls)
        
        # save the internal links to a file
        print("save the internal links to a file:", file_internal_path)
        with open(file_internal_path, "w", encoding="utf-8") as f:
            for internal_link in internal_urls:
                f.write(internal_link.strip() + "\n")

        # save the external links to a file
        print("save the external links to a file:", file_external_path)
        with open(file_external_path, "w", encoding="utf-8") as f:
            for external_link in external_urls:
                f.write(external_link.strip() + "\n")

        print("[+] Total Internal links:", len(internal_urls))
        print("[+] Total External links:", len(external_urls))
        print("[+] Total URLs          :", len(external_urls) + len(internal_urls))
        print("[+] Total crawled URLs  :", total_urls_visited)
        print("[+] args.max_urls       :", args.max_urls)
                        
        # write sitemap
        sitemap_path = f"{data_folder}/{domain_name}_{date_time_crawler}_sitemap.xml"
        sitemap.sitemap_xml_from_list(internal_urls, sitemap_path)
        import shutil
        shutil.copyfile(sitemap_path, config.project_folder + "sitemap.xml")

        # all done
        secs = time.time() - start_secs
        print("all done:", "duration:", round(secs/60.0, 1), "m")
    
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
    

    
