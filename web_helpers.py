from urllib import response
from urllib.parse import urlparse, urljoin
import os
import urllib.request
import ssl
import requests
import time

#-----------------------------------------
# 
#-----------------------------------------
# init the colorama module
import colorama
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
RED = colorama.Fore.RED
CYAN = colorama.Fore.CYAN
MAGENTA = colorama.Fore.MAGENTA

#-----------------------------------------
# dq
#-----------------------------------------
_wrap = lambda s, delim : delim if not s else delim + str(s) + delim
def dq(s=""):
    return _wrap(s, delim="\"")
def sq(s=""):
    return _wrap(s, delim="\'")

#-----------------------------------------
# 
#-----------------------------------------
def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

# # def is_remote(url):
# #     return url.strip().startswith('http')

# # def is_local(url):
# #     return not is_remote(url)

def is_absolute(url):
    return url.strip().startswith('http')

def is_relative(url):
    return not is_absolute(url)

def is_relative_to_base(url, base):
    return not is_absolute(url)

# https://stackoverflow.com/questions/10772503/check-url-is-a-file-or-directory


"""
urlparse("scheme://netloc/path;parameters?query#fragment")
ParseResult(scheme='scheme', netloc='netloc', path='/path;parameters', params='',
            query='query', fragment='fragment')
urlparse("http://docs.python.org:80/3/library/urllib.parse.html?highlight=params#url-parsing")
ParseResult(
    scheme  = 'http', 
    netloc  = 'docs.python.org:80',
    path    = '/3/library/urllib.parse.html', 
    params  = '',
    query   = 'highlight=params', 
    fragment= 'url-parsing'
)
"""    
def has_same_netloc(url, base):
    url_loc  = urlparse(url.strip() ).netloc
    base_loc = urlparse(base.strip()).netloc
    return url_loc == base_loc
    return url.strip().startswith(base.strip())

#https://stackoverflow.com/questions/6690739/high-performance-fuzzy-string-comparison-in-python-use-levenshtein-or-difflib
from difflib import SequenceMatcher
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio() #+ 0..1

# may just be a missing / for a folder
# https://stackoverflow.com/questions/16603282/how-to-compare-each-item-in-a-list-with-the-rest-only-once
def links_remove_similar(links):
    
    links = links_make_unique(links)
    
    # those have just a forgotten trailing slash
    def is_similar(a,b):
        
        a = a.strip()
        b = b.strip()

        ret = None
        if len(a)+1 == len(b):
            if a + '/' == b:
                ret = a
        elif len(b)+1 == len(a):
            if b + '/' == a:
                ret = b
            
        if ret:
            print("\t", RED, "is_similar:", ret, "a,b:", a, b, RESET)
        
        return ret
        
    excludes = []
    import itertools
    for a, b in itertools.combinations(links, 2):
        res = is_similar(a, b)
        if res:
            excludes.append(res) # the smaller one to be deleted
 
    excludes = links_make_unique(excludes)
    if excludes:
        print("links_remove_similar:", YELLOW, "excludes:", *excludes, RESET, sep="\n\t")    
         
    new_links = [link for link in links if link not in excludes]  
    #print("\t", GREEN, "new_links:", *new_links, RESET, sep="\n\t")   
    
    return new_links
            
    
    
# def links_remove_similar(links, base, thresh=0.8):
#     pass

def link_make_absolute(link, base):
    if is_relative(link):
        link = add_trailing_slash(base) + strip_leading_slash(link)
    return link

def links_make_absolute(links, base):
    ret = []
    for link in links:
        ret.append(link_make_absolute(link, base))
    return ret
        
def links_remove_invalids(links, base, invalids):
    #print(YELLOW, *links, RESET, sep="\n\t")
    ret = []
    
    for link in links:
        
        b_is_valid = True
        
        for invalid in invalids:
            if invalid in link:
                b_is_valid = False
                print("\t", RED, "invalid:", link, RESET, sep="\n\t")
                break
            
        if b_is_valid:
            ret.append(link)
            
    #print(GREEN, *ret, RESET, sep="\n\t")
    return ret
        
def links_remove_externals(links, base):
    return [u for u in links if (has_same_netloc(u, base) or is_relative(u))]

def links_remove_folders(links):
    return [u for u in links if not u.strip().endswith('/')]

def links_strip_query_and_fragment(links):
    return [strip_query_and_fragment(u) for u in links]

def links_make_relative(links, base):
    return [try_make_local(u, base) for u in links]

def links_make_unique(links):
    return list(set(links))

# def links_make_absolute_internals_only(links, base):
#     links = links_make_absolute(links, base)
#     links = links_remove_externals(links, base)
#     links = links_make_unique(links)
#     ####links = links_strip_query_and_fragment(links)
#     links = sorted(links)
#     return links

