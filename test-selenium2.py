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

# init the colorama module
import colorama
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
RED = colorama.Fore.RED
CYAN = colorama.Fore.CYAN

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

def get_relative_dots(url, base):
    ret = "../" * get_page_folder(url, base).count('/')
    
    # if not ret:
    #     ret = './'
        
    #print("get_relative_dots: -->", ret)
    return ret

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
 
#-----------------------------------------
# 
#-----------------------------------------
   
driver = webdriver.Chrome()
driver.implicitly_wait(10)

project_folder  = "page/_kd/"
base            = 'https://karlsruhe.digital/'
url             = 'https://karlsruhe.digital/en/about-karlsruhe-digital/'
#url             = 'https://karlsruhe.digital/'

# trailing slash
base            = wh.add_trailing_slash(base)
url             = wh.add_trailing_slash(url)
project_folder  = wh.add_trailing_slash(project_folder)
relative_path   = get_relative_dots(url, base)

print("base          :", base)
print("url           :", url)
print("project_folder:", project_folder)
print("relative_path :", '\'' + relative_path + '\'')

    
### project_folder + page_folder                 + page_name
### page/_kd/        en/about-karlsruhe-digital/   index.html
#exit(0)

#-----------------------------------------
# 
#-----------------------------------------

print(f"{CYAN}url: {url}{RESET}")

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
# 
#-----------------------------------------
path_base   = get_path_for_file(url, base, project_folder, ext="")
path_index  = path_base + ".html"

#-----------------------------------------
# make all links absolute with base
#-----------------------------------------
# collect internal files: skip externals
# make them all absolute urls

def assets_save_internals_locally(content, url, base, links, project_folder):
    
    #links = wh.links_make_absolute(links, base)
    links = wh.links_remove_externals(links, base)
    #links = wh.links_remove_folders(links)
    links = wh.links_make_unique(links)
    links = sorted(links)
    print("assets_save_internals_locally:", *links, sep='\n\t')
    
    for src in links:    
        print(f"{GREEN}\t src: {src}{RESET}")
        
        local_path  = project_folder + wh.try_make_local(src, base)  
        abs_src     = wh.link_make_absolute(src, base)             
        rel_src     = get_relative_dots(url, base) + wh.url_path_lstrip_slash(src)
        if not os.path.isfile(local_path):
        
            # download the referenced files to the same path as in the html
            sess = requests.Session()
            sess.get(base) # sets cookies
            res = sess.get(abs_src)
            
            wh.make_dirs(local_path)   
            with open(local_path, 'wb') as fp:
                fp.write(res.content)  
                print(f"{GREEN}\t\t wrote OK: {local_path}{RESET}")  
        else:
            print(f"{RED}\t\t already exists: {local_path}{RESET}")  
            
        # dots rel to url of this url, not to the image itself
        print(f"{GRAY}\t\t\t abs_src: {abs_src}{RESET}")  
        print(f"{GRAY}\t\t\t rel_src: {rel_src}{RESET}")  
        content = content.replace(src, rel_src)
            
    return content   

####content = wh.html_minify(content)    

list_img     = h.xpath('//img/@src')
list_img    += h.xpath('//link[contains(@rel, "icon")]/@href') # favicon
list_img    += wh.get_style_background_images(driver)
print(GRAY, *list_img, RESET, sep='\n')      
content     = assets_save_internals_locally(content, url, base, list_img, project_folder)   
path_images = wh.save_html(content, path_base + "_images.html", pretty=True)


list_head_href  = h.xpath('head//@href')

list_body_href  = h.xpath('body//@href')


list_scripts    = h.xpath('//script/@src')
list_scripts    = wh.links_make_absolute_internals_only(list_scripts, base)
#print(*list_scripts, sep='\n')

exit(0)

#-----------------------------------------
# 
#-----------------------------------------


path_original   = wh.save_html(content, path_base + "_original.html")
path_temp       = wh.load_html_from_string(driver, content)
os.remove(path_temp)
time.sleep(10)

content = wh.html_minify(content)

# write the raw page
path_minified = wh.save_html(content, path_base + "_minified.html")
path_temp     = wh.load_html_from_string(driver, content)
os.remove(path_temp)
time.sleep(10)


driver.refresh()
driver.close()
driver.quit()
exit(0)
    
# remove comments
import re
content = re.sub("<!--.*?-->", "", content)
print("len(content)", len(content))

# write the raw page
wh.make_dirs(path_index)
with open(path_index + "_orig.html", 'w', encoding="utf-8") as fp:
    fp.write(content)

# download the referenced files to the same path as in the html
sess = requests.Session()
sess.get(base) # sets cookies
    
#-----------------------------------------
# 
#-----------------------------------------
   


