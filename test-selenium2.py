"""
TODO

/* Background images */
.blog-hero {
  background-image: url("/wp-content/themes/karlsruhe-digital/images/beitragsseite_hero_slider.jpg");
}
.programm-hero {
  background-image: url("/wp-content/themes/karlsruhe-digital/images/programm_hero.jpg");
}
.blog-overview-hero {
  background-image: url("/wp-content/themes/karlsruhe-digital/images/bloguebersichtseite_hero_slider.jpg");
}
.searchpage-hero {
  background-image: url("/wp-content/themes/karlsruhe-digital/images/suchseite_hero_slider.jpg");
}
.search-hero {
  background-image: url("/wp-content/themes/karlsruhe-digital/images/suchergebnisse_hero_slider.jpg");
}


must scan style.css for bg images

https://pypi.org/project/cssutils/

/* Background images */
.blog-hero {
  background-image: url("https://particles.de/__test/wp-content/themes/karlsruhe-digital/images/beitragsseite_hero_slider.jpg");
}
.programm-hero {
  background-image: url("https://particles.de/__test/wp-content/themes/karlsruhe-digital/images/programm_hero.jpg");
}
.blog-overview-hero {
  background-image: url("https://particles.de/__test/wp-content/themes/karlsruhe-digital/images/bloguebersichtseite_hero_slider.jpg");
}
.searchpage-hero {
  background-image: url("https://particles.de/__test/wp-content/themes/karlsruhe-digital/images/suchseite_hero_slider.jpg");
}
.search-hero {
  background-image: url("https://particles.de/__test/wp-content/themes/karlsruhe-digital/images/suchergebnisse_hero_slider.jpg");
}

"""


# -----------------------------------------
# init the colorama module
# -----------------------------------------
from web_helpers import sq as sq
from web_helpers import dq as dq
from bs4 import BeautifulSoup, Comment
import time
import web_helpers as wh
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


def get_page_name(ext=".html", basename="index"):
    return basename + ext


def get_page_folder(url, base):
    if wh.has_same_netloc(url, base):
        page_folder = wh.url_path_lstrip_slash(url)
        if page_folder:
            wh.url_path_lstrip_slash(url)
        return page_folder
    else:
        print(f"{YELLOW}\t url: {url} has not same netloc {RESET}")
        return ''


def get_path_for_file(url, base, project_folder, ext=".html"):
    page_folder = get_page_folder(url, base)
    page_name = get_page_name(ext=ext, basename="index")
    #relative_path   = get_relative_path(url, base)

    # print("page_folder:", page_folder)
    # print("page_name  :", page_name)
    # # print("relative_path:", relative_path)

    ret = project_folder + page_folder + page_name
    ret = os.path.realpath(ret)

    return ret


def get_relative_dots(url, base):
    ret = "../" * get_page_folder(url, base).count('/')
    if not ret:
        ret = './'
    #print("get_relative_dots: -->", ret)
    return ret


def strip_protocols(url):
    url = url.replace("https://", "")
    url = url.replace("http://", "")
    url = url.replace("://", "")
    url = url.lstrip('/')
    return url


def get_path_local_root(url, base):
    #print("get_path_local_root:", "base:", base)
    #print("get_path_local_root:", "url :", url)
    # scheme = wh.url_scheme(url) # http
    url = wh.link_make_absolute(url, base)
    url = strip_protocols(url)
    base = strip_protocols(base)
    rooted = "/" + url.replace(base, "")
    #print("get_path_local_root:", "--> rooted:", rooted)
    return rooted

# https://karlsruhe.digital/en/2020/12/karlsruhe-becomes-pioneer-city-of-the-g20-global-smart-cities-alliance/
# https://karlsruhe.digital/
#                          /en/2020/12/karlsruhe-becomes-pioneer-city-of-the-g20-global-smart-cities-alliance/


