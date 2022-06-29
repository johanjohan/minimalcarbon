""" 
URL ASSUMPTIONS

If you don't know is website use https or http protocol, it's better to use '//'.
An optional authority component preceded by two slashes (//),

ASSUMPTIONS
a folder has no dot
a file has a dot for the extension, or a leading dot

https://docs.python.org/3/library/urllib.parse.html


WP API
https://github.com/MickaelWalter/wp-json-scraper

"""


from posixpath import join
from urllib import response
from urllib.parse import urlparse, urljoin, parse_qs
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
def vt_b(b_val):
    return (GREEN if b_val else RED) + str(b_val)[0] + RESET
    #return (GREEN if b_val else RED) + str(int(b_val)) + RESET
def vt_code(code):
    return (GREEN if code < 400 else RED) + str(code) + RESET
    #return (GREEN if b_val else RED) + str(int(b_val)) + RESET
#-----------------------------------------
# 
#-----------------------------------------

def url_exists(url):
    code = get_status_code(url)
    exists = True if code and code < 400 else False
    print("url_exists:", exists, "|", code, "|", url)
    return exists

# https://stackoverflow.com/questions/5074803/retrieving-parameters-from-a-url
def url_has_ver(url):
    try:
        value = parse_qs(urlparse(url).query)['ver'][0]
        ret = True
    except:
        #print(f"{RED}[!] url_has_ver: {url} {RESET}")
        ret = False
    #print("url_has_ver:", GREEN if ret else RED, ret, RESET, url)
    return ret

def url_get_ver(url):
    # ver= # ?ver=
    try:
        value = parse_qs(urlparse(url).query)['ver'][0]
        print("url_get_ver:", value)
        return value
    except:
        print(f"{RED}[!] url_get_ver: {url} {RESET}")
        return ""

#-----------------------------------------
# 
#-----------------------------------------

def url_is_valid(url): # need by crawler
    """
    Checks whether `url` is a valid URL.
    needs minimum //netloc to start with
    """
    parsed = urlparse(url)
    ret = bool(parsed.netloc) and (parsed.scheme.startswith('http') or url.strip().startswith('//'))
    #print("url_is_valid:", ret, url )
    return ret

# # def is_remote(url):
# #     return url.strip().startswith('http')

# # def is_local(url):
# #     return not is_remote(url)

def url_split(url):
    
    vb = False
    
    if vb: print("url_split:", CYAN, dq(url), RESET, GRAY)
    
    url         = url.strip()
    exts        = ["html", "htm", "php", "php3", "js", "shtm", "shtml", "asp", "cfm", "cfml"]
    root        = '/'
    
    protocol    = None
    loc         = None
    path        = None
    
    if not url:
        path = root
    else:
        # protocol
        if '://' in url:
            subs        = url.split('://')
            protocol    = subs[0]
            url         = subs[1]
        elif url.startswith('//'):
            #protocol = 'https'
            url = url.lstrip('//')
            
        url = url.lstrip('/')
            
        # loc
        subs = url.split('/')
        if subs:
            if '.' in subs[0]:
                parts = subs[0].split('.')
                if parts:
                    ext   = parts[-1].lower()
                    if not ext in exts:
                        loc = subs[0]
                        path = root + '/'.join(subs[1:]) 
                    else:
                        path = root + '/'.join(subs) 
                else:
                    pass
                    print(RED, "WARN no parts .:", subs[0], RESET)
                    _sleep()
            else:
                path = root + url   
        else:
            pass
            print(RED, "WARN no subs /:", url, RESET)
            _sleep()
            
    if vb: 
        print("\t", "protocol:", protocol)
        print("\t", "loc     :", loc)
        print("\t", "path    :", path)
        print(RESET, end='')
    
    return protocol, loc, path

