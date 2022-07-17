"""
# https://stackoverflow.com/questions/53729201/save-complete-web-page-incl-css-images-using-python-selenium

TODO

IDEA could scan all css and js for hidden images first
    how large will they be?
    
https://stackoverflow.com/questions/9519906/how-to-get-css-attribute-of-a-lxml-element/9520444#9520444

from style import *

html = ""<body>
    <p>A</p>
    <p id='b'>B</p>
    <p style='color:blue'>B</p>
</body>""

css = ""body {color:red;font-size:12px}
p {color:yellow;}
p.b {color:green;}""


def get_style(element, view):
    if element != None:
        inline_style = [x[1] for x in element.items() if x[0] == 'style']
        outside_style =  []
        if view.has_key(element):
            outside_style = view[element].getCssText()
        r = [[inline_style, outside_style]]
        r.append(get_style(element.getparent(), view))
        return r
    else:
        return None

document = getDocument(html)
view = getView(document, css)

elements = document.xpath('//p')
print get_style(elements[0], view) 

---------------------------------


The dictionary-like attribute access should work for width and height as well, if they are specified. You might encounter images that don't have these attributes explicitly set - your current code would throw a KeyError in this case. You can use get() and provide a default value instead:

for pic in soup.find_all('img'):
    print(pic.get('width', 'n/a'))

Or, you can find only img elements that have the width and height specified:

for pic in soup.find_all('img', width=True, height=True):
    print(pic['width'], pic['height']) 



------------------------------
>>> html = '<img src="http://somelink.com/somepic.jpg" width="200" height="100">'
>>> soup = BeautifulSoup(html)
>>> for tag in soup.find_all('img'):
...     print tag.attrs.get('height', None), tag.attrs.get('width', None)
... 
100 200
------------------------------
------------------------------
------------------------------
------------------------------
------------------------------
------------------------------
------------------------------
------------------------------
------------------------------
------------------------------
------------------------------



"""
from helpers_web import links_make_absolute, links_remove_externals, links_strip_query_and_fragment, sq as sq, strip_query_and_fragment, url_path
from helpers_web import dq as dq
from helpers_web import pa as pa
from helpers_web import qu as qu
from helpers_web import add_trailing_slash as ats
from bs4 import BeautifulSoup, Comment
import time
import helpers_web as wh
import os
import requests
import lxml.html
import lxml
import chromedriver_binary  # pip install chromedriver-binary-auto
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver  # pip install selenium
from selenium.webdriver.chrome.options import Options

import jsbeautifier
import cssbeautifier

from urllib.parse import urlparse
import pyautogui as pag

import image_sizes
import urllib.parse

import config
GREEN = config.GREEN
GRAY = config.GRAY
RESET = config.RESET
YELLOW = config.YELLOW
RED = config.RED
CYAN = config.CYAN
MAGENTA = config.MAGENTA

# -----------------------------------------
#
# -----------------------------------------
start_secs              = time.time()
images_written          = []
assets_written          = []
verbose                 = True

image_size_tuples       = []
urls_visited            = []

###b_extend_rescan_urls    = False