def url_path(url, char_lstrip=''): # '/'
    p = urlparse(url.strip()).path # '/3/library/urllib.parse.html'
    if char_lstrip:
        p = p.lstrip(char_lstrip)
    return p

def url_scheme(url): # '/'
    return urlparse(url.strip()).scheme

def url_path_lstrip_slash(url): # '/'
    return url_path(url, char_lstrip='/')

def try_make_local(url, base):
    if has_same_netloc(url, base):
        #ret = url.replace(base, "").lstrip('/')
        ret = url_path_lstrip_slash(url)
        #print("try_make_local:", url, "->", ret)
        return ret
    else:
        return url

#-----------------------------------------
# 
#-----------------------------------------

def has_trailing(url, s):
    return url.endswith(s)

def has_leading(url, s):
    return url.startswith(s)

def has_trailing_slash(url):
    return has_trailing(url.strip(), '/')

def has_no_trailing_slash(url):
    return not has_trailing_slash(url)

def has_leading_slash(url):
    return has_leading(url.strip(), '/')

def strip_leading_slash(url):
    return url.strip().lstrip('/')

def strip_trailing_slash(url):
    return url.strip().rstrip('/')

def strip_tail(url, delim):
    if delim in url:
        url = url.split(delim)[0]
        #print("--> strip_tail:", url)
    return url

def strip_query_and_fragment(url):
    return strip_tail(url, '?')

def add_trailing(url, to_add):
    return url.rstrip(to_add) + to_add

def add_trailing_slash(url):
    return add_trailing(url, '/')

#-----------------------------------------
# 
#-----------------------------------------
def make_dirs(the_path):
    dirs = os.path.dirname(the_path)
    if not os.path.exists(dirs):
        print("make_dirs:", dirs)
        os.makedirs(dirs)

def was_redirected(url):
    response = requests.head(url, allow_redirects=True)
    if response.history:
        print("Request was redirected:", url)
        for resp in response.history:
            print("\t", resp.status_code, resp.url)
        print("Final destination:", response.status_code, response.url)
        return True
    else:
        print("Request was not redirected")
        return False
    
    
# # assume that there is no files without extension on the Internet and all paths are unix...!!!!!
# # Unlike some operating systems, UNIX doesn’t require a dot (.) in a filename; 
# # in fact, you can use as many as you want. 
# # For instance, the filenames pizza and this.is.a.mess are both legal.
# def is_directory(url):   
#     print("is_directory:", url)
#     url     = url.replace("\\\\", "/")
#     url     = url.replace("\\",   "/")
#     url     = strip_trailing_slash(url)
#     subs    = url.split('/')
#     print("is_directory:", "subs:", subs)
#     last = subs[-1]
#     return not '.' in subs[-1]
    
# def is_file(url):   
#     return not is_directory(url)

def check_online_site_exists(url):
    from http import HTTPStatus
    try:
        response  = requests.head(url)
        ret       = True
    except:
        ret       = False
    print("check_site_exist:", url, "-->", ret)
    return ret

def is_online_file_and_exists(url):
    t = get_mime_type(url) # None on a folder or if not exists
    return t
  
### I suppose you can add a slash to a URL and see what happens from there. That might get you the results you are looking for.
def is_online_directory_or_not_exists(url):
    ret = not is_online_file_and_exists(url)
    print("is_online_directory_or_not_exists:", url, "-->", ret)
    print("check_online_site_exists:", check_online_site_exists(url))
    print()
    return ret
    
#-----------------------------------------
# 
#-----------------------------------------
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
}

# # def get_content_type(url):
# #     # seems to be incorrect many times
# #     try:
# #         r = requests.head(url, allow_redirects=True)
# #         ### {'Date': 'Thu, 16 Jun 2022 16:03:31 GMT', 'Server': 'Apache/2.4.54 (Unix)', 'X-Powered-By': 'PHP/7.4.30', 'Allow': 'GET, POST, PUT', 'Cache-Control': 'no-store, no-cache, must-revalidate', 'Expires': 'Sat, 26 Jul 1997 05:00:00 GMT', 'Pragma': 'no-cache', 'Vary': 'User-Agent,Accept-Encoding', 'Content-Encoding': 'gzip', 'Content-Type': 'text/html; charset=UTF-8', 'Set-Cookie': 'PHPSESSID=8bss92l8og8s789ldp0p3u5uvr; path=/', 'Keep-Alive': 'timeout=3, max=100', 'Connection': 'Keep-Alive'}
# #         return r.headers["content-type"] # "text/html; charset=UTF-8"
# #     except Exception as e:
# #         print(f"{RED}[!] {url} Exception: {e}{RESET}")
# #         return None
    
