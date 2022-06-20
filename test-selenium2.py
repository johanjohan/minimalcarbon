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



#-----------------------------------------
# init the colorama module
#-----------------------------------------
import config
GREEN = config.GREEN
GRAY = config.GRAY
RESET = config.RESET
YELLOW = config.YELLOW
RED = config.RED
CYAN = config.CYAN
MAGENTA = config.MAGENTA


# https://stackoverflow.com/questions/53729201/save-complete-web-page-incl-css-images-using-python-selenium

from selenium import webdriver # pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.common.exceptions import TimeoutException
import chromedriver_binary # pip install chromedriver-binary-auto
#from lxml import html
import lxml.html
import requests
import os
import web_helpers as wh
import time
from bs4 import BeautifulSoup, Comment



#-----------------------------------------
# 
#-----------------------------------------
# dq = wh.dq
# sq = wh.sq
from web_helpers import dq as dq
from web_helpers import sq as sq
#-----------------------------------------
# 
#-----------------------------------------

def get_page_name(ext = ".html", basename="index"):
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

def get_path_for_file(url, base, project_folder, ext = ".html"):
    page_folder     = get_page_folder(url, base)
    page_name       = get_page_name(ext=ext, basename="index") 
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
    #scheme = wh.url_scheme(url) # http
    url = wh.link_make_absolute(url, base)
    url  = strip_protocols(url)
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
    
    #scheme = wh.url_scheme(url) # http

    dots = get_relative_dots(url, base)
    # print("get_path_local_relative:", "dots:", dots)
    
    ret = dots + src.replace(base,"")
    # # # if ret.endswith('/'): # is a folder
    # # #     ret += get_page_name() # index.html
    # # #     #print(f"{CYAN}/ --> ret: {ret}{RESET}")  
    # TODO check above, should still load online

    # print("get_path_local_root:", src, "-->", ret)
    return ret

#-----------------------------------------
# 
#-----------------------------------------
def progress(perc, verbose_string="", VT=YELLOW, n=40):
  import math
  #if perc <= 0.0:
  print("{}[{}] [{:.1f}%] {}{}".format(VT, '.'*n, perc*100, verbose_string, RESET),  end ='\r')
  if perc >= 1.0:
      end ='\n'
  else:
      n =  min(n, math.ceil(n * perc))
      end ='\r'
  print("{}[{}{}".format(VT, '|'*n, RESET),  end =end)
  
def sleep_random(wait_secs = (1,2), verbose_string="", verbose_interval = 0.5, VT=YELLOW, n=40):
  if wait_secs and abs(wait_secs[1] - wait_secs[0]) > 0.0:
    import random, math
    s = random.uniform(wait_secs[0], wait_secs[1])
    print("sleep_random: {:.1f}...{:.1f} --> {:.1f}s".format(wait_secs[0], wait_secs[1], s))
    start_secs = time.time()
    progress(0, verbose_string=verbose_string, VT=VT, n=n)
    while time.time() - start_secs < s:
        perc = (time.time() - start_secs) / float(s)
        progress(perc, verbose_string=verbose_string, VT=VT, n=n)
        time.sleep(0.01)
    progress(1, verbose_string=verbose_string, VT=VT, n=n)
    
