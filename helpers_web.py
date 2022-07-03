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
def pa(s=""):
    return "(" + str(s) + ")"

#-----------------------------------------
# 
#-----------------------------------------
def vt_b(b_val):
    return (GREEN if b_val else RED) + str(b_val)[0] + RESET
    #return (GREEN if b_val else RED) + str(int(b_val)) + RESET
def vt_code(code):
    return (GREEN if code < 400 else RED) + str(code) + RESET
    #return (GREEN if b_val else RED) + str(int(b_val)) + RESET
    
def _saved_percent(size_orig, size_new):
    assert size_orig > 0
    perc = 100 - (size_new/size_orig*100)
    return perc

def vt_saved_percent_string(size_orig, size_new):
    pct = _saved_percent(size_orig, size_new)
    vt  = RED if pct <= 0 else GREEN
    return "{}{:+.1f}%{}".format(vt, pct, RESET)
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
    assert loc_base, "loc_base is None"
    
    ret = False
    if not loc_url: # local url
        ret = True
    else:
        tld_url  =  tldextract.extract(url) 
        tld_base =  tldextract.extract(base) 
        ret = (tld_url.domain == tld_base.domain)
        print("\n", GREEN, tld_url, GRAY, tld_base, RESET)
        
    #print("url_is_internal:", GREEN if ret else YELLOW, ret, RESET, "| loc_url:", dq(loc_url), "| loc_base:", dq(loc_base))
    print("url_is_internal:", YELLOW, int(ret), GREEN, dq(url), GRAY, dq(base), RESET)
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

def links_sanitize(links):
    links = links_make_unique(links)
    links = links_remove_comments(links, delim='#')
    links = links_remove_similar(links)
    links = links_remove_nones(links)
    return sorted(links)

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


# # # def __extract_css(style_string, parse_func): # parse_func=cssutils.parseString
# # #     urls  = []
# # #     try:
# # #         cssutils.log.setLevel(logging.CRITICAL)
# # #         sheet = parse_func(style_string)
# # #         print ("__extract_css: sheet.cssText:", MAGENTA, sheet.cssText, RESET)
# # #         for rule in sheet:
# # #             if rule.type == rule.STYLE_RULE:
# # #                 for property in rule.style:
# # #                     if property.name == 'background-image':
# # #                         if "url" in property.value:
# # #                             url = property.value.replace("(", "").replace(")", "")
# # #                             url = url.strip().lstrip("url")
# # #                             print("\t\t\t", CYAN, url, RESET)
# # #                             urls.append(url)
# # #     except Exception as e:
# # #         print(f"{RED}__extract_css: cssutils.parseString {e} {RESET}")
    
# # #     return urls   

def extract_background_image(property):
    try:
        if property.name == 'background-image':
            if "url" in property.value:
                url = property.value.replace("(", "").replace(")", "")
                url = url.strip().lstrip("url")
                print("\t\t\t", CYAN, url, RESET)
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
                    url = extract_background_image(property)
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
            url = extract_background_image(property)
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
    
    content = replace_all(content, "\n", " ")
    content = replace_all(content, "\t", " ")
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
    
def html_minify(content, vb=True):
    
    length_orig = len(content)
    
    if length_orig > 0:
        # pip install htmlmin
        
        import htmlmin
        try:
            # https://htmlmin.readthedocs.io/en/latest/reference.html
            content = htmlmin.minify(
                content, 
                remove_comments=True, 
                remove_empty_space=True,
                remove_all_empty_space=True,
                reduce_boolean_attributes=True,
                reduce_empty_attributes=True,
                remove_optional_attribute_quotes=False, # ??????? True TODO
                convert_charrefs=True,
                keep_pre=True,
                )
        except:
            print(f"{RED}could not htmlmin.minify!{RESET}")
         
        if False:   
            content = html_sanitize(content, vb)
            
        if vb:
            print(
                "html_minify: final len(content)", len(content), 
                "|", 
                "percent_saved:", vt_saved_percent_string(length_orig, len(content)))
    
    return content