""" 
url_is_absolute: False | ''
url_is_absolute: False | index.html
url_is_absolute: False | path/image.jpg
url_is_absolute: False | /path/image.jpg
url_is_absolute: True | karlsruhe.digital
url_is_absolute: True | karlsruhe.digital/path/image.jpg
url_is_absolute: True | www.karlsruhe.digital/path/image.jpg
url_is_absolute: True | //www.karlsruhe.digital/path/image.jpg
url_is_absolute: True | http://www.karlsruhe.digital/path/image.jpg
url_is_absolute: True | https://www.karlsruhe.digital/path/image.jpg
url_is_absolute: False | xxxxx://www.karlsruhe.digital/path/image.jpg
url_is_absolute: True | facebook.de/test.html
url_is_absolute: True | http://facebook.de/test.html
url_is_absolute: True | http://facebook.de
url_is_absolute: True | facebook.de
url_is_absolute: False | facebook
"""
def url_is_absolute(url): # absolute URL (that is, it starts with // or scheme://)
    # url = url.strip()
    # exts = ["html", "htm", "php", "php3", "js", "shtm", "shtml", "asp", "cfm", "cfml"]
    
    # ret = False
    # if url.startswith('http') or url.startswith('//'):
    #     ret = True
    # else:
    #     subs = url.split('/')
    #     if subs and '.' in subs[0]:
    #         parts = subs[0].split('.')
    #         if parts and not parts[-1].lower() in exts:
    #             ret = True
            
    # # # parsed = urlparse(url)
    # # # ret = bool(parsed.netloc) and (parsed.scheme.startswith('http') or url.strip().startswith('//')) # // WP specific?
    # print("url_is_absolute:", ret, "|", url )
    # return ret

    protocol, loc, path = url_split(url)
    
    # err check
    if protocol:
        assert loc
        assert path
    elif loc:
        assert path
    else:
        assert path
    
    ret = bool(loc)
    print("url_is_absolute:", GREEN if ret else YELLOW, ret, RESET, "|", url )
    return ret

def url_is_relative(url):
    ret = not url_is_absolute(url)
    #print("url_is_relative:", ret, "|", url)
    return ret

# # def is_relative_to_base(url, base):
# #     return not url_is_absolute(url)

# https://stackoverflow.com/questions/10772503/check-url-is-a-file-or-directory

def url_is_internal(url, base):
    _, loc_url, _  = url_split(url)
    _, loc_base, _ = url_split(base)
    assert loc_base, "loc_base is None"
    
    ret = False
    if not loc_url:
        ret = True
    elif loc_base in loc_url:
        ret = True
    #print("url_is_internal:", GREEN if ret else YELLOW, ret, RESET, "| loc_url:", dq(loc_url), "| loc_base:", dq(loc_base))
    return ret

def url_is_external(url, base):
    ret = not url_is_internal(url, base)
    #print("url_is_external:", YELLOW, ret, RESET, "| url:", dq(url), "| base:", dq(base))
    return ret

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
def _sleep(secs=33):
    print(RED, "DEBUG _sleep:", secs, RESET)
    time.sleep(secs)
    
def url_has_same_netloc(url, base):
    _, loc_url, _  = url_split(url)
    _, loc_base, _ = url_split(base)
    return loc_base in loc_url

#https://stackoverflow.com/questions/6690739/high-performance-fuzzy-string-comparison-in-python-use-levenshtein-or-difflib
from difflib import SequenceMatcher
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio() #+ 0..1


#https://stackoverflow.com/questions/17388213/find-the-similarity-metric-between-two-strings
""" 
>>> import jellyfish
>>> jellyfish.levenshtein_distance(u'jellyfish', u'smellyfish')
2
>>> jellyfish.jaro_distance(u'jellyfish', u'smellyfish')
0.89629629629629637
>>> jellyfish.damerau_levenshtein_distance(u'jellyfish', u'jellyfihs')
"""
# may just be a missing / for a folder
# https://stackoverflow.com/questions/16603282/how-to-compare-each-item-in-a-list-with-the-rest-only-once
def links_remove_similar(links):
    
    links = links_make_unique(links)
    
    # those have just a forgotten trailing slash
    def is_similar_by_missing_trailing_slash(a,b):
        
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
            #print("\t", RED, "is_similar_by_missing_trailing_slash:", ret, "a,b:", a, b, RESET)
            pass
        
        return ret
        
    excludes = []
    import itertools
    for a, b in itertools.combinations(links, 2):
        res = is_similar_by_missing_trailing_slash(a, b)
        if res:
            excludes.append(res) # the smaller one to be deleted
 
    excludes = links_make_unique(excludes)
    if excludes:
        #print("links_remove_similar:", YELLOW, "excludes:", *excludes, RESET, sep="\n\t") 
        pass   
         
    new_links = [link for link in links if link not in excludes]  
    #print("\t", GREEN, "new_links:", *new_links, RESET, sep="\n\t")   
    
    return new_links
            
    
    
