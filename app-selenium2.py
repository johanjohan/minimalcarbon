"""
TODO
"https:\/\/karlsruhe.digital\/wp-includes\/js\/wp-emoji-release.min.js?ver=5.2.15"
https://stackoverflow.com/questions/6076229/escaping-a-forward-slash-in-a-regular-expression


https:\/\/karlsruhe.digital\/

https://github.com/beautify-web/js-beautify
pip install jsbeautifier
pip install cssbeautifier


Python script to extract URLs from HTML documents. 
https://gist.github.com/zmwangx/49049218bd89c21ddabd647896af995a

Note: The new features discussed in this article — srcset/sizes/<picture> — are all supported in modern desktop and mobile browsers (including Microsoft's Edge browser, although not Internet Explorer.)


<img srcset="elva-fairy-480w.jpg 480w,
             elva-fairy-800w.jpg 800w"
     sizes="(max-width: 600px) 480px,
            800px"
     src="elva-fairy-800w.jpg"
     alt="Elva dressed as a fairy">


Note: The new features discussed in this article — srcset/sizes/<picture> — are all supported in modern desktop and mobile browsers (including Microsoft's Edge browser, although not Internet Explorer.)


<img srcset="elva-fairy-480w.jpg 480w,
             elva-fairy-800w.jpg 800w"
     sizes="(max-width: 600px) 480px,
            800px"
     src="elva-fairy-800w.jpg"
     alt="Elva dressed as a fairy">



http:// https://is_a_real_url.yes

TODO

now python replace tags via bs4 or selenium
https://stackoverflow.com/questions/55915856/change-element-in-python-using-selenium

var = 100
js = f"arguments[0].setAttribute('value', '{var}')"
browser.execute_script(js, get_draws)


EDIT SOLVED:

Figured out how to change the value of an element. I had to change the search method of that element to this:

get_draws = browser.find_element_by_tag_name('option')

Then my next line was pretty simple:

browser.execute_script(arguments[0].setAttribute('value', '100'), get_draws)

python replace tag with selenium
https://stackoverflow.com/questions/69732483/python-selenium-find-all-css-element-and-replace-all
https://www.geeksforgeeks.org/change-the-tags-contents-and-replace-with-the-given-string-using-beautifulsoup/
https://python.tutorialink.com/i-want-to-replace-the-html-code-with-my-own/


r=requests.get('https://neculaifantanaru.com/en/qualities-of-a-leader-inner-integrity.html')
soup=BeautifulSoup(r.text, 'html.parser')

try:
    articles = soup.find_all('p', {'class':"text_obisnuit"})
    for item in articles:  

        original_text=item.text
        #print(original_text)
        translated_output=ts.google(original_text, from_language='en', to_language='ro')
        print(item)

        item.string = translated_output
            
except Exception as e:
    print(e)

# To see that it was changed
for item in articles:   
    print(item)


translated_html = str(soup)

####################

    element =driver.find_element_by_id("some-random-number")
    driver.execute_script("arguments[0].innerText = '200'", element)
    
    element =  driver.find_element_by_class_name("something");
    driver.execute_script("arguments[0].setAttribute('style', 'transition: transform 2500ms bla bla bla')", element);       


#######################


37

I do not know of a Selenium method that is designed specifically to remove elements. However, you can do it with:

element = driver.find_element_by_class_name('classname')
driver.execute_script(""
var element = arguments[0];
element.parentNode.removeChild(element);
"", element)

############################
https://stackoverflow.com/questions/22515012/python-selenium-how-can-i-delete-an-element

def excludeTagFromWebDriver(driver : WebDriver, selector : str):
    i = 0
    soup = BeautifulSoup(driver.page_source, 'html.parser') # Parsing content using beautifulsoup
    while soup.find(selector):
        # print(soup.find(selector))
        js = ""
            var element = document.querySelector(""" + "'" + selector + "'" + """);
            if (element)
                element.parentNode.removeChild(element);
            ""
        driver.execute_script(js)
        soup = BeautifulSoup(driver.page_source, 'html.parser') # Parsing content using beautifulsoup
        i += 1
        # print('Removed tag with selector ' + "'" + selector + "'" + ' with nr: ', i)
    print('Removed ' + str(i) + ' tags with the selector ' + "'" + selector + "'" + " and all it's children tags.")
    return driver

driver = excludeTagFromWebDriver(driver,"sup")

###################################
        try:
            element = driver.find_element_by_xpath("//div[@class='chatContainer oldStyle']")
        driver.execute_script(""var element = arguments[0]; 
            element.parentNode.removeChild(element);"", element)
        except Exception:
            pass
##################################
chatBox = driver.find_element(By.XPATH, "//div[@class='chatContainer oldStyle']")
driver.execute_script("arguments[0].remove();", chatBox)



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

import jsbeautifier
import cssbeautifier


import config
GREEN = config.GREEN
GRAY = config.GRAY
RESET = config.RESET
YELLOW = config.YELLOW
RED = config.RED
CYAN = config.CYAN
MAGENTA = config.MAGENTA


# https://stackoverflow.com/questions/53729201/save-complete-web-page-incl-css-images-using-python-selenium


# -----------------------------------------
#
# -----------------------------------------

images_written = []
# -----------------------------------------
#
# -----------------------------------------


def strip_protocol(url):
    new_url = url
    new_url = new_url.lstrip("https://")
    new_url = new_url.lstrip("http://")
    new_url = new_url.lstrip("://")
    new_url = new_url.lstrip("//")
    new_url = new_url.lstrip('/')
    #print("strip_protocols:", url, "-->", new_url)
    return new_url

def sanitize_filepath(filepath):
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
# TODO  /en/ or invent /de/
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
        if folder and assuming_a_folder(folder):
            page_folder += folder + "/" 
    print("get_page_folder    :", GRAY, url, "-->", RESET, wh.sq(page_folder))
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

# -----------------------------------------
# based on ASSUMPTIONS!
# -----------------------------------------
def has_a_dot(url):
    return '.' in url

def assuming_a_file(url):
    url = url_path(url)
    url = wh.strip_query_and_fragment(url)
    return has_a_dot(url)

def assuming_a_folder(url):
    return not assuming_a_file(url)       

# -----------------------------------------
# 
# -----------------------------------------
def make_static(driver, url, base, project_folder, style_path, replacements_pre, wait_secs=(1, 2)):

    # ensure trailing slash
    url             = wh.add_trailing_slash(url)
    b_use_driver    = True

    # -----------------------------------------
    # GET content
    # -----------------------------------------
    content = ""
    for tries in range(10):
        
        print(f"{CYAN}[{tries}] GET url: {url} {RESET}")
        print(f"{CYAN}\t b_use_driver: {b_use_driver} {RESET}")
        print(f"{CYAN}\t wait_secs   : {wait_secs} {RESET}")
        wh.sleep_random(wait_secs, verbose_string=url, prefix="\t ") # verbose_string=url       
        
        try:
            if b_use_driver:
                driver.get(url) 
                wh.wait_for_page_has_loaded(driver)
                content = driver.page_source
            else:
                content = wh.get_content(url)
        except Exception as e:
            print(f"{RED}\t ERROR: GET url: {url} {RESET}")
            
        if content:
            break
        else:
            if tries == 0:
                url = "http://" + strip_protocol(url)
            else:
                url = "https://" + strip_protocol(url)
            print(f"{RED}\t will try with different PROTOCOL: {url} {RESET}")
            time.sleep(2)
    ### for tries   get />     

    # -----------------------------------------
    #
    # -----------------------------------------
    #path_index_base = get_path_for_file(url, base, project_folder, ext="")
    path_index_base = project_folder + get_page_folder(url, base) + "index"
    path_original   = wh.save_html(content, path_index_base + "_original.html")

    # -----------------------------------------
    # 
    # -----------------------------------------
    for fr, to in replacements_pre:
        print(GRAY, "\t replace:", fr, "-->", to, RESET)
        content = content.replace(fr, to)
    path_replaced_pre = wh.save_html(content, path_index_base + "_replaced_pre.html")
    
    # -----------------------------------------
    # make all links absolute with base
    # -----------------------------------------
    # collect internal files: skip externals
    # make them all absolute urls

    def assets_save_internals_locally(content, url, base, links, project_folder, b_strip_ver=True):
        
        global images_written
        
        links = wh.links_remove_comments(links, '#')
        ### links = wh.links_make_absolute(links, base)  NO!!!
        links = wh.links_remove_externals(links, base)
        ### links = wh.links_remove_folders(links) NO!!!
        links = wh.links_remove_invalids(links, ["s.w.org", "?p=", "mailto:", "javascript:", "whatsapp:"])
        ### links = wh.links_remove_similar(links) # https://karlsruhe.digital/en/home
        links = wh.links_make_unique(links)
        links = sorted(links)

        print(GRAY, "assets_save_internals_locally:", *links, RESET, sep='\n\t')

        for src in links:
            
            #src = src.strip()
            print(f"{CYAN}\t src: \'{src}\' {RESET} ")
            
            # check external
            if wh.url_is_external(src, base):
                print(f"{YELLOW}assets_save_internals_locally: is external: src: {src} {RESET}")
                exit(6) # TODO DEBUG
                continue
            
            abs_src = wh.link_make_absolute(src, base)
            new_src = get_path_local_root(abs_src, base)
            if b_strip_ver:
                if wh.url_has_ver(new_src):
                    new_src = wh.strip_query_and_fragment(new_src)
                    print("\t\t stripped ?ver=:", new_src)
                
            # is a file? add index.html/get_page_name() to folder-links
            # TODO may not do so wp_json/ and sitemap/
            if assuming_a_file(new_src) : 
                print(MAGENTA, "\t\t file:", RESET, new_src)
            else: 
                new_src = wh.add_trailing_slash(new_src)
                if not 'wp_json/' in new_src and not 'sitemap/' in new_src:  # TODO check WP_SPECIAL_DIRS
                    new_src += get_page_name()  # index.html
                    print(MAGENTA, "\t\t dir :", RESET,
                          new_src, "[added index.html]")
                else:
                    print(f"{MAGENTA}\t\t WP_SPECIAL_DIR: new_src: {new_src} {RESET}")
                    
            new_src     = sanitize_filepath(new_src)
            local_path  = project_folder + new_src.lstrip('/')
            
            # collect local images for a list to save at the end
            le_tuple = (
                src,
                new_src,
                local_path,
                # abs_src,
            )
            if any(ext in local_path.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                images_written.append(le_tuple)
                                        
   
            # get and save link-asset to disk
            wh.make_dirs(local_path)
            if not wh.file_exists_and_valid(local_path): 
                
                if assuming_a_file(abs_src): ##  may_be_a_folder(abs_src):  # folders may get exception below?
                    
                    wh.sleep_random(wait_secs, verbose_string=src, prefix="\t\t ") # abs_src

                    # get the file via session requests
                    max_tries = 10
                    for cnt in range(max_tries):
                        try:
                            print(f"{CYAN}\t\t [{cnt}] session.get: {abs_src}{RESET}")
                            session = requests.Session()
                            session.get(base)  # sets cookies
                            res = session.get(abs_src)
                            break
                        except Exception as e:
                            print("\n"*4)
                            print(f"{RED}\t\t ERROR {cnt} session.get: {abs_src}...sleep... {RESET}")
                            time.sleep(3)
                    
                    # write the file binary to disk local        
                    try:
                        with open(local_path, 'wb') as fp:
                            fp.write(res.content)
                            print(f"{GREEN}\t\t wrote OK: {local_path}{RESET}")
                    except:
                        print(f"{RED}\t\t local_path may be a directory?: {local_path}{RESET}")
                    
                else:
                    print(f"{RED}\t\t abs_src may be a directory?: {abs_src}{RESET}")
            else:
                print(f"{RED}\t\t already exists: {os.path.basename(local_path)}{RESET}")

            # dots rel to url of this url, not to the image itself
            print(f"{GRAY}\t\t\t src       : {src}{RESET}")
            print(f"{GRAY}\t\t\t new_src   : {new_src}{RESET}")
            print(f"{GRAY}\t\t\t abs_src   : {abs_src}{RESET}")
            print(f"{GRAY}\t\t\t local_path: {local_path}{RESET}")
            print(f"{GRAY}\t\t\t url       : {url}{RESET}")
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
    
    # links_head_css = h.xpath('head//link[@type="text/css"]/@href')
    # links_head_css = wh.links_strip_query_and_fragment(links_head_css)
    # links_head_css = wh.links_make_unique(links_head_css)
    # print("list_head_css", *links_head_css, sep="\n\t")

    links_head_href = h.xpath('head//@href')

    links_body_href = h.xpath('body//@href')

    # //link[not contains(@rel, "icon")]/@href
    links_link_href = h.xpath('//link/@href')

    links_img = h.xpath('//img/@src')
    links_img += h.xpath('//link[contains(@rel, "icon")]/@href')  # favicon
    links_img += wh.get_style_background_images(driver)
    links_img += wh.get_stylesheet_background_images_from_file(style_path) # TODO need to replace these in css as well
    links_css_text = h.xpath("//style/text()")
    for text in links_css_text:
        # text = cssbeautifier.beautify(text)
        # print("script", GRAY + text + RESET)
        links_img += wh.get_stylesheet_background_images_from_string(text)
    
    links_scripts = h.xpath('//script/@src')
    # list_script_text = h.xpath("//script/text()")
    # import re
    # import json
    # for text in list_script_text:
    #     text = jsbeautifier.beautify(text)
    #     print("script", GRAY + text + RESET)
    #     # j = json.loads(text)
    #     # print(MAGENTA, json.dumps(j, indent=4), RESET)
        
    #     # # # s = re.findall("'([^']*)'", text)
    #     #s = re.findall("(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})", text)
    #     s = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    #     #s = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text)
    #     regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"        
    #     s = re.findall(regex, text)
    #     print("s", YELLOW, *s, RESET, sep="\n\t")
        
    # exit(0)
    

    # https://realpython.com/python-zip-function/
    lists       = [ links_head_href,   links_body_href,  links_link_href,   links_img,   links_scripts] # links_head_css,   
    suffixes    = ["links_head_href", "links_body_href","links_link_href", "links_img", "links_scripts"]
    for links, suffix in zip(lists, suffixes):
        print("/" * 80)
        print(suffix)
        #print(GRAY, *links, RESET, sep='\n\t') # will be sorted etc in assets_save_internals_locally
        content = assets_save_internals_locally(
            content, url, base, links, project_folder)
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
    
    print("make_static: all done.")
### make_static />
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
        with open(config.sitemap_links_internal_path, "r") as file:
            lines = file.readlines()
            urls = [line.rstrip() for line in lines]
    urls = wh.links_remove_comments(urls, '#')

    # chrome init
    for tries in range(10):
        try:
            print(f"[{tries}] webdriver.Chrome()...")
            driver = webdriver.Chrome()
            driver.implicitly_wait(30)
            # driver.execute_script("alert('alert via selenium')")
            # time.sleep(33)
            # exit(0)
            break
        except Exception as e:
            print(f"{RED} {e} {RESET}")
            time.sleep(3)
    
    # loop urls from internal_urls file
    for count, url in enumerate(urls):
        
        # # # # DEBUG TODO
        # # # if count == 3:
        # # #     break

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
            
    # save image list
    path_images_written = "data/" + config.base_netloc + "_images_written.txt"
    images_written = sorted(list(set(images_written)))
    #print("images_written:", *images_written, sep="\n\t")
    with open(path_images_written, 'w', encoding="utf-8") as fp:
        fp.write('\n'.join('{},{},{}'.format(x[0],x[1],x[2]) for x in images_written))
        
    # todo this should work if in root of domain
    # # wh.replace_in_file(
    # #   style_path,
    # #   "background-image: url(\"/wp-content/",
    # #   "background-image: url(\"../../../../wp-content/" # rel to css/
    # # )
    
    driver.close()
    driver.quit()

    exit(0)
