"""
TODO
"https:\/\/karlsruhe.digital\/wp-includes\/js\/wp-emoji-release.min.js?ver=5.2.15"
https://stackoverflow.com/questions/6076229/escaping-a-forward-slash-in-a-regular-expression


https:\/\/karlsruhe.digital\/



"""

# -----------------------------------------
# init the colorama module
# -----------------------------------------
from helpers_web import sq as sq, url_path
from helpers_web import dq as dq
from bs4 import BeautifulSoup, Comment
import time
import helpers_web as wh
import os
import requests
import lxml.html
import chromedriver_binary  # pip install chromedriver-binary-auto
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver  # pip install selenium
import config
GREEN = config.GREEN
GRAY = config.GRAY
RESET = config.RESET
YELLOW = config.YELLOW
RED = config.RED
CYAN = config.CYAN
MAGENTA = config.MAGENTA


# https://stackoverflow.com/questions/53729201/save-complete-web-page-incl-css-images-using-python-selenium

#from lxml import html


# -----------------------------------------
#
# -----------------------------------------
# dq = wh.dq
# sq = wh.sq
# -----------------------------------------
#
# -----------------------------------------

def strip_protocols(url):
    new_url = url
    new_url = new_url.lstrip("https://")
    new_url = new_url.lstrip("http://")
    new_url = new_url.lstrip("://")
    new_url = new_url.lstrip("//")
    new_url = new_url.lstrip('/')
    #print("strip_protocols:", url, "-->", new_url)
    return new_url

def validate_filepath(filepath):
    rep = '_'
    fixedpath = filepath
    fixedpath = fixedpath.replace('?', rep)
    fixedpath = fixedpath.replace('%', rep)
    fixedpath = fixedpath.replace('*', rep)
    fixedpath = fixedpath.replace(':', rep)
    fixedpath = fixedpath.replace('|', rep)
    fixedpath = fixedpath.replace('\"',rep)
    fixedpath = fixedpath.replace('\'',rep)
    fixedpath = fixedpath.replace('<', rep)
    fixedpath = fixedpath.replace('>', rep)
    return fixedpath

# -----------------------------------------
# TODO deal witz /en/ or invent /de/
# -----------------------------------------

# index.html
def get_page_name(ext=".html", basename="index"):
    return basename + ext

"""
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
    path = get_path_local_root(url, base).lstrip('/')
    page_folder = ""
    subs = path.split('/')
    for folder in subs:
        if folder and is_a_folder(folder):
            page_folder += folder + "/" 
    print("get_page_folder    :", GRAY, url, "-->", RESET, page_folder)
    return page_folder               


"""
get_path_local_root: https://www.karlsruhe.digital/ --> /
get_path_local_root: https://www.media.karlsruhe.digital/ --> /media/
get_path_local_root: https://media.karlsruhe.digital/ --> /media/
get_path_local_root: https://media.karlsruhe.digital/my/folder/this.jpeg --> /media/my/folder/this.jpeg
get_path_local_root: https://karlsruhe.digital/ --> /
get_path_local_root: https://karlsruhe.digital/index.html --> /index.html
get_path_local_root: https://karlsruhe.digital/some/folder/image.png --> /some/folder/image.png

