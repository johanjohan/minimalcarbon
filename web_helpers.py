
from urllib.parse import urlparse, urljoin
import os
import urllib.request
import ssl
import requests

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
        print("--> strip_tail:", url)
    return url

def strip_query_and_fragment(url):
    return strip_tail(url, '?')
#-----------------------------------------
# 
#-----------------------------------------

def make_dirs(local_path):
    dirs = os.path.dirname(local_path)
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

#-----------------------------------------
# 
#-----------------------------------------