# def links_remove_similar(links, base, thresh=0.8):
#     pass

def link_make_absolute(link, base):
    protocol_url,  loc_url,    path_url    = url_split(link)
    protocol_base, loc_base,   path_base   = url_split(base)
    
    if not protocol_url:
        protocol_url = protocol_base
    
    if not loc_url:
        loc_url = loc_base
        
    ret = protocol_url + "://" + loc_url + path_url
    #print("link_make_absolute:", link, "-->", YELLOW, ret, RESET)    
    return ret

# # def link_make_absolute_OLD(link, base):
# #     if url_is_relative(link):
# #         link = add_trailing_slash(base) + strip_leading_slash(link) # base/link
# #     return link

# # def try_link_make_local_OLD(url, base):
# #     if url_has_same_netloc(url, base):
# #         ret = url
# #         ret = url_path_lstrip_double_slash(ret) # "//media.ka.de"
# #         ret = url_path_lstrip_slash(ret)        # "/media.ka.de"
# #     else:
# #         ret = url
# #     print("try_link_make_local_OLD:", url, "-->", ret)
# #     return ret

def try_link_make_local(url, base):
        
    ret = url
    if url_is_internal(url, base):
        
        _, loc_url, path_url  = url_split(url)
        ret = path_url
        ret = url_path_lstrip_slash(ret)        # "/media.ka.de"
    else:
        print(RED, "try_link_make_local:", "not internal: {}".format(url), RESET)
        exit(7)
        
    print("NEW try_link_make_local:", url, "-->", ret)
    return ret

def links_make_absolute(links, base):
    ret = []
    for link in links:
        ret.append(link_make_absolute(link, base))
    return ret

def links_remove_excludes(links, excludes):
    return [link for link in links if not any(exclude in link for exclude in excludes)]
        
def links_remove_invalids(links, invalids):
    print("links_remove_invalids:", invalids)
    # TODO is same as links_remove_excludes???????????????????
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


                
def links_remove_comments(links, delim='#'):
    return [u for u in links if not u.strip().startswith(delim)]

def links_remove_externals(links, base):
    return [u for u in links if (url_is_internal(u, base))]

def links_remove_folders(links):
    return [u for u in links if not u.strip().endswith('/')]

def links_strip_query_and_fragment(links):
    return [strip_query_and_fragment(u) for u in links]

def links_strip_trailing_slash(links):
    return [strip_trailing_slash(u) for u in links]

def links_make_relative(links, base):
    len_prev = len(links)
    links = links_remove_externals(links, base) # new
    print(YELLOW, "links_make_relative: now removes externals first:", len_prev -  len(links), RESET)
    return [try_link_make_local(u, base) for u in links]

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

def url_netloc(url): 
    loc = urlparse(url.strip()).netloc
    return loc

def url_has_fragment(url):
    f = urlparse(url.strip()).fragment
    ret = True if f else False
    print("url_has_fragment:", ret, url)
    return ret

def url_scheme(url): # '/'
    return urlparse(url.strip()).scheme

def url_path_lstrip_slash(url): # '/'
    return url_path(url, char_lstrip='/')

def url_path_lstrip_double_slash(url): # '/'
    return url_path(url, char_lstrip='//')


#-----------------------------------------
# 
#-----------------------------------------
def strip_protocol(url):
    
    if not url:
        return url
    
    new_url = url
    new_url = new_url.lstrip("https://")
    new_url = new_url.lstrip("http://")
    new_url = new_url.lstrip("://")
    new_url = new_url.lstrip("//")
    new_url = new_url.lstrip('/')
    #print("strip_protocols:", url, "-->", new_url)
    return new_url

# -----------------------------------------
# based on ASSUMPTION that a file has a dot
# -----------------------------------------
def _has_a_dot(url):
    return '.' in url

def url_is_assumed_file(url):
    print(url)
    #url = strip_protocol(url)
    
    if url == None:
        return False
    elif url.endswith('/'):
        return False

    url = url_path(url)
    url = strip_query_and_fragment(url)
    url = strip_trailing_slash(url)
    
    return _has_a_dot(url.split('/')[-1]) # last part

def url_is_assumed_folder(url):
    print(url)
     
    if url == None:
        return False
    
    url = url_path(url)
   
    if not url:
        return True
    elif url.endswith('/'):
        return True
    
    # # url = url_path(url)
    # # print("url_path:", url)
    # # if not url:
    # #     return True # just domain.com no /
    # # else:    
    return not url_is_assumed_file(url)   

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

