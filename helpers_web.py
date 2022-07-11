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
import pathlib
import datetime

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
_no_esc = lambda s : s.replace('\/', '/')
_wrap = lambda s, delim : delim if not s else delim + str(_no_esc(s)).strip() + delim
def dq(s=""):
    return _wrap(s, delim="\"")
def sq(s=""):
    return _wrap(s, delim="\'")
def pa(s=""):
    return "(" + str(_no_esc(s)).strip() + ")"
def qu(s=""):
    return _wrap(s, delim="&quot;")
#-----------------------------------------
# 
#-----------------------------------------
def vt_b(b_val):
    return (f'{GREEN}+T' if b_val else f'{RED}-F') + RESET
    #return (GREEN if b_val else RED) + str(int(b_val)) + RESET
def vt_http_status_code(code): # http status
    return (GREEN if code < 400 else RED) + str(code) + RESET
    #return (GREEN if b_val else RED) + str(int(b_val)) + RESET
    
def _saved_percent(size_orig, size_new):
    if size_orig <= 0:
        return 0
    perc = 100 - (size_new/size_orig*100)
    return perc

def saved_percent_string(size_orig, size_new, vt=""):
    pct = _saved_percent(size_orig, size_new)
    return "{}{:+.1f}%{}".format(vt, pct, RESET)

def vt_saved_percent_string(size_orig, size_new):
    pct = _saved_percent(size_orig, size_new)
    vt  = RED if pct < 0 else GREEN
    return saved_percent_string(size_orig, size_new, vt=vt)
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

""" 
>> import tldextract
>> tldextract.extract("http://lol1.domain.com:8888/some/page"
ExtractResult(subdomain='lol1', domain='domain', suffix='com')
>> tldextract.extract("http://sub.lol1.domain.com:8888/some/page"
ExtractResult(subdomain='sub.lol1', domain='domain', suffix='com')
>> urlparse.urlparse("http://sub.lol1.domain.com:8888/some/page")
ParseResult(scheme='http', netloc='sub.lol1.domain.com:8888', path='/some/page', params='', query='', fragment='')
"""
import tldextract

def url_is_internal(url, base):
    _, loc_url, _  = url_split(url)
    _, loc_base, _ = url_split(base)
    assert loc_base, "loc_base is None!!!"
    
    ret = False
    if not loc_url: # local url
        ret = True
    else:
        tld_url  =  tldextract.extract(url) 
        tld_base =  tldextract.extract(base) 
        ret = (tld_url.domain == tld_base.domain and tld_url.suffix == tld_base.suffix)
        #print("\n", GREEN, tld_url, GRAY, tld_base, RESET)
        
    #print("url_is_internal:", YELLOW, int(ret), GREEN, dq(url), GRAY, dq(base), RESET)
    return ret

def url_is_external(url, base):
    # tld_url  =  tldextract.extract(url) 
    # tld_base =  tldextract.extract(base) 
    # assert tld_base, "loc_base is None"
    
    # if not tld_url:
    #     ret = False
    # else:
    #     ret = (tld_url != tld_base)
        
    ret = not url_is_internal(url, base)
    
    #print("url_is_external:", YELLOW, int(ret), GREEN, dq(url), GRAY, dq(base), RESET)
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
    # # # if not loc_url and loc_base:
    # # #     return True # consider same as url is local
    # # # elif not loc_url and not loc_base:
    # # #     return True
    if not loc_url or not loc_base:
        return True
    #print("url_has_same_netloc: loc_base", loc_base, "loc_url", loc_url)
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
    
    if not loc_base:
        print(RED, "link_make_absolute:", "not loc_base", RESET)
        assert False    
    
    if not protocol_url:
        if protocol_base:
            protocol_url = protocol_base
        else:
            protocol_url = "https"
    
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
        assert False
        
    print("NEW try_link_make_local:", url, "-->", ret)
    return ret

def links_make_absolute(links, base):
    ret = []
    for link in links:
        ret.append(link_make_absolute(link, base))
    return ret

def links_remove_excludes(links, excludes):
    print("links_remove_excludes:", excludes)
    excludes = list(excludes)
    return [link for link in links if not any(exclude.strip() in link for exclude in excludes)]

    ###return links_remove_invalids(links, excludes)
        
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

                
def links_remove_nones(links):
    return [u for u in links if u]
         
def links_remove_comments(links, delim='#'):
    return [u for u in links if not u.startswith(delim)]

def links_remove_externals(links, base):
    return [u for u in links if not url_is_external(u, base)]

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

def links_strip(links):
    return [u.strip() for u in links]

def links_replace(links, replacements):
    
    def was_replaced(link, replacements):
        link = link.strip()      
        for rep in replacements:
            assert len(rep) >= 2
            new_link = link.replace(rep[0], rep[1])  
            if new_link != link:
                #print("\t", "replaced:", YELLOW, dq(new_link), RESET)
                return True, new_link
        return False, link

    ret = []
    for link in links:
        b_replaced, new_link = was_replaced(link, replacements)
        if not new_link in ret:
            #print("\t", "adding  :", GREEN, dq(new_link), RESET)
            ret.append(new_link)
    return ret
    
def links_sanitize(links):
    links = links_remove_comments(links, delim='#')
    links = links_remove_similar(links)
    links = links_remove_nones(links)
    links = links_strip(links)
    links = links_make_unique(links)
    links = sorted(links)
    return links

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

# parsed = urlparse('http://netloc/path;parameters?query=argument#fragment')
# ParseResult(scheme='http', netloc='netloc', path='/path', params='parameters', query='query=argument', fragment='fragment')
def url_ppqf(url):
    parsed = urlparse(url)
    ret = ""
    ret += parsed.path if parsed.path else '' # ---> may have /path
    #ret += ';' + parsed.parameters if parsed.parameters else ''
    ret += '?' + parsed.query if parsed.query else ''
    ret += '#' + parsed.fragment if parsed.fragment else ''
    return ret
    
def url_qf(url):
    parsed = urlparse(url)
    ret = ""
    ret += '?' + parsed.query if parsed.query else ''
    ret += '#' + parsed.fragment if parsed.fragment else ''
    return ret
    

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
    #print(url)
    #url = strip_protocol(url)
    
    if url == None:
        return False
    elif url.endswith('/'):
        return False

    url = url_path(url)
    ###url = strip_query_and_fragment(url)
    url = strip_trailing_slash(url)
    
    return _has_a_dot(url.split('/')[-1]) # last part

def url_is_assumed_folder(url):
    #print(url)
     
    if url == None:
        return False
    
    url = url_path(url)
   
    if not url:
        return True
    elif url.endswith('/'):
        return True
     
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

# https://en.wikipedia.org/wiki/URI_fragment
# scheme://netloc/path;parameters?query#fragment
def strip_query_and_fragment(url):
    new_url = url
    new_url = strip_tail(new_url, '?')
    new_url = strip_tail(new_url, '#')
    #print("strip_query_and_fragment", url, "-->", YELLOW, new_url, RESET)
    return new_url

def strip_query(url):
    parsed  = urlparse(url)
    new_url = url
    new_url = strip_query_and_fragment(new_url)
    if parsed.fragment:
        new_url += "#" + parsed.fragment
    #print("strip_query", url, "-->", YELLOW, new_url, RESET)
    return new_url

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
        assert False
        
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
        print(pre, vt_http_status_code(response.status), "|", vt_b(url != response.url), response.url)
        
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
# background_images
#-----------------------------------------
def get_background_images_from_style_attribute(driver):

    def _parse_style_attribute(style_string):
        
        #if 'background-image' in style_string:
        #if any(key in style_string for key in ['background-image', 'content']):
        for key in ['background-image', 'content']:
            if key in style_string:
                try:
                    url_string = style_string.split(' url("')[1].replace('");', '')
                except:
                    # may be a gradient
                    print(f"{RED}ERR missing background-image: style_string: {style_string} {RESET}")
                    url_string = None
                
                print(f"\t key: {MAGENTA}{key}{RESET}: {url_string}") 
                # # # if key == 'content':
                # # #     time.sleep(3)
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

def extract_background_image_from_property(property):
    try:
        if property.name in ['background-image', 'content']:
            if "url" in property.value:
                url = property.value.split(' url(')[-1]
                url = url.replace("(", "").replace(")", "").replace("!important", "")
                url = url.strip().lstrip("url")
                print("\t\t\t", YELLOW, property.name, CYAN, url, RESET)
                # # # if property.name == 'content':
                # # #     time.sleep(0.5) # <<< this one here
                return url
    except Exception as e:
        print(f"{RED}extract_background_image: cssutils.parseString {e} {RESET}")
        
    return None

def get_background_images_from_stylesheet_string(style_string):
    urls  = []
    try:
        cssutils.log.setLevel(logging.CRITICAL)
        sheet = cssutils.parseString(style_string) # <<<
        #print ("sheet.cssText:", MAGENTA, sheet.cssText, RESET)
        for rule in sheet:
            if rule.type == rule.STYLE_RULE:
                for property in rule.style:
                    url = extract_background_image_from_property(property)
                    if url:
                        urls.append(url)
    except Exception as e:
        print(f"{RED}get_background_images_from_stylesheet_string: cssutils.parseString {e} {RESET}")
    
    return urls  

def get_background_images_from_inline_style_tag(style_string):
    urls  = []
    try:
        cssutils.log.setLevel(logging.CRITICAL)
        style = cssutils.parseStyle(style_string) # <<<
        #print ("style.cssText:", MAGENTA, style.cssText, RESET)
        for property in style:
            url = extract_background_image_from_property(property)
            if url:
                urls.append(url)
                    
    except Exception as e:
        print(f"{RED}get_background_images_from_inline_style_tag: cssutils.parseString {e} {RESET}")
    
    return urls  

def get_background_images_from_stylesheet_file(style_path):
    urls  = []
    if os.path.isfile(style_path):
        with open(style_path, mode='r') as fp:
            style_string = fp.read()
            urls = get_background_images_from_stylesheet_string(style_string)
    else:
        print(f"{YELLOW}TODO: not yet downloaded: {style_path} {RESET}") # TODO 
        time.sleep(1)   
        
    return urls

# https://pythonhosted.org/cssutils/
# https://pythonhosted.org/cssutils/
# https://github.com/jaraco/cssutils
# https://cthedot.de/cssutils/
# https://stackoverflow.com/questions/59648732/replace-uri-value-in-a-font-face-css-rule-with-cssutils
# https://groups.google.com/g/cssutils?pli=1
# https://www.fullstackpython.com/cascading-style-sheets.html

def css_sheet_delete_rules(sheet, rules_to_delete):
    rules_to_delete = list(rules_to_delete)
    
    print("css_sheet_delete_rules:", rules_to_delete)

    # indices = []
    # for i, rule in enumerate(sheet):
    #     if rule.type in rules_to_delete:
    #         #print("\t\t", i, "rule", wh.CYAN, rule, wh.RESET)
    #         indices.append(i)
            
    indices = [i for i, rule in enumerate(sheet) if rule.type in rules_to_delete]
            
    print("css_sheet_delete_rules:", "indices", indices)
            
    for index in reversed(indices): # !!
        #print("deleteRule", index)
        sheet.deleteRule(index) 
        
    return sheet

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
        assert False # TODO!!!!!!!!!!!!!!!!!!!!
        
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
def html_sanitize(content, vb=False):
    
    # print(YELLOW, "html_sanitize:may be problematic for js --> RETURN", RESET)
    # return content
    
    length_orig = len(content)
    
    #content = replace_all(content, "\n", " ")
    content = replace_all(content, "\n\n", "\n")
    content = replace_all(content, "\t", " ")
    content = replace_all(content, "\t\t", " ")
    content = replace_all(content, "\r", " ")
    content = replace_all(content, "  ", " ")
    content = replace_all(content, "< ", "<") # assume that all <> are tags and NOT lt gt
    content = replace_all(content, " >", ">") 
    content = replace_all(content, "> <", "><") 
    content = replace_all(content, "} }", "}}") 
    content = replace_all(content, "{ {", "{{") 
    content = replace_all(content, ") )", "))") 
    content = replace_all(content, "( (", "((") 
    content = replace_all(content, "[ [", "[[") 
    content = replace_all(content, "] ]", "]]") 

    if vb:
        print("html_sanitize:", "percent_saved:", vt_saved_percent_string(length_orig, len(content)))
    
    return content
    
def html_minify(content, vb=False):
    
    length_orig = len(content)
    
    if length_orig > 0:
        # pip install htmlmin
        
        import htmlmin
        try:
            # https://htmlmin.readthedocs.io/en/latest/reference.html
            content = htmlmin.minify(
                input=content, 
                remove_comments=True, 
                remove_empty_space=False,
                remove_all_empty_space=False,
                reduce_boolean_attributes=True,
                reduce_empty_attributes=True,
                remove_optional_attribute_quotes=True, # ??????? False TODO
                convert_charrefs=True,
                keep_pre=True,
                pre_tags=['pre', 'textarea'],
                pre_attr='pre'
                )
        except:
            print(f"{RED}could not htmlmin.minify!{RESET}")
         
        # if False:   
        #     content = html_sanitize(content, vb)
            
        if vb:
            print(
                "html_minify:", len(content), 
                "|", 
                "percent_saved:", vt_saved_percent_string(length_orig, len(content)))
    
    return content

def __minify_on_disk(filename, func_mini):
    print("__minify_on_disk:", GRAY, os.path.basename(filename), RESET, end= ' ')
    data        = string_from_file(filename)
    mini_data   = func_mini(data)
    print(vt_saved_percent_string(len(data), len(mini_data)))
    if len(mini_data) < len(data):
        string_to_file(mini_data, filename)
    else:
        print("\t", "useless compressions: undo...")
    
def html_minify_on_disk(filename):
    assert filename.endswith(".html"), filename
    __minify_on_disk(filename, html_minify)
  
# http://opensource.perlig.de/rcssmin/  
import rcssmin    
def css_minify_on_disk(filename): 
    assert filename.endswith(".css"), filename
    __minify_on_disk(filename, rcssmin.cssmin)      
 
import rjsmin   
def js_minify_on_disk(filename): 
    assert filename.endswith(".js"), filename
    __minify_on_disk(filename, rjsmin.jsmin)      
    
    
#-----------------------------------------
# 
#-----------------------------------------
def replace_all(content, oldvalue, newvalue, vb = False):
    
    if not content:
        return content
    
    cnt_first = content.count(oldvalue)
    len_orig = len(content)
    
    # while oldvalue in content:
    #     content = content.replace(oldvalue, newvalue)
    content = content.replace(oldvalue, newvalue)
    
    cnt_last = content.count(oldvalue)
   
    if vb: 
        if len_orig - len(content) > 0: # verbose
            printvalue = oldvalue.replace("\n", "_n_").replace("\t", "_t_").replace("\r", "_r_")       
            print(
                "replace_all:", 
                CYAN,       dq( oldvalue.replace("\n", "_n_").replace("\t", "_t_").replace("\r", "_r_") ), RESET, 
                "| replaced", len_orig - len(content), "bytes",
                "| cnt:", cnt_first, "-->", cnt_last,
                MAGENTA,    dq( newvalue.replace("\n", "_n_").replace("\t", "_t_").replace("\r", "_r_") ), RESET
            )
        
    return content

#-----------------------------------------
# 
#-----------------------------------------
def file_replace_all(filename, string_from, string_to):
    
    #print("replace_all_in_file:", filename)
    
    # with open(filename, "r", encoding="utf-8") as fp:
    #     data = fp.read()
        
    data = string_from_file(filename)
        
    cnt = data.count(string_from)
    if cnt > 0:
        print("replace_all_in_file:", cnt, "|", CYAN + string_from + RESET, "-->", string_to)
    data = replace_all(data, string_from, string_to)  
    
    string_to_file(data, filename)
    
    # # # with open(filename, "w", encoding="utf-8") as fp:
    # # #     fp.write(data)
                
                
# -----------------------------------------
#
# -----------------------------------------
def file_make_unique(filename, sort):
    lines       = list_from_file(filename)
    len_orig    = len(lines)
    lines       = links_make_unique(lines)
    if sort:
        lines = sorted(lines)
    print("file_make_unique: elements removed:", len_orig -len(lines))
    list_to_file(lines, filename)
    
# -----------------------------------------
#
# -----------------------------------------

def list_from_file(path, mode="r", encoding="utf-8", sanitize=False):
    if not os.path.isfile(path):
        return []
    
    with open(path, mode=mode, encoding=encoding) as file:
        ret = [line.strip() for line in file]
        if sanitize:
            ret = links_sanitize(ret)
        return ret
    
def list_to_file(items, path, mode="w", encoding="utf-8"):
    print("list_to_file", path)
    # # with open(path, mode=mode, encoding=encoding) as file:
    # #     file.write(list_to_string(items))
    string_to_file(list_to_string(items), path, mode=mode, encoding=encoding)
 
def list_to_string(items):
    s = ""
    for item in items:
        if type(item) in [list, set]:
            s += ",".join(str(part) for part in item) + "\n"
        else:
            s += str(item) + "\n"
    return s
        
    return "\n".join(str(item) for item in items)

def string_from_file(path, sanitize=False):
    return list_to_string(list_from_file(path, sanitize=sanitize))

def string_to_file(string, path, mode="w", encoding="utf-8"):
    #print("string_to_file", GRAY, path, RESET)
    with open(path, mode=mode, encoding=encoding) as file:
        file.write(string)

def list_from_string(s):
    return list(s.split('\n'))
        
def list_print(items, sep="\n\t", vt=GRAY):
    print("list_print:", GRAY, *items, RESET, sep=sep)    
    print("list_print:", len(items), "items")  

# -----------------------------------------
#
# -----------------------------------------    
list_func_to_tuple = lambda s : tuple(s.split(','))
list_func_strip = lambda s : s.strip()
def list_exec(items, func): 
    return [func(item) for item in items]

    
""" 
    css = list_from_file(config.style_path)
    css = cssbeautifier.beautify(list_to_string(css))
    list_to_file(list_from_string(css), config.data_base_path + "test_XXXXXXX.css")
    
    list_exec(image_links, func=lambda s : tuple(s.split(',')))
    
    
""" 
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
def collect_files_func(project_folder, func):
    print("collect_files:", project_folder)
    assets = []
    for root, dirs, files in os.walk(project_folder):
        
        for file in files:
            if func(file): 
                path = os.path.abspath(os.path.join(root, file))
                #print("\t", os.path.basename(path))
                assets.append(path)
                
        for dir in dirs:
            if func(dir): 
                path = os.path.abspath(os.path.join(root, dir))
                #print("\t", os.path.basename(path))
                assets.append(path)
                
    print("collect_files:", len(assets), "assets found.")
    return assets
#-----------------------------------------
# 
#-----------------------------------------
def sanitize_umlauts(_orig_path):
    fixedpath = _orig_path
    
    fixedpath = fixedpath.replace('ä',  "ae")
    fixedpath = fixedpath.replace('ö',  "oe")
    fixedpath = fixedpath.replace('ü',  "ue")
    fixedpath = fixedpath.replace('Ä',  "Ae")
    fixedpath = fixedpath.replace('Ö',  "Oe")
    fixedpath = fixedpath.replace('Ü',  "Ue")
    fixedpath = fixedpath.replace('ß',  "ss")
    
    fixedpath = fixedpath.replace('©',  "_c_")
    fixedpath = fixedpath.replace('@',  "_at_")
    
    # ascii https://pythonguides.com/remove-non-ascii-characters-python/
    fixedpath = fixedpath.encode("ascii", "ignore").decode()
    
    return fixedpath    
    
def sanitize_filepath_and_url(_orig_path,  rep = '_'):
    fixedpath = _orig_path
    #fixedpath = fixedpath.replace('?',  rep) # is valid for url
    fixedpath = fixedpath.replace(' ',  rep)
    fixedpath = fixedpath.replace('%',  rep)
    fixedpath = fixedpath.replace('*',  rep)
    fixedpath = fixedpath.replace(':',  rep)
    fixedpath = fixedpath.replace('|',  rep)
    fixedpath = fixedpath.replace('\"', rep)
    fixedpath = fixedpath.replace('\'', rep)
    fixedpath = fixedpath.replace('<',  rep)
    fixedpath = fixedpath.replace('>',  rep)
    
    fixedpath = fixedpath.replace('\'',  rep)
    fixedpath = fixedpath.replace('\"',  rep)
    
    
    # change umlauts
    fixedpath = sanitize_umlauts(fixedpath)
    
    #print("sanitized:", RED, _orig_path, GREEN, fixedpath, RESET)
    
    return fixedpath
#-----------------------------------------
# 
#-----------------------------------------

def get_page_name(ext=".html", basename="index"):
    return basename + ext

"""
get_path_local_root: https://www.karlsruhe.digital/ --> /
get_path_local_root: https://www.media.karlsruhe.digital/ --> /media/
get_path_local_root: https://media.karlsruhe.digital/ --> /media/
get_path_local_root: https://media.karlsruhe.digital/my/folder/this.jpeg --> /media/my/folder/this.jpeg
get_path_local_root: https://karlsruhe.digital/ --> /
get_path_local_root: https://karlsruhe.digital/index.html --> /index.html
get_path_local_root: https://karlsruhe.digital/some/folder/image.png --> /some/folder/image.png

"""