# -----------------------------------------
# TODO  /en/ or invent /de/
# -----------------------------------------
def assets_save_internals_locally(
    content, 
    url, base,
    links, suffix,
    project_folder,
    b_strip_ver=True
):

    global images_written, assets_written

    links = wh.links_remove_comments(links, '#')
    # links = wh.links_make_absolute(links, base)  NO!!!
    links = wh.links_remove_externals(links, base)
    # links = wh.links_remove_folders(links) NO!!!
    links = wh.links_remove_invalids(links, ["s.w.org", "mailto:", "javascript:", "whatsapp:"]) # "?p=", 
    # links = wh.links_remove_similar(links) # https://karlsruhe.digital/en/home
    links = wh.links_remove_nones(links)
    links = wh.links_make_unique(links)
    links = sorted(links)
    print(GRAY, "assets_save_internals_locally:", *links, RESET, sep='\n\t')

    # loop the links
    for src in links:
        
        src = wh.link_make_absolute(src, base) # ??????ß
        
        # re-direction ie ?p=1234
        new_src, is_redirected = wh.get_redirected_url(src, timeout=10)  
        if is_redirected:
            print("\t", wh.YELLOW, "redirected:", src, wh.RESET, "-->", wh.YELLOW, new_src, wh.RESET)
            src = new_src
            time.sleep(3)

        print()
        print(f"{CYAN}\t [{(time.time() - start_secs)/60.0:.1f} m] src: \'{src}\' {RESET}")

        # checks
        if not src:
            print(f"{YELLOW}not src: src: {src} {RESET}")
            continue
        elif wh.url_is_external(src, base):
            print(f"{YELLOW}assets_save_internals_locally: is external: src: {src} {RESET}")
            continue

        abs_src = wh.link_make_absolute(src, base)
        new_src = wh.get_path_local_root_subdomains(abs_src, base)
        if b_strip_ver:
            # http://mysite.com/some_page/file.css?my_var='foo'#frag
            if wh.url_has_ver(new_src):
                q = urlparse(new_src).query
                new_src = wh.strip_query(new_src) # NEW
                print("\t\t stripped:", q, "-->", new_src)

        # is a file? add index.html/get_page_name() to folder-links
        # TODO may not do so wp_json/ and sitemap/
        if wh.url_is_assumed_file(new_src):
            #name, ext = os.path.splitext(new_src)
            #new_src = name + config.suffix_compressed + ext # use  config.suffix_compressed
            print(MAGENTA, "\t\t file:", RESET, new_src)
        else: # assumed dir
            # dir CAN BE is_a_dir/#section
            if not 'wp_json/' in wh.url_path(new_src) and not 'sitemap/' in wh.url_path(new_src):  # TODO check WP_SPECIAL_DIRS
                
                # ISSUE: /ueber-karlsruhe-digital/#section-4/index.html --> /ueber-karlsruhe-digital/index.html#section-4/
                #new_src += get_page_name()  # index.html
                index_src = ats(wh.url_path(new_src)) +  wh.get_page_name() + wh.url_qf(new_src)
                new_src   = index_src
    
                print(MAGENTA, "\t\t dir :", RESET, new_src, "[added index.html]")
            else:
                print(f"{YELLOW}\t\t WP_SPECIAL_DIR: new_src: {new_src} {RESET}")

        new_src     = wh.sanitize_filepath_and_url(new_src)
        local_path  = ats(project_folder) + new_src.lstrip('/')
        local_path  = wh.strip_query_and_fragment(local_path) # has no ?# on disk

        # collect local images for a list to save at the end
        le_tuple = (
            src,        # as found in html
            new_src,    # for wp "/file.ext"
            local_path, # local file path on disk
        )
        assert len(le_tuple) == 3  # images_written saving at very end
        if any(ext in local_path.lower() for ext in config.image_exts):
            images_written.append(le_tuple)
            
        assets_written.append(le_tuple)
        
        bOK = wh.download_asset(abs_src, local_path, base, max_tries=10, pre="\t\t")


        if verbose:
            print(f"{GRAY}\t\t\t src       : {src}{RESET}")
            #print(f"{GRAY}\t\t\t abs_src   : {abs_src}{RESET}")
            print(f"{GRAY}\t\t\t new_src   : {new_src}{RESET}")
            print(f"{GRAY}\t\t\t local_path: {local_path}{RESET}") 

        # post replace
        # TODO would be better to set tags or change tags or rename tags
        # NOTE this happens as well in app_200
        #no_f = lambda s: s # dangerous! as quotes may be removed by html-minify
        for f in [dq, sq, pa, qu]: ###, no_f]: # dangerous! as quotes may be removed by html-minify
            content = content.replace(f(src), f(new_src))
            if verbose:
                print(f"{GRAY }\t\t\t replaced: {f(src)} {RESET}-->") 
                print(f"{GREEN}\t\t\t           {f(new_src)} {RESET}") 

    return content