def add_leading_slash(url):
    url = url.strip().lstrip('/')
    url = '/' + url
    return url

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
    url = strip_tail(url, '#')
    url = strip_tail(url, '?')
    return url

def add_trailing(url, to_add):
    return url.rstrip(to_add) + to_add

def add_trailing_slash(url):
    return add_trailing(url, '/')

#-----------------------------------------
# 
#-----------------------------------------
def make_dirs(the_path):
    #print("make_dirs:", the_path)
    dir = os.path.dirname(the_path)
    if not os.path.exists(dir):
        print("make_dirs: new:", dir)
        os.makedirs(dir)
        
    # debug ONLY
    if dir.strip() in ("https", "sub_send"):
        print(RED, "make_dirs: DEBUG found:", dir, RESET)
        exit(1)
        
#-----------------------------------------
# 
#-----------------------------------------
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


# # def is_online_file_and_exists(url):
# #     t = get_mime_type(url) # None on a folder or if not exists
# #     return True if t else False
  
# # ### I suppose you can add a slash to a URL and see what happens from there. That might get you the results you are looking for.
# # def is_online_directory_or_not_exists(url):
# #     url = get_redirected_url(url)
# #     t = get_mime_type(url)
# #     ret = not is_online_file_and_exists(url)
# #     print("is_online_directory_or_not_exists:", url, "-->", ret)
# #     check_online_site_exists(url)
# #     ###ret = was_redirected(url)
# #     print()
# #     return ret
    
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

# https://docs.python.org/3/library/urllib.request.html#module-urllib.response
# https://docs.python.org/3/library/email.message.html#email.message.EmailMessage
# https://www.w3.org/wiki/LinkHeader
def _get_request(url, method=None): # 'HEAD'
    return urllib.request.Request(url, data=None, headers=headers, method=method) # user agent in headers

# https://stackoverflow.com/questions/33309914/retrieving-the-headers-of-a-file-resource-using-urllib-in-python-3
def get_response(url, timeout=10, method=None, pre="\t"): # 'HEAD'
    try:
        req         = _get_request(url, method=method)
        context     = ssl._create_unverified_context()
        response    = urllib.request.urlopen(req, context=context, timeout=timeout)
        #print("get_response:", url)
        print(pre, vt_code(response.status), "|", vt_b(url != response.url), response.url)
        
        if False:
            #print(GRAY + "\t\t", response.getheaders(), RESET) # list of two-tuples
            print(GRAY + "\t\t" + response.headers.as_string().replace("\n", "\n\t\t") + RESET)
        if False:
            #content = response.read().decode(response.headers.get_content_charset())
            content = response.read().decode('utf-8')
            print(CYAN, content, RESET) # content
            
        return response
    except urllib.error.HTTPError as error:
        print(f"{RED}[!] get_response: {url} error.code: {error.code} --> None {RESET}")
        return None
    except Exception as e:
        print(f"{RED}[!] get_response: {url} Exception: {e} --> None {RESET}")
        return None


"""
    Date: Tue, 21 Jun 2022 07:10:21 GMT
    Server: Apache/2.4.54 (Unix)
    X-Powered-By: PHP/7.4.30
    Link: <https://1001suns.com/wp-json/>; rel="https://api.w.org/"
    Vary: User-Agent,Accept-Encoding
    Content-Type: text/html; charset=UTF-8
    Connection: close
    Transfer-Encoding: chunked
"""    
def get_response_header_link(response):
    link = response.headers.get("Link", None)
    if link:
        link = link.split(';')[0].replace('<', '').replace('>', '') # Link: <https://1001suns.com/wp-json/>; rel="https://api.w.org/"
    print("get_response_header_link:", link)    
    return link
    
def get_redirected_url(url, timeout=10):
    try:
        if True:
            res     = get_response(url, timeout=timeout, method='HEAD') # None 'HEAD'
            new_url = res.url
            print("get_redirected_url:", vt_b(new_url != url), "|", url, "-->", new_url)   
            return new_url, (new_url != url)
        else:
            r = requests.head(url, timeout=timeout) 
            return r.url, (r.url != url)
    
    except Exception as e:
        print(f"{RED}[!] get_redirected_url: {url} Exception: {e}{RESET}")
        return url, False 
    