def make_static(url, base, project_folder, style_path, replacements_pre, wait_secs = (1,2)):
    
    # ensure trailing slash
    url             = wh.add_trailing_slash(url)
    print("url           :", url)
    print("wait_secs     :", wait_secs)

    # base            = wh.add_trailing_slash(base)
    # project_folder  = wh.add_trailing_slash(project_folder)
    # ###relative_path   = get_relative_dots(url, base)

    # print("base          :", base)
    # print("project_folder:", project_folder)
    # ####print("relative_path :", '\'' + relative_path + '\'')
    # print("style_path    :", '\'' + style_path + '\'')

    #-----------------------------------------
    # 
    #-----------------------------------------
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    #-----------------------------------------
    # 
    #-----------------------------------------
    print(f"{CYAN}url: {url}{RESET}")
    
    sleep_random(wait_secs, url)
    driver.get(url)
    #wh.scroll_down_all_the_way(driver, sleep_secs=2, npixels=555)
    #wh.wait_for_page_has_loaded_hash(driver, sleep_secs=0.5)

    # seq_query_field = driver.find_element(By.ID, "seq") # find_element_by_id("seq")
    # seq_query_field.send_keys(SEQUENCE)
    # blast_button = driver.find_element(By.ID, "blastButton1")
    # blast_button.click()

    content = driver.page_source
    h = lxml.html.fromstring(content)
    
    #-----------------------------------------
    # TODO manual replace instead links_remove_similar
    #-----------------------------------------
    # TODO manual replace instead links_remove_similar
    for fr, to in replacements_pre:
      print(YELLOW, "\t replace:", sq(fr), sq(to), RESET)
      content = content.replace(dq(fr), dq(to))
      content = content.replace(sq(fr), sq(to))

    #-----------------------------------------
    # 
    #-----------------------------------------
    path_base       = get_path_for_file(url, base, project_folder, ext="")
    path_index      = path_base + ".html"
    path_original   = wh.save_html(content, path_base + "_original.html")

    #-----------------------------------------
    # make all links absolute with base
    #-----------------------------------------
    # collect internal files: skip externals
    # make them all absolute urls

    def assets_save_internals_locally(content, url, base, links, project_folder):
        
        #links = wh.links_make_absolute(links, base)  NO!!!
        links = wh.links_remove_externals(links, base)
        ####links = wh.links_remove_folders(links) NO!!!
        links = wh.links_remove_invalids(links, base, ["s.w.org", "?p=", "mailto:","javascript:"])
        ###links = wh.links_remove_similar(links) # https://karlsruhe.digital/en/home
        links = wh.links_make_unique(links)
        links = sorted(links)   
        

        print("assets_save_internals_locally:", *links, sep='\n\t')
        
        for src in links:  
            
            src = src.strip()  
            
            # # # avoid replacing base only....YAK
            # # if src == base:
            # #     print(f"{RED}src == base: {base}{RESET}")
            # #     time.sleep(10)
            # #     continue
            
            print(f"{GREEN}\t src: {src}{RESET}")
            
            local_path  = project_folder + wh.try_make_local(src, base)  
            abs_src     = wh.link_make_absolute(src, base)             
            #new_src     = get_relative_dots(url, base) + wh.url_path_lstrip_slash(src)
            new_src     = get_path_local_root(src, base)
            #new_src     = get_path_local_relative(url, base, src) # works
            if not os.path.exists(local_path): # was isfile ERR new!!!!
            
                # download the referenced files to the same path as in the html
                if not abs_src.endswith('/'): # folders may get exception below?
                    sleep_random(wait_secs, abs_src)
                    
                sess = requests.Session()
                sess.get(base) # sets cookies
                res = sess.get(abs_src)
                
                wh.make_dirs(local_path)   
                try:
                    with open(local_path, 'wb') as fp:
                        fp.write(res.content)  
                        print(f"{GREEN}\t\t wrote OK: {local_path}{RESET}")  
                except:
                    print(f"{RED}\t\t may be a directory?: {local_path}{RESET}")  
            else:
                print(f"{RED}\t\t already exists: {local_path}{RESET}")  
                
            # dots rel to url of this url, not to the image itself
            print(f"{GRAY}\t\t\t abs_src: {abs_src}{RESET}")  
            print(f"{GRAY}\t\t\t new_src: {new_src}{RESET}")  
            #print(f"{MAGENTA}\t\t\t replace {src} \n\t\t\t --> {new_src}{RESET}")  
            
            # post replace
            # TODO would be better to set tags or change tags or rename tags
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            content = content.replace(dq(src), dq(new_src)) # try both
            content = content.replace(sq(src), sq(new_src)) # try both
                
        return content   

    ####content = wh.html_minify(content)    


    list_head_href  = h.xpath('head//@href')

    list_body_href  = h.xpath('body//@href')

    list_link_href  = h.xpath('//link/@href') # //link[not contains(@rel, "icon")]/@href

    list_img     = h.xpath('//img/@src')
    list_img    += h.xpath('//link[contains(@rel, "icon")]/@href') # favicon
    list_img    += wh.get_style_background_images(driver)
    list_img    += wh.get_stylesheet_background_images(style_path)

    list_scripts    = h.xpath('//script/@src')

    # https://realpython.com/python-zip-function/
    assets      = [list_head_href, list_body_href, list_link_href, list_img, list_scripts]
    suffixes    = ["list_head_href", "list_body_href", "list_link_href", "list_img", "list_scripts"]
    for asset, suffix in zip(assets, suffixes):
        print("/"* 80)
        print(suffix)
        print(GRAY, *asset, RESET, sep='\n\t')      
        content = assets_save_internals_locally(content, url, base, asset, project_folder)
        wh.save_html(content, path_base + "_" + suffix + ".html", pretty=True)

    #-----------------------------------------
    # 
    #-----------------------------------------


    content = wh.html_minify(content)
    path_minified = wh.save_html(content, path_index)
    path_pretty   = wh.save_html(content, path_base + "_pretty.html", pretty=True)
    # # path_temp     = wh.load_html_from_string(driver, content)
    # # os.remove(path_temp)
    # # time.sleep(10)


    # driver.refresh()
    driver.close()
    driver.quit()