def minify_on_disk(filename):

    print("minify_on_disk:", filename)
    
    # with open(filename, "r", encoding="utf-8") as file:
    #     data = file.read()
                
    # with open(filename, "w", encoding="utf-8") as file:
    #     file.write(html_minify(data))
    #     file.close()    
        
    data = string_from_file(filename)
    data = html_minify(data)
    string_to_file(data, filename)
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
# def replace_in_file(filename, string_from, string_to):
    
#     fp = open(filename, "rt")
#     data = fp.read()
#     data = data.replace(string_from, string_to)
#     fp.close()
    
#     #open the input file in write mode
#     fp = open(filename, "wt")
#     fp.write(data)
#     fp.close()

def replace_all_in_file_OLD(filename, string_from, string_to):
    
    #print("replace_all_in_file:", filename)
    
    # read and replace
    fp = open(filename, "r", encoding="utf-8")
    data = fp.read()
    
    cnt = data.count(string_from)
    if cnt > 0:
        print("replace_all_in_file:", cnt, "|", CYAN + string_from + RESET, "-->", string_to)
    
    data = replace_all(data, string_from, string_to)
    fp.close()
    
    # write changes
    fp = open(filename, "w", encoding="utf-8")
    fp.write(data)
    fp.close()
    
def replace_all_in_file(filename, string_from, string_to):
    
    #print("replace_all_in_file:", filename)
    
    with open(filename, "r", encoding="utf-8") as fp:
        data = fp.read()
        
    cnt = data.count(string_from)
    if cnt > 0:
        print("replace_all_in_file:", cnt, "|", CYAN + string_from + RESET, "-->", string_to)
    data = replace_all(data, string_from, string_to)  
    
    with open(filename, "w", encoding="utf-8") as fp:
        fp.write(data)
                
                
    
                  
# -----------------------------------------
#
# -----------------------------------------
def list_from_file(path, mode="r", encoding="utf-8", sanitize=False):
    with open(path, mode=mode, encoding=encoding) as file:
        ret = [line.strip() for line in file]
        if sanitize:
            ret = links_sanitize(ret)
        return ret
    
def list_to_file(items, path, mode="w", encoding="utf-8"):
    # # print("list_to_file", path)
    # # with open(path, mode=mode, encoding=encoding) as file:
    # #     file.write(list_to_string(items))
    string_to_file(list_to_string(items), path, mode=mode, encoding=encoding)
 
def list_to_string(items):
    return "\n".join(str(item) for item in items)

def string_from_file(path, sanitize=False):
    return list_to_string(list_from_file(path, sanitize=sanitize))

def string_to_file(string, path, mode="w", encoding="utf-8"):
    print("string_to_file", GRAY, path, RESET)
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
def sanitize_filepath_and_url(filepath,  rep = '_'):
    fixedpath = filepath
    #fixedpath = fixedpath.replace('?',  rep) # is valid for url
    fixedpath = fixedpath.replace('%',  rep)
    fixedpath = fixedpath.replace('*',  rep)
    fixedpath = fixedpath.replace(':',  rep)
    fixedpath = fixedpath.replace('|',  rep)
    fixedpath = fixedpath.replace('\"', rep)
    fixedpath = fixedpath.replace('\'', rep)
    fixedpath = fixedpath.replace('<',  rep)
    fixedpath = fixedpath.replace('>',  rep)
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

def get_project_total_size(project_folder):
    
    def __get_sizes(func):
        total_size = 0
        for file in collect_files_func(project_folder, func=func):
            if os.path.isfile(file):
                total_size += os.path.getsize(file)
        return total_size
                  
    f_originals=lambda file : any(file.lower().endswith(ext) for ext in [
        ".jpg", ".jpeg", ".png", ".gif", 
        ".pdf", 
        "index_original.html"
    ])
    total_size_originals = __get_sizes(f_originals)

    f_unpowered=lambda file : any(file.lower().endswith(ext) for ext in [
        "_unpowered.webp", 
        "_unpowered_screen.pdf", 
        "index.html"
    ])
    total_size_unpowered = __get_sizes(f_unpowered)
    
    perc100 = _saved_percent(total_size_originals, total_size_unpowered)
    
    print("get_project_total_size:", vt_saved_percent_string(total_size_originals, total_size_unpowered))
    
    return perc100

              
              
    