def was_redirected(url, timeout=10):
    new_url =  get_redirected_url(url, timeout=timeout)
    return (new_url != url)

def get_mime_type(url, timeout=10):
    try:
        contentType =  get_response(url, timeout=timeout, method='HEAD').headers.get_content_type()
        print("get_mime_type:", contentType)   
        return contentType
    except Exception as e:
        print(f"{RED}[!] get_mime_type: {url} Exception: {e} --> None {RESET}")
        return None        
        
# https://nicolasbouliane.com/blog/python-3-urllib-examples
def get_status_code(url, timeout=10):
    try:
        status = urllib.request.urlopen(
            _get_request(url, method=None), # 'HEAD'
            context=ssl._create_unverified_context(), 
            timeout=timeout
        ).status # 200...
    except urllib.error.HTTPError as error:
        print(f"{RED}[!] get_status_code: {url} error.code: {error.code} {RESET}")
        status = error.code # 404, 500, etc
    except Exception as e:
        print(f"{RED}[!] get_status_code: {url} Exception: {e} --> None {RESET}")
        status = None
    
    print("get_status_code:", status, url)   
    return status

def get_content(url, timeout=10):
    try:
        response =  get_response(url, timeout=timeout, method=None)
        content = response.read().decode('utf-8') # decode(response.headers.get_content_charset())
        print("get_content: len(content):", len(content)) 
        #print("get_content:", CYAN, content, RESET) # content
        return content
    except Exception as e:
        print(f"{RED}[!] get_content: {url} Exception: {e} --> None {RESET}")
        return None        
        
#-----------------------------------------
# file exists and is > 0
#-----------------------------------------
def file_exists_and_valid(filepath):
    
    filepath = filepath.strip()
    
    if os.path.exists(filepath):
        if os.path.isfile(filepath):
            if os.path.getsize(filepath) > 0:
                #print("file_exists_and_valid:", GREEN, "isfile", RESET, os.path.getsize(filepath), filepath)
                return True
        elif os.path.isdir(filepath):
            #print("file_exists_and_valid:", GREEN, "isdir", RESET, filepath)
            return True
       
    #print("file_exists_and_valid:", RED, "NO", RESET, filepath) 
    return False
    
    # import pathlib as p
    # path = p.Path(filepath)
    # if path.exists() and path.stat().st_size > 0:
    #     print("file_exists_and_valid:", GREEN, "OK", RESET, path.stat().st_size, filepath)
    #     return True
    # else:
    #     print("file_exists_and_valid:", RED, "NO", RESET, filepath)
    #     return False

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

def wait_for_page_has_loaded_readyState(driver, sleep_secs=1):
    
    # https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
    def _page_has_loaded_readyState(driver):
        #print("_page_has_loaded_readyState: {}".format(driver.current_url))
        page_state = driver.execute_script('return document.readyState;')
        return page_state == 'complete'

    # # # max_turns = 10
    # # # cnt = 0
    # # # while not _page_has_loaded_readyState(driver):
    # # #     print("wait_for_page_has_loaded_readyState: {} {}s {}".format(cnt, sleep_secs, driver.current_url))
    # # #     time.sleep(sleep_secs)
    # # #     if cnt := cnt + 1 >= max_turns:
    # # #         break
        
    max_tries = 20
    for tries in range(1, max_tries+1):
        print(MAGENTA + "[{}] wait_for_page_has_loaded_readyState: {}s | {}".format(tries, sleep_secs, driver.current_url) + RESET)
        if _page_has_loaded_readyState(driver):
            break
        else:
            print("\t", "sleep:", sleep_secs)
            time.sleep(sleep_secs)
            
    if tries == max_tries:
        print("\t", RED + "wait_for_page_has_loaded_readyState: tried out !!!" + RESET)
        
    return True
    
# https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
def wait_for_page_has_loaded_hash(driver, sleep_secs=1):
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

    
    # comparing old and new page DOM hash together to verify the page is fully loaded
    # # page_hash = 'empty'
    # # page_hash_new = ''
    # # # while page_hash != page_hash_new: 
    # # #     page_hash = get_page_hash(driver)
    # # #     time.sleep(sleep_secs)
    # # #     page_hash_new = get_page_hash(driver)
    # # #     print('<page_has_loaded> - page not loaded')
        
    max_secs = 30
    for cnt in range(max_secs):
         page_hash = get_page_hash(driver)
         print("wait_for_page_has_loaded_hash: sleep", sleep_secs, cnt)
         time.sleep(sleep_secs)
         page_hash_new = get_page_hash(driver)
         if page_hash_new == page_hash:
             print("wait_for_page_has_loaded_hash: ", "SUCCESS...")
             break
         
    print("wait_for_page_has_loaded_hash: loaded", driver.current_url)
    return True
    