# # def get_content_part(url, index):
# #     ct = get_content_type(url)
# #     if ct:
# #         subs = ct.split(';') # "text/html; charset=UTF-8"
# #         if len(subs) >= (index+1):
# #             return subs[index]

# #     return None

# # def get_encoding(url):
# #     return get_content_part(url, 1)
    
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

#-----------------------------------------
# 
#-----------------------------------------
def html_remove_comments(content):
    import re
    content = re.sub("<!--.*?-->", "", content)
    return  content

#-----------------------------------------
# 
#-----------------------------------------

def wait_for(condition_function, timeout):
    start_time = time.time()
    while time.time() < (start_time + timeout):
        if condition_function():
            return True
        else:
            time.sleep(0.1)
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )
#-----------------------------------------
# selenium
#-----------------------------------------
from selenium import webdriver # pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.common.exceptions import TimeoutException

# https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
def _scroll_down(driver, value):
    driver.execute_script("window.scrollBy(0,"+str(value)+")")

# Scroll down the page
def scroll_down_all_the_way(driver, sleep_secs=1, npixels=500):
    old_page = driver.page_source
    while True:
        print("scroll_down_all_the_way:", sleep_secs, driver.current_url)
        for i in range(2):
            _scroll_down(driver, npixels)
            time.sleep(sleep_secs)
        new_page = driver.page_source
        if new_page != old_page:
            old_page = new_page
        else:
            break
    return True

def wait_for_page_has_loaded_scrolling(driver, sleep_secs=1, npixels=500):
    return scroll_down_all_the_way(driver, sleep_secs=1, npixels=500)
    
#-----------------------------------------
# 
#-----------------------------------------
# # http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html
def wait_for_page_has_loaded_by_item(driver, by, item_to_find, timeout=60): # driver, By.TAG_NAME, 'footer', 60
    try:
        print("wait_for_page_load:", driver.current_url, "by:", by, "item_to_find:", item_to_find, "timeout:", timeout)
        WebDriverWait(driver, timeout).until(visibility_of_element_located((by, item_to_find)))
        return True
    except TimeoutException:
        print(f"{RED}Timed out {timeout}s waiting for page to load: {driver.current_url}{RESET}")
        return False
# wait_for_page_load(driver, By.TAG_NAME, 'footer', 60)

#-----------------------------------------
# 
#-----------------------------------------

def wait_for_page_has_loaded_readyState(driver, sleep_secs=0.1):
    
    # https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
    def _page_has_loaded_readyState(driver):
        print("page_has_loaded: {}".format(driver.current_url))
        page_state = driver.execute_script('return document.readyState;')
        return page_state == 'complete'

    while not _page_has_loaded_readyState(driver):
        time.sleep(sleep_secs)
        
    return True
    
# https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
def wait_for_page_has_loaded_hash(driver, sleep_secs=2):
    '''
    Waits for page to completely load by comparing current page hash values.
    '''

    def get_page_hash(driver):
        '''
        Returns html dom hash
        '''
        # can find element by either 'html' tag or by the html 'root' id
        dom = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
        # dom = driver.find_element_by_id('root').get_attribute('innerHTML')
        dom_hash = hash(dom.encode('utf-8'))
        return dom_hash

    page_hash = 'empty'
    page_hash_new = ''
    
    # comparing old and new page DOM hash together to verify the page is fully loaded
    while page_hash != page_hash_new: 
        page_hash = get_page_hash(driver)
        time.sleep(sleep_secs)
        page_hash_new = get_page_hash(driver)
        print('<page_has_loaded> - page not loaded')

    print('<page_has_loaded> - page loaded: {}'.format(driver.current_url))
    return True
    
#-----------------------------------------
# surrogate
#-----------------------------------------
def wait_for_page_has_loaded(driver):
    return wait_for_page_has_loaded_readyState(driver, sleep_secs=0.1)
#-----------------------------------------
# 
#-----------------------------------------
    
def replace_all(content, oldvalue, newvalue):
    while oldvalue in content:
        content = content.replace(oldvalue, newvalue)
    return content

