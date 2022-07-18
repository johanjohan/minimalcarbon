# https://www.thepythoncode.com/article/extract-all-website-links-python
# https://www.thepythoncode.com/code/extract-all-website-links-python
# pip3 install requests bs4 colorama

"""
TODO
    get rid of /wp-json/ and sitemap/
    in __export, could strip unneeded quotes...


strip trailing / so we can compare
"""

from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import time
import datetime
import helpers_web as wh
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
# 
#-----------------------------------------
internal_urls       = set()
external_urls       = set()

total_urls_visited  = 0

mime_types_allowed  = ["text/html", "text/plain"]
excludes            = ["bunte-nacht-karlsruhe.digital"] # ["/category/", "/author/"]
start_secs          = time.time()
args                = None

date_time_crawler   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

#-----------------------------------------
# 
#-----------------------------------------
def rectify(url, base):
    url = wh.replace_all(url, "http:// ",  "") # specific?
    url = wh.replace_all(url, "https:// ", "")     
          
    url = wh.link_make_absolute(url, base)
    url = wh.strip_query_and_fragment(url) # not needed for collection of pages
    url = wh.strip_trailing_slash(url) # so we can compare both valid versions
    return url
        
def rectify_local(url, base):
    url = wh.strip_trailing_slash(url) # so we can compare both valid versions
    return url
        
#-----------------------------------------
# 
#-----------------------------------------
def get_all_website_links(url, max_urls, wait_secs=(0.001, 0.002)):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    
    global internal_urls, external_urls
    urls = set()
    
    url = rectify(url, config.base)
    
    if wh.url_is_external(url, config.base):
        print(RED, "get_all_website_links:", "is external:", url, RESET)
        external_urls.add(url)     
        return urls
    
    # get content
    for tries in range(10):
        print(MAGENTA + f"[{tries}] tries: {url}", RESET)
        wh.sleep_random(wait_secs, verbose_string=url) # NEW
        response    = wh.get_response(url, timeout=config.timeout)
        if response:
            url         = response.url
            url         = rectify(url, config.base)
            content     = response.read().decode('utf-8')
            if content:
                break
        else:
            print(RED, "request failed...sleep and try again...", url, RESET)
            time.sleep(1)
            
    if not content:
        print(RED, "get_all_website_links:", "not content:", url, RESET)
        return urls
     
    internal_urls.add(url)    
    soup = BeautifulSoup(content, "html.parser")
    
    for a_tag in soup.findAll("a"):
        
        href = a_tag.attrs.get("href")
        href = rectify(href, config.base)      
        
        if href == "" or href is None:
            print("\t\t", "href is None:", RED, href, RESET)
            continue
        
        if any(ex in href for ex in config.protocol_excludes):
            print("\t\t", "skipping protocol:", RED, href, RESET)
            continue
                
        if not wh.url_is_valid(href):
            print(f"{RED}[!] get_all_website_links: bad url: {href} {RESET}")
            continue

        #-----------------------------------------
        # external link
        #-----------------------------------------       
        if wh.url_is_external(href,  config.base):
            if href not in external_urls:
                print(
                    "\t\t",
                    f"{total_urls_visited}/{max_urls}", 
                    f"{GRAY}[!] External: {href}{RESET}"
                )
                external_urls.add(href)
            continue
                
        #-----------------------------------------
        # internal link
        #-----------------------------------------     
        if href in internal_urls: ### or wh.strip_trailing_slash(href) in internal_urls:
            #print("\t\t", f"{YELLOW}skipping href in internal_urls: {href} {RESET}")
            continue
          
        # get_response: redirected, mime etc
        for tries in range(3):
            hresponse = wh.get_response(href, timeout=config.timeout, method='HEAD') 
            if hresponse:
                break
            else:
                print(f"{YELLOW}[{tries}] trying again: {href}{RESET}")
                time.sleep(1)
            
        if not hresponse:
            print(f"{RED}[!] not hresponse: {href}{RESET}")
            wh.string_to_file(href + '\n', config.path_links_errors, mode="a")
            continue
        
        href = rectify(hresponse.url, config.base) # may be redirected
         
        mime_type =  hresponse.headers.get_content_type()
        if not mime_type in mime_types_allowed:
            print("\t\t", f"{RED}[!] skipped mime_type: {mime_type}{RESET}")
            continue
        
        # internal url
        print(
            "\t\t",
            f"{total_urls_visited}/{max_urls}", 
            mime_type, 
            f"{GREEN}[*] Internal: {hresponse.url}{RESET}"
        )
        assert wh.url_is_internal(href, config.base), href
        internal_urls.add(href)
        urls.add(href) # only store internals
        
    ### for a_tag
        
    return urls