# -----------------------------------------
#
# -----------------------------------------
def make_static(
    driver, 
    url, base, 
    project_folder, 
    style_path, 
    replacements_pre, 
    wait_secs=(1, 2), 
    turns_for_slow_funcs=config.turns_for_slow_funcs
    ):

    ####url = wh.add_trailing_slash(url)  NO!!!

    # -----------------------------------------
    # GET content
    # -----------------------------------------
    content = ""
    for tries in range(10):

        print(f"{CYAN}[{tries}] GET url: {url} {RESET}")
        print(f"{CYAN}\t wait_secs   : {wait_secs} {RESET}")
        print(f"{CYAN}\t counter     : {make_static.counter} {RESET}")
        wh.sleep_random(wait_secs, verbose_string=url, prefix="\t ")  # verbose_string=url

        try:
            driver.get(url)
            wh.wait_for_page_has_loaded_hash(driver, max_tries=20)
            content = driver.page_source
        except Exception as e:
            print(f"{RED}\t ERROR: GET url: {url} {RESET}")
            
        if content:
            break # all OK
        else:
            # try another protocol
            if (tries % 2):
                url = "http://" + wh.strip_protocol(url)
            else:
                url = "https://" + wh.strip_protocol(url)
            print(f"{RED}\t will try with different PROTOCOL: {url} {RESET}")
            time.sleep(2)
    # for tries   get />
    
    # NO NO NO make sure utf-8
    #assert content
    # # # # # content = content.encode('utf-8') # NEW # .encode('ascii', 'ignore') no no no
    # # # # # content = urllib.parse.unquote(content) # NEW  no no no
 
    # -----------------------------------------
    #
    # -----------------------------------------
    path_index_base = project_folder + wh.get_page_folder(url, base) + "index"
    
    #if config.DEBUG: 
    path_original = wh.save_html(content, path_index_base + "_original.html")

    # -----------------------------------------
    #
    # -----------------------------------------
    for fr, to in replacements_pre:
        #print(GRAY, "\t replace:", fr, "-->", to, RESET)
        content = content.replace(fr, to)
        
    if(config.DEBUG): 
        path_replaced_pre = wh.save_html(content, path_index_base + "_replaced_pre.html")

    # -----------------------------------------
    # make lists
    # -----------------------------------------
    h = lxml.html.fromstring(content)
      
    # -----------------------------------------
    # all urls a links
    # -----------------------------------------
    links_a_href = h.xpath('//a/@href')
    
    # -----------------------------------------
    # make lists
    # -----------------------------------------
    links_head_href = h.xpath('head//@href')

    links_body_href = h.xpath('body//@href')

    # //link[not contains(@rel, "icon")]/@href
    links_link_href = h.xpath('//link/@href')

    #-----------
    # images
    #-----------
    if True:
        # driver.find_element_by_xpath('//a[@href="'+url+'"]')
        links_img  = h.xpath('//img/@src')
        links_img += h.xpath('//link[contains(@rel, "icon")]/@href')  # favicon
        links_img += wh.get_background_images_from_style_attribute(driver)
        # TODO need to replace these in css as well
        links_img += wh.get_background_images_from_stylesheet_file(style_path)
        
        for text in h.xpath("//style/text()"):
            links_img += wh.get_background_images_from_stylesheet_string(text)
        
        for text in  h.xpath("//div/@style"):
            links_img += wh.get_background_images_from_inline_style_tag(text)
        for text in  h.xpath("//video/@style"):
            links_img += wh.get_background_images_from_inline_style_tag(text)        
        # a lot of images in media.
        for text in  h.xpath("//*/@style"):
            links_img += wh.get_background_images_from_inline_style_tag(text)
        
        if True: 
        # media.ka    
            import json
            for jstring in  h.xpath("//*/@data-vjs_setup"):
                j = json.loads(jstring)
                #print(json.dumps(j, indent=4), sep="\n\t\t")
                print("\t\t\t", j.get("poster", None))
                links_img.append(j.get("poster", None))
          
        if make_static.counter < turns_for_slow_funcs: 
            print("\t\t", "driver.find_elements: By.XPATH <body>", flush=True)
            for e in driver.find_elements(By.XPATH, "//body//*"):
                imgpath = e.value_of_css_property("background-image")
                if imgpath != "none" and "url" in imgpath:
                    print("\t\t\t", wh.CYAN, wh.dq(imgpath), wh.RESET)
                    url = wh.extract_url(imgpath)
                    url = urllib.parse.unquote(url) # !!!
                    links_img.append( url )
                    
        image_sizes.find_all_image_size_tuples(
            image_size_tuples, 
            driver, 
            config.base,
            config.bases, 
            b_scan_srcset=False, 
            pre="\t\t"
        )
        print("\t\t", "len(image_size_tuples):", len(image_size_tuples))
        
        # to file
        try:
            # TODO at the very end create header nd make unique
            wh.list_to_file(image_size_tuples, config.path_image_sizes, mode="a")
        except Exception as e:
            print(wh.RED, e, wh.RESET)   
            
    else:           
        # this loads ALL images in one go, not just the ones in each page  >> takes some extra time replacing links..
        links_img = image_sizes.file_image_sizes_get_urls()
        #print("links_img", wh.GRAY, *links_img, wh.RESET, sep="\n\t")
            
    #-----------
    # fonts
    #-----------
    
    #-----------
    # scripts
    #-----------
    links_scripts = h.xpath('//script/@src')

    #-----------
    # perform
    #-----------
    # https://realpython.com/python-zip-function/
    lists =     [links_head_href,   links_body_href,   links_link_href,   links_img,   links_scripts]  # links_head_css,
    suffixes = ["links_head_href", "links_body_href", "links_link_href", "links_img", "links_scripts"]

    for links, suffix in zip(lists, suffixes):
        print(MAGENTA, end='')
        print("/" * 80)
        print(suffix)
        print(RESET, end='')
        # print(GRAY, *links, RESET, sep='\n\t') # will be sorted etc in assets_save_internals_locally
        
        content = assets_save_internals_locally(
            content,
            url, base,
            links, suffix,
            project_folder
        )
        
        # if False and config.DEBUG: 
        #     wh.save_html(content, path_index_base + "_" + suffix + ".html", pretty=True)

    # -----------------------------------------
    # save
    # -----------------------------------------
    ####content = wh.html_minify(content) # only at the very end!!!!
    path_minified   = wh.save_html(content, path_index_base + ".html") # index.html
    ###path_pretty = wh.save_html(content, path_index_base + "_pretty.html", pretty=True)

    make_static.counter += 1
    
    print("make_static: all done.")
    
    return wh.links_sanitize(links_a_href)
    