def get_path_local_relative(url, base, src):

    url = wh.link_make_absolute(url, base)
    src = wh.link_make_absolute(src, base)
    # print("get_path_local_relative:", "url :", url)
    # print("get_path_local_relative:", "base:", base)
    # print("get_path_local_relative:", "src :", src)

    # scheme = wh.url_scheme(url) # http

    dots = get_relative_dots(url, base)
    # print("get_path_local_relative:", "dots:", dots)

    ret = dots + src.replace(base, "")
    # # # if ret.endswith('/'): # is a folder
    # # #     ret += get_page_name() # index.html
    # # #     #print(f"{CYAN}/ --> ret: {ret}{RESET}")
    # TODO check above, should still load online

    # print("get_path_local_root:", src, "-->", ret)
    return ret

# -----------------------------------------
#
# -----------------------------------------


def progress(perc, verbose_string="", VT=YELLOW, n=26):
    import math
    # if perc <= 0.0:
    print("{}[{}] [{:.1f}%] {}{}".format(
        VT, '.'*n, perc*100, verbose_string, RESET),  end='\r')
    if perc >= 1.0:
        end = '\n'
    else:
        n = min(n, math.ceil(n * perc))
        end = '\r'
    print("{}[{}{}".format(VT, '|'*n, RESET),  end=end)


def sleep_random(wait_secs=(1, 2), verbose_string="", verbose_interval=0.5, VT=YELLOW, n=26):
    if wait_secs and abs(wait_secs[1] - wait_secs[0]) > 0.0:
        import random
        import math
        s = random.uniform(wait_secs[0], wait_secs[1])
        print(
            "sleep_random: {:.1f}...{:.1f} --> {:.1f}s".format(wait_secs[0], wait_secs[1], s))
        start_secs = time.time()
        progress(0, verbose_string=verbose_string, VT=VT, n=n)
        while time.time() - start_secs < s:
            perc = (time.time() - start_secs) / float(s)
            progress(perc, verbose_string=verbose_string, VT=VT, n=n)
            time.sleep(0.01)
        progress(1, verbose_string=verbose_string, VT=VT, n=n)

def get_html_and_content(driver, url, b_use_driver):
    print("get_html_and_content: b_use_driver:", b_use_driver, url)
    if b_use_driver:
        driver.get(url)
        wh.wait_for_page_has_loaded(driver)
        content = driver.page_source
    else:
        content = wh.get_content(url)
    h = lxml.html.fromstring(content)
    return h, content

def may_be_a_folder(url):
    url = wh.strip_query_and_fragment(url)
    return url.endswith('/')   

def has_a_dot(url):
    return '.' in url
    