#-----------------------------------------
# 
#-----------------------------------------
def to_posix(filepath):
    return pathlib.Path(filepath).as_posix()
 
#-----------------------------------------
# 
#-----------------------------------------
#https://pypi.org/project/art/ 
import art
def logo(text,  font="tarty3", vt=CYAN, npad=2, secs=2): # tarty3 tarty7 sub-zero
    nl = "\n"*npad
    print(nl + vt + art.text2art(text, font=font) + RESET + nl)
    time.sleep(secs)
    
def logo_filename(filename,  font="tarty3", vt=MAGENTA, npad=2): # tarty3 tarty7 sub-zero
    text = os.path.splitext(os.path.basename(filename))[0]
    logo(text,  font=font, vt=vt, npad=npad)
    
#-----------------------------------------
# 
#-----------------------------------------

def image_has_transparency(img):
    if img.info.get("transparency", None) is not None:
        return True
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True

    return False

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
# 
#-----------------------------------------

#-----------------------------------------
# 
#-----------------------------------------
if __name__ == "__main__":
    logo_filename(__file__)
    print("\n"*3 + "you started the wrong file..." + "\n"*3)
    
    # # https://stackoverflow.com/questions/17388213/find-the-similarity-metric-between-two-strings
    # import jellyfish
    # a = "https://domain.com/has/just/forgotten/slash/"
    # b = "https://domain.com/has/just/forgotten/slash"
    
    # a = "https://domain.com/has/just/forgotten/slash/"
    # b = "http://domain.com/has/just/forgotten/slash"
    
    # a = "https://google.com"
    # b = "https://apple.de/"
    
    # print( jellyfish.levenshtein_distance(a, b) )
    # print( jellyfish.jaro_distance(a, b) )
    # print( jellyfish.damerau_levenshtein_distance(a, b) )
    # print( jellyfish.jaro_winkler_similarity(a, b) )
    # print( jellyfish.hamming_distance(a, b) )
    # print( jellyfish.match_rating_comparison(a, b) )
    
    
    #get_path_local_root_subdomains('', '')
    #get_path_local_root_subdomains('/', '/')
    get_path_local_root_subdomains('', 'karlsruhe.digital/')
    get_path_local_root_subdomains('', 'https://karlsruhe.digital/')
    #get_path_local_root_subdomains('karlsruhe.digital/', '')
    #get_path_local_root_subdomains('https://karlsruhe.digital/', '')
    get_path_local_root_subdomains('local/image.png', 'karlsruhe.digital/')
    get_path_local_root_subdomains('/local/image.png', 'https://karlsruhe.digital/')
    get_path_local_root_subdomains('karlsruhe.digital/local/image.png', 'https://karlsruhe.digital/')
    get_path_local_root_subdomains('media.karlsruhe.digital/local/image.png', 'https://karlsruhe.digital/')


    # print(wh.url_is_external("", ""))
    # print(wh.url_is_external("xxx", ""))
    print(url_is_external("", "https://karlsruhe.digital/"))
    print(url_is_external(".path", "https://karlsruhe.digital/"))
    print(url_is_external("path", "https://karlsruhe.digital/"))
    print(url_is_external("/path", "https://karlsruhe.digital/"))
    print(url_is_external("/path/", "https://karlsruhe.digital/"))
    print(url_is_external("index.html", "https://karlsruhe.digital/"))
    print(url_is_external("karlsruhe.digital", "https://karlsruhe.digital/"))
    print(url_is_external("karlsruhe.digital/index.html", "https://karlsruhe.digital/"))
    print(url_is_external("karlsruhe.digital/index.html", "https://karlsruhe.digital/"))
    print(url_is_external("karlsruhe.digital/index.html", "https://karlsruhe.digital/"))
    print(url_is_external("media.karlsruhe.digital/index.html", "https://karlsruhe.digital/"))
    print(url_is_external("media.karlsruhe.digital/folder/index.html", "https://karlsruhe.digital/"))
    print(url_is_external("zkm.de", "https://karlsruhe.digital/"))
    
    exit(0)           