#-----------------------------------------
# surrogate
#-----------------------------------------
def wait_for_page_has_loaded(driver):
    return wait_for_page_has_loaded_readyState(driver, sleep_secs=1)
#-----------------------------------------
# 
#-----------------------------------------
def replace_all(content, oldvalue, newvalue):
    if not content:
        return content
    
    cnt_first = content.count(oldvalue)
    len_orig = len(content)
    
    # while oldvalue in content:
    #     content = content.replace(oldvalue, newvalue)
    content = content.replace(oldvalue, newvalue)
    
    cnt_last = content.count(oldvalue)
    
    if False: # verbose
        printvalue = oldvalue.replace("\n", "_n_").replace("\t", "_t_").replace("\r", "_r_")       
        print(
            "replace_all:", 
            CYAN, dq(printvalue), RESET, 
            "| replaced", len_orig - len(content), "bytes",
            "| cnt:", cnt_first, "-->", cnt_last
        )
        
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
import cssutils
import logging
import cssbeautifier
def get_stylesheet_background_images_from_string(style_string):
    
    # # #style_string = html_minify(style_string)
    # # style_string = cssbeautifier.beautify(style_string)
    # # print(GRAY + style_string + RESET)
    
    urls  = []
    try:
        cssutils.log.setLevel(logging.CRITICAL)
        sheet = cssutils.parseString(style_string)
        #print (sheet.cssText)
        for rule in sheet:
            if rule.type == rule.STYLE_RULE:
                for property in rule.style:
                    if property.name == 'background-image':
                        if "url" in property.value:
                            url = property.value.replace("(", "").replace(")", "")
                            url = url.strip().lstrip("url")
                            #print("\t\t\t", CYAN, url, RESET)
                            urls.append(url)
    except Exception as e:
        print(f"{RED}get_stylesheet_background_images_from_string: cssutils.parseString {e} {RESET}")
    
    if urls:    
        print("get_stylesheet_background_images_from_string:", CYAN, *urls, RESET, sep="\n\t")
        
    return urls

def get_stylesheet_background_images_from_file(style_path):
    urls  = []
    if os.path.isfile(style_path):
        with open(style_path, mode='r') as fp:
            style_string = fp.read()
            urls = get_stylesheet_background_images_from_string(style_string)
    else:
        print(f"{YELLOW}TODO: style_path not yet downloaded: {style_path} {RESET}") # TODO 
        time.sleep(2)   
        
    return urls

#-----------------------------------------
# 
#-----------------------------------------   
def save_html(content, path, pretty=False):
    
    print("save_html:", path)
    
    if pretty:
        from bs4 import BeautifulSoup, Comment
        soup = BeautifulSoup(content, 'html.parser')    
        content = soup.prettify()
        
    make_dirs(path)
    try:
        if not os.path.isfile(path):
            with open(path, 'w', encoding="utf-8") as fp:
                fp.write(content)
        else:
            print(f"{MAGENTA}\t save_html: file already exists: {os.path.basename(path)} {RESET}")
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
                remove_optional_attribute_quotes=False, # ??????? True TODO
                convert_charrefs=True,
                )
        except:
            print(f"{RED}could not htmlmin.minify!{RESET}")
            
        
        if True:
            content = replace_all(content, "\n", " ")
            content = replace_all(content, "\t", " ")
            content = replace_all(content, "\r", " ")
            #print("len(content)", len(content))
            content = replace_all(content, "  ", " ")
            content = replace_all(content, "< ", "<") # assume that all <> are tags and NOT lt gt
            content = replace_all(content, " >", ">") 
            content = replace_all(content, "> <", "><") 
            content = replace_all(content, "} }", "}}") 
            content = replace_all(content, "{ {", "{{") 
            #print("len(content)", len(content))
            
        percent = round(len(content) / length_orig * 100, 1)
        percent_saved = round(100 - percent, 1)
        print("html_minify: final len(content)", len(content), "|", GREEN, "percent_saved:", percent_saved, "%", RESET)
    
    return content