"""
def get_path_local_root(url, base):
    
    # externals should be removed before
    if not wh.url_has_same_netloc(url, base):
        print(f"{YELLOW}get_path_local_root: url: {url} has not same netloc {base} {RESET}")
        exit(1)        
    
    # # # # new_url  = strip_protocols(url)
    # # # # new_base = strip_protocols(base).rstrip('/')
    
    loc_url   = wh.url_netloc(url).lstrip("www.")   # loc_url:  media.karlsruhe.digital
    loc_base  = wh.url_netloc(base)                 # loc_base:       karlsruhe.digital
    subdomain = loc_url.replace(loc_base, '').replace('.', '')
    if subdomain: 
        subdomain = "sub_" + subdomain + '/'
 
    path = wh.url_path_lstrip_slash(url)
    rooted = subdomain + path 
    rooted = wh.add_leading_slash(rooted)
    #print("get_path_local_root:", GRAY, url, "-->", RESET, rooted)
    return rooted

# # # # # def get_path_for_file(url, base, project_folder, ext=".html"):
# # # # #     page_folder = get_page_folder(url, base)
# # # # #     page_name = get_page_name(ext=ext, basename="index")
# # # # #     #relative_path   = get_relative_path(url, base)

# # # # #     # print("page_folder:", page_folder)
# # # # #     # print("page_name  :", page_name)
# # # # #     # # print("relative_path:", relative_path)

# # # # #     ret = project_folder + page_folder + page_name
# # # # #     ret = os.path.realpath(ret)

# # # # #     return ret

# # # # # def get_relative_dots(url, base):
# # # # #     ret = "../" * get_page_folder(url, base).count('/')
# # # # #     if not ret:
# # # # #         ret = './'
# # # # #     #print("get_relative_dots: -->", ret)
# # # # #     return ret


# # # # # # # def get_path_local_root_OLD(url, base):
# # # # # # #     #print("get_path_local_root:", "base:", base)
# # # # # # #     #print("get_path_local_root:", "url :", url)
# # # # # # #     # scheme = wh.url_scheme(url) # http
# # # # # # #     url = wh.link_make_absolute(url, base)
# # # # # # #     url = strip_protocols(url)
# # # # # # #     base = strip_protocols(base)
# # # # # # #     rooted = "/" + url.replace(base, "")
# # # # # # #     #print("get_path_local_root:", "--> rooted:", rooted)
# # # # # # #     return rooted


# # # # # https://karlsruhe.digital/en/2020/12/karlsruhe-becomes-pioneer-city-of-the-g20-global-smart-cities-alliance/
# # # # # https://karlsruhe.digital/
# # # # #                          /en/2020/12/karlsruhe-becomes-pioneer-city-of-the-g20-global-smart-cities-alliance/

# # # # # def get_path_local_relative(url, base, src):

# # # # #     url = wh.link_make_absolute(url, base)
# # # # #     src = wh.link_make_absolute(src, base)
# # # # #     # print("get_path_local_relative:", "url :", url)
# # # # #     # print("get_path_local_relative:", "base:", base)
# # # # #     # print("get_path_local_relative:", "src :", src)

# # # # #     # scheme = wh.url_scheme(url) # http

# # # # #     dots = get_relative_dots(url, base)
# # # # #     # print("get_path_local_relative:", "dots:", dots)

# # # # #     ret = dots + src.replace(base, "")
# # # # #     # # # if ret.endswith('/'): # is a folder
# # # # #     # # #     ret += get_page_name() # index.html
# # # # #     # # #     #print(f"{CYAN}/ --> ret: {ret}{RESET}")
# # # # #     # TODO check above, should still load online

# # # # #     # print("get_path_local_root:", src, "-->", ret)
# # # # #     return ret


# -----------------------------------------
#
# -----------------------------------------


def has_a_dot(url):
    return '.' in url

def is_a_file(url):
    url = url_path(url)
    url = wh.strip_query_and_fragment(url)
    return has_a_dot(url)

def is_a_folder(url):
    return not is_a_file(url)       
    # # url = wh.strip_query_and_fragment(url)
    # # return url.endswith('/')  

def make_static(driver, url, base, project_folder, style_path, replacements_pre, wait_secs=(1, 2)):

    # ensure trailing slash
    url             = wh.add_trailing_slash(url)
    b_use_driver    = True

    # -----------------------------------------
    #
    # -----------------------------------------
    print(f"{CYAN}url: {url} {RESET}")
    print(f"{CYAN}b_use_driver: {b_use_driver} wait_secs: {wait_secs} {RESET}")
    
    # # -----------------------------------------
    # #
    # # -----------------------------------------
    # driver = webdriver.Chrome()
    # driver.implicitly_wait(10)

    wh.sleep_random(wait_secs, url)
    if b_use_driver:
        driver.get(url)
        wh.wait_for_page_has_loaded(driver)
        content = driver.page_source
    else:
        content = wh.get_content(url)

    # -----------------------------------------
    #
    # -----------------------------------------
    #path_index_base = get_path_for_file(url, base, project_folder, ext="")
    path_index_base = project_folder + get_page_folder(url, base) + "index"
    path_original   = wh.save_html(content, path_index_base + "_original.html")

    # -----------------------------------------
    # TODO manual replace instead links_remove_similar
    # -----------------------------------------
    # TODO manual replace instead links_remove_similar
    for fr, to in replacements_pre:
        print(YELLOW, "\t replace:", fr, "-->", to, RESET)
        content = content.replace(fr, to)
    path_replaced = wh.save_html(content, path_index_base + "_replaced_pre.html")
    
    # -----------------------------------------
    # make all links absolute with base
    # -----------------------------------------
    # collect internal files: skip externals
    # make them all absolute urls

    def assets_save_internals_locally(content, url, base, links, project_folder):
        
        b_strip_ver = True

        links = wh.links_remove_comments(links, '#')
        # links = wh.links_make_absolute(links, base)  NO!!!
        links = wh.links_remove_externals(links, base)
        # links = wh.links_remove_folders(links) NO!!!
        links = wh.links_remove_invalids(links, base, ["s.w.org", "?p=", "mailto:", "javascript:"])
        # links = wh.links_remove_similar(links) # https://karlsruhe.digital/en/home
        links = wh.links_make_unique(links)
        links = sorted(links)

        print(GRAY, "assets_save_internals_locally:", *links, RESET, sep='\n\t')

        for src in links:
            
            src = src.strip()
            print(f"{GREEN}\t src: {src}{RESET}")
            
            # check external
            if wh.url_is_absolute(src) and not wh.url_has_same_netloc(src, base):
                print(f"{YELLOW}\t is absolute and external: src: {src}{RESET}")
                time.sleep(5)
                continue
            
            
            abs_src = wh.link_make_absolute(src, base)
            ###abs_src_stripped = wh.strip_query_and_fragment(abs_src)
            #new_src     = get_relative_dots(url, base) + wh.url_path_lstrip_slash(src)
            #new_src = get_path_local_root(src, base)
            new_src = get_path_local_root(abs_src, base)
            # new_src     = get_path_local_relative(url, base, src) # works
             

            # strip query ver=x.x.x
            if b_strip_ver:
                if wh.url_has_ver(new_src):
                    new_src = wh.strip_query_and_fragment(new_src)
                    print("\t\t stripped ?ver=:", new_src)
                
            # is a file? add index.html/get_page_name() to folder-links
            # TODO may not do so wp_json/ and sitemap/
            if is_a_file(new_src) : # is a file
                print(MAGENTA, "\t\t file:", RESET, new_src)
            else:
                new_src = wh.add_trailing_slash(new_src)
                if not 'wp_json/' in new_src and not 'sitemap/' in new_src:  # TODO check WP_SPECIAL_DIRS
                    new_src += get_page_name()  # index.html
                    print(MAGENTA, "\t\t dir :", RESET,
                          new_src, "[added index.html]")
                else:
                    print(f"{MAGENTA}\t\t WP_SPECIAL_DIR: new_src: {new_src} {RESET}")
                    
            new_src = validate_filepath(new_src)
            local_path = project_folder + new_src.lstrip('/')
            wh.make_dirs(local_path)
  
            # get and save link-asset to disk
            if not wh.file_exists_and_valid(local_path): 

                ####wh.make_dirs(local_path)
                
                # only save files in this go, local_path
                if is_a_file(abs_src): ##  may_be_a_folder(abs_src):  # folders may get exception below?
                    
                    wh.sleep_random(wait_secs, abs_src)

                    # TODO >>> shifted right1
                    max_tries = 10
                    for cnt in range(max_tries):
                        try:
                            print(f"{GREEN}\t\t [{cnt}] session.get: {abs_src}{RESET}")
                            session = requests.Session()
                            session.get(base)  # sets cookies
                            res = session.get(abs_src)
                            break
                        except Exception as e:
                            print("\n"*4)
                            print(f"{RED}\t\t ERROR {cnt} session.get: {abs_src}...sleep... {RESET}")
                            time.sleep(3)
                    
                    # write the file        
                    try:
                        with open(local_path, 'wb') as fp:
                            fp.write(res.content)
                            print(f"{GREEN}\t\t wrote OK: {local_path}{RESET}")
                    except:
                        print(f"{RED}\t\t local_path may be a directory?: {local_path}{RESET}")
                    ### END shifted <<<<<<<<<<<<<<
                    
                else:
                    print(f"{RED}\t\t abs_src may be a directory?: {abs_src}{RESET}")
            else:
                print(f"{RED}\t\t already exists: {local_path}{RESET}")

            # dots rel to url of this url, not to the image itself
            print(f"{GRAY}\t\t\t url       : {url}{RESET}")
            print(f"{GRAY}\t\t\t abs_src   : {abs_src}{RESET}")
            print(f"{GRAY}\t\t\t new_src   : {new_src}{RESET}")
            print(f"{GRAY}\t\t\t local_path: {local_path}{RESET}")
            #print(f"{MAGENTA}\t\t\t replace {src} \n\t\t\t --> {new_src}{RESET}")

            # post replace
            # TODO would be better to set tags or change tags or rename tags
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            content = content.replace(dq(src), dq(new_src))  # try both
            content = content.replace(sq(src), sq(new_src))  # try both

        return content

    # -----------------------------------------
    # make lists
    # -----------------------------------------
    h = lxml.html.fromstring(content)

    list_head_href = h.xpath('head//@href')

    list_body_href = h.xpath('body//@href')

    # //link[not contains(@rel, "icon")]/@href
    list_link_href = h.xpath('//link/@href')

    list_img = h.xpath('//img/@src')
    list_img += h.xpath('//link[contains(@rel, "icon")]/@href')  # favicon
    list_img += wh.get_style_background_images(driver)
    list_img += wh.get_stylesheet_background_images(style_path)

    list_scripts = h.xpath('//script/@src')

    # https://realpython.com/python-zip-function/
    assets = [list_head_href, list_body_href,
              list_link_href, list_img, list_scripts]
    suffixes = ["list_head_href", "list_body_href",
                "list_link_href", "list_img", "list_scripts"]
    for asset, suffix in zip(assets, suffixes):
        print("/" * 80)
        print(suffix)
        #print(GRAY, *asset, RESET, sep='\n\t') # will be sorted etc in assets_save_internals_locally
        content = assets_save_internals_locally(
            content, url, base, asset, project_folder)
        wh.save_html(content, path_index_base + "_" + suffix + ".html", pretty=True)

    # -----------------------------------------
    #
    # -----------------------------------------

    content = wh.html_minify(content)
    path_minified   = wh.save_html(content, path_index_base + ".html")
    path_pretty     = wh.save_html(content, path_index_base + "_pretty.html", pretty=True)
    # # path_temp     = wh.load_html_from_string(driver, content)
    # # os.remove(path_temp)
    # # time.sleep(10)

    # # # driver.refresh()
    # # print("closing driver...")
    # # driver.close()
    # # driver.quit()
    
    print("all done.")

# -----------------------------------------
#
# -----------------------------------------


if __name__ == "__main__":

    # LOG: "C:\Users\michaelsaup\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt"

    # assert os.path.exists("page/__KD__/")
    # assert os.path.exists("page/__KD__/index.html")

    # assert os.path.isdir("page/__KD__/")
    # #assert os.path.isdir("page/__KD__/index.html") # err

    # assert os.path.isfile("page/__KD__/") # err
    # assert os.path.isfile("page/__KD__/index.html")
    # exit(0)

    # # assert wh.is_directory("page/__KD__/")
    # # assert wh.is_directory("page/__KD__")
    # # #assert wh.is_directory("page/__KD__/index.html") # err
    # # #assert wh.is_directory("/index.html")# err
    # # #assert wh.is_directory("index.html")# err
    # # assert wh.is_directory("/")
    # # assert wh.is_directory("dir")
    # # assert wh.is_directory("/dir")
    # # assert wh.is_directory("/dir/")
    # # assert wh.is_directory("")
    # # assert wh.is_directory(".")
    # # assert wh.is_directory("./")

    # wh.get_status_code("https://1001suns.com")
    # wh.get_status_code("https://1001suns.com/")
    # wh.get_status_code("https://1001suns.com/index.php")
    # wh.get_status_code("https://1001suns.com/index.phpXXXXXXX")

    # wh.get_mime_type("https://1001suns.com/empty/twitter.svg")
    # wh.get_mime_type("https://1001suns.com/empty")
    # wh.get_mime_type("https://1001suns.com/empty/")

    # wh.get_redirected_url("https://1001suns.com")
    # wh.get_redirected_url("https://1001suns.com/")
    # wh.get_redirected_url("https://1001suns.com/index.php")

    # wh.get_response_link(wh.get_response("https://1001suns.com"))
    # wh.get_response_link(wh.get_response("https://karlsruhe.digital"))
    # exit(0)

    # wh.url_exists("https://1001suns.com/reallyBadDOESNOTexist")
    # wh.url_exists("https://1001suns.com/reallyBadDOESNOTexist.csv")
    # wh.url_exists("https://1001suns.com/empty")
    # wh.url_exists("https://1001suns.com/empty/")
    # wh.url_exists("https://1001suns.com/empty/twitter.svg")
    # wh.url_exists("https://1001suns.com") # actually points to a file
    # wh.url_exists("https://1001suns.com/")
    # wh.url_exists("https://1001suns.com/index.php")

    # if wh.url_has_ver("https://1001suns.com/empty/twitter.svg"):
    #     wh.url_get_ver("https://1001suns.com/empty/twitter.svg")
    # if wh.url_has_ver("https://1001suns.com/empty/twitter.svg?ver=1.2.3.4"):
    #     wh.url_get_ver("https://1001suns.com/empty/twitter.svg?ver=1.2.3.4")
    
    
    # wh.url_has_fragment("https://1001suns.com/empty/twitter.svg")
    # wh.url_has_fragment("https://1001suns.com/empty/")
    # wh.url_has_fragment("https://1001suns.com/empty/#frag123")
    # wh.url_has_fragment("https://1001suns.com/empty/index.css?ver=1.2.3.4")
    # wh.url_has_fragment("https://1001suns.com/empty/index.css?ver=1.2.3.4#frag655")
    
    # wh.has_same_netloc("https://media.karlsruhe.digital/", "https://karlsruhe.digital")
    # wh.has_same_netloc("https://media.karlsruheXXX.digital/", "https://karlsruhe.digital")
    
    
    # get_page_folder("https://www.karlsruhe.digital/", "https://karlsruhe.digital")
    # get_page_folder("https://www.media.karlsruhe.digital/", "https://karlsruhe.digital")
    # get_page_folder("https://media.karlsruhe.digital/", "https://karlsruhe.digital")
    # get_page_folder("https://media.karlsruhe.digital/my/folder/this.jpeg", "https://karlsruhe.digital")
    # get_page_folder("https://karlsruhe.digital/", "https://karlsruhe.digital")
    # get_page_folder("https://karlsruhe.digital/index.html", "https://karlsruhe.digital")
    # get_page_folder("https://karlsruhe.digital/some/folder/image.png", "https://karlsruhe.digital")
    
    # wh.url_is_absolute("https://www.karlsruhe.digital/path/image.jpg")
    # wh.url_is_absolute("https://www.karlsruhe.digital")
    # wh.url_is_absolute("http://www.karlsruhe.digital")
    # wh.url_is_absolute("htt://www.karlsruhe.digital")
    # wh.url_is_absolute("//www.karlsruhe.digital/path/image.jpg")
    # wh.url_is_absolute("www.karlsruhe.digital/path/image.jpg")
    # wh.url_is_absolute("/path/image.jpg")

    # exit(0)

    # -----------------------------------------
    #
    # -----------------------------------------

    # TODO style_path must be downloaded first....immediately change links to local......

    if False:
        urls = [
            # 'https://karlsruhe.digital/',
            'https://karlsruhe.digital/en/about-karlsruhe-digital/',
            'https://karlsruhe.digital/en/home/',
            'https://karlsruhe.digital/en/it-hotspot-karlsruhe/',
            'https://karlsruhe.digital/en/blog-2/',
            'https://karlsruhe.digital/en/search/',
        ]
    else:
        with open(config.sitemap_links_internal_path) as file:
            lines = file.readlines()
            urls = [line.rstrip() for line in lines]
    urls = wh.links_remove_comments(urls, '#')


    driver = webdriver.Chrome()
    driver.implicitly_wait(30)
    
    for count, url in enumerate(urls):

        print("\n"*5 + CYAN + "#"*88 + RESET + "\n"*5)
        print(f"{CYAN}url: {url}{RESET}")
        wh.progress(count / len(urls), verbose_string="TOTAL", VT=CYAN, n=80)
        print("\n"*5)

        if not (url in config.sitemap_links_ignore):
            make_static(
                driver,
                url,
                config.base,
                config.project_folder,
                config.style_path,
                config.replacements_pre,
                wait_secs=config.wait_secs
            )
        else:
            print(f"{YELLOW}IGNORED url: {url}{RESET}" + "\n"*5)

    # todo this should work if in root of domain
    # # wh.replace_in_file(
    # #   style_path,
    # #   "background-image: url(\"/wp-content/",
    # #   "background-image: url(\"../../../../wp-content/" # rel to css/
    # # )
    
    driver.close()
    driver.quit()

    exit(0)
