# https://stackoverflow.com/questions/53729201/save-complete-web-page-incl-css-images-using-python-selenium

from selenium import webdriver # pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
import chromedriver_binary # pip install chromedriver-binary-auto
from lxml import html
import requests
import os
import web_helpers as wh


driver = webdriver.Chrome()
base = 'https://karlsruhe.digital/'
URL  = base
FOLDER = "page/_kd/"

# init the colorama module
import colorama
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
RED = colorama.Fore.RED
CYAN = colorama.Fore.CYAN

print(f"{CYAN}\t URL: {URL}{RESET}")

driver.get(URL)
# seq_query_field = driver.find_element(By.ID, "seq") # find_element_by_id("seq")
# seq_query_field.send_keys(SEQUENCE)
# blast_button = driver.find_element(By.ID, "blastButton1")
# blast_button.click()

# wait until results are loaded
WebDriverWait(driver, 60).until(visibility_of_element_located((By.CLASS_NAME, 'owl-next')))


content = driver.page_source
# write the page content
if not os.path.isdir(FOLDER):
    os.makedirs(FOLDER)
    
with open(FOLDER + 'page.html', 'w', encoding="utf-8") as fp:
    fp.write(content)

# download the referenced files to the same path as in the html
sess = requests.Session()
sess.get(base)            # sets cookies
        
# parse html
h = html.fromstring(content)
# get css/js files loaded in the head
for hr in h.xpath('head//@href'):
        
    print(f"{YELLOW}\t hr: {hr}{RESET}")
        
    if wh.is_local(hr):
        local_path = FOLDER + hr
        local_path = wh.strip_query_and_fragment(local_path)
        hr = base + hr
    else:
        local_path = FOLDER + wh.url_path(hr).lstrip('/')
        
    print("hr        :", hr)
    print("local_path:", local_path)
    
    res = sess.get(hr)    
    if res.status_code == 200:
        if wh.has_no_trailing_slash(local_path): # is a file
            
            wh.make_dirs(local_path)         
            with open(local_path, 'wb') as fp:
                fp.write(res.content)
            print("saved:", local_path)
            
            content = content.replace(hr, wh.url_path(hr).lstrip('/'))
        else:
            print(f"{RED}\t not a file: {local_path}{RESET}")
    else:
        print(f"{RED}\t bad status: {res.status_code}{RESET}")
        

# get image/js files from the body.  skip anything loaded from outside sources
for src in h.xpath('//@src'):
    
    if wh.has_same_netloc(src, base):
        src = wh.try_make_local(src, base)
    
    print(f"{GREEN}\t src: {src}{RESET}")
    
    if not src or src.startswith('http'): # skip anything loaded from outside sources
        print(f"{RED}\t skipping external: {src}{RESET}")
        continue
    
    local_path = FOLDER + src
    print(local_path)
    local_path = wh.strip_query_and_fragment(local_path)
            
    src = base + src
    res = sess.get(src)
    
    wh.make_dirs(local_path)       
    with open(local_path, 'wb') as fp:
        fp.write(res.content)  
        
    content = content.replace(src, wh.url_path(src).lstrip('/'))
    
with open(FOLDER + 'page_local.html', 'w', encoding="utf-8") as fp:
    fp.write(content)