"""
#-----------------------------------------
# TODO need to change all local links to absolute with domain...
# need to change links to other
# <section style="background-image: url('https://karlsruhe.digital/wp-content/uploads/2019/09/ÜberKadigi.jpg')">

could scan all images on disk
    convert to webp
    replace old image links as text in all files with new ones
    
same with links to other index.html


https://stackoverflow.com/questions/27688606/how-to-fetch-style-background-image-url-using-selenium-webdrive
<div class="body" style="background-image: url('http://d1oiazdc2hzjcz.cloudfront.net/promotions/precious/2x/p_619_o_6042_precious_image_1419849753.png');">
 WebElement img = driver.findElement(By.className('body'));
 String imgpath = img.getCssValue("background-image");
 
some_variable=self.driver.find_element_by_xpath("//div[@class='body' and contains(@style,'url')]")
some_variable2=some_variable.get_attribute('style')

<div class="d-flex align-items-center bg-cover h-100" style="background-image: url('wp-content/uploads/2019/08/Header-1.jpg')">
                            <div class="container content">
                                <div class="row">
                                    <div class="col-xl-7 col-lg-8 color-white">
                                        <h2 class="slide-heading">Karlsruhe<br><span class="heading-light">Motor of Digitization</span></h2>
                                                                                                                            <a href="/en/about-karlsruhe-digital/" class="button button-full">Read more</a>
                                                                            </div>
                                </div>
                            </div>
                        </div>
                        
#-----------------------------------------

element = driver.find_element_by_xpath("//div[@class='Header']/div[@class='Header-jpeg']")
element.value_of_css_property("background-image")

background-image.*?url\((.*?)\)

IWebElement abc = driver.FindElement(By.XPath("//div[contains(@style, 'background-image: url(http://test.com/images/abc.png);')]"));

substring-before(substring-after(.//*[@class='card-image']/@style, "url('"), ");")

"""

# import re
# x = re.search('/background-image.*?url\((.*?)\)/mi', content) 
# print(x)
# exit(0)

# '//div[@style]'
# '//*[contains(@style,"background") and contains(@style,"url(")]'
# //*[contains(@style,'background-image')]

# for e in h.xpath('//div[@style]'):
#     print(f"{YELLOW}\t e: {e.values} {RESET}")

# div = driver.find_element(By.XPATH, "//div")
# print(div)
   
# bg_url = div.value_of_css_property('background-image') # 'url("https://i.xxxx.com/img.jpg")'
# # strip the string to leave just the URL part
# bg_url = bg_url.lstrip('url("').rstrip('")')
# # https://i.xxxx.com/img.jpg 
# print("bg_url",bg_url)

# for div in h.xpath("//div"):
#     print(f"{YELLOW}\t div: {div} {div.tag} {div.text} {RESET}")

# import cssutils
# soup = BeautifulSoup(content, 'html.parser')
# div  = soup.find('div', attrs={'style': True})
# print(div)
# if div:
#     print(re.search(r'url\("(.+)"\)', div['style']).group(1))

# # urls = []
# # soup = BeautifulSoup(content, 'html.parser')
# # for ele in soup.find_all('div', attrs={'style': True}):
# #     print(ele)
# #     pattern = re.compile('.*background-image:\s*url\((.*)\);')
# #     match = pattern.match(ele.div['style'])
# #     if match:
# #         urls.append(match.group(1))
# # print("urls", urls)
    
# div_style = soup.find('div')['style']
# style = cssutils.parseStyle(div_style)
# url = style['background-image']
# print("url", url)

links = wh.get_style_background_images(driver)
print(links)    
 
exit(0)
#-----------------------------------------
# 
#-----------------------------------------

# get css/js files loaded in the head
if True:
    for hr in h.xpath('head//@href'):
            
        print(f"{YELLOW}\t hr: {hr}{RESET}")
            
        if wh.is_relative(hr):
            local_path = project_folder + hr
            local_path = wh.strip_query_and_fragment(local_path)
            hr = base + hr
        else:
            local_path = project_folder + wh.url_path_lstrip_slash(hr)
            hr = hr
            
        # print("hr        :", hr)
        # print("local_path:", local_path)
        
        content = content.replace(
            hr, 
            relative_path 
            + 
            wh.strip_query_and_fragment(
                wh.url_path_lstrip_slash(hr)
            )
        )
        
        if not os.path.isfile(local_path):
            res = sess.get(hr)    
            if res.status_code == 200:
                if wh.has_no_trailing_slash(local_path): # is a file
                    
                    wh.make_dirs(local_path)         
                    with open(local_path, 'wb') as fp:
                        fp.write(res.content)
                    #print("saved:", local_path)
                else:
                    print(f"{RED}\t not a file: {local_path}{RESET}")
            else:
                print(f"{RED}\t bad status: {res.status_code}{RESET}")
        else:
            print(f"{RED}\t already exists: {local_path}{RESET}")
            
#-----------------------------------------
# 
#-----------------------------------------
# get image/js files from the body.  
for src in h.xpath('//@src'):
       
    src = wh.try_make_local(src, base)
        
    if not src or src.startswith('http'): # skip anything loaded from outside sources
        print(f"{RED}\t skipping external: {src}{RESET}")
        continue
    
    print(f"{GREEN}\t src: {src}{RESET}")
    
 
    local_path = project_folder + src
    local_path = wh.strip_query_and_fragment(local_path)
    #print(local_path)
            
    src = base + src
    
    content = content.replace(src, relative_path + wh.url_path_lstrip_slash(src))
    
    if not os.path.isfile(local_path):
        res = sess.get(src)
        wh.make_dirs(local_path)   
        with open(local_path, 'wb') as fp:
            fp.write(res.content)  
    else:
        print(f"{RED}\t already exists: {local_path}{RESET}")        

# always write index.html    
with open(path_index, 'w', encoding="utf-8") as fp:
    fp.write(content)
 
#-----------------------------------------
# webbrowser
#-----------------------------------------
if True:
    print("open:", path_index)

    if False:
        os.system("start " + path_index)
    else:
        import webbrowser
        assert os.path.isfile(path_index)
        
        # MacOS
        # chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
        # Windows
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        # Linux
        # chrome_path = '/usr/bin/google-chrome %s'
        webbrowser.get(chrome_path).open('file://' + path_index)