#-----------------------------------------
# 
#-----------------------------------------
# def replace_in_file(filename, string_from, string_to):
    
#     fp = open(filename, "rt")
#     data = fp.read()
#     data = data.replace(string_from, string_to)
#     fp.close()
    
#     #open the input file in write mode
#     fp = open(filename, "wt")
#     fp.write(data)
#     fp.close()

def replace_all_in_file(filename, string_from, string_to):
    
    #print("replace_all_in_file:", filename)
    
    fp = open(filename, "r", encoding="utf-8")
    data = fp.read()
    
    cnt = data.count(string_from)
    if cnt > 0:
        print("replace_all_in_file:", cnt, "|", CYAN + string_from + RESET, "-->", string_to)
    
    data = replace_all(data, string_from, string_to)
    fp.close()
    
    #open the input file in write mode
    fp = open(filename, "w", encoding="utf-8")
    fp.write(data)
    fp.close()

# -----------------------------------------
#
# -----------------------------------------

def progress_string(perc, verbose_string="", VT=MAGENTA, n=16, cdone='■', crest='-'):
    return VT + "[" + cdone*round(n*perc) + crest*round(n*(1-perc)) + "] [{:.1f}%] ".format(perc*100) + verbose_string + RESET 

def progress(perc, verbose_string="", VT=MAGENTA, n=16, prefix="", cdone='■', crest='-'): # | .
    import math
    # if perc <= 0.0:
    print("{}{}[{}] [{:.1f}%] {}{}".format(VT, prefix, crest*n, perc*100, verbose_string, RESET),  end='\r')
    if perc >= 1.0:
        end = '\n'
    else:
        n = min(n, math.ceil(n * perc))
        end = '\r'
    print("{}{}[{}{}".format(VT, prefix, cdone*n, RESET),  end=end)


def sleep_random(wait_secs=(1, 2), verbose_string="", verbose_interval=0.5, VT=MAGENTA, n=16, prefix=""):
    if wait_secs and abs(wait_secs[1] - wait_secs[0]) > 0.0:
        import random
        import math
        s = random.uniform(wait_secs[0], wait_secs[1])
        #print("sleep_random: {:.1f}...{:.1f} --> {:.1f}s".format(wait_secs[0], wait_secs[1], s))
        start_secs = time.time()
        progress(0, verbose_string=verbose_string, VT=VT, n=n, prefix=prefix)
        while time.time() - start_secs < s:
            perc = (time.time() - start_secs) / float(s)
            progress(perc, verbose_string=verbose_string, VT=VT, n=n, prefix=prefix)
            time.sleep(0.01)
        progress(1, verbose_string=verbose_string, VT=VT, n=n, prefix=prefix)
             
#-----------------------------------------
# 
#-----------------------------------------
def collect_files_endswith(project_folder, allowed_extensions):
    allowed_extensions = [e.lower() for e in allowed_extensions]
    print("collect_files:", project_folder)
    print("collect_files:", allowed_extensions)
    assets = []
    for root, dirs, files in os.walk(project_folder):
        for file in files:
            if any(file.lower().endswith(ext) for ext in allowed_extensions): 
                path = os.path.abspath(os.path.join(root, file))
                #print("\t", os.path.basename(path))
                assets.append(path)
    print("collect_files:", len(assets), "assets found.")
    return assets

#-----------------------------------------
# 
#-----------------------------------------

#-----------------------------------------
# 
#-----------------------------------------
if __name__ == "__main__":
    print("\n"*3 + "you started the wrong file..." + "\n"*3)
    
    # https://stackoverflow.com/questions/17388213/find-the-similarity-metric-between-two-strings
    import jellyfish
    a = "https://domain.com/has/just/forgotten/slash/"
    b = "https://domain.com/has/just/forgotten/slash"
    
    a = "https://domain.com/has/just/forgotten/slash/"
    b = "http://domain.com/has/just/forgotten/slash"
    
    a = "https://google.com"
    b = "https://apple.de/"
    
    print( jellyfish.levenshtein_distance(a, b) )
    print( jellyfish.jaro_distance(a, b) )
    print( jellyfish.damerau_levenshtein_distance(a, b) )
    print( jellyfish.jaro_winkler_similarity(a, b) )
    print( jellyfish.hamming_distance(a, b) )
    print( jellyfish.match_rating_comparison(a, b) )

    