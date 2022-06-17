
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

#-----------------------------------------
# 
#-----------------------------------------
def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def is_remote(url):
    return url.strip().startswith('http')

def is_local(url):
    return not is_remote(url)

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

def url_path(url, char_lstrip=''): # '/'
    p = urlparse(url.strip()).path # '/3/library/urllib.parse.html'
    if char_lstrip:
        p = p.lstrip(char_lstrip)
    return p

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

#-----------------------------------------
# 
#-----------------------------------------
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
}

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

#-----------------------------------------
# 
#-----------------------------------------
# # http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html
def wait_for_page_load(driver, by, item_to_find, timeout=60): # driver, By.TAG_NAME, 'footer', 60
    try:
        print("wait_for_page_load:", driver.current_url, "by:", by, "item_to_find:", item_to_find, "timeout:", timeout)
        WebDriverWait(driver, timeout).until(visibility_of_element_located((by, item_to_find)))
    except TimeoutException:
        print(f"{RED}Timed out {timeout}s waiting for page to load: {driver.current_url}{RESET}")
# wait_for_page_load(driver, By.TAG_NAME, 'footer', 60)

# https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
def page_has_loaded(driver):
    print("page_has_loaded: {}".format(driver.current_url))
    page_state = driver.execute_script('return document.readyState;')
    return page_state == 'complete'
# while not page_has_loaded(driver):
#     time.sleep(0.1)
    
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