#-----------------------------------------
# crawl
#-----------------------------------------
def crawl(url, max_urls):
    """
    https://faun.pub/extract-all-website-links-in-python-48f07619db95
    https://github.com/KoderKumar/Link-Extractor
    
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    
    global internal_urls, external_urls
    global total_urls_visited
    total_urls_visited += 1
    
    url = rectify(url, config.base)
    
    print()
    print("\n" + CYAN + "-"*88 + RESET)
    print(f"{CYAN}[*] Crawling: {url}{RESET}")
    print(f"{CYAN}[*] {round((time.time() - start_secs)/60.0, 1)}m {RESET}")
     
    links = get_all_website_links(url, max_urls)
    
    wh.list_to_file(internal_urls, config.path_sitemap_links_internal, mode="w") # save for safety
    
    for link in links:
        
        # app timeout?
        if (args.app_timeout > 0) and (time.time() - start_secs > args.app_timeout):
            print(f"{RED}[*] app_timeout: {args.app_timeout}s {RESET}")
            break
        
        # max_urls?
        if total_urls_visited > max_urls:
            print(f"{RED}[*] max_urls: {max_urls} {RESET}")
            break
        
        ### if not link in internal_urls:
        crawl(link, max_urls=max_urls)

#-----------------------------------------
# main
#-----------------------------------------
if __name__ == "__main__":
    
    wh.logo_filename(__file__)
    wh.log("__file__", __file__, filepath=config.path_log_params)
        
    def_url = config.base 
    import argparse
    parser = argparse.ArgumentParser(description="Link Extractor Tool with Python")
    parser.add_argument("--url",        default=def_url,    type=str,   help="The URL to extract links from.")
    parser.add_argument("--max-urls",   default=5000,       type=int,   help="Number of max URLs to crawl.")
    parser.add_argument("--crawl",      default=True,       type=bool,  help="crawl True or False")
    parser.add_argument("--app_timeout",default=60*60*2,    type=float, help="app_timeout in secs. -1 means no timeout")
    
    args, _unknown_args = parser.parse_known_args()
    for arg in vars(args):
        wh.log(str(arg).rjust(15) + ':', getattr(args, arg), filepath=config.path_log_params)
    wh.log("args:", args, filepath=config.path_log_params)
            
    #-----------------------------------------
    # crawl
    #-----------------------------------------
    
    ############domain_name = urlparse(args.url).netloc
    #####print("\n"*4, wh.CYAN)
    ######print("domain_name                       :", domain_name)
    print("\n"*4, wh.RESET)
    # print("config.path_sitemap_links_internal:", config.path_sitemap_links_internal)
    # print("config.path_sitemap_links_external:", config.path_sitemap_links_external)
    wh.file_make_unique(config.path_sitemap_links_internal, sort=True)
    wh.file_make_unique(config.path_sitemap_links_external, sort=True)
 
    if not args.crawl:
        print(wh.RED, "args.crawl:", args.crawl, wh.RESET)
    else:
        crawl(args.url, max_urls=args.max_urls)

        # internal
        internal_urls = [s.replace('http://', 'https://') for s in internal_urls]
        # internal_urls = wh.links_remove_similar(internal_urls) # end vs end/
        # internal_urls = wh.links_make_unique(internal_urls)
        internal_urls = wh.links_remove_excludes(internal_urls, excludes)
        internal_urls = wh.strip_query_and_fragment(internal_urls) # NEW
        #internal_urls = wh.links_strip_trailing_slash(internal_urls)
        internal_urls = wh.links_sanitize(internal_urls)
        internal_urls = sorted(internal_urls)
        
        # external
        external_urls = wh.links_remove_similar(external_urls)
        external_urls = wh.links_make_unique(external_urls )
        external_urls = wh.links_strip_trailing_slash(external_urls)
        external_urls = wh.links_sanitize(external_urls)
        external_urls = sorted(external_urls)
        
        # save the internal links to a file
        print("save the internal links to a file:", config.path_sitemap_links_internal)
        # # with open(config.path_sitemap_links_internal, "w", encoding="utf-8") as f:
        # #     for internal_link in internal_urls:
        # #         f.write(internal_link.strip() + "\n")
        wh.list_to_file(internal_urls, config.path_sitemap_links_internal, mode="a")
        wh.file_make_unique(config.path_sitemap_links_internal, sort=True)

        # save the external links to a file
        print("save the external links to a file:", config.path_sitemap_links_external)
        # with open(config.path_sitemap_links_external, "w", encoding="utf-8") as f:
        #     for external_link in external_urls:
        #         f.write(external_link.strip() + "\n")
        wh.list_to_file(external_urls, config.path_sitemap_links_external, mode="a")
        wh.file_make_unique(config.path_sitemap_links_external, sort=True)

        wh.log("[+] Total Internal links:", len(internal_urls), filepath=config.path_log_params)
        wh.log("[+] Total External links:", len(external_urls), filepath=config.path_log_params)
        wh.log("[+] Total URLs          :", len(external_urls) + len(internal_urls), filepath=config.path_log_params)
        wh.log("[+] Total crawled URLs  :", total_urls_visited, filepath=config.path_log_params)
        wh.log("[+] args.max_urls       :", args.max_urls, filepath=config.path_log_params)
                                
        # # # write sitemap ---> at very end!
        # # sitemap_path = config.path_sitemap_xml
        # # sitemap.sitemap_xml_from_list(internal_urls, sitemap_path)
        # # import shutil
        # # dst = config.project_folder + "sitemap.xml"
        # # wh.make_dirs(dst)
        # # shutil.copyfile(sitemap_path, dst)

        # all done
        secs = time.time() - start_secs
        wh.log("all done:", "duration:", round(secs/60.0, 1), "m", filepath=config.path_log_params)
        wh.log("\n"*4, filepath=config.path_log_params) 
    
    #-----------------------------------------
    # END
    #-----------------------------------------
    
