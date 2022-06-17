# https://stackoverflow.com/questions/53729201/save-complete-web-page-incl-css-images-using-python-selenium

from selenium import webdriver # pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
import chromedriver_binary # pip install chromedriver-binary-auto
from lxml import html
import requests
import os
from urllib.parse import urlparse, urljoin

driver = webdriver.Chrome()
base = 'https://karlsruhe.digital/'
URL  = base
FOLDER = "page/_kd/"

# init the colorama module
import colorama
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
RED = colorama.Fore.RED
CYAN = colorama.Fore.CYAN


def is_remote(url):
    return url.strip().startswith('http')

def is_local(url):
    return not is_remote(url)


"""
urlparse("scheme://netloc/path;parameters?query#fragment")
ParseResult(scheme='scheme', netloc='netloc', path='/path;parameters', params='',
            query='query', fragment='fragment')
urlparse("http://docs.python.org:80/3/library/urllib.parse.html?highlight=params#url-parsing")
ParseResult(scheme='http', netloc='docs.python.org:80',
            path='/3/library/urllib.parse.html', params='',
            query='highlight=params', fragment='url-parsing')
"""    
def has_same_netloc(url, base):
    url_loc  = urlparse(url.strip() ).netloc
    base_loc = urlparse(base.strip()).netloc
    return url_loc == base_loc
    
    return url.strip().startswith(base.strip())

def url_path(url):
    return urlparse(url.strip()).path

def try_make_local(url, base):
    if has_same_netloc(url, base):
        ret = url.replace(base, "").lstrip('/')
        print("try_make_local:", url, "->", ret)
        return ret
    else:
        return url


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
        print("--> strip_tail:", url)
    return url

def strip_query_and_fragment(url):
    return strip_tail(url, '?')

def make_dirs(local_path):
    dirs = os.path.dirname(local_path)
    if not os.path.exists(dirs):
        print("make_dirs:", dirs)
        os.makedirs(dirs)



print(f"{CYAN}\t URL: {URL}{RESET}")

driver.get(URL)
# seq_query_field = driver.find_element(By.ID, "seq") # find_element_by_id("seq")
# seq_query_field.send_keys(SEQUENCE)
# blast_button = driver.find_element(By.ID, "blastButton1")
# blast_button.click()

# wait until results are loaded
WebDriverWait(driver, 60).until(visibility_of_element_located((By.CLASS_NAME, 'owl-next')))


content = driver.page_source
# write the page content
if not os.path.isdir(FOLDER):
    os.makedirs(FOLDER)
    
with open(FOLDER + 'page.html', 'w', encoding="utf-8") as fp:
    fp.write(content)

# download the referenced files to the same path as in the html
sess = requests.Session()
sess.get(base)            # sets cookies
        
# parse html
h = html.fromstring(content)
# get css/js files loaded in the head
for hr in h.xpath('head//@href'):
        
    print(f"{YELLOW}\t hr: {hr}{RESET}")
        
    if is_local(hr):
        local_path = FOLDER + hr
        local_path = strip_query_and_fragment(local_path)
        hr = base + hr
    else:
        local_path = FOLDER + url_path(hr).lstrip('/')
        
    print("hr        :", hr)
    print("local_path:", local_path)
    
    res = sess.get(hr)    
    if res.status_code == 200:
        if has_no_trailing_slash(local_path): # is a file
            
            make_dirs(local_path)         
            with open(local_path, 'wb') as fp:
                fp.write(res.content)
            print("saved:", local_path)
            
            content = content.replace(hr, url_path(hr).lstrip('/'))
        else:
            print(f"{RED}\t not a file: {local_path}{RESET}")
    else:
        print(f"{RED}\t bad status: {res.status_code}{RESET}")
        

# get image/js files from the body.  skip anything loaded from outside sources
for src in h.xpath('//@src'):
    
    if has_same_netloc(src, base):
        src = try_make_local(src, base)
    
    print(f"{GREEN}\t src: {src}{RESET}")
    
    if not src or src.startswith('http'): # skip anything loaded from outside sources
        print(f"{RED}\t skipping external: {src}{RESET}")
        continue
    
    local_path = FOLDER + src
    print(local_path)
    local_path = strip_query_and_fragment(local_path)
            
    src = base + src
    res = sess.get(src)
    
    make_dirs(local_path)       
    with open(local_path, 'wb') as fp:
        fp.write(res.content)  
        
    content = content.replace(src, url_path(src).lstrip('/'))
    
with open(FOLDER + 'page_local.html', 'w', encoding="utf-8") as fp:
    fp.write(content)