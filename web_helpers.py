
from urllib.parse import urlparse, urljoin
import os

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