def get_path_local_root_subdomains(url, base, sanitize=True):
    assert base, "needs a valid base"
    
    base = link_make_absolute(base, base)
    url  = link_make_absolute(url, base)
    #print(f"get_path_local_root_subdomains: {url} | {base}")
    
    # externals should be removed before
    if not url_has_same_netloc(url, base):
        print(f"{YELLOW}get_path_local_root_subdomains: url: {url} has not same netloc {base} {RESET}")
        assert False

    # loc_url:  media.karlsruhe.digital
    # loc_base:       karlsruhe.digital
    loc_url   = url_netloc(url).lstrip("www.")
    loc_base  = url_netloc(base)
    subdomain = loc_url.replace(loc_base, '').replace('.', '') # --> media
    if subdomain: # '' or 'sub_dir/'
        subdomain = strip_leading_slash(subdomain)
        subdomain = "sub_" + subdomain
        subdomain = add_trailing_slash(subdomain)
        
    rooted = '/' + subdomain + strip_leading_slash(url_ppqf(url))
    
    if sanitize:
        rooted = sanitize_filepath_and_url(rooted)
    
    #print("get_path_local_root_subdomains:", GRAY, url, "-->", RESET, rooted)
    return rooted

"""
TODO maybe deal with de/ en/

get_path_local_root:  https://www.karlsruhe.digital/ -->  /
get_page_folder    :  https://www.karlsruhe.digital/ --> 
get_path_local_root:  https://www.media.karlsruhe.digital/ -->  /media/
get_page_folder    :  https://www.media.karlsruhe.digital/ -->  media/
get_path_local_root:  https://media.karlsruhe.digital/ -->  /media/
get_page_folder    :  https://media.karlsruhe.digital/ -->  media/
get_path_local_root:  https://media.karlsruhe.digital/my/folder/this.jpeg -->  /media/my/folder/this.jpeg
get_page_folder    :  https://media.karlsruhe.digital/my/folder/this.jpeg -->  media/my/folder/
get_path_local_root:  https://karlsruhe.digital/ -->  /
get_page_folder    :  https://karlsruhe.digital/ --> 
get_path_local_root:  https://karlsruhe.digital/index.html -->  /index.html
get_page_folder    :  https://karlsruhe.digital/index.html --> 
get_path_local_root:  https://karlsruhe.digital/some/folder/image.png -->  /some/folder/image.png
get_page_folder    :  https://karlsruhe.digital/some/folder/image.png -->  some/folder/
"""
def get_page_folder(url, base):
    
    path = get_path_local_root_subdomains(url, base).lstrip('/')
    path = strip_query_and_fragment(path) # NEW
    
    page_folder = ""
    subs = path.split('/')
    for folder in subs:
        if folder and url_is_assumed_folder(folder):
            page_folder += folder + "/"
            
    print("get_page_folder    :", GRAY, url, "-->", RESET, sq(page_folder))
    return page_folder


#-----------------------------------------
# 
#-----------------------------------------
def get_directory_total_size(start_path):
    print("get_size:", CYAN, start_path, RESET)
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    print("get_size: total_size:", round(total_size / (1024*1024), 1), "MB")
    return total_size

def get_project_total_size(project_folder, prefix, use_pdf):
    
    # TODO list all files,size to csv
    print("get_project_total_size:", YELLOW, "use_pdf:", use_pdf, RESET)
    
    def __get_sizes(func, excludes, csv_out_path):
        collected = [["cnt","ext","file","fsize","dt_m"]]
        total_size = 0
        files = collect_files_func(project_folder, func=func)
        
        files = links_remove_excludes(files, excludes)
        if not use_pdf:
            print("\t", "...excluding pdfs")
            files = links_remove_excludes(files, [".pdf"])
            
        files = links_sanitize(files)
        for cnt, file in enumerate(files):
            if os.path.isfile(file):
                fsize = os.path.getsize(file)
                m_time = os.path.getmtime(file)
                dt_m = datetime.datetime.fromtimestamp(m_time).isoformat()
                name, ext = os.path.splitext(file)
                total_size += fsize
                collected.append([
                    cnt, ext, file,fsize, dt_m
                ])
        list_to_file(collected, csv_out_path)
        return total_size
     
    # recursive import             
    import config
    
    total_size_originals = __get_sizes(
        config.f_originals, 
        excludes=config.f_originals_excludes,
        csv_out_path=config.path_stats + prefix + "_export_original_files.csv"
    )
    
    total_size_unpowered = __get_sizes(
        config.f_unpowered, 
        excludes=["font", "sub_media", "real3d-flipbook"], # some svg are fontawesome yakk
        csv_out_path=config.path_stats + prefix + "_export_unpowered_files.csv"
    )
    
    del config

    print(f"total_size_originals: {total_size_originals:,} bytes | {YELLOW}{total_size_originals/1000000:,.1f} MB{RESET}")
    print(f"total_size_unpowered: {total_size_unpowered:,} bytes | {YELLOW}{total_size_unpowered/1000000:,.1f} MB{RESET}")
    
    
    perc100_saved = _saved_percent(total_size_originals, total_size_unpowered)
    
    print("get_project_total_size:", vt_saved_percent_string(total_size_originals, total_size_unpowered))
    
    return perc100_saved, total_size_originals, total_size_unpowered

              
#-----------------------------------------
# 
#-----------------------------------------
              
def gzip_file(in_path, out_path):
    import gzip
    with open(in_path, 'rb') as f_in, gzip.open(out_path, 'wb') as f_out:
        f_out.writelines(f_in)       
#-----------------------------------------
# 
#-----------------------------------------
def to_posix(filepath):
    return pathlib.Path(filepath).as_posix()
 
#-----------------------------------------
# 
#-----------------------------------------
#https://pypi.org/project/art/ 
# https://github.com/sepandhaghighi/art/blob/master/FontList.ipynb
import art
def logo(text,  font="tarty2", vt=CYAN, npad=2, secs=2): # tarty3++ tarty7 sub-zero straight fancy133 fancy13 tarty2 
    nl = "\n"*npad
    print(nl + vt + art.text2art(text, font=font) + RESET + nl)
    time.sleep(secs)
    
def logo_filename(filename,  font="tarty2", vt=MAGENTA, npad=2): # tarty3 tarty7 sub-zero
    text = os.path.splitext(os.path.basename(filename))[0]
    logo(text,  font=font, vt=vt, npad=npad)
    
#-----------------------------------------
# 
#-----------------------------------------
# https://stackoverflow.com/questions/43864101/python-pil-check-if-image-is-transparent
def image_has_transparency(img):
    
    # # # if img.info.get("transparency", None) is not None:
    # # #     return True
    # # # if img.mode == "P":
    # # #     transparent = img.info.get("transparency", -1)
    # # #     for _, index in img.getcolors():
    # # #         if index == transparent:
    # # #             return True
    # # # elif img.mode == "RGBA":
    # # #     extrema = img.getextrema()
    # # #     if extrema[3][0] < 255:
    # # #         return True
    # # # return False

    # # def im_has_alpha(np_image):
    # #     '''
    # #     returns True for Image with alpha channel
    # #     '''
    # #     h,w,c = np_image.shape
    # #     return True if c ==4 else False
    
    # #     # # # https://stackoverflow.com/questions/51417774/how-to-determine-if-a-png-picture-has-a-transparency-layer-in-python
    # #     # # print("np_image.shape:", np_image.shape) # shapetuple of ints
    # #     # # nchannels = np_image.shape[2]
    # #     # # return nchannels in [2, 4]


    # # # import numpy as np
    # # # return im_has_alpha(np.array(img))
    
    # # https://pillow.readthedocs.io/en/stable/handbook/concepts.html
    # return img.mode in ["RGBA", "LA", "PA", "RGBa", "La"]
    
    #https://stackoverflow.com/questions/65615059/check-if-an-image-is-transparent-or-not
    
    alpha_range = img.convert('RGBA').getextrema()[-1]
    if alpha_range == (255,255):
        return False
    else:
        return True
 

def image_show(path, secs=1):
    path = os.path.normpath(path)
    #print("image_show:", path)
    assert os.path.isfile(path)
    
    import subprocess
    import time
    # https://www.etcwiki.org/wiki/IrfanView_Command_Line_Options
    p = subprocess.Popen(["C:/Program Files/IrfanView/i_view64.exe", path])
    time.sleep(secs)
    p.kill()
    
    # from PIL import Image
    # img = Image.open(path)
    # img.show()    
    

#-----------------------------------------
# https://codegolf.stackexchange.com/questions/187465/find-the-closest-three-digit-hex-colour
#-----------------------------------------
# lambda x:'#'+''.join(f"{(int(x[i:i+2],16)+8)//17:X}"for i in(1,3,5))
# lambda x:(f(x[:-2])if x[3:]else"#")+f'{(int(x[-2:],16)+8)//17:X}'
def color_hex6_to_hex3(hex6):
    f = lambda x:(f(x[:-2])if x[3:]else"#")+f'{(int(x[-2:],16)+8)//17:X}'
    return f(hex6)
    
#-----------------------------------------
# 
#-----------------------------------------
def format_dict(d, tab=""):
    klen = 0
    for key, value in d.items():
        klen = max(klen, len(key))
        
    s = ""
    s += tab + "{\n"
    indent = tab + "\t"
    for key, value in d.items():
        is_dict = (type(value) == dict)
        ss = "" + format_dict(value, tab=tab+'\t') if is_dict else value # \n
        key_rjust = key.rjust(klen, ' ')
        if is_dict:
            s += indent + f"{key_rjust}: {ss}" + '\n'
        else:
            s += indent + f"{key_rjust}: {ss}" + '\n'
    s += tab +"}"   
    return s
    

def log(*values, filepath, mode="a", echo=True):
    
    make_dirs(filepath)
    
    with open(filepath, mode=mode, encoding="utf-8") as fp:
        
        if not values or values == None:
            line = ''
        else:

            string = ' '.join(str(x) for x in values)
            string = string.strip()
            string = string.rstrip('\n') 
                    
            if '__file__' in string:
                import platform
                n   = len(string) + 1
                nls = 2
                lines = [
                    "\n" * nls,
                    "+" + "-" * n,
                    "|",
                    f"| {platform.node()}",
                    f"| {string}",
                    "|",
                    "+" + "-" * n,
                    "\n" * nls,
                ]
                line = '\n'.join(lines)

                print(line)
            else:
                date = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")
                line = f"{date}: {string}"
                if echo: print(line)
        
        fp.write(line + '\n')
    
#-----------------------------------------
# 
#-----------------------------------------