# make_static />
make_static.counter = 0

# -----------------------------------------
#
# -----------------------------------------
if __name__ == "__main__":
    

    # print(__file__)
    # print(os.path.basename(__file__))
    wh.logo_filename(__file__)
    wh.log("__file__", __file__, filepath=config.path_log_params)

    if False:
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

        # wh.get_response_header_link(wh.get_response("https://1001suns.com"))
        # wh.get_response_header_link(wh.get_response("https://karlsruhe.digital"))
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

        # print("check substring:", "karlsruhe.digital" in "karlsruhe.digital")
        # print("check substring:", "karlsruhe.digital" == "karlsruhe.digital")
        # print("check substring:", "karlsruhe.digital" in "media.karlsruhe.digital")
        # print("check substring:", "karlsruhe.digital" in "arlsruhe.digital")
        # exit(0)

        # base="https://karlsruhe.digital"
        # links = [
        #     "",
        #     "index.html",
        #     "path/image.jpg",
        #     "/path/image.jpg",
        #     "karlsruhe.digital",
        #     "karlsruhe.digital/path/image.jpg",
        #     "www.karlsruhe.digital/path/image.jpg",
        #     "//www.karlsruhe.digital/path/image.jpg",
        #     "http://www.karlsruhe.digital/path/image.jpg",
        #     "https://www.karlsruhe.digital/path/image.jpg",
        #     "xxxxx://www.karlsruhe.digital/path/image.jpg",
        #     "facebook.de/test.html",
        #     "http://facebook.de/test.html",
        #     "http://facebook.de",
        #     "facebook.de",
        #     "facebook",
        #     "facebook.html",
        #     "facebook.php",
        #     "facebook.com/facebook.php",
        #     "facebook.com/facebook.com/facebook.php",
        # ]
        # for link in links:
        #     print("_"*66)
        #     #wh.url_is_absolute(link)
        #     #wh.url_is_relative(link)
        #     #wh.url_split(link)
        #     #wh.url_is_internal(link, base)
        #     wh.try_link_make_local(link, base)
        #     #wh.link_make_absolute(link, base)
        #     print()

        # print("1", "".split('/'))
        # print("2", "".split('/')[-1])
        # print("3", "".split('/')[-1] + "_added")
        # print("4", '.' in "".split('/')[-1])

        # func = wh.url_is_assumed_folder
        # func = wh.url_is_assumed_file
        # print(func(None), "\n")
        # print(func(""), "\n")
        # print(func("https://"), "\n")
        # print(func("https://domain.com"), "\n")
        # print(func("https://domain.com/"), "\n")
        # print(func("https://domain.com/folder"), "\n")
        # print(func("https://domain.com/folder/"), "\n")
        # print(func("https://domain.com/folder/nodot"), "\n")
        # print(func("https://domain.com/folder/nodot#fragment"), "\n")
        # print(func("https://domain.com/folder/nodot?p=123"), "\n")
        # print(func("https://domain.com/folder/with.dot"), "\n")
        # print(func("https://domain.com/folder/with.dot?p=123"), "\n")
        # print(func("https://domain.com/folder/with.dot?p=12#frag3"), "\n")
        # print(func("https://domain.com/folder/with.dot#frag3"), "\n")
        # print(func("https://domain.com/folder/with.dot/"), "\n")

        # exit(0)

        # # css = wh.list_from_file(config.style_path)
        # # css = cssbeautifier.beautify(wh.list_to_string(css))
        # # wh.list_to_file(wh.list_from_string(css), config.data_base_path + "test_XXXXXXX.css")

        # image_links = wh.list_from_file(
        #     #config.data_base_path + "links_img" + ".txt", 
        #     config.image_tuples_written_path, 
        #     sanitize=True
        # )
        
        # #image_links = wh.list_exec(image_links, func=lambda s : tuple(s.split(',')))
        # image_links = wh.list_exec(image_links, func=wh.list_func_to_tuple)
        # wh.list_print(image_links)
        # exit(0)

        # TODO style_path must be downloaded first....immediately change links to local......
        pass

    # # # # # -----------------------------------------
    # # # # # copy sitemap
    # # # # # -----------------------------------------
    # # # # import shutil
    # # # # wh.make_dirs(config.project_folder)
    # # # # shutil.copyfile(config.path_sitemap_xml,
    # # # #                 config.project_folder + "sitemap.xml")
    
    # -----------------------------------------
    # 
    # -----------------------------------------
    image_size_tuples = []
    image_sizes.file_image_sizes_make_unique()
    
    wh.file_make_unique(config.path_image_sizes_visited, sort=True)
    urls_visited = wh.list_from_file(config.path_image_sizes_visited)

    # -----------------------------------------
    # 
    # -----------------------------------------
    urls = wh.list_from_file(config.path_sitemap_links_internal)
    
    urls = wh.links_remove_comments(urls, '#')
    urls = wh.links_strip_query_and_fragment(urls)
    urls = wh.links_replace(urls, config.replacements_pre)
    urls = wh.links_make_absolute(urls, config.base)
    urls = wh.links_sanitize(urls)
    ###print("urls:", GREEN, *urls, RESET, sep="\n\t")
    urls_len_orig = len(urls)

    # -----------------------------------------
    # chrome init
    # -----------------------------------------            
    for tries in range(10):
        try:
            print(f"[{tries}] webdriver.Chrome()...")
            print(f"[{tries}] {config.options}")
            print(wh.MAGENTA, end='')
            driver = webdriver.Chrome(options=config.options)
            driver.implicitly_wait(config.implicit_wait)
            # driver.execute_script("alert('alert via selenium')")
            break
        except Exception as e:
            print(f"{RED} {e} {RESET}")
            time.sleep(3)
    print(wh.RESET)

    # # # # # -----------------------------------------
    # # # # # RE-scan for new links:
    # # # # # -----------------------------------------     
    # # # # if b_extend_rescan_urls:   
    # # # #     links_a_href    = []
    # # # #     valid_exts      = [".html", ".htm", ".php", ""] # ""!!!
    # # # #     wh.log("re-scanning for new links in given urls...", filepath=config.path_log_params)
        
    # # # #     # rescan only links without frags
    # # # #     urls_no_frag = wh.links_strip_query_and_fragment(urls)
    # # # #     urls_no_frag = wh.links_make_unique(urls_no_frag)
    # # # #     for count, url in enumerate(urls_no_frag):
    # # # #         print()
    # # # #         name, ext = os.path.splitext(url)
    # # # #         print(name, ext)
    # # # #         if not ext in valid_exts:
    # # # #             print("\t", YELLOW, "skipping:", RED, wh.dq(ext), RESET)
    # # # #             continue
            
    # # # #         wh.progress(count / len(urls_no_frag), verbose_string="TOTAL", VT=CYAN, n=16)
    # # # #         print()
    # # # #         wh.sleep_random(config.wait_secs, verbose_string=url, n=16) 
            
    # # # #         if content := wh.get_content(url):
    # # # #             links_a_href.append(url)
    # # # #             tree    = lxml.html.fromstring(content)
    # # # #             hrefs   = tree.xpath('//a/@href')
    # # # #             #print("\t hrefs:", GRAY, "."*len(hrefs), RESET)
    # # # #             for href in hrefs:
    # # # #                 href = href.strip()
    # # # #                 name, ext = os.path.splitext(href)
    # # # #                 if ext in valid_exts:
    # # # #                     if not href in links_a_href:
    # # # #                         print("\t\t append:", GREEN, href, RESET)
    # # # #                         links_a_href.append(href)
    # # # #         else:
    # # # #             print(RED, "error logged:", config.path_links_errors)
    # # # #             wh.string_to_file(url + "\n", config.path_links_errors, mode="a")                
    # # # #         ###break # debug
    # # # #     ### for />
        
    # # # #     # errs
    # # # #     if os.path.isfile(config.path_links_errors):
    # # # #         wh.file_make_unique(config.path_links_errors, sort=True)    

    # # # #     # add to urls
    # # # #     print("len(links_a_href):", len(links_a_href))
    # # # #     print("urls_len_orig    :", urls_len_orig)
    # # # #     urls = links_a_href
    # # # #     urls = wh.links_remove_externals(urls, config.base)
    # # # #     urls = wh.links_remove_excludes(urls, ["whatsapp:", "mailto:", "javascript:"])
    # # # #     urls = wh.links_make_absolute(urls, config.base)
    # # # #     urls = wh.links_sanitize(urls)   
    # # # #     print("len(urls) after:", len(urls), "added:", len(urls) - urls_len_orig)  
    # # # #     time.sleep(3)
        
    # # # #     # save back to file 
    # # # #     wh.list_to_file(urls, config.path_sitemap_links_internal)             
    # # # # else:
    # # # #     pag.alert(text=f"not rescanning urls...", timeout=10000)  
      
    print("urls:", GREEN, *urls, RESET, sep="\n\t")
    print("len(urls):", len(urls))
    #wh.log("urls:", *[f"\n\t{u}" for u in urls], filepath=config.path_log_params)

    # -----------------------------------------
    # make_static
    # -----------------------------------------  
    # loop urls from internal_urls file
    for count, url in enumerate(urls):

        # # # # DEBUG TODO save some time
        # # # if count == 3:
        # # #     break

        print()
        wh.progress(count / len(urls), verbose_string="TOTAL", VT=CYAN, n=66)
        print()
        print(f"{CYAN}[{(time.time() - start_secs)/60.0:.1f} m] url: {url}{RESET}")

        #if not (url in config.sitemap_links_ignore):
        if not any(ignore in url for ignore in config.sitemap_links_ignore): # sitemap/ wp-json/ 
            
            if not (url in urls_visited):
                links_a_href_from_url = make_static(
                    driver,
                    url,
                    config.base,
                    config.project_folder,
                    config.path_stylesheet,
                    config.replacements_pre,
                    wait_secs=config.wait_secs
                )
                #print("found links_a_href_from_url:", YELLOW, *links_a_href_from_url, RESET, sep="\n\t") 
                # not using links_a_href_from_url as we are pre-scanning above...
                
                wh.string_to_file(url + '\n', config.path_image_sizes_visited, mode="a") # log
            else:
                print("already visited:", wh.GRAY, url)
        else:
            print(f"{YELLOW}IGNORED url: {url}{RESET}" + "\n"*5)
            
        
    ### for />

    driver.close()
    driver.quit()
    
    image_sizes.file_image_sizes_make_unique()

    # save images written
    images_written = sorted(list(set(images_written)))
    print("saving images_written:", config.path_image_tuples_written)
    with open(config.path_image_tuples_written, 'w', encoding="utf-8") as fp:
        fp.write('\n'.join('{},{},{}'.format(x[0], x[1], x[2]) for x in images_written))
        
        
    assets_written = sorted(list(set(assets_written)))
    print("saving assets_written:", config.path_asset_tuples_written)
    wh.list_to_file(assets_written, config.path_asset_tuples_written)
    

    # # append css
    # print("appending css:", config.path_custom_css)
    # with open(config.path_stylesheet, 'a', encoding="utf-8") as outfile:
    #     with open(config.path_custom_css, 'r', encoding="utf-8") as infile:
    #         data = infile.read()
    #         outfile.write(data)

    # all done
    wh.log("all done: duration: {:.1f}m".format((time.time() - start_secs)/60.0), filepath=config.path_log_params)

    exit(0)
