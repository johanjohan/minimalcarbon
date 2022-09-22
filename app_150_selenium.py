""" 
    ERROR
    
DevTools listening on ws://127.0.0.1:60159/devtools/browser/9edb20d1-1bd5-4ee4-a380-979f394658a9
 Message: session not created: This version of ChromeDriver only supports Chrome version 102
Current browser version is 105.0.5195.127 with binary path C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
Stacktrace:

https://stackoverflow.com/questions/72111139/this-version-of-chromedriver-only-supports-chrome-version-102

    One option is to use chromedriver-autoinstaller to do it all at once:

    import chromedriver_autoinstaller as chromedriver
    chromedriver.install()

    Alternatively use chromedriver-binary-auto to find the required version and install the driver:

    pip install --upgrade --force-reinstall chromedriver-binary-auto
    import chromedriver_binary

    No restarting is required.


"""



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
### --> pip install --upgrade --force-reinstall chromedriver-binary-auto
import chromedriver_binary  # pip install chromedriver-binary-auto #  once there is an update
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

from app_050_sitemap_crawl import rectify

import datetime
import sys
import signal
import pyautogui as pag
import copy

import config
GREEN   = config.GREEN
GRAY    = config.GRAY
RESET   = config.RESET
YELLOW  = config.YELLOW
RED     = config.RED
CYAN    = config.CYAN
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