def make_static(driver, url, base, project_folder, style_path, replacements_pre, wait_secs=(1, 2)):

    # ensure trailing slash
    url             = wh.add_trailing_slash(url)
    main_url        = url
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

    sleep_random(wait_secs, main_url)
    h, content = get_html_and_content(driver, main_url, b_use_driver)

    # -----------------------------------------
    # TODO manual replace instead links_remove_similar
    # -----------------------------------------
    # TODO manual replace instead links_remove_similar
    for fr, to in replacements_pre:
        print(YELLOW, "\t replace:", sq(fr), sq(to), RESET)
        content = content.replace(dq(fr), dq(to))
        content = content.replace(sq(fr), sq(to))

    # -----------------------------------------
    #
    # -----------------------------------------
    path_base = get_path_for_file(url, base, project_folder, ext="")
    path_index = path_base + ".html"
    path_original = wh.save_html(content, path_base + "_original.html")

    # -----------------------------------------
    # make all links absolute with base
    # -----------------------------------------
    # collect internal files: skip externals
    # make them all absolute urls

    def assets_save_internals_locally(content, url, base, links, project_folder):
        
        b_strip_ver = True

        # links = wh.links_make_absolute(links, base)  NO!!!
        links = wh.links_remove_externals(links, base)
        # links = wh.links_remove_folders(links) NO!!!
        links = wh.links_remove_invalids(
            links, base, ["s.w.org", "?p=", "mailto:", "javascript:"])
        # links = wh.links_remove_similar(links) # https://karlsruhe.digital/en/home
        links = wh.links_make_unique(links)
        links = sorted(links)

        print("assets_save_internals_locally:", *links, sep='\n\t')

        for src in links:
            src = src.strip()
            print(f"{GREEN}\t src: {src}{RESET}")

            local_path = project_folder + wh.try_make_local(src, base)
            abs_src = wh.link_make_absolute(src, base)
            ###abs_src_stripped = wh.strip_query_and_fragment(abs_src)
            #new_src     = get_relative_dots(url, base) + wh.url_path_lstrip_slash(src)
            new_src = get_path_local_root(src, base)
            # new_src     = get_path_local_relative(url, base, src) # works

            # strip query ver=x.x.x
            if b_strip_ver:
                if wh.url_has_ver(new_src):
                    new_src = wh.strip_query_and_fragment(new_src)
                    print("\t\t stripped ?ver=:", new_src)
                
            # is a file? add index.html/get_page_name() to folder-links
            # TODO may not do so wp_json/ and sitemap/
            if has_a_dot(new_src) : # is a file
                print(MAGENTA, "\t\t file:", RESET, new_src)
            else:
                new_src = wh.add_trailing_slash(new_src)
                if not 'wp_json/' in new_src and not 'sitemap/' in new_src:  # TODO check WP_SPECIAL_DIRS
                    new_src += get_page_name()  # index.html
                    print(MAGENTA, "\t\t dir :", RESET,
                          new_src, "[added index.html]")
                else:
                    print(f"{MAGENTA}\t\t WP_SPECIAL_DIR: new_src: {new_src} {RESET}")
                    
            # local_path should only be written folders, index to be written later...        
            # if not'.' in local_path:
            #     local_path = wh.add_trailing_slash(local_path) + get_page_name() # TODO if not 'wp_json/' in new_src and not 'sitemap/'
            #     print(f"{MAGENTA}\t\t local_path: {local_path} {RESET}")
                
            # get and save link-asset to disk
            if not wh.file_exists_no_null(local_path): 

                wh.make_dirs(local_path)
                
                # only save files in this go, local_path
                # download the referenced files to the same path as in the html
                if not may_be_a_folder(abs_src):  # folders may get exception below?
                    
                    sleep_random(wait_secs, abs_src)

                    # TODO >>> shifted right1
                    max_tries = 10
                    for cnt in range(max_tries):
                        try:
                            print(f"{GREEN}\t\t [{cnt}] sess.get: {abs_src}{RESET}")
                            session = requests.Session()
                            session.get(base)  # sets cookies
                            res = session.get(abs_src)
                            break
                        except Exception as e:
                            print(f"{RED}\t\t ERROR {cnt} session.get: {abs_src}...sleep... {RESET}")
                            time.sleep(3)
                            
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

    ####content = wh.html_minify(content)

    # -----------------------------------------
    # make lists
    # -----------------------------------------

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
        print(GRAY, *asset, RESET, sep='\n\t')
        content = assets_save_internals_locally(
            content, url, base, asset, project_folder)
        wh.save_html(content, path_base + "_" + suffix + ".html", pretty=True)

    # -----------------------------------------
    #
    # -----------------------------------------

    content = wh.html_minify(content)
    path_minified   = wh.save_html(content, path_index)
    path_pretty     = wh.save_html(content, path_base + "_pretty.html", pretty=True)
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
        with open(config.sitemap_links_path) as file:
            lines = file.readlines()
            urls = [line.rstrip() for line in lines]

    driver = webdriver.Chrome()
    driver.implicitly_wait(30)
    
    for count, url in enumerate(urls):

        print("\n"*5 + CYAN + "#"*88 + RESET + "\n"*5)
        print(f"{CYAN}url: {url}{RESET}")
        progress(count / len(urls), verbose_string="TOTAL", VT=CYAN, n=80)
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