#-----------------------------------------
# 
#-----------------------------------------
if __name__ == "__main__":
    logo_filename(__file__)
    print("\n"*3 + "you started the wrong file..." + "\n"*3)
    
    d = {
        "ssss": 1,
        "2": 1,
        "123456789012345": "dsdsdsdsdsdsdsdsdsd",
        "sub" : {
            "ssss": 1,
            "2": 1,
            "123456789012345": "dsdsdsdsdsdsdsdsdsd",            
        }
    }
    
    
    print(format_dict(d))
    exit(0)
    
    # # # https://stackoverflow.com/questions/17388213/find-the-similarity-metric-between-two-strings
    # # import jellyfish
    # # a = "https://domain.com/has/just/forgotten/slash/"
    # # b = "https://domain.com/has/just/forgotten/slash"
    
    # # a = "https://domain.com/has/just/forgotten/slash/"
    # # b = "http://domain.com/has/just/forgotten/slash"
    
    # # a = "https://google.com"
    # # b = "https://apple.de/"
    
    # # print( jellyfish.levenshtein_distance(a, b) )
    # # print( jellyfish.jaro_distance(a, b) )
    # # print( jellyfish.damerau_levenshtein_distance(a, b) )
    # # print( jellyfish.jaro_winkler_similarity(a, b) )
    # # print( jellyfish.hamming_distance(a, b) )
    # # print( jellyfish.match_rating_comparison(a, b) )
    
    
    # #get_path_local_root_subdomains('', '')
    # #get_path_local_root_subdomains('/', '/')
    # get_path_local_root_subdomains('', 'karlsruhe.digital/')
    # get_path_local_root_subdomains('', 'https://karlsruhe.digital/')
    # #get_path_local_root_subdomains('karlsruhe.digital/', '')
    # #get_path_local_root_subdomains('https://karlsruhe.digital/', '')
    # get_path_local_root_subdomains('local/image.png', 'karlsruhe.digital/')
    # get_path_local_root_subdomains('/local/image.png', 'https://karlsruhe.digital/')
    # get_path_local_root_subdomains('karlsruhe.digital/local/image.png', 'https://karlsruhe.digital/')
    # get_path_local_root_subdomains('media.karlsruhe.digital/local/image.png', 'https://karlsruhe.digital/')


    # func = url_is_internal
    # # print(func("", ""))
    # # print(func("xxx", ""))
    # print(func("", "https://karlsruhe.digital/"))
    # print(func(".path", "https://karlsruhe.digital/"))
    # print(func("path", "https://karlsruhe.digital/"))
    # print(func("/path", "https://karlsruhe.digital/"))
    # print(func("/path/", "https://karlsruhe.digital/"))
    # print(func("index.html", "https://karlsruhe.digital/"))
    # print(func("karlsruhe.digital", "https://karlsruhe.digital/"))
    # print(func("karlsruhe.digital/index.html", "https://karlsruhe.digital/"))
    # print(func("karlsruhe.digital/index.html", "https://karlsruhe.digital/"))
    # print(func("karlsruhe.digital/index.html", "https://karlsruhe.digital/"))
    # print(func("media.karlsruhe.digital/index.html", "https://karlsruhe.digital/"))
    # print(func("media.karlsruhe.digital/folder/index.html", "https://karlsruhe.digital/"))
    # print(func("zkm.de", "https://karlsruhe.digital/"))
    
    # print(func("karlsruhe.de", "https://karlsruhe.digital/"))
    
    
    # sanitize_filepath_and_url("/wp-content/uploads/2019/08/Gründen.jpg")
    # sanitize_filepath_and_url("/wp-content/uploads/2019/08/Grü:nden.jpg")
    # sanitize_filepath_and_url("/wp-content/uploads/2019/08öäüÖÄÜß/Grü:nden.jpg")
    
    cases = {
        "#FF0000": "#F00",
        "#00FF00": "#0F0",
        "#D913C4": "#D1C",
        "#C0DD39": "#BD3",
        "#28A086": "#298",
        "#C0Cf6f": "#BC7",
        
        "FF0000": "#F00",
        "00FF00": "#0F0",
        "D913C4": "#D1C",
        "C0DD39": "#BD3",
        "28A086": "#298",
        "C0Cf6f": "#BC7",
    }

    for case, expected in cases.items():
        actual = color_hex6_to_hex3(case)
        print(f"{'-+'[expected==actual]} {case}: expected {expected}, got {actual}")
    
    """
    + #FF0000: expected #F00, got #F00
    + #00FF00: expected #0F0, got #0F0
    + #D913C4: expected #D1C, got #D1C
    + #C0DD39: expected #BD3, got #BD3
    + #28A086: expected #298, got #298
    + #C0Cf6f: expected #BC7, got #BC7
    
    + FF0000: expected #F00, got #F00 
    + 00FF00: expected #0F0, got #0F0 
    + D913C4: expected #D1C, got #D1C 
    + C0DD39: expected #BD3, got #BD3 
    + 28A086: expected #298, got #298 
    + C0Cf6f: expected #BC7, got #BC7
    """
    
    
    aart = """
<pre id="hero-aart" style="font-size: 1em; line-height:1em; background-color: #000000; font-weight: bold; padding: 4px 5px; --fs: 9px;"><b style="color:#080A14">1</b><b style="color:#080912">0</b><b style="color:#080910">1</b><b style="color:#08080F">0</b><b style="color:#090810">1</b><b style="color:#09080F">0</b><b style="color:#090810">0</b><b style="color:#090911">1</b><b style="color:#090A11">1</b><b style="color:#090B13">0</b><b style="color:#0A0C18">1</b><b style="color:#0B0F22">1</b><b style="color:#0A0D1E">0</b><b style="color:#090B18">1</b><b style="color:#0A0C1B">1</b><b style="color:#0B1024">0</b><b style="color:#0B0E1C">0</b><b style="color:#0A0C16">101</b><b style="color:#0B0D18">1</b><b style="color:#0C0D1D">1</b><b style="color:#0C132A">1</b><b style="color:#0C1936">0</b><b style="color:#0C1328">0</b><b style="color:#0D0F1F">0</b><b style="color:#0E0F1F">0</b><b style="color:#0D0F1D">0</b><b style="color:#0D0F1A">0</b><b style="color:#0D0F19">001</b><b style="color:#0C111F">0</b><b style="color:#0C1529">1</b><b style="color:#0C1425">0</b><b style="color:#0D121E">1</b><b style="color:#0D111E">0</b><b style="color:#0D111D">0</b><b style="color:#0E121E">0</b><b style="color:#0E131E">11</b><b style="color:#0F131F">1</b><b style="color:#0F1320">1</b><b style="color:#0D1523">1</b><b style="color:#0C192D">0</b><b style="color:#0C1A2F">0</b><b style="color:#0C1726">0</b><b style="color:#0C1725">10</b><b style="color:#0C1826">1</b><b style="color:#0C1928">1</b><b style="color:#0D1D31">01</b><b style="color:#0E1A2B">0</b><b style="color:#0D1A2A">1</b><b style="color:#0D1B2A">0</b><b style="color:#0D1B2B">0</b><b style="color:#0D1C2B">1</b><b style="color:#0C1D2C">0</b><b style="color:#0C1D2D">0</b><b style="color:#0D1F30">0</b><b style="color:#0D2033">1</b><b style="color:#0C2339">0</b><b style="color:#0C243C">1</b><b style="color:#0C2439">1</b><b style="color:#0C2840">0</b><b style="color:#0C314E">0</b><b style="color:#0C314B">0</b><b style="color:#0C3048">0</b><b style="color:#0C2D44">10</b><b style="color:#0C2E44">0</b><b style="color:#0C2D44">1</b><b style="color:#0C2C42">1</b><b style="color:#0C2D45">0</b><b style="color:#0C314E">1</b><b style="color:#0C314F">1</b><b style="color:#0C2D48">1</b><b style="color:#0C2B43">0</b><b style="color:#0C2C45">1</b><b style="color:#0C2A41">0</b><b style="color:#0C283D">0</b><b style="color:#0C273B">00</b><b style="color:#0C2639">1</b><b style="color:#0C2538">1</b><b style="color:#0C2539">0</b><b style="color:#0C2337">0</b><b style="color:#0C2438">1</b><b style="color:#0C243A">1</b><b style="color:#0C2641">1</b><b style="color:#0C253F">0</b><b style="color:#0C2138">1</b><b style="color:#0C2238">1</b><b style="color:#0C233C">1</b><b style="color:#0B2038">1</b><b style="color:#0C233E">1</b><b style="color:#0B213B">1</b><b style="color:#0B223D">1</b><b style="color:#0C213C">1</b><b style="color:#0C203A">1</b><b style="color:#0A1C35">0</b><b style="color:#0B1E37">1</b><b style="color:#0B1B32">0</b><b style="color:#0A1A2E">0</b><b style="color:#0A1B32">1</b><b style="color:#0B1E39">1</b><b style="color:#0A203D">0</b><b style="color:#0A2240">1</b><b style="color:#0A1E39">0</b><b style="color:#0A1A30">0</b><b style="color:#0A192F">1</b><b style="color:#0A1B34">0</b><b style="color:#091A32">0</b><b style="color:#081D37">1</b><b style="color:#091C35">1</b><b style="color:#09182D">0</b><b style="color:#091B33">1</b><b style="color:#0A1D38">0</b><b style="color:#09192D">0</b><b style="color:#091829">11</b><b style="color:#091727">0</b><b style="color:#081523">0</b><b style="color:#091321">0</b>
<b style="color:#080911">0</b><b style="color:#080A14">1</b><b style="color:#080912">1</b><b style="color:#090910">0</b><b style="color:#090810">0</b><b style="color:#0A080F">00</b><b style="color:#0A0910">1</b><b style="color:#090A11">0</b><b style="color:#090A12">0</b><b style="color:#090B14">0</b><b style="color:#0A0D1B">0</b><b style="color:#0A1023">1</b><b style="color:#0A0D1C">0</b><b style="color:#0B0C19">1</b><b style="color:#0B0E1F">1</b><b style="color:#0C1124">1</b><b style="color:#0B0D1A">1</b><b style="color:#0B0C16">1</b><b style="color:#0B0D16">0</b><b style="color:#0B0D17">1</b><b style="color:#0C0E1B">0</b><b style="color:#0C0F21">0</b><b style="color:#0C1732">1</b><b style="color:#0E1834">1</b><b style="color:#0D1123">0</b><b style="color:#0E0F1E">1</b><b style="color:#0E0F1F">0</b><b style="color:#0D0F1D">0</b><b style="color:#0D0F1A">1</b><b style="color:#0D0F18">0</b><b style="color:#0D101A">0</b><b style="color:#0C111D">0</b><b style="color:#0D1324">1</b><b style="color:#0C172B">0</b><b style="color:#0D1323">1</b><b style="color:#0E111F">0</b><b style="color:#0E121E">0</b><b style="color:#0E131E">1</b><b style="color:#0F131E">0</b><b style="color:#0F131F">10</b><b style="color:#0E1420">0</b><b style="color:#0C1524">1</b><b style="color:#0C182B">1</b><b style="color:#0D1C32">1</b><b style="color:#0D1827">1</b><b style="color:#0C1826">00</b><b style="color:#0C1928">1</b><b style="color:#0D1A2B">1</b><b style="color:#0D1E31">0</b><b style="color:#0D1F34">0</b><b style="color:#0D1C2D">1</b><b style="color:#0C1C2D">1</b><b style="color:#0C1D2D">1</b><b style="color:#0D1D2D">1</b><b style="color:#0D1E2E">1</b><b style="color:#0D1F2F">1</b><b style="color:#0D2030">1</b><b style="color:#0C2133">1</b><b style="color:#0C2236">0</b><b style="color:#0C263D">0</b><b style="color:#0C2943">0</b><b style="color:#0B283F">0</b><b style="color:#0C2B44">0</b><b style="color:#0C2E4A">1</b><b style="color:#0C314C">0</b><b style="color:#0C344E">1</b><b style="color:#0C354F">0</b><b style="color:#0C344D">10</b><b style="color:#0C344E">0</b><b style="color:#0B344F">0</b><b style="color:#0B3551">1</b><b style="color:#0C395A">0</b><b style="color:#0C3859">0</b><b style="color:#0B3450">1</b><b style="color:#0C324D">1</b><b style="color:#0C334E">0</b><b style="color:#0B324C">0</b><b style="color:#0C3049">0</b><b style="color:#0C2F48">1</b><b style="color:#0C2E47">1</b><b style="color:#0C2E46">1</b><b style="color:#0B2E45">0</b><b style="color:#0B2D45">10</b><b style="color:#0B2C44">1</b><b style="color:#0C2E49">1</b><b style="color:#0C2F4C">1</b><b style="color:#0B2E49">1</b><b style="color:#0C2B45">1</b><b style="color:#0C2C47">0</b><b style="color:#0B2B46">00</b><b style="color:#0C2D4B">0</b><b style="color:#0B2A46">1</b><b style="color:#0B2C4B">1</b><b style="color:#0C2C4B">0</b><b style="color:#0B2945">1</b><b style="color:#0B2743">0</b><b style="color:#0B2742">1</b><b style="color:#0A233B">1</b><b style="color:#0B233C">0</b><b style="color:#09243F">0</b><b style="color:#0A2848">1</b><b style="color:#0B2B4E">1</b><b style="color:#0A2847">0</b><b style="color:#09243E">0</b><b style="color:#092238">1</b><b style="color:#092239">0</b><b style="color:#09243F">0</b><b style="color:#082542">1</b><b style="color:#082644">1</b><b style="color:#08223C">0</b><b style="color:#09223B">1</b><b style="color:#0A2542">0</b><b style="color:#09223B">1</b><b style="color:#091F33">1</b><b style="color:#0A1F33">0</b><b style="color:#091E32">1</b><b style="color:#091C2C">1</b><b style="color:#081A2A">0</b><b style="color:#081929">1</b>
<b style="color:#080810">1</b><b style="color:#090912">0</b><b style="color:#090B15">0</b><b style="color:#090A13">1</b><b style="color:#090911">1</b><b style="color:#0A0910">0</b><b style="color:#0A090F">1</b><b style="color:#0A0910">0</b><b style="color:#0A0A10">1</b><b style="color:#0A0A12">0</b><b style="color:#0A0B13">0</b><b style="color:#0A0B16">0</b><b style="color:#0A0E1E">0</b><b style="color:#0B1124">0</b><b style="color:#0B0D1C">1</b><b style="color:#0B0D1B">1</b><b style="color:#0C1124">0</b><b style="color:#0C1022">1</b><b style="color:#0C0D19">1</b><b style="color:#0B0D17">1</b><b style="color:#0C0D17">1</b><b style="color:#0C0E19">1</b><b style="color:#0D0E1D">1</b><b style="color:#0C1226">1</b><b style="color:#0E1B39">1</b><b style="color:#0D172E">0</b><b style="color:#0D1020">0</b><b style="color:#0E101F">1</b><b style="color:#0E1020">1</b><b style="color:#0D0F1C">0</b><b style="color:#0D0F1A">0</b><b style="color:#0D111B">1</b><b style="color:#0D111D">1</b><b style="color:#0E121F">0</b><b style="color:#0D1627">0</b><b style="color:#0D172B">0</b><b style="color:#0D1422">0</b><b style="color:#0E1321">0</b><b style="color:#0F131F">101</b><b style="color:#0E1421">1</b><b style="color:#0D1522">0</b><b style="color:#0D1624">0</b><b style="color:#0C1829">1</b><b style="color:#0D1D34">0</b><b style="color:#0C192B">1</b><b style="color:#0D1927">1</b><b style="color:#0D1928">1</b><b style="color:#0E1A29">0</b><b style="color:#0D1B2C">0</b><b style="color:#0D1F32">1</b><b style="color:#0D2137">0</b><b style="color:#0D1E30">0</b><b style="color:#0D1F2F">10</b><b style="color:#0D1F30">0</b><b style="color:#0C2030">1</b><b style="color:#0C2132">0</b><b style="color:#0C2234">1</b><b style="color:#0C2236">1</b><b style="color:#0C2437">1</b><b style="color:#0B283F">0</b><b style="color:#0D2B45">0</b><b style="color:#0C2B45">0</b><b style="color:#0C2C46">0</b><b style="color:#0C314E">0</b><b style="color:#0B2F49">0</b><b style="color:#0B3048">0</b><b style="color:#0B344E">1</b><b style="color:#0B3853">1</b><b style="color:#0B3953">00</b><b style="color:#0B3954">0</b><b style="color:#0B3A59">0</b><b style="color:#0B3E62">1</b><b style="color:#0B3C5E">1</b><b style="color:#0B3956">0</b><b style="color:#0B3853">0</b><b style="color:#0B3855">1</b><b style="color:#0B3854">1</b><b style="color:#0B354F">1</b><b style="color:#0C344D">1</b><b style="color:#0B334D">1</b><b style="color:#0B334C">0</b><b style="color:#0B324B">1</b><b style="color:#0B314B">1</b><b style="color:#0B314A">01</b><b style="color:#0B334F">1</b><b style="color:#0C3453">1</b><b style="color:#0B314D">0</b><b style="color:#0B314C">1</b><b style="color:#0C304E">1</b><b style="color:#0B2F4C">1</b><b style="color:#0B304F">0</b><b style="color:#0B304E">1</b><b style="color:#0B2E4B">0</b><b style="color:#0C3153">0</b><b style="color:#0C2F4F">1</b><b style="color:#0C2C4A">0</b><b style="color:#0C2A48">1</b><b style="color:#0B2842">0</b><b style="color:#0A2640">0</b><b style="color:#0A2742">1</b><b style="color:#0A2844">1</b><b style="color:#0C2F52">1</b><b style="color:#0B2E51">1</b><b style="color:#0A2946">0</b><b style="color:#09253E">1</b><b style="color:#09243B">1</b><b style="color:#09253E">1</b><b style="color:#092946">0</b><b style="color:#092B4D">1</b><b style="color:#092844">0</b><b style="color:#082540">1</b><b style="color:#0A2948">1</b><b style="color:#092642">1</b><b style="color:#092339">01</b><b style="color:#092237">0</b><b style="color:#0A1F32">0</b><b style="color:#091E2F">0</b><b style="color:#091D2E">0</b><b style="color:#091C2C">1</b>
<b style="color:#08080E">0</b><b style="color:#09080F">1</b><b style="color:#090A12">1</b><b style="color:#090B16">1</b><b style="color:#090A14">1</b><b style="color:#090A11">1</b><b style="color:#0A0910">10</b><b style="color:#0B0911">0</b><b style="color:#0A0911">0</b><b style="color:#0A0A13">1</b><b style="color:#0B0B14">1</b><b style="color:#0A0C16">0</b><b style="color:#0B0F21">1</b><b style="color:#0C1124">0</b><b style="color:#0D0E1D">0</b><b style="color:#0C0E1E">0</b><b style="color:#0C1328">0</b><b style="color:#0D0F1E">1</b><b style="color:#0C0E18">0</b><b style="color:#0C0D17">0</b><b style="color:#0C0E18">1</b><b style="color:#0D0E1A">1</b><b style="color:#0D0F1F">0</b><b style="color:#0D172F">1</b><b style="color:#0F1D3A">0</b><b style="color:#0D1427">1</b><b style="color:#0D1020">1</b><b style="color:#0E1120">0</b><b style="color:#0F1020">0</b><b style="color:#0D101C">0</b><b style="color:#0D111C">1</b><b style="color:#0E111C">1</b><b style="color:#0E121F">1</b><b style="color:#0E1322">1</b><b style="color:#0D172B">1</b><b style="color:#0D1729">1</b><b style="color:#0E1521">0</b><b style="color:#0E1420">1</b><b style="color:#0E1421">0</b><b style="color:#0D1522">0</b><b style="color:#0D1523">0</b><b style="color:#0D1623">0</b><b style="color:#0D1724">0</b><b style="color:#0C1928">0</b><b style="color:#0D1E35">1</b><b style="color:#0D1D30">1</b><b style="color:#0E1B2A">0</b><b style="color:#0E1A2A">0</b><b style="color:#0E1B2B">1</b><b style="color:#0D1D2D">0</b><b style="color:#0D1F33">0</b><b style="color:#0E223A">0</b><b style="color:#0D2033">1</b><b style="color:#0D2030">1</b><b style="color:#0D2031">1</b><b style="color:#0C2131">0</b><b style="color:#0C2234">1</b><b style="color:#0D2235">0</b><b style="color:#0D2336">1</b><b style="color:#0D2437">1</b><b style="color:#0C273B">0</b><b style="color:#0B2940">1</b><b style="color:#0D2C47">1</b><b style="color:#0C2D48">1</b><b style="color:#0B2F48">1</b><b style="color:#0B3351">1</b><b style="color:#0B324D">0</b><b style="color:#0A3148">0</b><b style="color:#0B3048">0</b><b style="color:#0B344C">0</b><b style="color:#0B3953">1</b><b style="color:#0B3C58">0</b><b style="color:#0B3D59">1</b><b style="color:#0B3E5E">1</b><b style="color:#0B4266">1</b><b style="color:#0B3F61">1</b><b style="color:#0B3D5B">0</b><b style="color:#0B3C59">1</b><b style="color:#0B3D5B">0</b><b style="color:#0B3D5C">1</b><b style="color:#0B3B56">1</b><b style="color:#0B3A54">1</b><b style="color:#0B3953">0</b><b style="color:#0B3852">1</b><b style="color:#0B3851">0</b><b style="color:#0B3750">0</b><b style="color:#0C3651">0</b><b style="color:#0B3752">0</b><b style="color:#0B3858">1</b><b style="color:#0C395A">0</b><b style="color:#0B3656">1</b><b style="color:#0A3654">0</b><b style="color:#0B3757">1</b><b style="color:#0B3454">1</b><b style="color:#0C3759">0</b><b style="color:#0B3453">1</b><b style="color:#0B3454">0</b><b style="color:#0C375B">0</b><b style="color:#0B3455">1</b><b style="color:#0B3252">0</b><b style="color:#0B2D49">1</b><b style="color:#0B2C46">0</b><b style="color:#0A2B45">0</b><b style="color:#0A2C49">1</b><b style="color:#0A2F50">1</b><b style="color:#0C355A">0</b><b style="color:#0A3051">0</b><b style="color:#0A2A46">0</b><b style="color:#0A2741">1</b><b style="color:#0A2740">0</b><b style="color:#092842">1</b><b style="color:#092E50">0</b><b style="color:#092D4E">1</b><b style="color:#0A2843">0</b><b style="color:#0A2B49">1</b><b style="color:#0A2A48">0</b><b style="color:#09253E">1</b><b style="color:#09253C">1</b><b style="color:#09253B">0</b><b style="color:#082336">1</b><b style="color:#0A2133">0</b><b style="color:#0A1F32">0</b><b style="color:#091E31">11</b>
<b style="color:#09090F">0</b><b style="color:#0A080F">0</b><b style="color:#0A0910">0</b><b style="color:#090A13">1</b><b style="color:#0A0B18">1</b><b style="color:#0A0B15">1</b><b style="color:#0A0912">0</b><b style="color:#0B0910">01</b><b style="color:#0B0A10">0</b><b style="color:#0B0A12">1</b><b style="color:#0B0B13">1</b><b style="color:#0B0C13">1</b><b style="color:#0C0D18">0</b><b style="color:#0C1123">0</b><b style="color:#0C1224">0</b><b style="color:#0C0D1D">0</b><b style="color:#0D1023">1</b><b style="color:#0D1327">1</b><b style="color:#0D0F1B">0</b><b style="color:#0C0E17">11</b><b style="color:#0C0F19">0</b><b style="color:#0D0F1C">1</b><b style="color:#0D1223">0</b><b style="color:#0F1C38">1</b><b style="color:#0F1B35">1</b><b style="color:#0E1223">1</b><b style="color:#0F1020">0</b><b style="color:#0F1323">0</b><b style="color:#0E1320">0</b><b style="color:#0E111D">00</b><b style="color:#0E121E">0</b><b style="color:#0F1221">0</b><b style="color:#0E1424">1</b><b style="color:#0E192E">0</b><b style="color:#0E1727">1</b><b style="color:#0E1422">0</b><b style="color:#0D1522">1</b><b style="color:#0D1623">0</b><b style="color:#0E1623">1</b><b style="color:#0E1724">0</b><b style="color:#0D1724">1</b><b style="color:#0D1928">0</b><b style="color:#0D1D34">1</b><b style="color:#0E1E35">1</b><b style="color:#0E1B2C">0</b><b style="color:#0E1B2B">0</b><b style="color:#0E1C2C">1</b><b style="color:#0D1D2E">0</b><b style="color:#0D2034">1</b><b style="color:#0D243C">0</b><b style="color:#0D2135">1</b><b style="color:#0D2133">1</b><b style="color:#0C2133">0</b><b style="color:#0C2234">1</b><b style="color:#0C2235">0</b><b style="color:#0D2336">0</b><b style="color:#0C2436">0</b><b style="color:#0C2739">1</b><b style="color:#0C283B">0</b><b style="color:#0C2A40">1</b><b style="color:#0C2C47">0</b><b style="color:#0C2F4A">1</b><b style="color:#0B2F49">1</b><b style="color:#0C3352">0</b><b style="color:#0B324F">0</b><b style="color:#0B3048">01</b><b style="color:#0B3047">0</b><b style="color:#0B3148">1</b><b style="color:#0B344D">0</b><b style="color:#0B3A56">0</b><b style="color:#0B4061">0</b><b style="color:#0C4368">0</b><b style="color:#0B3F60">0</b><b style="color:#0B3E5B">0</b><b style="color:#0B3D5A">0</b><b style="color:#0B3E5C">1</b><b style="color:#0B3F5F">1</b><b style="color:#0B3C58">1</b><b style="color:#0B3C57">00</b><b style="color:#0B3B57">1</b><b style="color:#0B3B56">00</b><b style="color:#0B3A57">0</b><b style="color:#0B3B58">1</b><b style="color:#0B3D5F">01</b><b style="color:#0C395A">1</b><b style="color:#0B3A5C">1</b><b style="color:#0B3A5B">1</b><b style="color:#0B3A5C">1</b><b style="color:#0C3B5D">0</b><b style="color:#0B3859">1</b><b style="color:#0C3A5D">1</b><b style="color:#0C3A5E">1</b><b style="color:#0C385C">0</b><b style="color:#0B3352">1</b><b style="color:#0A314B">0</b><b style="color:#0A304A">0</b><b style="color:#0A304C">0</b><b style="color:#0A3252">0</b><b style="color:#0B365A">1</b><b style="color:#0B375C">0</b><b style="color:#0A3150">1</b><b style="color:#0A2C45">1</b><b style="color:#0B2B44">0</b><b style="color:#0A2942">0</b><b style="color:#0A2D4A">0</b><b style="color:#093256">1</b><b style="color:#092C4A">1</b><b style="color:#0A2C4B">1</b><b style="color:#0A2C4C">0</b><b style="color:#0A2842">1</b><b style="color:#0A263F">0</b><b style="color:#0A263E">1</b><b style="color:#092438">1</b><b style="color:#0A2134">1</b><b style="color:#0A2032">1</b><b style="color:#0A1F32">1</b><b style="color:#0A1E31">0</b><b style="color:#091E30">0</b>
<b style="color:#0A090F">010</b><b style="color:#0A0911">0</b><b style="color:#0A0A13">0</b><b style="color:#0A0C19">1</b><b style="color:#0A0B15">0</b><b style="color:#0B0A12">1</b><b style="color:#0B0A11">11</b><b style="color:#0C0B11">0</b><b style="color:#0C0B13">1</b><b style="color:#0B0B13">0</b><b style="color:#0C0C15">0</b><b style="color:#0C0E1B">1</b><b style="color:#0C1326">0</b><b style="color:#0D1123">0</b><b style="color:#0D0E1D">0</b><b style="color:#0D1328">0</b><b style="color:#0D1223">0</b><b style="color:#0D0F19">0</b><b style="color:#0D0E18">1</b><b style="color:#0E0F18">0</b><b style="color:#0D0F1A">1</b><b style="color:#0E101F">0</b><b style="color:#0E152A">0</b><b style="color:#111F3D">1</b><b style="color:#0F172D">1</b><b style="color:#0E1222">1</b><b style="color:#0D1423">0</b><b style="color:#0E1423">0</b><b style="color:#0E121F">1</b><b style="color:#0E121D">1</b><b style="color:#0F131E">1</b><b style="color:#0F131F">0</b><b style="color:#0F1321">0</b><b style="color:#0E1727">0</b><b style="color:#0E1A2F">0</b><b style="color:#0E1625">0</b><b style="color:#0E1522">1</b><b style="color:#0D1622">0</b><b style="color:#0D1623">1</b><b style="color:#0E1724">01</b><b style="color:#0D1826">1</b><b style="color:#0E1B2F">0</b><b style="color:#0E1F37">1</b><b style="color:#0E1B2C">1</b><b style="color:#0E1B2A">0</b><b style="color:#0E1B2B">1</b><b style="color:#0D1D2D">1</b><b style="color:#0D1F32">1</b><b style="color:#0E233B">0</b><b style="color:#0E2136">0</b><b style="color:#0D1F31">0</b><b style="color:#0D2131">0</b><b style="color:#0C2232">1</b><b style="color:#0C2234">0</b><b style="color:#0D2235">0</b><b style="color:#0D2336">0</b><b style="color:#0C2537">0</b><b style="color:#0C273A">0</b><b style="color:#0C293D">0</b><b style="color:#0C2B43">0</b><b style="color:#0D2D48">0</b><b style="color:#0C2C46">0</b><b style="color:#0C314E">1</b><b style="color:#0C314C">1</b><b style="color:#0C2E46">1</b><b style="color:#0C2D46">1</b><b style="color:#0B2E46">1</b><b style="color:#0B2E47">1</b><b style="color:#0B2F47">0</b><b style="color:#0B314A">0</b><b style="color:#0C3958">1</b><b style="color:#0C4064">1</b><b style="color:#0B3E5E">0</b><b style="color:#0B3D5A">0</b><b style="color:#0B3B58">0</b><b style="color:#0B3C59">1</b><b style="color:#0B3D5D">0</b><b style="color:#0B3B57">1</b><b style="color:#0C3B55">0</b><b style="color:#0B3B55">11</b><b style="color:#0B3B56">1</b><b style="color:#0B3B57">10</b><b style="color:#0C3B5A">0</b><b style="color:#0C3E61">1</b><b style="color:#0B3C5E">1</b><b style="color:#0C3A5A">0</b><b style="color:#0C3B5D">0</b><b style="color:#0B3A5B">1</b><b style="color:#0C3C5F">1</b><b style="color:#0B3A5B">0</b><b style="color:#0C395B">0</b><b style="color:#0C3A5E">0</b><b style="color:#0C3A5F">1</b><b style="color:#0C3759">0</b><b style="color:#0B334F">0</b><b style="color:#0B314B">1</b><b style="color:#0A304D">1</b><b style="color:#0A314F">0</b><b style="color:#0B3658">1</b><b style="color:#0C385D">1</b><b style="color:#0B3559">0</b><b style="color:#0A314F">1</b><b style="color:#0A2D47">1</b><b style="color:#0A2E46">1</b><b style="color:#092D48">0</b><b style="color:#0A3355">0</b><b style="color:#0A3257">1</b><b style="color:#0A3051">0</b><b style="color:#0A3052">0</b><b style="color:#0A2C47">0</b><b style="color:#0A2943">11</b><b style="color:#09273D">0</b><b style="color:#092538">0</b><b style="color:#092436">0</b><b style="color:#0A2234">1</b><b style="color:#092133">0</b><b style="color:#092135">1</b><b style="color:#09233A">0</b>
<b style="color:#0A080F">1</b><b style="color:#0A090F">00</b><b style="color:#0A0910">1</b><b style="color:#0A0911">0</b><b style="color:#0A0B14">1</b><b style="color:#0B0D1A">1</b><b style="color:#0B0C16">1</b><b style="color:#0B0A12">1</b><b style="color:#0C0A12">1</b><b style="color:#0C0B12">00</b><b style="color:#0C0B13">0</b><b style="color:#0C0C14">1</b><b style="color:#0C0D16">0</b><b style="color:#0D0F1D">0</b><b style="color:#0C1429">1</b><b style="color:#0D1122">1</b><b style="color:#0D1020">1</b><b style="color:#0E152B">0</b><b style="color:#0E101F">1</b><b style="color:#0D0F19">1</b><b style="color:#0E0F18">0</b><b style="color:#0E0E18">0</b><b style="color:#0E0F1C">0</b><b style="color:#0F1122">1</b><b style="color:#0F1A34">0</b><b style="color:#11203D">0</b><b style="color:#0E1528">0</b><b style="color:#0E1322">0</b><b style="color:#0E1523">0</b><b style="color:#0F1423">0</b><b style="color:#0F121E">1</b><b style="color:#0F131D">1</b><b style="color:#0F131E">1</b><b style="color:#0F1320">0</b><b style="color:#0F1422">1</b><b style="color:#0E182B">1</b><b style="color:#0F192E">1</b><b style="color:#0F1624">1</b><b style="color:#0E1622">0</b><b style="color:#0D1622">0</b><b style="color:#0E1623">1</b><b style="color:#0F1724">1</b><b style="color:#0D1725">1</b><b style="color:#0D1A2B">0</b><b style="color:#0E1F38">1</b><b style="color:#0E1C2E">0</b><b style="color:#0F1B2A">01</b><b style="color:#0E1C2C">0</b><b style="color:#0D1E30">0</b><b style="color:#0E223A">1</b><b style="color:#0E2136">0</b><b style="color:#0E1F30">0</b><b style="color:#0D2030">0</b><b style="color:#0D2130">1</b><b style="color:#0C2232">0</b><b style="color:#0D2233">1</b><b style="color:#0D2335">1</b><b style="color:#0E2436">0</b><b style="color:#0D2538">0</b><b style="color:#0C273B">1</b><b style="color:#0B293F">0</b><b style="color:#0E2C47">0</b><b style="color:#0D2B46">1</b><b style="color:#0D2F4B">0</b><b style="color:#0D304B">0</b><b style="color:#0D2B45">0</b><b style="color:#0D2B43">1</b><b style="color:#0D2C43">1</b><b style="color:#0D2C44">1</b><b style="color:#0C2D46">0</b><b style="color:#0B2F48">1</b><b style="color:#0C3555">0</b><b style="color:#0C3658">0</b><b style="color:#0B3651">1</b><b style="color:#0B3A55">1</b><b style="color:#0C3B56">0</b><b style="color:#0B3B57">0</b><b style="color:#0C3C5C">1</b><b style="color:#0C3B56">0</b><b style="color:#0C3A54">1110</b><b style="color:#0B3A55">0</b><b style="color:#0B3A56">1</b><b style="color:#0C3B5B">0</b><b style="color:#0C3E61">1</b><b style="color:#0C3C5D">0</b><b style="color:#0B3A5B">0</b><b style="color:#0C3C5D">0</b><b style="color:#0C3B5C">0</b><b style="color:#0C3D5F">1</b><b style="color:#0C395B">1</b><b style="color:#0D3B5F">1</b><b style="color:#0D395D">0</b><b style="color:#0C3A5E">1</b><b style="color:#0C3555">0</b><b style="color:#0B314C">1</b><b style="color:#0B324D">1</b><b style="color:#0B324F">1</b><b style="color:#0B3456">0</b><b style="color:#0C3A5F">0</b><b style="color:#0C375A">0</b><b style="color:#0C3456">1</b><b style="color:#0A314F">0</b><b style="color:#0A2F49">00</b><b style="color:#0A3352">1</b><b style="color:#0A3559">0</b><b style="color:#0B3559">00</b><b style="color:#0B314F">1</b><b style="color:#0A2D47">0</b><b style="color:#0A2E49">1</b><b style="color:#0B2A43">1</b><b style="color:#0A293E">0</b><b style="color:#09293D">1</b><b style="color:#09273A">1</b><b style="color:#09263A">0</b><b style="color:#09263B">1</b><b style="color:#092741">11</b>
<b style="color:#0A090F">1</b><b style="color:#0A080F">1</b><b style="color:#0A090F">10</b><b style="color:#0B0910">1</b><b style="color:#0A0911">0</b><b style="color:#0B0B14">0</b><b style="color:#0B0D1B">0</b><b style="color:#0B0C16">0</b><b style="color:#0C0B13">1</b><b style="color:#0C0B12">0</b><b style="color:#0C0B13">1</b><b style="color:#0D0B12">1</b><b style="color:#0C0B13">1</b><b style="color:#0C0C15">0</b><b style="color:#0C0E18">0</b><b style="color:#0D1120">1</b><b style="color:#0D152B">1</b><b style="color:#0E1021">1</b><b style="color:#0E1226">1</b><b style="color:#0E152A">0</b><b style="color:#0E0F1C">0</b><b style="color:#0D0F19">1</b><b style="color:#0E0E19">1</b><b style="color:#0E0F1B">1</b><b style="color:#0F101F">0</b><b style="color:#0E1427">1</b><b style="color:#11213E">0</b><b style="color:#101D36">0</b><b style="color:#0E1424">1</b><b style="color:#0E1322">0</b><b style="color:#0E1526">1</b><b style="color:#0F1322">1</b><b style="color:#0F121F">1</b><b style="color:#0F131E">1</b><b style="color:#0F131F">0</b><b style="color:#101320">1</b><b style="color:#0E1523">1</b><b style="color:#0F1A2F">0</b><b style="color:#0E182B">1</b><b style="color:#0E1623">0</b><b style="color:#0E1622">1</b><b style="color:#0E1623">1</b><b style="color:#0E1724">11</b><b style="color:#0D1928">0</b><b style="color:#0E1F37">1</b><b style="color:#0E1C30">0</b><b style="color:#0F1A2A">0</b><b style="color:#0E1B2A">1</b><b style="color:#0E1B2B">1</b><b style="color:#0D1D2E">0</b><b style="color:#0E2239">1</b><b style="color:#0F2137">0</b><b style="color:#0E1F31">1</b><b style="color:#0E1F2F">1</b><b style="color:#0D2030">1</b><b style="color:#0D2131">1</b><b style="color:#0D2232">1</b><b style="color:#0D2334">0</b><b style="color:#0D2335">0</b><b style="color:#0E2436">1</b><b style="color:#0E2638">0</b><b style="color:#0D273D">1</b><b style="color:#0D2B45">0</b><b style="color:#0D2B46">1</b><b style="color:#0D2D48">1</b><b style="color:#0E2E4B">0</b><b style="color:#0D2B43">1</b><b style="color:#0C2B40">10</b><b style="color:#0D2B41">1</b><b style="color:#0D2B44">0</b><b style="color:#0C2E47">1</b><b style="color:#0D3556">0</b><b style="color:#0D3453">1</b><b style="color:#0C2F47">1</b><b style="color:#0D3048">0</b><b style="color:#0D364F">1</b><b style="color:#0C3A56">1</b><b style="color:#0C3C5B">0</b><b style="color:#0C3A56">1</b><b style="color:#0D3954">0</b><b style="color:#0D3953">10</b><b style="color:#0D3954">0</b><b style="color:#0C3A54">1</b><b style="color:#0C3A55">1</b><b style="color:#0C3C5C">1</b><b style="color:#0D3F62">0</b><b style="color:#0D3B5C">1</b><b style="color:#0C3C5D">0</b><b style="color:#0D3C5E">0</b><b style="color:#0D3D60">0</b><b style="color:#0D3C5E">1</b><b style="color:#0D3C5F">1</b><b style="color:#0E3C60">0</b><b style="color:#0D395D">0</b><b style="color:#0D3759">0</b><b style="color:#0C3553">1</b><b style="color:#0C324E">0</b><b style="color:#0B324E">1</b><b style="color:#0C3455">1</b><b style="color:#0D395E">0</b><b style="color:#0D3B60">1</b><b style="color:#0B3557">0</b><b style="color:#0C3556">0</b><b style="color:#0B3351">1</b><b style="color:#0A314C">0</b><b style="color:#0A3352">0</b><b style="color:#0A385C">1</b><b style="color:#0A3557">1</b><b style="color:#0D3B61">0</b><b style="color:#0B3658">0</b><b style="color:#0A324E">0</b><b style="color:#0B314D">0</b><b style="color:#0B2F49">1</b><b style="color:#0C2B44">0</b><b style="color:#0C2B43">1</b><b style="color:#0B2A40">01</b><b style="color:#0A2A42">1</b><b style="color:#0A2C49">0</b><b style="color:#0A2B46">0</b><b style="color:#09273C">1</b>
<b style="color:#0A090F">0</b><b style="color:#09080F">0</b><b style="color:#0A090F">1</b><b style="color:#0A0910">0</b><b style="color:#0B0910">1</b><b style="color:#0B0A10">1</b><b style="color:#0B0A11">0</b><b style="color:#0B0B14">1</b><b style="color:#0C0D1B">1</b><b style="color:#0C0D17">1</b><b style="color:#0C0B13">1</b><b style="color:#0C0B12">0</b><b style="color:#0D0B13">0</b><b style="color:#0D0B14">1</b><b style="color:#0D0C14">0</b><b style="color:#0D0D15">0</b><b style="color:#0D0E19">1</b><b style="color:#0D1224">1</b><b style="color:#0E162B">1</b><b style="color:#0E1122">1</b><b style="color:#0F162C">1</b><b style="color:#0E1325">1</b><b style="color:#0E0F1B">0</b><b style="color:#0E0F19">1</b><b style="color:#0E101A">0</b><b style="color:#0F111D">0</b><b style="color:#0E1221">1</b><b style="color:#0F182F">1</b><b style="color:#132442">0</b><b style="color:#0E192D">1</b><b style="color:#0E1423">10</b><b style="color:#0F1526">1</b><b style="color:#0F1322">0</b><b style="color:#0F1220">0</b><b style="color:#0F131F">1</b><b style="color:#11131F">0</b><b style="color:#101422">1</b><b style="color:#0E1726">0</b><b style="color:#0F1B32">0</b><b style="color:#0E1828">1</b><b style="color:#0E1624">0</b><b style="color:#0E1623">1</b><b style="color:#0E1624">1</b><b style="color:#0E1725">0</b><b style="color:#0D1827">1</b><b style="color:#0F1D35">1</b><b style="color:#0F1E34">1</b><b style="color:#0F1B2A">0</b><b style="color:#0E1B2A">0</b><b style="color:#0F1B2B">0</b><b style="color:#0E1D2E">0</b><b style="color:#0F2238">0</b><b style="color:#0F223A">1</b><b style="color:#0E1F30">0</b><b style="color:#0E1F2F">0</b><b style="color:#0D1F2F">0</b><b style="color:#0E2130">0</b><b style="color:#0E2231">1</b><b style="color:#0E2232">1</b><b style="color:#0E2334">0</b><b style="color:#0E2336">1</b><b style="color:#0F2437">0</b><b style="color:#0E263A">1</b><b style="color:#0D2941">1</b><b style="color:#0D2B45">1</b><b style="color:#0D2C47">0</b><b style="color:#0E2F4A">1</b><b style="color:#0D2B41">0</b><b style="color:#0D2A3E">10</b><b style="color:#0C2B3F">1</b><b style="color:#0D2B44">1</b><b style="color:#0D2D47">1</b><b style="color:#0F3557">0</b><b style="color:#0D314E">0</b><b style="color:#0E2D46">1</b><b style="color:#0F2C44">0</b><b style="color:#0E2D45">1</b><b style="color:#0E324B">1</b><b style="color:#0D3A58">0</b><b style="color:#0D3A56">0</b><b style="color:#0E3853">1</b><b style="color:#0D3853">10</b><b style="color:#0D3852">1</b><b style="color:#0E3953">1</b><b style="color:#0D3954">1</b><b style="color:#0D3C5D">1</b><b style="color:#0D3E60">0</b><b style="color:#0D3A5B">0</b><b style="color:#0D3C5E">11</b><b style="color:#0E3E62">0</b><b style="color:#0D3C60">1</b><b style="color:#0F3E63">1</b><b style="color:#0E3C60">1</b><b style="color:#0D3758">10</b><b style="color:#0D3554">0</b><b style="color:#0C344F">0</b><b style="color:#0C3453">0</b><b style="color:#0D385B">1</b><b style="color:#0E3F65">1</b><b style="color:#0D395C">0</b><b style="color:#0C3554">0</b><b style="color:#0C3657">0</b><b style="color:#0C3554">1</b><b style="color:#0C3552">0</b><b style="color:#0B3A5D">0</b><b style="color:#0B395C">0</b><b style="color:#0C3A5D">1</b><b style="color:#0D3D63">0</b><b style="color:#0B3556">0</b><b style="color:#0C3554">0</b><b style="color:#0B334D">1</b><b style="color:#0B3148">0</b><b style="color:#0B2F47">0</b><b style="color:#0B2E46">0</b><b style="color:#0C2E46">0</b><b style="color:#0B2D47">0</b><b style="color:#0B3150">1</b><b style="color:#0B2E4A">0</b><b style="color:#0B2A40">1</b><b style="color:#0A2A3E">0</b>
<b style="color:#0A080F">0</b><b style="color:#0A090F">0</b><b style="color:#0A0910">1</b><b style="color:#0B0A10">111</b><b style="color:#0B0A11">0</b><b style="color:#0C0B12">1</b><b style="color:#0C0C15">0</b><b style="color:#0C0E1C">1</b><b style="color:#0C0D17">0</b><b style="color:#0C0B13">0</b><b style="color:#0D0B13">1</b><b style="color:#0D0C14">0</b><b style="color:#0E0C15">1</b><b style="color:#0D0C15">1</b><b style="color:#0D0E16">0</b><b style="color:#0E0F1A">0</b><b style="color:#0E1428">1</b><b style="color:#0F162B">1</b><b style="color:#0F1225">1</b><b style="color:#0F182F">0</b><b style="color:#0F1121">1</b><b style="color:#0E101A">0</b><b style="color:#0E1019">1</b><b style="color:#0F111B">0</b><b style="color:#0F111F">0</b><b style="color:#0F1324">0</b><b style="color:#121F3A">1</b><b style="color:#13223F">0</b><b style="color:#0F1527">0</b><b style="color:#101322">1</b><b style="color:#101524">1</b><b style="color:#101626">1</b><b style="color:#101322">1</b><b style="color:#10131F">0</b><b style="color:#11141F">0</b><b style="color:#111420">0</b><b style="color:#111522">1</b><b style="color:#0F192B">1</b><b style="color:#0F1C32">1</b><b style="color:#0E1826">1</b><b style="color:#0F1724">00</b><b style="color:#0F1725">1</b><b style="color:#0F1826">1</b><b style="color:#0F1C31">0</b><b style="color:#0F2038">0</b><b style="color:#0F1B2A">01</b><b style="color:#0F1B2B">0</b><b style="color:#0F1C2D">1</b><b style="color:#0F2236">1</b><b style="color:#0F233B">1</b><b style="color:#0E1F31">1</b><b style="color:#0E1F2F">11</b><b style="color:#0E1F30">1</b><b style="color:#0E2131">0</b><b style="color:#0E2232">1</b><b style="color:#0E2233">1</b><b style="color:#0E2335">1</b><b style="color:#0E2336">0</b><b style="color:#0F2538">1</b><b style="color:#0E273F">1</b><b style="color:#0E2B46">10</b><b style="color:#0F2E4C">1</b><b style="color:#0D2A41">0</b><b style="color:#0D293D">11</b><b style="color:#0D2A3E">0</b><b style="color:#0D2B41">0</b><b style="color:#0D2D49">0</b><b style="color:#0F3557">1</b><b style="color:#0E2E4A">0</b><b style="color:#0E2C44">1</b><b style="color:#0E2C42">10</b><b style="color:#0E2C44">0</b><b style="color:#0E314D">0</b><b style="color:#0E3753">1</b><b style="color:#0E3854">1</b><b style="color:#0F3853">0</b><b style="color:#0E3753">1</b><b style="color:#0E3752">01</b><b style="color:#0D3954">1</b><b style="color:#0E3C5D">1</b><b style="color:#0E3C5E">0</b><b style="color:#0D3A5A">1</b><b style="color:#0E3C5E">1</b><b style="color:#0E3E60">1</b><b style="color:#0E3E61">0</b><b style="color:#0F3E63">0</b><b style="color:#0F3F63">1</b><b style="color:#0E395B">0</b><b style="color:#0D3653">0</b><b style="color:#0E3757">0</b><b style="color:#0D3756">1</b><b style="color:#0D3554">1</b><b style="color:#0D3859">0</b><b style="color:#0F3F65">0</b><b style="color:#0E3E63">1</b><b style="color:#0D3858">0</b><b style="color:#0C3552">0</b><b style="color:#0C3857">1</b><b style="color:#0C3858">0</b><b style="color:#0B395A">1</b><b style="color:#0B3E63">1</b><b style="color:#0C3A5E">1</b><b style="color:#0D3D63">1</b><b style="color:#0C3B5E">1</b><b style="color:#0C395B">1</b><b style="color:#0C3653">1</b><b style="color:#0B344D">1</b><b style="color:#0B334B">1</b><b style="color:#0B324A">10</b><b style="color:#0B334F">0</b><b style="color:#0B3454">0</b><b style="color:#0B324E">1</b><b style="color:#0B2D44">1</b><b style="color:#0C2F44">0</b><b style="color:#0C2B3F">1</b>
<b style="color:#0A090F">1</b><b style="color:#0A0910">0</b><b style="color:#0B0A10">11</b><b style="color:#0B0910">0</b><b style="color:#0B0A10">0</b><b style="color:#0B0A11">0</b><b style="color:#0C0B11">0</b><b style="color:#0C0B12">0</b><b style="color:#0C0C15">0</b><b style="color:#0D0F1D">1</b><b style="color:#0E0E19">0</b><b style="color:#0D0C14">0</b><b style="color:#0E0C14">1</b><b style="color:#0E0D14">0</b><b style="color:#0F0D16">1</b><b style="color:#0F0E16">1</b><b style="color:#0E0F17">0</b><b style="color:#0E101C">1</b><b style="color:#0F172C">1</b><b style="color:#0F162A">0</b><b style="color:#0F162B">1</b><b style="color:#11172C">1</b><b style="color:#0F111E">1</b><b style="color:#0F111B">00</b><b style="color:#10121D">1</b><b style="color:#101221">1</b><b style="color:#10172B">0</b><b style="color:#152544">1</b><b style="color:#111D35">1</b><b style="color:#101524">0</b><b style="color:#111423">0</b><b style="color:#111628">0</b><b style="color:#111525">0</b><b style="color:#111421">0</b><b style="color:#111520">10</b><b style="color:#101521">1</b><b style="color:#0F1624">1</b><b style="color:#101B2F">1</b><b style="color:#0F1C30">1</b><b style="color:#0F1726">1</b><b style="color:#101825">11</b><b style="color:#101927">0</b><b style="color:#0F1B2D">1</b><b style="color:#10213B">0</b><b style="color:#0F1C2C">1</b><b style="color:#0F1B29">0</b><b style="color:#0F1B2A">0</b><b style="color:#101C2D">1</b><b style="color:#0F2134">0</b><b style="color:#10243D">0</b><b style="color:#0F2031">0</b><b style="color:#0E1F2F">11</b><b style="color:#0E2030">1</b><b style="color:#0E2130">1</b><b style="color:#0F2131">0</b><b style="color:#0F2232">1</b><b style="color:#0F2334">1</b><b style="color:#0E2336">0</b><b style="color:#0F2437">0</b><b style="color:#0F263B">0</b><b style="color:#0F2B46">0</b><b style="color:#0E2B46">0</b><b style="color:#0F2E4B">1</b><b style="color:#0E2A40">0</b><b style="color:#0E283C">1</b><b style="color:#0D283B">1</b><b style="color:#0E293D">1</b><b style="color:#0E2A40">1</b><b style="color:#0E2E4A">0</b><b style="color:#103456">0</b><b style="color:#0E2C46">1</b><b style="color:#0D2B41">0</b><b style="color:#0E2B40">0</b><b style="color:#0D2B40">0</b><b style="color:#0D2C42">0</b><b style="color:#0E2E48">1</b><b style="color:#0F2F49">1</b><b style="color:#0E324B">1</b><b style="color:#0E3851">1</b><b style="color:#0F3852">0</b><b style="color:#0E3752">0</b><b style="color:#0F3752">0</b><b style="color:#0E3854">0</b><b style="color:#0F3D5F">1</b><b style="color:#0E3B5C">1</b><b style="color:#0E3A5A">0</b><b style="color:#0E3C5E">1</b><b style="color:#0F3E62">1</b><b style="color:#0F3D61">0</b><b style="color:#114166">0</b><b style="color:#0F3B5D">1</b><b style="color:#0D3754">1</b><b style="color:#0D3652">0</b><b style="color:#0D3958">1</b><b style="color:#0D395A">0</b><b style="color:#0D3859">0</b><b style="color:#0E3E63">1</b><b style="color:#0F426A">1</b><b style="color:#0C3B5E">1</b><b style="color:#0C3856">0</b><b style="color:#0D3854">0</b><b style="color:#0C3959">1</b><b style="color:#0C3C5E">1</b><b style="color:#0B4065">1</b><b style="color:#0B3D61">1</b><b style="color:#0D4066">0</b><b style="color:#0C3B5D">1</b><b style="color:#0D3E62">1</b><b style="color:#0C3B5B">1</b><b style="color:#0C3651">0</b><b style="color:#0C364F">0</b><b style="color:#0C354F">11</b><b style="color:#0B3855">1</b><b style="color:#0B395A">1</b><b style="color:#0B3551">0</b><b style="color:#0B324A">0</b><b style="color:#0A3149">0</b><b style="color:#0B3148">1</b><b style="color:#0B2F45">1</b>
<b style="color:#0A090F">0</b><b style="color:#0A0910">1</b><b style="color:#0B0910">1</b><b style="color:#0B090F">10</b><b style="color:#0B0A10">1</b><b style="color:#0C0A10">0</b><b style="color:#0C0A11">1</b><b style="color:#0C0B11">0</b><b style="color:#0D0B12">1</b><b style="color:#0D0D15">0</b><b style="color:#0E0F1E">0</b><b style="color:#0E0E19">0</b><b style="color:#0E0D15">1</b><b style="color:#0F0D15">1</b><b style="color:#0F0E16">1</b><b style="color:#100E16">1</b><b style="color:#0F0E16">0</b><b style="color:#0F0E17">1</b><b style="color:#0F111F">0</b><b style="color:#10192F">1</b><b style="color:#10162A">0</b><b style="color:#111931">0</b><b style="color:#111426">0</b><b style="color:#10111D">1</b><b style="color:#0F121B">0</b><b style="color:#10121C">0</b><b style="color:#10121F">1</b><b style="color:#111423">0</b><b style="color:#121D34">0</b><b style="color:#162745">1</b><b style="color:#11182C">1</b><b style="color:#111523">1</b><b style="color:#111524">0</b><b style="color:#111729">1</b><b style="color:#121424">1</b><b style="color:#121421">0</b><b style="color:#111520">1</b><b style="color:#101521">0</b><b style="color:#101523">0</b><b style="color:#0F1827">1</b><b style="color:#101E34">0</b><b style="color:#101B2D">1</b><b style="color:#101925">1</b><b style="color:#101926">1</b><b style="color:#101927">1</b><b style="color:#101A2A">0</b><b style="color:#11213B">0</b><b style="color:#101E30">0</b><b style="color:#0F1B29">0</b><b style="color:#0F1B2A">0</b><b style="color:#101C2C">0</b><b style="color:#0F1F32">1</b><b style="color:#11243E">1</b><b style="color:#0F2032">1</b><b style="color:#0E202F">0</b><b style="color:#0E1F2F">1</b><b style="color:#0F2030">11</b><b style="color:#102131">1</b><b style="color:#0F2232">0</b><b style="color:#0F2332">1</b><b style="color:#0F2335">0</b><b style="color:#0F2436">1</b><b style="color:#0F2539">0</b><b style="color:#0E2A43">1</b><b style="color:#0E2B46">1</b><b style="color:#102E4B">1</b><b style="color:#0E2941">1</b><b style="color:#0E273B">10</b><b style="color:#0E283B">1</b><b style="color:#0E293F">1</b><b style="color:#0F304D">0</b><b style="color:#103352">1</b><b style="color:#0E2B42">1</b><b style="color:#0E2B3F">000</b><b style="color:#0E2B40">1</b><b style="color:#0E2C45">0</b><b style="color:#0F2D47">0</b><b style="color:#0E2C42">0</b><b style="color:#0E2F45">0</b><b style="color:#0E354E">0</b><b style="color:#0F3853">0</b><b style="color:#0F3753">1</b><b style="color:#0F3956">1</b><b style="color:#0F3D60">0</b><b style="color:#0F3A5A">0</b><b style="color:#0E3A5C">1</b><b style="color:#0F3C60">0</b><b style="color:#103E63">0</b><b style="color:#114066">1</b><b style="color:#103E62">0</b><b style="color:#0E3755">0</b><b style="color:#0D3651">1</b><b style="color:#0D3550">1</b><b style="color:#0D3858">1</b><b style="color:#0D395B">0</b><b style="color:#0D3A5D">1</b><b style="color:#0F426A">1</b><b style="color:#0D3E62">1</b><b style="color:#0C3857">0</b><b style="color:#0C3753">0</b><b style="color:#0C3752">0</b><b style="color:#0C3959">1</b><b style="color:#0C3F65">0</b><b style="color:#0C3F66">1</b><b style="color:#0D3F65">0</b><b style="color:#0C3C5E">1</b><b style="color:#0C3B5D">0</b><b style="color:#0D3C60">0</b><b style="color:#0B3856">1</b><b style="color:#0B3650">1</b><b style="color:#0B354F">1</b><b style="color:#0C3652">1</b><b style="color:#0B3959">0</b><b style="color:#0B3A5B">0</b><b style="color:#0A3551">1</b><b style="color:#0A334B">10</b><b style="color:#0A324A">1</b><b style="color:#0B3149">01</b>
<b style="color:#0A090F">1</b><b style="color:#0B0910">0</b><b style="color:#0B0A11">0</b><b style="color:#0B0B12">0</b><b style="color:#0C0D14">0</b><b style="color:#0C0E16">1</b><b style="color:#0C0F17">0</b><b style="color:#0D1018">1</b><b style="color:#0C1018">0</b><b style="color:#0D1018">1</b><b style="color:#0E1019">1</b><b style="color:#0E111B">0</b><b style="color:#0F1323">1</b><b style="color:#0E111D">0</b><b style="color:#0F0F17">0</b><b style="color:#0F0E16">0</b><b style="color:#0F0E15">1</b><b style="color:#0F0E16">0</b><b style="color:#0F0F17">1</b><b style="color:#0F1019">0</b><b style="color:#101324">1</b><b style="color:#111C33">1</b><b style="color:#10192E">1</b><b style="color:#121C33">0</b><b style="color:#111422">1</b><b style="color:#10131D">000</b><b style="color:#111321">1</b><b style="color:#111627">0</b><b style="color:#152541">0</b><b style="color:#15233E">1</b><b style="color:#101628">1</b><b style="color:#121524">1</b><b style="color:#111727">1</b><b style="color:#12182A">0</b><b style="color:#121523">0</b><b style="color:#111622">1</b><b style="color:#121622">0</b><b style="color:#101623">0</b><b style="color:#101724">1</b><b style="color:#101A2B">1</b><b style="color:#101F37">1</b><b style="color:#111A2A">1</b><b style="color:#111926">1</b><b style="color:#111927">0</b><b style="color:#101928">1</b><b style="color:#112037">1</b><b style="color:#111F35">1</b><b style="color:#101B29">1</b><b style="color:#101C2A">0</b><b style="color:#111C2D">1</b><b style="color:#101F31">1</b><b style="color:#10263F">0</b><b style="color:#0F2134">0</b><b style="color:#0F2030">10</b><b style="color:#0F2031">1</b><b style="color:#0F2131">1</b><b style="color:#102131">1</b><b style="color:#102232">1</b><b style="color:#0F2332">0</b><b style="color:#102332">1</b><b style="color:#102334">0</b><b style="color:#0F2437">1</b><b style="color:#102840">0</b><b style="color:#0F2B47">1</b><b style="color:#112E4B">1</b><b style="color:#0F2941">1</b><b style="color:#102639">01</b><b style="color:#0F273A">1</b><b style="color:#0F283E">1</b><b style="color:#103150">0</b><b style="color:#0F304E">1</b><b style="color:#0E2940">0</b><b style="color:#0F293E">1</b><b style="color:#0E293E">1</b><b style="color:#0E293D">1</b><b style="color:#0E2A3E">1</b><b style="color:#0F2B43">1</b><b style="color:#0F2D46">0</b><b style="color:#0F2A40">0</b><b style="color:#0E2B3F">0</b><b style="color:#0F2C42">0</b><b style="color:#0F314A">0</b><b style="color:#0F3752">1</b><b style="color:#0F3A59">0</b><b style="color:#103E62">0</b><b style="color:#0F3959">1</b><b style="color:#0F3B5E">1</b><b style="color:#113E63">0</b><b style="color:#124066">0</b><b style="color:#124167">0</b><b style="color:#0F3858">1</b><b style="color:#0F3551">1</b><b style="color:#0F344F">00</b><b style="color:#0E3757">0</b><b style="color:#0E395D">0</b><b style="color:#0F3F64">1</b><b style="color:#104065">0</b><b style="color:#0D3757">1</b><b style="color:#0D3551">0</b><b style="color:#0D344E">1</b><b style="color:#0D344F">1</b><b style="color:#0D395A">0</b><b style="color:#0E4168">0</b><b style="color:#0E3E64">0</b><b style="color:#0D3C60">1</b><b style="color:#0D3858">0</b><b style="color:#0D3958">0</b><b style="color:#0D395A">0</b><b style="color:#0C3551">0</b><b style="color:#0B344D">0</b><b style="color:#0B334D">0</b><b style="color:#0C3959">11</b><b style="color:#0B324C">1</b><b style="color:#0B334B">1</b><b style="color:#0C334B">1</b><b style="color:#0C3148">1</b><b style="color:#0C3249">0</b><b style="color:#0C334A">1</b><b style="color:#0C2F45">0</b>
<b style="color:#0B2231">0</b><b style="color:#0C2333">0</b><b style="color:#0B2536">1</b><b style="color:#0C2636">1</b><b style="color:#0D2637">10</b><b style="color:#0C2637">1</b><b style="color:#0D2636">1</b><b style="color:#0D2637">1</b><b style="color:#0D2536">0</b><b style="color:#0D2636">1</b><b style="color:#0D2535">0</b><b style="color:#0E2638">1</b><b style="color:#0F283E">0</b><b style="color:#0F2537">0</b><b style="color:#0E2130">1</b><b style="color:#0E1E2D">1</b><b style="color:#0F1D2A">0</b><b style="color:#0F1B28">0</b><b style="color:#101926">1</b><b style="color:#0F1927">0</b><b style="color:#101F33">1</b><b style="color:#11253F">0</b><b style="color:#11243F">0</b><b style="color:#11223A">0</b><b style="color:#101B2B">0</b><b style="color:#101B29">1</b><b style="color:#101C29">1</b><b style="color:#101C2B">0</b><b style="color:#101D2D">1</b><b style="color:#112239">1</b><b style="color:#163152">0</b><b style="color:#11243E">1</b><b style="color:#101E30">0</b><b style="color:#101E2E">0</b><b style="color:#102034">1</b><b style="color:#102033">1</b><b style="color:#0F1E2D">1</b><b style="color:#101E2D">11</b><b style="color:#0F1E2D">1</b><b style="color:#0F1E2E">0</b><b style="color:#102338">0</b><b style="color:#10253E">0</b><b style="color:#102030">0</b><b style="color:#101F2F">1</b><b style="color:#101F30">1</b><b style="color:#102339">0</b><b style="color:#112741">0</b><b style="color:#102031">1</b><b style="color:#102030">1</b><b style="color:#102131">1</b><b style="color:#102235">0</b><b style="color:#112A43">0</b><b style="color:#10253B">0</b><b style="color:#102333">001</b><b style="color:#102334">0</b><b style="color:#102436">0</b><b style="color:#102537">0</b><b style="color:#112537">10</b><b style="color:#112538">1</b><b style="color:#102639">1</b><b style="color:#0F293F">0</b><b style="color:#102D4A">1</b><b style="color:#10304E">0</b><b style="color:#102B44">0</b><b style="color:#10273B">1</b><b style="color:#0F273A">1</b><b style="color:#0F273B">0</b><b style="color:#0F2940">0</b><b style="color:#113354">1</b><b style="color:#0F2E4A">1</b><b style="color:#0F293D">1</b><b style="color:#0F283C">0</b><b style="color:#10283B">0</b><b style="color:#0F293A">1</b><b style="color:#10293B">0</b><b style="color:#0F2A40">1</b><b style="color:#102C46">1</b><b style="color:#102A3F">100</b><b style="color:#0F2A40">1</b><b style="color:#0F2E47">1</b><b style="color:#103756">0</b><b style="color:#113E62">1</b><b style="color:#103B5B">0</b><b style="color:#103D61">1</b><b style="color:#124166">1</b><b style="color:#13446A">1</b><b style="color:#113B5C">1</b><b style="color:#0F3552">1</b><b style="color:#0F3450">1</b><b style="color:#0F344F">00</b><b style="color:#0F3757">1</b><b style="color:#103D62">0</b><b style="color:#124268">0</b><b style="color:#0F395B">0</b><b style="color:#0E334F">1</b><b style="color:#0E324C">1</b><b style="color:#0E314C">0</b><b style="color:#0D334E">1</b><b style="color:#0E3C60">0</b><b style="color:#104067">0</b><b style="color:#0F3C61">0</b><b style="color:#0E3757">0</b><b style="color:#0E3756">0</b><b style="color:#0E334F">1</b><b style="color:#0D3656">1</b><b style="color:#0D334F">1</b><b style="color:#0D334E">1</b><b style="color:#0E3859">0</b><b style="color:#0D3655">0</b><b style="color:#0D324B">0</b><b style="color:#0D3149">0</b><b style="color:#0C3249">010</b><b style="color:#0C334B">1</b><b style="color:#0C344C">1</b><b style="color:#0C364E">1</b>
<b style="color:#0C2F43">0</b><b style="color:#0B2C3F">1</b><b style="color:#0B2B3E">1</b><b style="color:#0B2A3C">0</b><b style="color:#0C293B">0</b><b style="color:#0C293A">0</b><b style="color:#0C283A">00</b><b style="color:#0D283A">101</b><b style="color:#0D293A">1</b><b style="color:#0D2A3B">1</b><b style="color:#0E2B3F">0</b><b style="color:#0F2E47">0</b><b style="color:#0F2D43">1</b><b style="color:#0F2C3F">111</b><b style="color:#0E2A3C">0</b><b style="color:#102739">0</b><b style="color:#102436">1</b><b style="color:#112942">0</b><b style="color:#122C49">0</b><b style="color:#122D4A">0</b><b style="color:#11253B">0</b><b style="color:#102232">1</b><b style="color:#112333">1</b><b style="color:#112232">1</b><b style="color:#112233">0</b><b style="color:#102337">1</b><b style="color:#132E4C">1</b><b style="color:#153456">1</b><b style="color:#10253D">0</b><b style="color:#102336">10</b><b style="color:#10253C">1</b><b style="color:#102335">1</b><b style="color:#102232">100</b><b style="color:#102332">0</b><b style="color:#102334">1</b><b style="color:#102943">0</b><b style="color:#11283F">1</b><b style="color:#112336">01</b><b style="color:#11253A">0</b><b style="color:#112C48">0</b><b style="color:#102438">1</b><b style="color:#102335">0</b><b style="color:#102434">0</b><b style="color:#102438">1</b><b style="color:#112B46">0</b><b style="color:#11283F">1</b><b style="color:#112535">1</b><b style="color:#102433">0</b><b style="color:#112434">11</b><b style="color:#112536">1</b><b style="color:#112638">1</b><b style="color:#112639">0000</b><b style="color:#10273C">1</b><b style="color:#102D49">0</b><b style="color:#11304F">1</b><b style="color:#102C46">1</b><b style="color:#10273B">0</b><b style="color:#102639">0</b><b style="color:#11263A">1</b><b style="color:#102A42">0</b><b style="color:#123556">1</b><b style="color:#102C44">0</b><b style="color:#10273B">1</b><b style="color:#11273A">0</b><b style="color:#112739">11</b><b style="color:#11273A">0</b><b style="color:#11283D">1</b><b style="color:#112C45">0</b><b style="color:#10283E">0</b><b style="color:#10293D">1</b><b style="color:#11293F">0</b><b style="color:#10293F">0</b><b style="color:#102A42">0</b><b style="color:#11314F">1</b><b style="color:#123555">1</b><b style="color:#113959">1</b><b style="color:#124065">0</b><b style="color:#15466D">0</b><b style="color:#124063">1</b><b style="color:#0F3653">0</b><b style="color:#0F344F">0</b><b style="color:#0F334E">0</b><b style="color:#0E334E">1</b><b style="color:#0F3350">0</b><b style="color:#103859">1</b><b style="color:#134369">0</b><b style="color:#113D61">1</b><b style="color:#0E3351">1</b><b style="color:#0E314D">1</b><b style="color:#0E304B">0</b><b style="color:#0E304A">1</b><b style="color:#0E3655">0</b><b style="color:#103F66">1</b><b style="color:#113F65">1</b><b style="color:#0F3556">0</b><b style="color:#0F3655">0</b><b style="color:#0E324D">1</b><b style="color:#0D314A">0</b><b style="color:#0D3555">1</b><b style="color:#0E3453">1</b><b style="color:#0E385A">0</b><b style="color:#0E3452">0</b><b style="color:#0D314A">0</b><b style="color:#0D3148">0</b><b style="color:#0D3248">1</b><b style="color:#0D334A">0</b><b style="color:#0D344B">1</b><b style="color:#0D364D">0</b><b style="color:#0D3952">1</b><b style="color:#0D3F5B">0</b><b style="color:#0D4766">0</b>
<b style="color:#0B2C40">0</b><b style="color:#0B2A3D">11</b><b style="color:#0B293C">0</b><b style="color:#0C293B">11011</b><b style="color:#0C2A3B">1</b><b style="color:#0D2A3C">0</b><b style="color:#0F2B3C">1</b><b style="color:#0E2A3C">1</b><b style="color:#0F2A3D">0</b><b style="color:#102C40">1</b><b style="color:#112F49">1</b><b style="color:#102F45">1</b><b style="color:#0F2D41">1</b><b style="color:#112F42">0</b><b style="color:#103043">1</b><b style="color:#0F3144">1</b><b style="color:#113146">0</b><b style="color:#113046">1</b><b style="color:#123451">1</b><b style="color:#133453">1</b><b style="color:#13304D">0</b><b style="color:#11263A">0</b><b style="color:#122638">1</b><b style="color:#112637">1</b><b style="color:#112537">1</b><b style="color:#112639">0</b><b style="color:#112840">1</b><b style="color:#16385A">0</b><b style="color:#133150">0</b><b style="color:#11263C">0</b><b style="color:#112538">1</b><b style="color:#11263B">0</b><b style="color:#11283F">1</b><b style="color:#112537">0</b><b style="color:#112536">010</b><b style="color:#112537">0</b><b style="color:#11263A">1</b><b style="color:#112D48">1</b><b style="color:#11283E">0</b><b style="color:#112538">0</b><b style="color:#11263A">0</b><b style="color:#112E4B">0</b><b style="color:#11283D">0</b><b style="color:#102538">11</b><b style="color:#112639">0</b><b style="color:#112C46">0</b><b style="color:#112A42">1</b><b style="color:#112538">1</b><b style="color:#112535">0</b><b style="color:#112534">1</b><b style="color:#112434">1</b><b style="color:#112534">1</b><b style="color:#112535">1</b><b style="color:#112536">10</b><b style="color:#112537">0</b><b style="color:#112538">1</b><b style="color:#102639">1</b><b style="color:#112B45">0</b><b style="color:#11304F">0</b><b style="color:#112C46">1</b><b style="color:#112639">1</b><b style="color:#112538">11</b><b style="color:#112A42">1</b><b style="color:#123454">0</b><b style="color:#10283E">0</b><b style="color:#112638">001</b><b style="color:#122638">10</b><b style="color:#11263B">0</b><b style="color:#122A44">0</b><b style="color:#12273C">0</b><b style="color:#11263A">1</b><b style="color:#12273B">0</b><b style="color:#12283E">1</b><b style="color:#112941">1</b><b style="color:#133251">1</b><b style="color:#12304D">1</b><b style="color:#133152">0</b><b style="color:#163D60">1</b><b style="color:#164165">1</b><b style="color:#113655">1</b><b style="color:#103450">0</b><b style="color:#10334D">1</b><b style="color:#10324C">1</b><b style="color:#0F324D">1</b><b style="color:#0F3351">1</b><b style="color:#123D61">0</b><b style="color:#144469">1</b><b style="color:#0F3556">1</b><b style="color:#0F314E">0</b><b style="color:#0F304A">0</b><b style="color:#0F2F48">1</b><b style="color:#0E314D">1</b><b style="color:#103C60">0</b><b style="color:#123E65">1</b><b style="color:#10395D">0</b><b style="color:#103555">0</b><b style="color:#0F314D">0</b><b style="color:#0E2F48">1</b><b style="color:#0E2F47">1</b><b style="color:#0F3758">1</b><b style="color:#0F395D">1</b><b style="color:#0E334F">0</b><b style="color:#0E3048">1</b><b style="color:#0E3148">0</b><b style="color:#0E3249">1</b><b style="color:#0E344B">1</b><b style="color:#0E374F">0</b><b style="color:#0E3B55">1</b><b style="color:#0E3F5B">0</b><b style="color:#0E415D">1</b><b style="color:#0D3C56">1</b><b style="color:#0D3148">0</b>
<b style="color:#0A2B3F">0</b><b style="color:#0A2B3E">1</b><b style="color:#0A2B3D">1</b><b style="color:#0B2B3E">1</b><b style="color:#0B2B3D">00</b><b style="color:#0C2C3E">10</b><b style="color:#0C2B3D">0</b><b style="color:#0D2B3D">0</b><b style="color:#132E3E">1</b><b style="color:#152F40">1</b><b style="color:#0F2B3F">0</b><b style="color:#112C40">1</b><b style="color:#182E41">1</b><b style="color:#223246">0</b><b style="color:#15324D">1</b><b style="color:#113048">1</b><b style="color:#1A3546">1</b><b style="color:#153346">1</b><b style="color:#103146">1</b><b style="color:#103348">1</b><b style="color:#11344A">0</b><b style="color:#10364E">0</b><b style="color:#123E5E">0</b><b style="color:#133D60">0</b><b style="color:#12314B">1</b><b style="color:#12283B">1</b><b style="color:#12283A">0</b><b style="color:#12283B">00</b><b style="color:#11293C">1</b><b style="color:#122F4B">0</b><b style="color:#173C5F">1</b><b style="color:#112D48">0</b><b style="color:#11283C">0</b><b style="color:#11263A">1</b><b style="color:#102940">0</b><b style="color:#11293F">0</b><b style="color:#112639">0000</b><b style="color:#112638">1</b><b style="color:#102940">1</b><b style="color:#112F4B">1</b><b style="color:#10273D">0</b><b style="color:#11263B">1</b><b style="color:#112E49">1</b><b style="color:#112B44">0</b><b style="color:#112639">000</b><b style="color:#112C45">0</b><b style="color:#112C46">0</b><b style="color:#102538">1</b><b style="color:#112535">1</b><b style="color:#122534">0</b><b style="color:#112433">0</b><b style="color:#102333">110</b><b style="color:#112433">0</b><b style="color:#102433">0</b><b style="color:#102434">0</b><b style="color:#102435">1</b><b style="color:#11273F">0</b><b style="color:#12304F">1</b><b style="color:#122C47">1</b><b style="color:#102336">0</b><b style="color:#102334">0</b><b style="color:#102336">0</b><b style="color:#102A46">0</b><b style="color:#133150">0</b><b style="color:#102438">0</b><b style="color:#112334">0</b><b style="color:#112333">0</b><b style="color:#112334">1</b><b style="color:#122434">0</b><b style="color:#122435">1</b><b style="color:#122437">0</b><b style="color:#122941">1</b><b style="color:#12263B">0</b><b style="color:#122538">0</b><b style="color:#132539">1</b><b style="color:#13253A">0</b><b style="color:#13273F">0</b><b style="color:#153150">0</b><b style="color:#132D4A">0</b><b style="color:#163455">0</b><b style="color:#1A3D5F">0</b><b style="color:#132D4B">1</b><b style="color:#11283F">1</b><b style="color:#112A41">0</b><b style="color:#112D45">1</b><b style="color:#103049">1</b><b style="color:#10324D">0</b><b style="color:#0F3657">1</b><b style="color:#14436A">0</b><b style="color:#123D60">0</b><b style="color:#0F314E">1</b><b style="color:#102F4A">0</b><b style="color:#0F2F48">1</b><b style="color:#0F2E48">1</b><b style="color:#0F3757">1</b><b style="color:#134066">0</b><b style="color:#11385A">0</b><b style="color:#12395C">1</b><b style="color:#0F324E">0</b><b style="color:#0E2E46">0</b><b style="color:#0E2F47">1</b><b style="color:#0F3451">1</b><b style="color:#113C61">0</b><b style="color:#0E3552">0</b><b style="color:#0E324A">1</b><b style="color:#0F344C">1</b><b style="color:#0E354E">1</b><b style="color:#0E3851">1</b><b style="color:#0E3952">0</b><b style="color:#0E3750">0</b><b style="color:#0E3349">0</b><b style="color:#0E2B3E">1</b><b style="color:#0D2334">0</b><b style="color:#0D1F2E">0</b><b style="color:#0C1E2D">1</b>
<b style="color:#0A2C3F">0</b><b style="color:#0A2C40">0</b><b style="color:#0A2D40">0</b><b style="color:#0B2D40">10</b><b style="color:#0B2E40">1</b><b style="color:#0B2E41">1</b><b style="color:#0C2E41">0</b><b style="color:#0C2E40">1</b><b style="color:#0C2E3F">0</b><b style="color:#133141">0</b><b style="color:#163342">1</b><b style="color:#0C2C40">0</b><b style="color:#0E2E41">1</b><b style="color:#143144">1</b><b style="color:#1D3747">1</b><b style="color:#103146">0</b><b style="color:#103550">0</b><b style="color:#1B3B4E">1</b><b style="color:#153749">1</b><b style="color:#113549">1</b><b style="color:#11354A">0</b><b style="color:#11364B">1</b><b style="color:#11354B">1</b><b style="color:#113851">0</b><b style="color:#134265">0</b><b style="color:#144365">1</b><b style="color:#11334B">1</b><b style="color:#112D3F">0</b><b style="color:#122B3D">1</b><b style="color:#112B3D">0</b><b style="color:#102B3D">0</b><b style="color:#102B41">1</b><b style="color:#153859">1</b><b style="color:#15395B">0</b><b style="color:#0F2B42">1</b><b style="color:#10293C">00</b><b style="color:#102C44">1</b><b style="color:#10293E">0</b><b style="color:#12273A">0</b><b style="color:#11273A">10</b><b style="color:#12273A">1</b><b style="color:#11283B">1</b><b style="color:#122E47">1</b><b style="color:#19334B">0</b><b style="color:#10283D">1</b><b style="color:#112C45">1</b><b style="color:#112F4A">1</b><b style="color:#10273A">0</b><b style="color:#112739">1</b><b style="color:#11263A">0</b><b style="color:#102B43">1</b><b style="color:#112F49">0</b><b style="color:#112638">0</b><b style="color:#112535">1</b><b style="color:#122534">0</b><b style="color:#102433">0</b><b style="color:#102333">1</b><b style="color:#102332">0</b><b style="color:#102232">1</b><b style="color:#112232">1</b><b style="color:#102232">1</b><b style="color:#102231">0</b><b style="color:#112231">0</b><b style="color:#112336">1</b><b style="color:#132E4C">1</b><b style="color:#132B46">1</b><b style="color:#102132">0</b><b style="color:#102131">0</b><b style="color:#122131">1</b><b style="color:#172D47">1</b><b style="color:#142D48">1</b><b style="color:#102132">1</b><b style="color:#112131">0</b><b style="color:#122031">1</b><b style="color:#122130">01</b><b style="color:#112131">0</b><b style="color:#122132">1</b><b style="color:#13253B">1</b><b style="color:#132337">0</b><b style="color:#132132">1</b><b style="color:#132133">0</b><b style="color:#132235">0</b><b style="color:#14253C">1</b><b style="color:#162E4C">0</b><b style="color:#142A48">1</b><b style="color:#1C3B5B">0</b><b style="color:#183250">0</b><b style="color:#122237">0</b><b style="color:#122033">1</b><b style="color:#121F33">1</b><b style="color:#112033">1</b><b style="color:#112237">1</b><b style="color:#112640">0</b><b style="color:#143557">0</b><b style="color:#153C5F">1</b><b style="color:#113253">1</b><b style="color:#102D47">0</b><b style="color:#102D45">0</b><b style="color:#0F2D45">1</b><b style="color:#0F304D">1</b><b style="color:#133F65">0</b><b style="color:#12395C">1</b><b style="color:#113656">1</b><b style="color:#103657">0</b><b style="color:#0F2F49">1</b><b style="color:#0E2F48">0</b><b style="color:#103554">0</b><b style="color:#10385A">0</b><b style="color:#0F3657">0</b><b style="color:#0E314C">0</b><b style="color:#0E2E45">0</b><b style="color:#0E2C41">0</b><b style="color:#0E283D">0</b><b style="color:#0E2436">0</b><b style="color:#0E1F2F">1</b><b style="color:#0E1C2B">0</b><b style="color:#0D1A28">10000</b>
<b style="color:#0B3044">0</b><b style="color:#0A2F43">0</b><b style="color:#0C3043">1</b><b style="color:#0B2F43">1</b><b style="color:#0B3043">10</b><b style="color:#0C3145">00</b><b style="color:#0C3044">0</b><b style="color:#0C3043">0</b><b style="color:#153646">1</b><b style="color:#203F4A">0</b><b style="color:#1A3C4B">1</b><b style="color:#103345">1</b><b style="color:#113447">1</b><b style="color:#1E404F">1</b><b style="color:#103447">1</b><b style="color:#0F344A">1</b><b style="color:#204559">0</b><b style="color:#234657">1</b><b style="color:#284A57">0</b><b style="color:#1D4253">0</b><b style="color:#214458">1</b><b style="color:#133754">0</b><b style="color:#123750">1</b><b style="color:#123A56">1</b><b style="color:#16476B">1</b><b style="color:#144263">1</b><b style="color:#123850">1</b><b style="color:#133347">1</b><b style="color:#122D40">0</b><b style="color:#112C3F">11</b><b style="color:#122F47">0</b><b style="color:#183F62">1</b><b style="color:#123351">0</b><b style="color:#102A3F">1</b><b style="color:#112A3B">1</b><b style="color:#122B3E">0</b><b style="color:#112D45">0</b><b style="color:#12283B">1</b><b style="color:#12273A">1101</b><b style="color:#152B3E">1</b><b style="color:#284257">1</b><b style="color:#112B43">0</b><b style="color:#11293F">1</b><b style="color:#122F4C">1</b><b style="color:#11263A">1</b><b style="color:#122637">1</b><b style="color:#122536">1</b><b style="color:#11273D">0</b><b style="color:#132D48">1</b><b style="color:#112335">1</b><b style="color:#102232">0</b><b style="color:#102131">1</b><b style="color:#10212F">0</b><b style="color:#10202F">1</b><b style="color:#11202E">1</b><b style="color:#111F2C">0</b><b style="color:#121E2C">1</b><b style="color:#121E2B">1</b><b style="color:#121D2A">1</b><b style="color:#131D2A">0</b><b style="color:#141D2A">1</b><b style="color:#152741">0</b><b style="color:#152842">0</b><b style="color:#121A28">0</b><b style="color:#131A28">0</b><b style="color:#141C29">1</b><b style="color:#1A2A44">1</b><b style="color:#152339">1</b><b style="color:#131926">1</b><b style="color:#141925">1</b><b style="color:#141825">1</b><b style="color:#141A25">1</b><b style="color:#151A25">1</b><b style="color:#151A26">11</b><b style="color:#161D30">0</b><b style="color:#161C2E">1</b><b style="color:#161926">1</b><b style="color:#171927">1</b><b style="color:#171A2A">1</b><b style="color:#182036">0</b><b style="color:#1A2842">1</b><b style="color:#1C2C49">1</b><b style="color:#223653">0</b><b style="color:#161E33">1</b><b style="color:#151829">1</b><b style="color:#141728">0</b><b style="color:#131727">1</b><b style="color:#141727">1</b><b style="color:#13172B">1</b><b style="color:#141F3A">1</b><b style="color:#192E4D">0</b><b style="color:#13213D">0</b><b style="color:#121E37">0</b><b style="color:#12182C">1</b><b style="color:#12192C">0</b><b style="color:#10192E">0</b><b style="color:#142B4A">0</b><b style="color:#162E4F">0</b><b style="color:#132641">1</b><b style="color:#11223B">1</b><b style="color:#10213C">1</b><b style="color:#0F1C32">1</b><b style="color:#11223E">1</b><b style="color:#11223C">0</b><b style="color:#10192B">0</b><b style="color:#101C34">0</b><b style="color:#0F172A">0</b><b style="color:#0F1320">1</b><b style="color:#0F121E">0</b><b style="color:#0F121D">0</b><b style="color:#0F121C">0</b><b style="color:#0F121B">01</b><b style="color:#0E121B">1</b><b style="color:#0E121A">0</b><b style="color:#0E121B">1</b><b style="color:#0E111A">01</b>
<b style="color:#0A3348">0</b><b style="color:#093146">1</b><b style="color:#093145">1</b><b style="color:#0C3448">1</b><b style="color:#0B3247">0</b><b style="color:#093248">1</b><b style="color:#0A3348">0</b><b style="color:#0A3249">0</b><b style="color:#0A3349">0</b><b style="color:#0B3249">0</b><b style="color:#13384A">1</b><b style="color:#2A4C51">0</b><b style="color:#34565C">0</b><b style="color:#294E57">0</b><b style="color:#1D4050">0</b><b style="color:#2B4D58">1</b><b style="color:#294E5D">1</b><b style="color:#224757">0</b><b style="color:#345967">1</b><b style="color:#3A5F6E">0</b><b style="color:#3E636D">1</b><b style="color:#3E6472">0</b><b style="color:#416677">1</b><b style="color:#274C67">0</b><b style="color:#193F57">1</b><b style="color:#1A4157">0</b><b style="color:#1B465F">0</b><b style="color:#1F5172">0</b><b style="color:#16415B">0</b><b style="color:#123C53">1</b><b style="color:#13394E">0</b><b style="color:#123143">0</b><b style="color:#112D3F">0</b><b style="color:#102C3F">0</b><b style="color:#153752">0</b><b style="color:#194062">0</b><b style="color:#122F48">0</b><b style="color:#112B3D">0</b><b style="color:#112A3B">1</b><b style="color:#112C41">1</b><b style="color:#122D42">1</b><b style="color:#12293B">0</b><b style="color:#13293B">0</b><b style="color:#13293C">1</b><b style="color:#13293B">0</b><b style="color:#162C3F">1</b><b style="color:#37505F">1</b><b style="color:#2E485A">1</b><b style="color:#193042">0</b><b style="color:#1A354D">0</b><b style="color:#11273C">0</b><b style="color:#112638">0</b><b style="color:#122536">1</b><b style="color:#12263A">1</b><b style="color:#142F4A">0</b><b style="color:#112334">0</b><b style="color:#102130">1</b><b style="color:#10212F">1</b><b style="color:#10212E">1</b><b style="color:#10202D">1</b><b style="color:#111E2B">1</b><b style="color:#121E2A">11</b><b style="color:#141E29">0</b><b style="color:#151E28">1</b><b style="color:#141D28">1</b><b style="color:#141C27">1</b><b style="color:#152338">1</b><b style="color:#182B46">1</b><b style="color:#131A27">1</b><b style="color:#131925">0</b><b style="color:#131B28">0</b><b style="color:#172B46">1</b><b style="color:#141E30">0</b><b style="color:#141824">0</b><b style="color:#151823">0</b><b style="color:#151722">1</b><b style="color:#151822">01</b><b style="color:#161823">1</b><b style="color:#171923">1</b><b style="color:#191D2B">0</b><b style="color:#1A1D2D">0</b><b style="color:#181924">1</b><b style="color:#191925">0</b><b style="color:#1B1A27">1</b><b style="color:#1D2338">0</b><b style="color:#1E2A44">0</b><b style="color:#263653">1</b><b style="color:#1E263C">0</b><b style="color:#171727">1</b><b style="color:#171725">1</b><b style="color:#171625">1</b><b style="color:#151625">0</b><b style="color:#151526">0</b><b style="color:#13182E">0</b><b style="color:#192A49">1</b><b style="color:#172641">1</b><b style="color:#111A2F">0</b><b style="color:#121B32">1</b><b style="color:#131325">1</b><b style="color:#121224">1</b><b style="color:#192034">1</b><b style="color:#20324D">1</b><b style="color:#1A263C">0</b><b style="color:#181F33">0</b><b style="color:#141426">1</b><b style="color:#151C32">0</b><b style="color:#17233B">1</b><b style="color:#182237">0</b><b style="color:#131525">0</b><b style="color:#10101F">0</b><b style="color:#11162C">1</b><b style="color:#101325">0</b><b style="color:#10121C">1</b><b style="color:#10111B">0</b><b style="color:#0F1019">01</b><b style="color:#131319">0</b><b style="color:#18161C">1</b><b style="color:#16141A">0</b><b style="color:#111117">0</b><b style="color:#101117">0</b><b style="color:#12121A">1</b><b style="color:#0E1016">1</b>
<b style="color:#093247">1</b><b style="color:#083249">0</b><b style="color:#083247">1</b><b style="color:#0A3448">1</b><b style="color:#0A344A">0</b><b style="color:#093349">1</b><b style="color:#0A354C">0</b><b style="color:#0A344B">0</b><b style="color:#0F384F">0</b><b style="color:#123C5A">1</b><b style="color:#143E5F">1</b><b style="color:#153B53">1</b><b style="color:#1C4150">0</b><b style="color:#1D4451">1</b><b style="color:#1C4252">0</b><b style="color:#1C4150">0</b><b style="color:#1E4455">1</b><b style="color:#224857">1</b><b style="color:#284E5C">1</b><b style="color:#284D57">1</b><b style="color:#1F475A">0</b><b style="color:#1D4455">0</b><b style="color:#284E5C">1</b><b style="color:#305766">0</b><b style="color:#244B5B">0</b><b style="color:#1E4556">0</b><b style="color:#1C4354">0</b><b style="color:#1C4860">1</b><b style="color:#1B4B6A">0</b><b style="color:#153D53">0</b><b style="color:#143E52">0</b><b style="color:#123B4E">0</b><b style="color:#0E3044">1</b><b style="color:#0F2C3E">0</b><b style="color:#133143">0</b><b style="color:#1D3F5B">1</b><b style="color:#173A59">0</b><b style="color:#112D40">0</b><b style="color:#122D3E">1</b><b style="color:#163040">0</b><b style="color:#173447">0</b><b style="color:#183243">1</b><b style="color:#132D3D">0</b><b style="color:#18303F">1</b><b style="color:#142C3B">0</b><b style="color:#19303E">1</b><b style="color:#1F3541">1</b><b style="color:#203747">0</b><b style="color:#233D4F">1</b><b style="color:#233B4C">1</b><b style="color:#122A40">0</b><b style="color:#122638">0</b><b style="color:#132635">0</b><b style="color:#172A39">1</b><b style="color:#15324B">0</b><b style="color:#112436">1</b><b style="color:#112330">0</b><b style="color:#10222F">1</b><b style="color:#142530">0</b><b style="color:#13212D">0</b><b style="color:#13202B">0</b><b style="color:#121E2A">0</b><b style="color:#111D29">0</b><b style="color:#151E28">1</b><b style="color:#161E27">1</b><b style="color:#141C26">0</b><b style="color:#111A25">0</b><b style="color:#131F2E">0</b><b style="color:#192E49">0</b><b style="color:#111A26">0</b><b style="color:#141B25">1</b><b style="color:#131D2B">1</b><b style="color:#162A45">0</b><b style="color:#131B2A">0</b><b style="color:#141922">0</b><b style="color:#131720">1</b><b style="color:#141721">10</b><b style="color:#191A23">0</b><b style="color:#191B23">1</b><b style="color:#1F1E25">1</b><b style="color:#23212B">1</b><b style="color:#1E212F">0</b><b style="color:#1A1B26">1</b><b style="color:#1A1925">0</b><b style="color:#1C1A27">0</b><b style="color:#24293E">0</b><b style="color:#26354F">1</b><b style="color:#29334A">1</b><b style="color:#1F1A26">1</b><b style="color:#201D28">0</b><b style="color:#1B1A25">0</b><b style="color:#221E26">1</b><b style="color:#141525">1</b><b style="color:#171827">0</b><b style="color:#18223D">0</b><b style="color:#20314D">1</b><b style="color:#161F32">0</b><b style="color:#141B2B">1</b><b style="color:#171F32">0</b><b style="color:#1A1926">0</b><b style="color:#141627">1</b><b style="color:#253449">0</b><b style="color:#222E3F">1</b><b style="color:#1F2534">1</b><b style="color:#1A1C27">0</b><b style="color:#191C29">1</b><b style="color:#1E2A41">1</b><b style="color:#1A2335">0</b><b style="color:#1F242E">1</b><b style="color:#1A1C25">0</b><b style="color:#161720">1</b><b style="color:#1F2331">0</b><b style="color:#1F222D">0</b><b style="color:#15171F">1</b><b style="color:#13151C">0</b><b style="color:#0F1018">1</b><b style="color:#0E1018">0</b><b style="color:#101119">0</b><b style="color:#111118">1</b><b style="color:#111219">1</b><b style="color:#100F16">1</b><b style="color:#141218">0</b><b style="color:#1C1C21">0</b><b style="color:#0E1115">1</b>
<b style="color:#0A3244">1</b><b style="color:#0C3447">1</b><b style="color:#093144">1</b><b style="color:#0A3245">0</b><b style="color:#093044">1</b><b style="color:#072F43">1</b><b style="color:#072F45">1</b><b style="color:#073147">1</b><b style="color:#092F47">1</b><b style="color:#0A314F">1</b><b style="color:#103758">0</b><b style="color:#0A304C">0</b><b style="color:#0D3348">1</b><b style="color:#0D3245">1</b><b style="color:#0A2D40">0</b><b style="color:#0A2D3F">1</b><b style="color:#113242">0</b><b style="color:#103343">1</b><b style="color:#113546">0</b><b style="color:#173C48">0</b><b style="color:#153B4D">1</b><b style="color:#103A55">0</b><b style="color:#0F374C">1</b><b style="color:#123849">0</b><b style="color:#123A4B">1</b><b style="color:#0D3447">0</b><b style="color:#0F3548">0</b><b style="color:#0B3247">1</b><b style="color:#12405C">1</b><b style="color:#113B54">1</b><b style="color:#10394C">1</b><b style="color:#0F384C">00</b><b style="color:#0D3347">1</b><b style="color:#0F3041">0</b><b style="color:#0E2E42">0</b><b style="color:#133858">0</b><b style="color:#13344D">1</b><b style="color:#122D3E">0</b><b style="color:#142F3F">1</b><b style="color:#163241">0</b><b style="color:#143143">0</b><b style="color:#122D3D">1</b><b style="color:#102A3B">1</b><b style="color:#0E2938">0</b><b style="color:#142E3C">1</b><b style="color:#152E3D">0</b><b style="color:#122939">0</b><b style="color:#143047">0</b><b style="color:#14334E">1</b><b style="color:#162F45">1</b><b style="color:#112736">0</b><b style="color:#122734">1</b><b style="color:#142835">0</b><b style="color:#193042">0</b><b style="color:#1E2F3C">0</b><b style="color:#2B373C">0</b><b style="color:#182936">0</b><b style="color:#1B2C34">0</b><b style="color:#182730">1</b><b style="color:#16232B">0</b><b style="color:#14202D">0</b><b style="color:#1F2A33">1</b><b style="color:#19242E">0</b><b style="color:#17242E">0</b><b style="color:#1C2830">0</b><b style="color:#152029">0</b><b style="color:#141F28">0</b><b style="color:#152639">1</b><b style="color:#141C26">1</b><b style="color:#1B2329">1</b><b style="color:#1A2129">0</b><b style="color:#242F3D">0</b><b style="color:#212730">1</b><b style="color:#191E26">1</b><b style="color:#1E212A">1</b><b style="color:#1A1E26">0</b><b style="color:#161A22">1</b><b style="color:#161820">00</b><b style="color:#161821">1</b><b style="color:#1B1D27">1</b><b style="color:#1A2132">0</b><b style="color:#1E212E">1</b><b style="color:#1C1F2B">0</b><b style="color:#1A1C29">0</b><b style="color:#1F273B">1</b><b style="color:#202C43">1</b><b style="color:#1D202F">1</b><b style="color:#1A1720">0</b><b style="color:#1C1E2A">1</b><b style="color:#1C1E2B">1</b><b style="color:#1D1E2A">0</b><b style="color:#181828">1</b><b style="color:#151A31">0</b><b style="color:#1C304E">1</b><b style="color:#18243C">1</b><b style="color:#13182A">1</b><b style="color:#131829">1</b><b style="color:#131C30">0</b><b style="color:#151523">0</b><b style="color:#192237">1</b><b style="color:#182237">1</b><b style="color:#181C2A">0</b><b style="color:#161622">0</b><b style="color:#111220">0</b><b style="color:#141C30">0</b><b style="color:#20222E">0</b><b style="color:#221F24">1</b><b style="color:#221E21">0</b><b style="color:#2B2525">1</b><b style="color:#232127">1</b><b style="color:#1F2533">1</b><b style="color:#1C1F29">0</b><b style="color:#16151B">1</b><b style="color:#14131A">0</b><b style="color:#111119">0</b><b style="color:#0F0F17">0</b><b style="color:#0C0D15">1</b><b style="color:#0C0C14">1</b><b style="color:#0B0C14">0</b><b style="color:#0C0C14">1</b><b style="color:#0C0B13">0</b><b style="color:#0C0A12">1</b><b style="color:#0A0A12">1</b>
<b style="color:#082D3F">0</b><b style="color:#0B3040">0</b><b style="color:#082D3F">1</b><b style="color:#072D3F">0</b><b style="color:#072C3E">01</b><b style="color:#0A2F42">1</b><b style="color:#0A2F41">0</b><b style="color:#082E41">1</b><b style="color:#082C3F">1</b><b style="color:#0A2E40">1</b><b style="color:#0E3141">1</b><b style="color:#103241">1</b><b style="color:#0E3141">0</b><b style="color:#173946">1</b><b style="color:#143643">0</b><b style="color:#0D2F40">00</b><b style="color:#0B3042">0</b><b style="color:#0B3144">0</b><b style="color:#123849">1</b><b style="color:#0D3649">1</b><b style="color:#113D55">1</b><b style="color:#133B4C">0</b><b style="color:#113949">0</b><b style="color:#0B3447">0</b><b style="color:#0A3246">0</b><b style="color:#0E3548">1</b><b style="color:#10364B">1</b><b style="color:#113851">1</b><b style="color:#153E51">1</b><b style="color:#224B5D">1</b><b style="color:#244E5F">1</b><b style="color:#1A4A5B">0</b><b style="color:#2B5C6B">1</b><b style="color:#2C5360">1</b><b style="color:#244356">1</b><b style="color:#324E67">0</b><b style="color:#304556">1</b><b style="color:#324E5C">1</b><b style="color:#3D5B66">1</b><b style="color:#385562">0</b><b style="color:#273F4A">1</b><b style="color:#1F3843">1</b><b style="color:#203A46">1</b><b style="color:#1B343F">0</b><b style="color:#152E3B">0</b><b style="color:#162F3C">0</b><b style="color:#172E3B">1</b><b style="color:#182E3D">1</b><b style="color:#112735">0</b><b style="color:#0C222E">0</b><b style="color:#0E232E">0</b><b style="color:#0E212D">1</b><b style="color:#10222D">1</b><b style="color:#15262F">0</b><b style="color:#14252E">1</b><b style="color:#10232D">0</b><b style="color:#0D1F29">0</b><b style="color:#101F28">0</b><b style="color:#121F27">1</b><b style="color:#152228">1</b><b style="color:#16232A">1</b><b style="color:#132029">1</b><b style="color:#14222B">1</b><b style="color:#152129">1</b><b style="color:#182229">1</b><b style="color:#141E23">0</b><b style="color:#171E24">0</b><b style="color:#1A2125">1</b><b style="color:#20252B">1</b><b style="color:#1D2229">1</b><b style="color:#2A2D32">1</b><b style="color:#2E3237">0</b><b style="color:#1E2127">1</b><b style="color:#202329">1</b><b style="color:#1F2329">0</b><b style="color:#26292D">1</b><b style="color:#25262E">1</b><b style="color:#232229">0</b><b style="color:#292A32">0</b><b style="color:#293233">1</b><b style="color:#2C3B3B">0</b><b style="color:#353D41">0</b><b style="color:#3F4549">1</b><b style="color:#3C4146">1</b><b style="color:#373B41">1</b><b style="color:#201D25">0</b><b style="color:#1A1822">1</b><b style="color:#191722">0</b><b style="color:#2F2F37">1</b><b style="color:#38373D">0</b><b style="color:#464447">0</b><b style="color:#403A3C">1</b><b style="color:#2A3144">1</b><b style="color:#1A2C49">0</b><b style="color:#14182D">0</b><b style="color:#151728">0</b><b style="color:#181C2A">1</b><b style="color:#1E2434">1</b><b style="color:#171C2B">1</b><b style="color:#20293A">0</b><b style="color:#202028">0</b><b style="color:#2C292B">1</b><b style="color:#252428">1</b><b style="color:#23252C">0</b><b style="color:#292D36">1</b><b style="color:#302F30">0</b><b style="color:#363330">0</b><b style="color:#33302E">1</b><b style="color:#2F2D2D">0</b><b style="color:#353B45">0</b><b style="color:#3A434F">1</b><b style="color:#1B1E28">0</b><b style="color:#13131A">0</b><b style="color:#14141C">1</b><b style="color:#19181E">1</b><b style="color:#1A191E">1</b><b style="color:#111217">0</b><b style="color:#0C0D14">0</b><b style="color:#0D0E15">1</b><b style="color:#0F1017">0</b><b style="color:#101017">11</b><b style="color:#0C0D14">0</b>
<b style="color:#122E3B">0</b><b style="color:#0E2C3B">0</b><b style="color:#0F2E3B">1</b><b style="color:#112E3B">0</b><b style="color:#102E3C">0</b><b style="color:#102F3C">1</b><b style="color:#0A2B3B">1</b><b style="color:#092B3C">0</b><b style="color:#0C2C3C">1</b><b style="color:#0D2D3D">0</b><b style="color:#0C2B3A">1</b><b style="color:#102E3B">1</b><b style="color:#14303C">1</b><b style="color:#15313C">1</b><b style="color:#17333E">0</b><b style="color:#17333F">0</b><b style="color:#13303D">1</b><b style="color:#10303F">1</b><b style="color:#0B2D3E">0</b><b style="color:#0F3141">0</b><b style="color:#1D3B45">0</b><b style="color:#1F3F49">0</b><b style="color:#22444E">0</b><b style="color:#2C4D56">0</b><b style="color:#254651">0</b><b style="color:#0C3346">1</b><b style="color:#153C4E">1</b><b style="color:#20414E">0</b><b style="color:#21404D">0</b><b style="color:#1C3F50">1</b><b style="color:#193F50">0</b><b style="color:#365C69">0</b><b style="color:#385861">0</b><b style="color:#33555F">1</b><b style="color:#355966">1</b><b style="color:#3C6371">1</b><b style="color:#456875">0</b><b style="color:#435D6A">1</b><b style="color:#395666">1</b><b style="color:#2D4A56">1</b><b style="color:#33515D">1</b><b style="color:#314C56">1</b><b style="color:#2B4147">1</b><b style="color:#1D363E">1</b><b style="color:#1A343E">1</b><b style="color:#162E37">0</b><b style="color:#152D37">1</b><b style="color:#253B43">1</b><b style="color:#354B52">1</b><b style="color:#374C50">0</b><b style="color:#2F454C">1</b><b style="color:#2E444C">1</b><b style="color:#2E434A">1</b><b style="color:#2A3D44">0</b><b style="color:#1A2D37">1</b><b style="color:#0D212D">1</b><b style="color:#091C28">0</b><b style="color:#0A1C27">1</b><b style="color:#0A1C26">1</b><b style="color:#0B1C26">1</b><b style="color:#0F1D26">0</b><b style="color:#0F1C24">1</b><b style="color:#0C1921">0</b><b style="color:#09161E">010</b><b style="color:#101A21">0</b><b style="color:#0D171E">1</b><b style="color:#121920">1</b><b style="color:#161C20">1</b><b style="color:#1B1E21">1</b><b style="color:#1E2024">0</b><b style="color:#222429">0</b><b style="color:#2B2F37">0</b><b style="color:#31353D">0</b><b style="color:#292D36">0</b><b style="color:#1D2026">1</b><b style="color:#222429">1</b><b style="color:#383C3F">1</b><b style="color:#2A282A">0</b><b style="color:#322F32">0</b><b style="color:#282423">0</b><b style="color:#34302D">0</b><b style="color:#39342D">0</b><b style="color:#54524B">0</b><b style="color:#504D49">1</b><b style="color:#3B373A">0</b><b style="color:#211B27">1</b><b style="color:#171327">1</b><b style="color:#14112A">1</b><b style="color:#121029">1</b><b style="color:#151128">0</b><b style="color:#201E30">1</b><b style="color:#1E2238">1</b><b style="color:#1F314F">0</b><b style="color:#121833">0</b><b style="color:#111126">01</b><b style="color:#111127">1</b><b style="color:#151529">0</b><b style="color:#141629">1</b><b style="color:#0F1122">1</b><b style="color:#10111F">1</b><b style="color:#111220">1</b><b style="color:#121220">0</b><b style="color:#141521">0</b><b style="color:#1B1A26">0</b><b style="color:#25232C">0</b><b style="color:#22222D">1</b><b style="color:#1D1D29">0</b><b style="color:#1B1B25">0</b><b style="color:#1C1C27">1</b><b style="color:#161822">1</b><b style="color:#10111A">1</b><b style="color:#0F0F17">1</b><b style="color:#101017">0</b><b style="color:#111117">1</b><b style="color:#111017">1</b><b style="color:#0F0E15">1</b><b style="color:#0E0E15">1</b><b style="color:#0F0E15">1</b><b style="color:#121118">1</b><b style="color:#111016">1</b><b style="color:#111117">1</b><b style="color:#0E0E15">1</b>
<b style="color:#183038">0</b><b style="color:#0D2836">0</b><b style="color:#17323C">1</b><b style="color:#293E40">0</b><b style="color:#273D41">1</b><b style="color:#21393E">0</b><b style="color:#072737">0</b><b style="color:#062738">0</b><b style="color:#092938">1</b><b style="color:#072737">1</b><b style="color:#082837">1</b><b style="color:#0A2A39">1</b><b style="color:#092937">1</b><b style="color:#0A2838">0</b><b style="color:#0B2A39">0</b><b style="color:#0C2F3D">0</b><b style="color:#06293A">1</b><b style="color:#05293B">1</b><b style="color:#04293C">0</b><b style="color:#062B3E">1</b><b style="color:#092E3F">1</b><b style="color:#082F41">0</b><b style="color:#0D3244">0</b><b style="color:#1C3F4A">0</b><b style="color:#133949">0</b><b style="color:#0B3345">0</b><b style="color:#254955">0</b><b style="color:#284851">1</b><b style="color:#28454D">0</b><b style="color:#305158">0</b><b style="color:#375A62">0</b><b style="color:#30535A">1</b><b style="color:#254852">1</b><b style="color:#2D515D">1</b><b style="color:#2F525D">0</b><b style="color:#2C4F5C">0</b><b style="color:#335864">0</b><b style="color:#335866">1</b><b style="color:#1F3F50">1</b><b style="color:#0A2939">1</b><b style="color:#0A2937">1</b><b style="color:#082736">1</b><b style="color:#072636">1</b><b style="color:#072535">0</b><b style="color:#062433">0</b><b style="color:#072534">1</b><b style="color:#162E38">1</b><b style="color:#263A41">1</b><b style="color:#364A50">1</b><b style="color:#3F5155">1</b><b style="color:#3B4C50">0</b><b style="color:#425458">0</b><b style="color:#43565B">1</b><b style="color:#3C4C4F">1</b><b style="color:#25363C">0</b><b style="color:#152933">1</b><b style="color:#253234">0</b><b style="color:#252B2B">1</b><b style="color:#122027">0</b><b style="color:#0B1C26">1</b><b style="color:#121F26">1</b><b style="color:#101E25">0</b><b style="color:#0E1C23">0</b><b style="color:#0D1A21">1</b><b style="color:#0D1A22">0</b><b style="color:#17222A">0</b><b style="color:#121C23">1</b><b style="color:#101A21">0</b><b style="color:#131D25">0</b><b style="color:#0F181F">0</b><b style="color:#0F151D">1</b><b style="color:#12171F">1</b><b style="color:#1A1F28">0</b><b style="color:#2E323A">1</b><b style="color:#3A3E45">1</b><b style="color:#2C3036">0</b><b style="color:#1E1F24">1</b><b style="color:#1F1F23">1</b><b style="color:#2F3132">1</b><b style="color:#272222">0</b><b style="color:#302722">0</b><b style="color:#3B2D22">1</b><b style="color:#4C4031">1</b><b style="color:#595243">0</b><b style="color:#625D52">0</b><b style="color:#52453A">0</b><b style="color:#35292A">1</b><b style="color:#302730">1</b><b style="color:#312638">0</b><b style="color:#342B4F">1</b><b style="color:#2C2551">1</b><b style="color:#231F40">0</b><b style="color:#23203A">1</b><b style="color:#27314C">10</b><b style="color:#232438">11</b><b style="color:#22233B">1</b><b style="color:#2A2846">1</b><b style="color:#232541">1</b><b style="color:#222439">1</b><b style="color:#1F2132">0</b><b style="color:#1B1D2D">0</b><b style="color:#191A2A">0</b><b style="color:#201F2C">1</b><b style="color:#252634">1</b><b style="color:#222331">1</b><b style="color:#1F1F2F">0</b><b style="color:#212135">1</b><b style="color:#2B2C42">0</b><b style="color:#1F1F35">1</b><b style="color:#181626">1</b><b style="color:#14121F">1</b><b style="color:#14111B">1</b><b style="color:#12101A">0</b><b style="color:#111018">0</b><b style="color:#100F17">0</b><b style="color:#0E0D15">01</b><b style="color:#0F0E16">0</b><b style="color:#100F17">1</b><b style="color:#100F16">1</b><b style="color:#0F0E15">1</b><b style="color:#100F15">0</b><b style="color:#101016">1</b>
<b style="color:#112B31">1</b><b style="color:#162E36">0</b><b style="color:#1A323B">1</b><b style="color:#1C373E">0</b><b style="color:#142F37">0</b><b style="color:#163138">0</b><b style="color:#19343C">0</b><b style="color:#16323B">1</b><b style="color:#062534">0</b><b style="color:#092735">1</b><b style="color:#062635">1</b><b style="color:#072736">0</b><b style="color:#082836">0</b><b style="color:#062636">1</b><b style="color:#052638">0</b><b style="color:#042738">1</b><b style="color:#04283A">0</b><b style="color:#04283B">1</b><b style="color:#042A3C">1</b><b style="color:#042A3D">0</b><b style="color:#042B3E">0</b><b style="color:#042C40">1</b><b style="color:#052E42">0</b><b style="color:#042E42">1</b><b style="color:#042F43">0</b><b style="color:#073145">0</b><b style="color:#083245">0</b><b style="color:#0C3647">1</b><b style="color:#103849">0</b><b style="color:#123B4C">1</b><b style="color:#1A404E">1</b><b style="color:#0D3749">0</b><b style="color:#073348">0</b><b style="color:#0B3548">1</b><b style="color:#123B4D">1</b><b style="color:#1C414D">0</b><b style="color:#204654">1</b><b style="color:#234D5E">1</b><b style="color:#143D4E">0</b><b style="color:#0A3144">0</b><b style="color:#0A2B3C">1</b><b style="color:#0A2938">0</b><b style="color:#082737">0</b><b style="color:#082837">0</b><b style="color:#0A2A38">0</b><b style="color:#0C2C3A">1</b><b style="color:#092A38">1</b><b style="color:#102D37">0</b><b style="color:#162C37">1</b><b style="color:#21343B">1</b><b style="color:#142831">0</b><b style="color:#0E2633">0</b><b style="color:#172C35">0</b><b style="color:#1F2F33">1</b><b style="color:#10232B">0</b><b style="color:#192C34">0</b><b style="color:#374A4F">1</b><b style="color:#2D3736">0</b><b style="color:#242F31">0</b><b style="color:#283537">0</b><b style="color:#333F3D">1</b><b style="color:#364340">0</b><b style="color:#2D3B3C">0</b><b style="color:#1E2B2E">0</b><b style="color:#19232A">1</b><b style="color:#242E34">0</b><b style="color:#1B232A">1</b><b style="color:#283236">1</b><b style="color:#323B41">0</b><b style="color:#22282C">0</b><b style="color:#1F2024">0</b><b style="color:#1A1B1E">0</b><b style="color:#1A1B1F">0</b><b style="color:#222021">1</b><b style="color:#252424">0</b><b style="color:#343630">0</b><b style="color:#282420">0</b><b style="color:#251D1B">1</b><b style="color:#2C221D">0</b><b style="color:#332B22">0</b><b style="color:#41382C">0</b><b style="color:#595347">1</b><b style="color:#575141">1</b><b style="color:#534C3A">1</b><b style="color:#4D4A3B">1</b><b style="color:#403B37">1</b><b style="color:#3B373C">1</b><b style="color:#36323F">1</b><b style="color:#393643">1</b><b style="color:#404252">1</b><b style="color:#474253">1</b><b style="color:#4D4755">0</b><b style="color:#4C4553">1</b><b style="color:#4F4D59">0</b><b style="color:#4A4652">0</b><b style="color:#3F414F">0</b><b style="color:#3D3F4D">1</b><b style="color:#3B3C4C">0</b><b style="color:#393D4D">1</b><b style="color:#39404E">1</b><b style="color:#404852">1</b><b style="color:#4D535A">0</b><b style="color:#494F58">1</b><b style="color:#414753">1</b><b style="color:#424954">0</b><b style="color:#3B424D">0</b><b style="color:#3B404B">1</b><b style="color:#41444D">1</b><b style="color:#474449">0</b><b style="color:#5D5856">1</b><b style="color:#494045">1</b><b style="color:#372D35">0</b><b style="color:#292531">0</b><b style="color:#261F29">0</b><b style="color:#222028">1</b><b style="color:#1F2027">0</b><b style="color:#25272D">0</b><b style="color:#2A2A30">0</b><b style="color:#1A1A1F">0</b><b style="color:#17181D">1</b><b style="color:#191A1F">0</b><b style="color:#1C1D22">1</b><b style="color:#1C1D24">1</b><b style="color:#1A1D24">1</b><b style="color:#181A22">0</b>
<b style="color:#424E44">1</b><b style="color:#415148">1</b><b style="color:#2E413E">1</b><b style="color:#384E4B">0</b><b style="color:#324945">1</b><b style="color:#273C3C">0</b><b style="color:#293D3B">0</b><b style="color:#2A403B">0</b><b style="color:#1D3533">0</b><b style="color:#0C2933">0</b><b style="color:#082634">0</b><b style="color:#052435">0</b><b style="color:#052536">0</b><b style="color:#042739">0</b><b style="color:#022739">1</b><b style="color:#03273B">0</b><b style="color:#03283B">1</b><b style="color:#042A3D">1</b><b style="color:#042B3D">1</b><b style="color:#042B3E">0</b><b style="color:#042C40">1</b><b style="color:#042D41">0</b><b style="color:#042F44">1</b><b style="color:#042F45">0</b><b style="color:#043046">1</b><b style="color:#043047">0</b><b style="color:#053047">0</b><b style="color:#043248">0</b><b style="color:#053249">0</b><b style="color:#06334A">0</b><b style="color:#07354B">0</b><b style="color:#07354C">00</b><b style="color:#08364C">1</b><b style="color:#0D3A4C">0</b><b style="color:#133E4E">1</b><b style="color:#08354A">0</b><b style="color:#07354B">0</b><b style="color:#08364C">0</b><b style="color:#09384D">1</b><b style="color:#0C394C">1</b><b style="color:#173D49">1</b><b style="color:#0C2E3D">1</b><b style="color:#0C343E">1</b><b style="color:#143B43">1</b><b style="color:#15414A">0</b><b style="color:#184048">0</b><b style="color:#194048">0</b><b style="color:#0A2A38">0</b><b style="color:#042231">0</b><b style="color:#052331">0</b><b style="color:#04212F">1</b><b style="color:#0A2531">1</b><b style="color:#0E2530">0</b><b style="color:#0B202D">1</b><b style="color:#0C232F">0</b><b style="color:#102733">0</b><b style="color:#102530">1</b><b style="color:#0E222D">0</b><b style="color:#12242E">1</b><b style="color:#10242C">1</b><b style="color:#11242B">1</b><b style="color:#0C1D24">0</b><b style="color:#102025">0</b><b style="color:#0F1C24">1</b><b style="color:#0E1B22">0</b><b style="color:#0C171D">0</b><b style="color:#0F181E">0</b><b style="color:#10191E">0</b><b style="color:#10171D">0</b><b style="color:#11161C">0</b><b style="color:#12151A">1</b><b style="color:#131618">0</b><b style="color:#1B1B1B">1</b><b style="color:#292927">0</b><b style="color:#2C2721">0</b><b style="color:#322519">1</b><b style="color:#413321">1</b><b style="color:#493D2D">0</b><b style="color:#51493F">1</b><b style="color:#5D5E5B">0</b><b style="color:#56524B">0</b><b style="color:#3E3125">1</b><b style="color:#342B1C">0</b><b style="color:#2C261A">1</b><b style="color:#2A2D27">0</b><b style="color:#2D3133">1</b><b style="color:#3F4049">0</b><b style="color:#3A4652">0</b><b style="color:#3E4550">1</b><b style="color:#433B45">1</b><b style="color:#403541">0</b><b style="color:#3F323F">1</b><b style="color:#40313E">0</b><b style="color:#3D2E3C">0</b><b style="color:#363144">0</b><b style="color:#353447">0</b><b style="color:#323347">1</b><b style="color:#2E3146">0</b><b style="color:#2D3144">1</b><b style="color:#363949">0</b><b style="color:#424753">0</b><b style="color:#50545E">0</b><b style="color:#5B5E63">1</b><b style="color:#4B525C">1</b><b style="color:#303947">0</b><b style="color:#323842">1</b><b style="color:#3A4046">0</b><b style="color:#3A3C3E">0</b><b style="color:#514E4C">0</b><b style="color:#5F5A55">1</b><b style="color:#505356">0</b><b style="color:#40464F">0</b><b style="color:#343840">0</b><b style="color:#29292E">0</b><b style="color:#252225">0</b><b style="color:#1F1E20">0</b><b style="color:#212222">1</b><b style="color:#282728">0</b><b style="color:#2F2E2C">0</b><b style="color:#3F3C38">1</b><b style="color:#44413D">0</b><b style="color:#3A3A3B">1</b><b style="color:#3F4347">1</b><b style="color:#2B2E32">0</b>
<b style="color:#0C202B">0</b><b style="color:#0A202A">0</b><b style="color:#031C29">0</b><b style="color:#051E2A">0</b><b style="color:#0A242F">0</b><b style="color:#07222D">0</b><b style="color:#07212D">1</b><b style="color:#07232E">0</b><b style="color:#04212E">1</b><b style="color:#02202E">0</b><b style="color:#03202F">0</b><b style="color:#02202F">0</b><b style="color:#042637">1</b><b style="color:#042F44">1</b><b style="color:#032D43">1</b><b style="color:#042E44">0</b><b style="color:#032F44">0</b><b style="color:#043046">1</b><b style="color:#043147">0</b><b style="color:#033046">1</b><b style="color:#033148">0</b><b style="color:#043248">1</b><b style="color:#043249">0</b><b style="color:#04334A">11</b><b style="color:#04334B">0</b><b style="color:#04344B">1</b><b style="color:#04344A">0</b><b style="color:#04354B">0</b><b style="color:#04354C">0</b><b style="color:#05364C">0</b><b style="color:#06374C">1</b><b style="color:#05364D">1</b><b style="color:#06374E">10</b><b style="color:#05364E">1</b><b style="color:#06374E">0</b><b style="color:#06364D">0</b><b style="color:#06354E">0</b><b style="color:#07364D">0</b><b style="color:#09374C">1</b><b style="color:#0B3A4E">1</b><b style="color:#08354A">1</b><b style="color:#0B3544">1</b><b style="color:#0B2E3C">0</b><b style="color:#062939">1</b><b style="color:#062838">0</b><b style="color:#092838">1</b><b style="color:#092837">1</b><b style="color:#042433">0</b><b style="color:#032232">1</b><b style="color:#04212F">1</b><b style="color:#05202D">0</b><b style="color:#061E2C">0</b><b style="color:#061C2A">1</b><b style="color:#061B28">0</b><b style="color:#051825">0</b><b style="color:#0C1E29">0</b><b style="color:#12222B">0</b><b style="color:#0B1B22">0</b><b style="color:#061720">0</b><b style="color:#051520">0</b><b style="color:#08151E">0</b><b style="color:#09151D">0</b><b style="color:#07141B">0</b><b style="color:#09141B">0</b><b style="color:#09131A">1</b><b style="color:#0A1218">1</b><b style="color:#0B1218">0</b><b style="color:#0D1118">1</b><b style="color:#0E1217">1</b><b style="color:#121516">1</b><b style="color:#171614">0</b><b style="color:#1A1614">0</b><b style="color:#241C17">0</b><b style="color:#37291E">1</b><b style="color:#4C3F2A">0</b><b style="color:#5D5A49">0</b><b style="color:#5F5F50">0</b><b style="color:#606258">1</b><b style="color:#5F635E">1</b><b style="color:#53493E">1</b><b style="color:#3B2B1F">1</b><b style="color:#2D2016">1</b><b style="color:#261E16">0</b><b style="color:#24221D">1</b><b style="color:#252526">1</b><b style="color:#30313A">1</b><b style="color:#2A313C">1</b><b style="color:#232530">1</b><b style="color:#231923">1</b><b style="color:#211723">1</b><b style="color:#211821">0</b><b style="color:#21181E">0</b><b style="color:#201922">1</b><b style="color:#1D1925">0</b><b style="color:#1C1B2A">1</b><b style="color:#1C1D30">1</b><b style="color:#191A29">1</b><b style="color:#171922">1</b><b style="color:#161820">1</b><b style="color:#1C1F2B">0</b><b style="color:#2B2F3D">1</b><b style="color:#41454E">0</b><b style="color:#3A4048">0</b><b style="color:#3E4349">0</b><b style="color:#383B3F">1</b><b style="color:#3C4043">1</b><b style="color:#3B3B3A">1</b><b style="color:#454444">0</b><b style="color:#4D4E51">1</b><b style="color:#505156">1</b><b style="color:#605F60">0</b><b style="color:#545759">0</b><b style="color:#30363A">0</b><b style="color:#362D2A">0</b><b style="color:#231D1C">0</b><b style="color:#181416">1</b><b style="color:#1F1818">1</b><b style="color:#271D18">0</b><b style="color:#3A3029">1</b><b style="color:#4F453B">1</b><b style="color:#433D38">1</b><b style="color:#292828">0</b><b style="color:#1A1818">1</b>
<b style="color:#021725">1</b><b style="color:#021825">1</b><b style="color:#041A26">0</b><b style="color:#061B27">0</b><b style="color:#071D29">1</b><b style="color:#081E29">1</b><b style="color:#0B212B">0</b><b style="color:#041B29">0</b><b style="color:#031B28">0</b><b style="color:#031A27">0</b><b style="color:#041B29">0</b><b style="color:#041A28">1</b><b style="color:#042131">1</b><b style="color:#042A3E">00</b><b style="color:#042B3F">11</b><b style="color:#042C40">0</b><b style="color:#042C41">0</b><b style="color:#042D41">0</b><b style="color:#032D42">0</b><b style="color:#042E43">010</b><b style="color:#052F44">0</b><b style="color:#042F45">0</b><b style="color:#033045">1</b><b style="color:#043046">11</b><b style="color:#053046">1</b><b style="color:#043148">1</b><b style="color:#043147">0</b><b style="color:#053147">1</b><b style="color:#043247">1</b><b style="color:#043147">1</b><b style="color:#043248">0</b><b style="color:#053248">10</b><b style="color:#053249">0</b><b style="color:#053248">0</b><b style="color:#053247">0</b><b style="color:#063146">000</b><b style="color:#062F44">0</b><b style="color:#052B3C">1</b><b style="color:#042536">1</b><b style="color:#042434">1</b><b style="color:#042433">0</b><b style="color:#032231">1</b><b style="color:#03212E">1</b><b style="color:#041E2B">1</b><b style="color:#051D2B">1</b><b style="color:#041A28">0</b><b style="color:#051A27">0</b><b style="color:#051824">0</b><b style="color:#051822">1</b><b style="color:#071A23">0</b><b style="color:#0D1D26">0</b><b style="color:#091923">1</b><b style="color:#0B1921">1</b><b style="color:#0A171E">0</b><b style="color:#08141B">1</b><b style="color:#07131A">1</b><b style="color:#071219">1</b><b style="color:#081118">1</b><b style="color:#081017">1</b><b style="color:#0A1016">0</b><b style="color:#0B1016">0</b><b style="color:#0C1016">1</b><b style="color:#0C1015">1</b><b style="color:#0F1214">1</b><b style="color:#121314">1</b><b style="color:#191615">0</b><b style="color:#261F1D">0</b><b style="color:#4E4940">0</b><b style="color:#60615A">0</b><b style="color:#5F6257">1</b><b style="color:#5D5945">0</b><b style="color:#5F5F4E">1</b><b style="color:#5F5F51">0</b><b style="color:#41301F">0</b><b style="color:#291910">0</b><b style="color:#1F140E">0</b><b style="color:#19100D">0</b><b style="color:#180F0D">1</b><b style="color:#160E0E">0</b><b style="color:#160F17">1</b><b style="color:#15101C">0</b><b style="color:#171213">0</b><b style="color:#110B0B">1</b><b style="color:#120C0B">0</b><b style="color:#110B0A">0</b><b style="color:#120D0B">1</b><b style="color:#100D0E">0</b><b style="color:#140F0A">1</b><b style="color:#1A1710">0</b><b style="color:#232521">0</b><b style="color:#131414">1</b><b style="color:#141413">0</b><b style="color:#1B1F20">0</b><b style="color:#1E2226">1</b><b style="color:#3D4143">0</b><b style="color:#3C4042">1</b><b style="color:#2D2C2E">1</b><b style="color:#36332F">0</b><b style="color:#292828">1</b><b style="color:#28282A">1</b><b style="color:#363A38">0</b><b style="color:#35383A">0</b><b style="color:#393C3A">0</b><b style="color:#2B2B2E">1</b><b style="color:#312F32">1</b><b style="color:#312F33">1</b><b style="color:#1D2028">0</b><b style="color:#14141A">0</b><b style="color:#131219">11</b><b style="color:#17161C">1</b><b style="color:#181518">1</b><b style="color:#171214">1</b><b style="color:#191414">0</b><b style="color:#191515">1</b><b style="color:#131111">1</b><b style="color:#131311">1</b>
<b style="color:#041621">0</b><b style="color:#01141F">00</b><b style="color:#021520">0</b><b style="color:#1B2B30">1</b><b style="color:#1E2E32">0</b><b style="color:#122328">0</b><b style="color:#0B1C25">0</b><b style="color:#14262D">1</b><b style="color:#12222A">1</b><b style="color:#0A1C26">0</b><b style="color:#061620">0</b><b style="color:#031A27">0</b><b style="color:#022131">1</b><b style="color:#042333">1</b><b style="color:#032233">0</b><b style="color:#032334">00</b><b style="color:#042435">1</b><b style="color:#042536">1</b><b style="color:#042537">00</b><b style="color:#042738">1</b><b style="color:#032638">1</b><b style="color:#042739">1</b><b style="color:#05283A">0</b><b style="color:#04283A">0</b><b style="color:#04293B">11</b><b style="color:#05293C">0</b><b style="color:#04293C">1</b><b style="color:#042A3D">0</b><b style="color:#052B3E">0</b><b style="color:#052B3D">0</b><b style="color:#052B3E">1</b><b style="color:#052C3E">0</b><b style="color:#052C3F">1</b><b style="color:#052C40">0</b><b style="color:#052D3F">0</b><b style="color:#052D40">1</b><b style="color:#062C40">11</b><b style="color:#062D40">001</b><b style="color:#072D41">1</b><b style="color:#052A3D">1</b><b style="color:#042435">1</b><b style="color:#031F2D">1</b><b style="color:#041F2C">1</b><b style="color:#061D2A">0</b><b style="color:#061C29">0</b><b style="color:#051A27">1</b><b style="color:#061925">1</b><b style="color:#051823">1</b><b style="color:#051721">0</b><b style="color:#051520">0</b><b style="color:#05141F">0</b><b style="color:#0C1A23">0</b><b style="color:#15232A">1</b><b style="color:#172228">1</b><b style="color:#121B20">0</b><b style="color:#0A1319">0</b><b style="color:#081117">0</b><b style="color:#070F16">0</b><b style="color:#080F15">1</b><b style="color:#090E14">1</b><b style="color:#0A0F14">0</b><b style="color:#0B0F14">0</b><b style="color:#0B0E14">1</b><b style="color:#0C0F13">1</b><b style="color:#101212">0</b><b style="color:#141212">1</b><b style="color:#1D1713">1</b><b style="color:#2A1F17">0</b><b style="color:#3D3327">1</b><b style="color:#575647">0</b><b style="color:#5E604A">0</b><b style="color:#5E583B">1</b><b style="color:#606049">1</b><b style="color:#59543A">1</b><b style="color:#33200E">1</b><b style="color:#23140C">1</b><b style="color:#1B100C">0</b><b style="color:#140D0B">0</b><b style="color:#120A0A">0</b><b style="color:#0F090A">1</b><b style="color:#0E080A">1</b><b style="color:#0E0809">1</b><b style="color:#0E0B0C">1</b><b style="color:#0C090B">0</b><b style="color:#0C0707">0</b><b style="color:#120E0B">0</b><b style="color:#110D0B">0</b><b style="color:#0A0608">0</b><b style="color:#19150F">1</b><b style="color:#2D2715">0</b><b style="color:#2A2619">0</b><b style="color:#15120F">1</b><b style="color:#15110F">0</b><b style="color:#2B251E">1</b><b style="color:#1E1B16">0</b><b style="color:#2C2A21">0</b><b style="color:#3E3C35">0</b><b style="color:#322C27">0</b><b style="color:#2F2823">1</b><b style="color:#3D352B">0</b><b style="color:#423A30">1</b><b style="color:#1D1713">1</b><b style="color:#191412">0</b><b style="color:#372E29">1</b><b style="color:#191519">1</b><b style="color:#0C0B11">1</b><b style="color:#0B0A10">1</b><b style="color:#0D0C10">0</b><b style="color:#0E0C11">0</b><b style="color:#0E0C12">1</b><b style="color:#181A21">0</b><b style="color:#121217">0</b><b style="color:#262221">1</b><b style="color:#2D2728">0</b><b style="color:#312D2E">1</b><b style="color:#322F30">0</b><b style="color:#292422">1</b><b style="color:#1F1A18">1</b>
<b style="color:#061118">0</b><b style="color:#020E16">0</b><b style="color:#000C15">0</b><b style="color:#010D15">1</b><b style="color:#09141A">1</b><b style="color:#0D191F">0</b><b style="color:#061119">1</b><b style="color:#020E16">0</b><b style="color:#071218">1</b><b style="color:#0E171C">0</b><b style="color:#071017">0</b><b style="color:#050E14">1</b><b style="color:#020F17">1</b><b style="color:#02111A">0</b><b style="color:#04141D">0</b><b style="color:#03151E">0</b><b style="color:#0B1D27">0</b><b style="color:#10212A">0</b><b style="color:#091D26">0</b><b style="color:#041923">0</b><b style="color:#041823">1</b><b style="color:#051824">0</b><b style="color:#061A25">0</b><b style="color:#051A26">1</b><b style="color:#041A26">1</b><b style="color:#051B28">0</b><b style="color:#041B28">0</b><b style="color:#051D2A">0</b><b style="color:#051E2B">00</b><b style="color:#061F2C">1</b><b style="color:#061F2D">1</b><b style="color:#05202E">0</b><b style="color:#06212F">01</b><b style="color:#05212F">0</b><b style="color:#052231">0</b><b style="color:#062232">0</b><b style="color:#062333">0</b><b style="color:#062334">1</b><b style="color:#072434">0</b><b style="color:#062334">0</b><b style="color:#062535">1</b><b style="color:#072636">0</b><b style="color:#092736">0</b><b style="color:#062536">1</b><b style="color:#072637">10</b><b style="color:#062231">1</b><b style="color:#051B28">0</b><b style="color:#051825">1</b><b style="color:#051824">1</b><b style="color:#061722">1</b><b style="color:#071721">1</b><b style="color:#07161F">0</b><b style="color:#06141D">0</b><b style="color:#06141C">1</b><b style="color:#06131A">1</b><b style="color:#071219">00</b><b style="color:#071017">0</b><b style="color:#070F16">0</b><b style="color:#091017">0</b><b style="color:#0C1217">1</b><b style="color:#161616">1</b><b style="color:#0D1114">1</b><b style="color:#090E13">11</b><b style="color:#0B0F13">0</b><b style="color:#0C1014">0</b><b style="color:#0E1215">0</b><b style="color:#111312">1</b><b style="color:#181510">0</b><b style="color:#20180E">1</b><b style="color:#352611">0</b><b style="color:#4F472D">1</b><b style="color:#5C5E49">0</b><b style="color:#5E5C43">0</b><b style="color:#5E5737">1</b><b style="color:#606150">1</b><b style="color:#5C5B48">1</b><b style="color:#50452B">1</b><b style="color:#372711">0</b><b style="color:#1E1107">1</b><b style="color:#1C140F">1</b><b style="color:#17110F">0</b><b style="color:#100A09">1</b><b style="color:#0D0709">1</b><b style="color:#0A0708">0</b><b style="color:#080609">0</b><b style="color:#070507">0</b><b style="color:#080507">1</b><b style="color:#09070A">0</b><b style="color:#0C0B0D">1</b><b style="color:#070509">1</b><b style="color:#06040A">1</b><b style="color:#050409">1</b><b style="color:#040408">0</b><b style="color:#050508">0</b><b style="color:#070709">0</b><b style="color:#0D0A0A">1</b><b style="color:#0A090B">1</b><b style="color:#060609">1</b><b style="color:#08080A">1</b><b style="color:#0A090B">1</b><b style="color:#0A0B0D">1</b><b style="color:#100F0F">0</b><b style="color:#191512">1</b><b style="color:#0B090B">0</b><b style="color:#0D0A0B">1</b><b style="color:#0C0A0B">1</b><b style="color:#09080A">1</b><b style="color:#08080A">0</b><b style="color:#07060A">1</b><b style="color:#09080B">0</b><b style="color:#09080C">0</b><b style="color:#06060A">1</b><b style="color:#09080E">0</b><b style="color:#07060A">1</b><b style="color:#070709">0</b><b style="color:#0B0A0C">0</b><b style="color:#0E0D0F">0</b><b style="color:#0E0E10">0</b><b style="color:#0C0C0D">1</b><b style="color:#0B0A0C">0</b>
<b style="color:#040609">1</b><b style="color:#010406">1</b><b style="color:#000305">0</b><b style="color:#000306">0</b><b style="color:#040508">0</b><b style="color:#010306">1</b><b style="color:#000306">1</b><b style="color:#010407">00</b><b style="color:#020306">1</b><b style="color:#050305">1</b><b style="color:#070406">1</b><b style="color:#010204">0</b><b style="color:#020205">0</b><b style="color:#010305">1</b><b style="color:#07090B">0</b><b style="color:#1C1F1F">1</b><b style="color:#1D1F1D">0</b><b style="color:#0E1413">1</b><b style="color:#04090C">0</b><b style="color:#03070D">1</b><b style="color:#03080D">0</b><b style="color:#04090F">0</b><b style="color:#060B12">1</b><b style="color:#060C13">1</b><b style="color:#060D15">1</b><b style="color:#060E16">1</b><b style="color:#071018">1</b><b style="color:#071119">0</b><b style="color:#06111A">0</b><b style="color:#06141E">0</b><b style="color:#07151F">1</b><b style="color:#071520">1</b><b style="color:#071824">1</b><b style="color:#081824">1</b><b style="color:#071925">0</b><b style="color:#061722">0</b><b style="color:#071A26">1</b><b style="color:#081925">0</b><b style="color:#071A27">1</b><b style="color:#0F2029">0</b><b style="color:#0C1D27">0</b><b style="color:#061B29">0</b><b style="color:#061A27">1</b><b style="color:#071D2B">0</b><b style="color:#071C2A">1</b><b style="color:#071D2A">0</b><b style="color:#071D2B">1</b><b style="color:#071F2C">0</b><b style="color:#071D2A">0</b><b style="color:#06151E">1</b><b style="color:#06121A">10</b><b style="color:#061219">0</b><b style="color:#071118">01</b><b style="color:#071016">011</b><b style="color:#081016">0</b><b style="color:#080F15">0</b><b style="color:#080E14">1</b><b style="color:#0A0F14">1</b><b style="color:#101416">1</b><b style="color:#1B1A18">0</b><b style="color:#0B1013">0</b><b style="color:#0A0F13">1</b><b style="color:#0C1013">1</b><b style="color:#0C1113">0</b><b style="color:#0E1415">1</b><b style="color:#202A28">1</b><b style="color:#1D251D">0</b><b style="color:#181811">0</b><b style="color:#1A140D">0</b><b style="color:#23160B">1</b><b style="color:#4A422D">1</b><b style="color:#616351">1</b><b style="color:#5E5B42">1</b><b style="color:#5E583D">0</b><b style="color:#5F6052">1</b><b style="color:#606359">0</b><b style="color:#605D45">1</b><b style="color:#3C2D15">1</b><b style="color:#282012">1</b><b style="color:#1B150F">0</b><b style="color:#150F0D">1</b><b style="color:#130D09">10</b><b style="color:#0D0808">0</b><b style="color:#0A0808">1</b><b style="color:#0E0C0C">0</b><b style="color:#0F0E0D">0</b><b style="color:#151413">0</b><b style="color:#1B1C1B">1</b><b style="color:#100F12">0</b><b style="color:#0A080D">1</b><b style="color:#070508">1</b><b style="color:#050507">0</b><b style="color:#050407">1</b><b style="color:#060608">1</b><b style="color:#08080A">0</b><b style="color:#141619">1</b><b style="color:#0A0A0D">0</b><b style="color:#060608">10</b><b style="color:#111215">0</b><b style="color:#101113">0</b><b style="color:#09090D">0</b><b style="color:#060609">0</b><b style="color:#040408">111</b><b style="color:#050407">1</b><b style="color:#040407">1</b><b style="color:#040408">0</b><b style="color:#070508">1</b><b style="color:#060507">0</b><b style="color:#050407">0</b><b style="color:#050509">1</b><b style="color:#050508">1</b><b style="color:#050507">1</b><b style="color:#050406">00</b><b style="color:#050507">11</b>
</pre>
    """
    import lxml
    import lxml.html
    from lxml import etree
    tree = lxml.html.fromstring(aart)
    styles = tree.xpath('//b//@style')
    for style in styles:
        color = style.split(':')[1]
        hex3 = color_hex6_to_hex3(color)
        #print("\t", color, "-->", hex3)
        style.getparent().attrib['style'] = "color:" + hex3
        
    content = etree.tostring(tree).decode("utf-8")
    print(content)
    string_to_file(content, "D:/__BUP_V_KOMPLETT/X/111_BUP/33projects/2022/2022-karlsruhe.digital/2022/sitemap/scraped/ascii-art/" + "bunte_nacht_der_digitalisierung_hero_slider__not-bad__pre3color.html")
    

    
    # "C:/Users/michaelsaup/Downloads/287305871_1050848149176283_8014478396700614358_n.jpg"
    # https://towardsdatascience.com/image-segmentation-using-pythons-scikit-image-module-533a61ecc980
    exit(0)           