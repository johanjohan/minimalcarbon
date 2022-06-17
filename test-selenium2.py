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

def get_page_name():
    return "index.html"

def get_page_folder(url, base):
    if wh.has_same_netloc(url, base):
        page_folder = wh.url_path_lstrip_slash(url)
        if page_folder:
            wh.url_path_lstrip_slash(url)
        return page_folder
    else:
        print(f"{RED}\t url: {url} has not same netloc {RESET}")
        exit(0)     

def get_relative_path(url, base):
    return "../" * get_page_folder(url, base).count('/')

def get_path_for_file(url, base, project_folder):
    page_folder     = get_page_folder(url, base)
    page_name       = get_page_name() 
    #relative_path   = get_relative_path(url, base)
    
    # print("page_folder:", page_folder)
    # print("page_name  :", page_name)
    # # print("relative_path:", relative_path)
    
    ret = project_folder + page_folder + page_name
    #ret = os.path.realpath(ret)

    return ret
    
# page_folder     = get_page_folder(url, base)
# page_name       = get_page_name() 
relative_path   = get_relative_path(url, base)

print("base          :", base)
print("url           :", url)
print("project_folder:", project_folder)
# print("page_folder   :", page_folder)
# print("page_name     :", page_name)
print("relative_path :", relative_path)

    
### project_folder + page_folder                 + page_name
### page/_kd/        en/about-karlsruhe-digital/   index.html
#exit(0)

#-----------------------------------------
# 
#-----------------------------------------

print(f"{CYAN}\t URL: {url}{RESET}")

driver.get(url)
wh.scroll_down_all_the_way(driver, sleep_secs=0.25, npixels=1000)
wh.wait_for_page_has_loaded_hash(driver, sleep_secs=0.5)

# seq_query_field = driver.find_element(By.ID, "seq") # find_element_by_id("seq")
# seq_query_field.send_keys(SEQUENCE)
# blast_button = driver.find_element(By.ID, "blastButton1")
# blast_button.click()

content = driver.page_source

# write the raw page
wh.make_dirs(get_path_for_file(url, base, project_folder))
with open(get_path_for_file(url, base, project_folder) + "_orig.html", 'w', encoding="utf-8") as fp:
    fp.write(content)

# download the referenced files to the same path as in the html
sess = requests.Session()
sess.get(base) # sets cookies
    
#-----------------------------------------
# 
#-----------------------------------------
   
# parse html
h = lxml.html.fromstring(content)

#-----------------------------------------
# TODO need to change all local links to absolute with domain...
# need to change links to other
#-----------------------------------------

#-----------------------------------------
# 
#-----------------------------------------

# get css/js files loaded in the head
if True:
    for hr in h.xpath('head//@href'):
            
        print(f"{YELLOW}\t hr: {hr}{RESET}")
            
        if wh.is_local(hr):
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
with open(get_path_for_file(url, base, project_folder), 'w', encoding="utf-8") as fp:
    fp.write(content)
 
#-----------------------------------------
# webbrowser
#-----------------------------------------
if True:
    print("open:", get_path_for_file(url, base, project_folder))
    if True:
        import webbrowser
        webbrowser.open('file://' + get_path_for_file(url, base, project_folder))
    else:
        os.system("start " + get_path_for_file(url, base, project_folder))