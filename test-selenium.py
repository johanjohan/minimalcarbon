# https://stackoverflow.com/questions/53729201/save-complete-web-page-incl-css-images-using-python-selenium

from selenium import webdriver # pip install selenium
from selenium.webdriver.common.by import By
import chromedriver_binary # pip install chromedriver-binary-auto
from lxml import html
import requests
import os

driver = webdriver.Chrome()
URL = 'https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastx&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome'
SEQUENCE = 'CCTAAACTATAGAAGGACAGCTCAAACACAAAGTTACCTAAACTATAGAAGGACAGCTCAAACACAAAGTTACCTAAACTATAGAAGGACAGCTCAAACACAAAGTTACCTAAACTATAGAAGGACAGCTCAAACACAAAGTTACCTAAACTATAGAAGGACA' 
base = 'https://blast.ncbi.nlm.nih.gov/'

driver.get(URL)
seq_query_field = driver.find_element(By.ID, "seq") # find_element_by_id("seq")
seq_query_field.send_keys(SEQUENCE)
blast_button = driver.find_element(By.ID, "blastButton1")
blast_button.click()

content = driver.page_source
# write the page content
if not os.path.isdir('page/'):
    os.mkdir('page/')
    
with open('page/page.html', 'w') as fp:
    fp.write(content)

# download the referenced files to the same path as in the html
sess = requests.Session()
sess.get(base)            # sets cookies

# parse html
h = html.fromstring(content)
# get css/js files loaded in the head
for hr in h.xpath('head//@href'):
    if not hr.startswith('http'):
        local_path = 'page/' + hr
        print("local_path:", local_path)
        
        if '?' in local_path:
            local_path = local_path.split('?')[0]
            print("--> local_path:", local_path)
        
        hr = base + hr
    res = sess.get(hr)
    if not os.path.exists(os.path.dirname(local_path)):
        os.makedirs(os.path.dirname(local_path))
    with open(local_path, 'wb') as fp:
        fp.write(res.content)

# get image/js files from the body.  skip anything loaded from outside sources
for src in h.xpath('//@src'):
    if not src or src.startswith('http'):
        continue
    local_path = 'page/' + src
    print(local_path)
    
    if '?' in local_path:
        local_path = local_path.split('?')[0]
        print("--> local_path:", local_path)
            
    src = base + src
    res = sess.get(hr)
    if not os.path.exists(os.path.dirname(local_path)):
        os.makedirs(os.path.dirname(local_path))
    with open(local_path, 'wb') as fp:
        fp.write(res.content)  