#-----------------------------------------
# background_images
#-----------------------------------------
def get_style_background_images(driver):

    def _parse_style_attribute(style_string):
        if 'background-image' in style_string:
            
            try:
                url_string = style_string.split(' url("')[1].replace('");', '')
            except:
                # may be a gradient
                print(f"{RED}ERR missing background-image: style_string: {style_string} {RESET}")
                url_string = None
            
            #print(f"{GRAY}\t background-image: {url_string} {RESET}")
            return url_string
        return None

    links = []
    for div in driver.find_elements(By.XPATH, "//*[@style]"): #  '//div[@style]'
        #print(f"{YELLOW}\t div: {div} {RESET}")
        style = div.get_attribute('style')
        #print(f"{GRAY}\t style: {style} {RESET}")
        link = _parse_style_attribute(style)
        if not link in links:
            #print(f"{GREEN}\t background-image: {link} {RESET}")
            links.append(link)
    links = [link for link in links if link is not None]
   
    return links

#-----------------------------------------
# https://pypi.org/project/cssutils/
# https://pythonhosted.org/cssutils/docs/scripts.html
# https://github.com/jaraco/cssutils
# https://pythonhosted.org/cssutils/docs/parse.html#parsefile
# https://pythonhosted.org/cssutils/docs/css.html
#-----------------------------------------
def get_stylesheet_background_images(style_path):
    import cssutils
    urls  = []
    if os.path.isfile(style_path):
        try:
            sheet = cssutils.parseFile(style_path)
        except:
            pass
        #print (sheet.cssText)
        for rule in sheet:
            if rule.type == rule.STYLE_RULE:
                for property in rule.style:
                    if property.name == 'background-image':
                        if "url" in property.value:
                            url = property.value.replace("(", "").replace(")", "")
                            url = url.strip().lstrip("url")
                            print("\t\t\t", CYAN, url, RESET)
                            urls.append(url)
    else:
        # TODO
        print(f"{YELLOW}\t style_path not yet downloaded TODO: {style_path} {RESET}")
                    
    return urls

#-----------------------------------------
# 
#-----------------------------------------   
def save_html(content, path, pretty=False):
    
    if pretty:
        from bs4 import BeautifulSoup, Comment
        soup = BeautifulSoup(content, 'html.parser')    
        content = soup.prettify()
        
    make_dirs(path)
    try:
        with open(path, 'w', encoding="utf-8") as fp:
            fp.write(content)
        print("save_html:", path)
    except Exception as e:
        print(f"{RED}save_html: may be a folder: {path} --> {e} {RESET}")
        exit(1) # TODO!!!!!!!!!!!!!!!!!!!!
        
    return path

def load_html(driver, path):
    driver.get(path)
    return path
        
    import tempfile
    with tempfile.NamedTemporaryFile(dir=dir, delete=False, suffix='.html') as tmp:
        tmp.close() # already open
        print("tmp.name:", tmp.name)
        save_html(content, tmp.name)
        driver.get(tmp.name)
        #wait_for_page_has_loaded(driver)
        return tmp.name
        

def load_html_from_string(driver, content, dir='.'):
    import tempfile
    with tempfile.NamedTemporaryFile(dir=dir, delete=False, suffix='.html') as tmp:
        tmp.close() # already opened --> permission err
        save_html(content, tmp.name)        
        return load_html(driver, tmp.name)
        
#-----------------------------------------
# 
#-----------------------------------------
def html_minify(content):
    
    length_orig = len(content)
    print("html_minify: length_orig:", length_orig)
    if length_orig > 0:
        if True:
            content = replace_all(content, "\n", " ")
            content = replace_all(content, "\t", " ")
            content = replace_all(content, "\r", " ")
            #print("len(content)", len(content))
            content = replace_all(content, "  ", " ")
            #print("len(content)", len(content))

        # pip install htmlmin
        import htmlmin
        try:
            content = htmlmin.minify(
                content, 
                remove_comments=True, 
                remove_empty_space=True,
                remove_all_empty_space=True,
                reduce_boolean_attributes=True,
                reduce_empty_attributes=True,
                remove_optional_attribute_quotes=True,
                convert_charrefs=True,
                )
        except:
            print(f"{RED}could not htmlmin.minify!{RESET}")
            
        percent = round(len(content) / length_orig * 100, 1)
        percent_saved = round(100 - percent, 1)
        print("html_minify: final len(content)", len(content), "|", GREEN, "percent_saved:", percent_saved, "%", RESET)
    
    return content
#-----------------------------------------
# 
#-----------------------------------------
def replace_in_file(filename, string_from, string_to):
    
    fp = open(filename, "rt")
    data = fp.read()
    data = data.replace(string_from, string_to)
    fp.close()
    
    #open the input file in write mode
    fp = open(filename, "wt")
    fp.write(data)
    fp.close()
      
#-----------------------------------------
# 
#-----------------------------------------

#-----------------------------------------
# 
#-----------------------------------------

#-----------------------------------------
# 
#-----------------------------------------
if __name__ == "__main__":
    print("\n"*3 + "you started the wrong file..." + "\n"*3)