#-----------------------------------------
# 
#-----------------------------------------
    
if __name__ == "__main__":
  
    # assert os.path.exists("page/__KD__/")
    # assert os.path.exists("page/__KD__/index.html")
      
    # assert os.path.isdir("page/__KD__/")
    # #assert os.path.isdir("page/__KD__/index.html") # err
    
    # assert os.path.isfile("page/__KD__/") # err
    # assert os.path.isfile("page/__KD__/index.html")
    # exit(0)

    #-----------------------------------------
    # 
    #-----------------------------------------
    
    # TODO style_path must be downloaded first....immediately change links to local......
    
    if False:
      urls            = [
          #'https://karlsruhe.digital/',
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
    
    for count, url in enumerate(urls):
        print("\n"*5 + CYAN + "#"*88 + RESET + "\n"*5)
        print(f"{CYAN}url: {url}{RESET}")
        progress(count / len(urls), verbose_string="TOTAL", VT=CYAN, n=88)
        print("\n"*5)
        
        if not (url in config.sitemap_links_ignore):
            make_static(
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
        
    exit(0)
    
# # # # # # remove comments
# # # # # import re
# # # # # content = re.sub("<!--.*?-->", "", content)
# # # # # print("len(content)", len(content))

# # # # # # write the raw page
# # # # # wh.make_dirs(path_index)
# # # # # with open(path_index + "_orig.html", 'w', encoding="utf-8") as fp:
# # # # #     fp.write(content)

# # # # # # download the referenced files to the same path as in the html
# # # # # sess = requests.Session()
# # # # # sess.get(base) # sets cookies
    
# # # # # #-----------------------------------------
# # # # # # 
# # # # # #-----------------------------------------
   


# # # # # """
# # # # # #-----------------------------------------
# # # # # # TODO need to change all local links to absolute with domain...
# # # # # # need to change links to other
# # # # # # <section style="background-image: url('https://karlsruhe.digital/wp-content/uploads/2019/09/ÜberKadigi.jpg')">

# # # # # could scan all images on disk
# # # # #     convert to webp
# # # # #     replace old image links as text in all files with new ones
    
# # # # # same with links to other index.html


# # # # # https://stackoverflow.com/questions/27688606/how-to-fetch-style-background-image-url-using-selenium-webdrive
# # # # # <div class="body" style="background-image: url('http://d1oiazdc2hzjcz.cloudfront.net/promotions/precious/2x/p_619_o_6042_precious_image_1419849753.png');">
# # # # #  WebElement img = driver.findElement(By.className('body'));
# # # # #  String imgpath = img.getCssValue("background-image");
 
# # # # # some_variable=self.driver.find_element_by_xpath("//div[@class='body' and contains(@style,'url')]")
# # # # # some_variable2=some_variable.get_attribute('style')

# # # # # <div class="d-flex align-items-center bg-cover h-100" style="background-image: url('wp-content/uploads/2019/08/Header-1.jpg')">
# # # # #                             <div class="container content">
# # # # #                                 <div class="row">
# # # # #                                     <div class="col-xl-7 col-lg-8 color-white">
# # # # #                                         <h2 class="slide-heading">Karlsruhe<br><span class="heading-light">Motor of Digitization</span></h2>
# # # # #                                                                                                                             <a href="/en/about-karlsruhe-digital/" class="button button-full">Read more</a>
# # # # #                                                                             </div>
# # # # #                                 </div>
# # # # #                             </div>
# # # # #                         </div>
                        
# # # # # #-----------------------------------------

# # # # # element = driver.find_element_by_xpath("//div[@class='Header']/div[@class='Header-jpeg']")
# # # # # element.value_of_css_property("background-image")

# # # # # background-image.*?url\((.*?)\)

# # # # # IWebElement abc = driver.FindElement(By.XPath("//div[contains(@style, 'background-image: url(http://test.com/images/abc.png);')]"));

# # # # # substring-before(substring-after(.//*[@class='card-image']/@style, "url('"), ");")

# # # # # """

# # # # # # import re
# # # # # # x = re.search('/background-image.*?url\((.*?)\)/mi', content) 
# # # # # # print(x)
# # # # # # exit(0)

# # # # # # '//div[@style]'
# # # # # # '//*[contains(@style,"background") and contains(@style,"url(")]'
# # # # # # //*[contains(@style,'background-image')]

# # # # # # for e in h.xpath('//div[@style]'):
# # # # # #     print(f"{YELLOW}\t e: {e.values} {RESET}")

# # # # # # div = driver.find_element(By.XPATH, "//div")
# # # # # # print(div)
   
# # # # # # bg_url = div.value_of_css_property('background-image') # 'url("https://i.xxxx.com/img.jpg")'
# # # # # # # strip the string to leave just the URL part
# # # # # # bg_url = bg_url.lstrip('url("').rstrip('")')
# # # # # # # https://i.xxxx.com/img.jpg 
# # # # # # print("bg_url",bg_url)

# # # # # # for div in h.xpath("//div"):
# # # # # #     print(f"{YELLOW}\t div: {div} {div.tag} {div.text} {RESET}")

# # # # # # import cssutils
# # # # # # soup = BeautifulSoup(content, 'html.parser')
# # # # # # div  = soup.find('div', attrs={'style': True})
# # # # # # print(div)
# # # # # # if div:
# # # # # #     print(re.search(r'url\("(.+)"\)', div['style']).group(1))

# # # # # # # urls = []
# # # # # # # soup = BeautifulSoup(content, 'html.parser')
# # # # # # # for ele in soup.find_all('div', attrs={'style': True}):
# # # # # # #     print(ele)
# # # # # # #     pattern = re.compile('.*background-image:\s*url\((.*)\);')
# # # # # # #     match = pattern.match(ele.div['style'])
# # # # # # #     if match:
# # # # # # #         urls.append(match.group(1))
# # # # # # # print("urls", urls)
    
# # # # # # div_style = soup.find('div')['style']
# # # # # # style = cssutils.parseStyle(div_style)
# # # # # # url = style['background-image']
# # # # # # print("url", url)

# # # # # links = wh.get_style_background_images(driver)
# # # # # print(links)    
 
# # # # # exit(0)
# # # # # #-----------------------------------------
# # # # # # 
# # # # # #-----------------------------------------

# # # # # # get css/js files loaded in the head
# # # # # if True:
# # # # #     for hr in h.xpath('head//@href'):
            
# # # # #         print(f"{YELLOW}\t hr: {hr}{RESET}")
            
# # # # #         if wh.is_relative(hr):
# # # # #             local_path = project_folder + hr
# # # # #             local_path = wh.strip_query_and_fragment(local_path)
# # # # #             hr = base + hr
# # # # #         else:
# # # # #             local_path = project_folder + wh.url_path_lstrip_slash(hr)
# # # # #             hr = hr
            
# # # # #         # print("hr        :", hr)
# # # # #         # print("local_path:", local_path)
        
# # # # #         content = content.replace(
# # # # #             hr, 
# # # # #             relative_path 
# # # # #             + 
# # # # #             wh.strip_query_and_fragment(
# # # # #                 wh.url_path_lstrip_slash(hr)
# # # # #             )
# # # # #         )
        
# # # # #         if not os.path.isfile(local_path):
# # # # #             res = sess.get(hr)    
# # # # #             if res.status_code == 200:
# # # # #                 if wh.has_no_trailing_slash(local_path): # is a file
                    
# # # # #                     wh.make_dirs(local_path)         
# # # # #                     with open(local_path, 'wb') as fp:
# # # # #                         fp.write(res.content)
# # # # #                     #print("saved:", local_path)
# # # # #                 else:
# # # # #                     print(f"{RED}\t not a file: {local_path}{RESET}")
# # # # #             else:
# # # # #                 print(f"{RED}\t bad status: {res.status_code}{RESET}")
# # # # #         else:
# # # # #             print(f"{RED}\t already exists: {local_path}{RESET}")
            
# # # # # #-----------------------------------------
# # # # # # 
# # # # # #-----------------------------------------
# # # # # # get image/js files from the body.  
# # # # # for src in h.xpath('//@src'):
       
# # # # #     src = wh.try_make_local(src, base)
        
# # # # #     if not src or src.startswith('http'): # skip anything loaded from outside sources
# # # # #         print(f"{RED}\t skipping external: {src}{RESET}")
# # # # #         continue
    
# # # # #     print(f"{GREEN}\t src: {src}{RESET}")
    
 
# # # # #     local_path = project_folder + src
# # # # #     local_path = wh.strip_query_and_fragment(local_path)
# # # # #     #print(local_path)
            
# # # # #     src = base + src
    
# # # # #     content = content.replace(src, relative_path + wh.url_path_lstrip_slash(src))
    
# # # # #     if not os.path.isfile(local_path):
# # # # #         res = sess.get(src)
# # # # #         wh.make_dirs(local_path)   
# # # # #         with open(local_path, 'wb') as fp:
# # # # #             fp.write(res.content)  
# # # # #     else:
# # # # #         print(f"{RED}\t already exists: {local_path}{RESET}")        

# # # # # # always write index.html    
# # # # # with open(path_index, 'w', encoding="utf-8") as fp:
# # # # #     fp.write(content)
 
# # # # # #-----------------------------------------
# # # # # # webbrowser
# # # # # #-----------------------------------------
# # # # # if True:
# # # # #     print("open:", path_index)

# # # # #     if False:
# # # # #         os.system("start " + path_index)
# # # # #     else:
# # # # #         import webbrowser
# # # # #         assert os.path.isfile(path_index)
        
# # # # #         # MacOS
# # # # #         # chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
# # # # #         # Windows
# # # # #         chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
# # # # #         # Linux
# # # # #         # chrome_path = '/usr/bin/google-chrome %s'
# # # # #         webbrowser.get(chrome_path).open('file://' + path_index)