b_redirect_stdout       = False
b_use_difference_links  = False # usually False
# -----------------------------------------
#
# -----------------------------------------
# def handler(signum, frame):   
#     if "Yes" == pag.confirm(text=f"Ctrl-c was pressed. Do you really want to exit?", buttons=['Yes', 'No']):
#         exit(0)
                
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
    
    url = rectify(url, base, b_absolute=True)

    global images_written, assets_written

    links = wh.links_remove_comments(links, '#')
    # links = wh.links_make_absolute(links, base)  NO!!!
    links = wh.links_remove_externals(links, base)
    # links = wh.links_remove_folders(links) NO!!!
    links = wh.links_remove_invalids(links, ["s.w.org", "mailto:", "javascript:", "whatsapp:", "data:"]) # "?p=", 
    # links = wh.links_remove_similar(links) # https://karlsruhe.digital/en/home
    links = wh.links_remove_nones(links)
    links = wh.links_make_unique(links)
    links = sorted(links)
    print(GRAY, "assets_save_internals_locally:", *links, RESET, sep='\n\t')

    # loop the links
    for src in links:
        
        # >>> do not change "src" for replacements happening later !!!!!!!!!!!
        
        print()
        print(f"{CYAN}\t [{(time.time() - start_secs)/60.0:.1f} m] src: \'{src}\' {RESET}")

        # checks
        if not src:
            print(f"{YELLOW}assets_save_internals_locally: not src: src: {src} {RESET}")
            continue
        elif wh.url_is_external(src, base):
            print(f"{YELLOW}assets_save_internals_locally: is external: src: {src} {RESET}")
            continue

        # # # # # # # # abs_src = wh.url_transliterate(src) # NEW
        # # # # # # # # abs_src = wh.link_make_absolute(abs_src, base) # from redirected
        # # # # # # # # # re-direction ie ?p=1234
        # # # # # # # # # mostly adds a trailing /
        # # # # # # # # redirected_src, is_redirected = wh.get_redirected_url(abs_src, timeout=10)  
        # # # # # # # # if is_redirected:
        # # # # # # # #     abs_src = wh.link_make_absolute(redirected_src, base)
        # # # # # # # #     print("\t", wh.YELLOW, "redirected:", src, wh.RESET, "-->", wh.YELLOW, abs_src, wh.RESET)
        # # # # # # # # new_src = wh.get_path_local_root_subdomains(abs_src, base)
        
        abs_src = copy.copy(src)
        abs_src = wh.link_make_absolute(abs_src, base)
        abs_src, __is_redirected = wh.get_redirected_url(abs_src, timeout=10)  
        # abs_src: do NOT change firtzher as it will download the asset
        new_src = copy.copy(abs_src)
        new_src = wh.get_path_local_root_subdomains(new_src, base)
       
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
            # dir CAN/MAY be is_a_dir/#section
            if not 'wp_json/' in wh.url_path(new_src) and not 'sitemap/' in wh.url_path(new_src):  # TODO check WP_SPECIAL_DIRS
                # ISSUE: /ueber-karlsruhe-digital/#section-4/index.html --> /ueber-karlsruhe-digital/index.html#section-4/
                index_src = ats(wh.url_path(new_src)) +  wh.get_page_name() + wh.url_qf(new_src)
                new_src   = index_src
                print(MAGENTA, "\t\t dir :", RESET, new_src, "[added index.html]")
            else:
                print(f"{YELLOW}\t\t WP_SPECIAL_DIR: new_src: {new_src} {RESET}")

        #new_src     = wh.sanitize_filepath_and_url(new_src)                 # transliterate
        new_src     = wh.url_transliterate(new_src)                 # transliterate
        new_src     = wh.strip_trailing_slash(new_src)                      # new rectify
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
            content_orig =  copy.copy(content)
            content = content.replace(f(src), f(new_src))
            if verbose and (content_orig != content):
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
    
    url = rectify(url, base, b_absolute=True)

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
        try:
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
            
            if False: 
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
                    if "url" in imgpath: # imgpath != "none" and 
                        print("\t\t\t", wh.CYAN, wh.dq(imgpath), wh.RESET)
                        url = wh.extract_url(imgpath)
                        url = urllib.parse.unquote(url) # driver.find_elements does url encoding --> unquote
                        links_img.append( url )
                        
        except Exception as e:
            print(wh.RED, e, wh.RESET)
            # imgpath = e.value_of_css_property("background-image")
            # selenium.common.exceptions.StaleElementReferenceException: Message: stale element reference: element is not attached to the page document
            exit(1)        
    else:           
        # this loads ALL images in one go, not just the ones in each page  >> takes some extra time replacing links..
        links_img = image_sizes.file_image_sizes_get_urls()
        #print("links_img", wh.GRAY, *links_img, wh.RESET, sep="\n\t")
        
    #-----------
    # image sizes
    #-----------                    
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
    lists =    [ links_head_href,   links_body_href,   links_link_href,   links_img,   links_scripts]  # links_head_css,
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
    
    ###signal.signal(signal.SIGINT, handler)

    # -----------------------------------------
    # 
    # -----------------------------------------
    image_sizes.file_image_sizes_make_unique()
    image_size_tuples = image_sizes.load_image_size_tuples()
    
    wh.file_make_unique(config.path_image_sizes_visited, sort=True)
    urls_visited = wh.list_from_file(config.path_image_sizes_visited)
    
    # -----------------------------------------
    # 
    # -----------------------------------------
    if b_use_difference_links:
        if "Cancel" == pag.confirm(text=f"using b_use_difference_links: {b_use_difference_links}", buttons=['Continue', 'Cancel']):
            exit(0)
        urls = wh.list_from_file(config.path_sitemap_links_int_diff)
    else:
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
      
    #print("urls:", GREEN, *urls, RESET, sep="\n\t")
    print("len(urls):", len(urls))
    #wh.log("urls:", *[f"\n\t{u}" for u in urls], filepath=config.path_log_params)

    # -----------------------------------------
    # stdout
    # -----------------------------------------  

    if b_redirect_stdout:
        path_log = config.path_stats + "__logs/" + "log_" + config.dt_now_string + ".log"
        wh.make_dirs(path_log)
        print(wh.YELLOW, "redirecting stdout to:", path_log)
        sys.stdout = open(path_log, 'w', encoding="utf-8")      
    # -----------------------------------------
    # make_static
    # -----------------------------------------  
    # loop urls from internal_urls file
    for count, url in enumerate(urls):

        # # ###########################
        # # # DEBUG TODO save some time
        # # if count == 3:
        # #     print(YELLOW, "DEBUG BREAK", RESET)
        # #     break
        # # ###########################

        print()
        wh.progress(count / len(urls), verbose_string="TOTAL", VT=CYAN, n=66)
        print()
        print(f"{CYAN}[{(time.time() - start_secs)/60.0:.1f} m] url: {url}{RESET}")
        
        if b_redirect_stdout:
            dts = datetime.datetime.now().strftime("%Y %m %d %H:%M:%S")
            verbose_string = f"{dts} [{(time.time() - start_secs)/60.0:.1f} m] url: {os.path.basename(url)}"
            print(wh.progress_string(count / len(urls), verbose_string=verbose_string, VT=CYAN, n=66), file=sys.stderr)

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

    sys.stdout.close()
    exit(0)
