import chromedriver_binary  # pip install chromedriver-binary-auto
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver  # pip install selenium
from selenium.webdriver.chrome.options import Options

import config
import helpers_web as wh
import helpers_web as hw
import time
import os

start_secs      = time.time()
image_sizes = []

def append_image_sizes(url, e):
    if e:
        tpl  = (
            url, 
            e.size['width'], 
            e.size['height'], 
            e.get_attribute("naturalWidth"), 
            e.get_attribute("naturalHeight")
        )        
        
        list_tpl = list(tpl)
        if not list_tpl in image_sizes:
            line = ','.join([str(value) for value in tpl])
            #wh.string_to_file(line + '\n', config.path_image_sizes, mode="a")
            print("\t\t", wh.MAGENTA, line, wh.RESET)
            image_sizes.append(list_tpl)
    else:
        print(wh.RED, "e is None...!!!", wh.RESET)
        
def extract_url(string):
    if "url" in string:
        url = string
        url = url.split('url')[-1]
        url = url.split(')')[0]
        url = url.strip().lstrip('(')
        for q in ["\"", "\'"]:
            url = url.strip().lstrip(q).rstrip(q)
        #print(string, YELLOW, url, RESET)
        return url
    else:
        return string
                    
if __name__ == "__main__":
    
    wh.logo_filename(__file__)
    wh.log("__file__", __file__, filepath=config.path_log_params)
    
    # -----------------------------------------
    # chrome init
    # -----------------------------------------    
    driver = None        
    for tries in range(10):
        try:
            print(f"[{tries}] webdriver.Chrome()...")
            print(f"[{tries}] {config.options}")
            driver = webdriver.Chrome(options=config.options)
            #driver.implicitly_wait(1)
            break
        except Exception as e:
            print(f"{wh.RED} {e} {wh.RESET}")
            time.sleep(3)

    # -----------------------------------------
    # index.html
    # -----------------------------------------   
    urls = config.path_sitemap_links_internal         
    urls = wh.list_from_file(urls)
    urls = wh.links_remove_comments(urls, '#')
    urls = wh.links_replace(urls, config.replacements_pre)
    urls = wh.links_remove_externals(urls, config.base)
    urls = wh.links_strip_query_and_fragment(urls)
    urls = wh.links_make_absolute(urls, config.base)
    urls = wh.links_sanitize(urls)

    for count, url in enumerate(urls):
        
        url = wh.get_path_local_root_subdomains(url, config.base)
        ###protocol, loc, path = wh.url_split(url)
        
        # replace for localhost
        url = "http://127.0.0.1/" + url.lstrip('/')

        wh.progress(count / len(urls), verbose_string="TOTAL", VT=wh.CYAN, n=66)
        print()
        print(f"{wh.CYAN}[{(time.time() - start_secs)/60.0:.1f} m] url: {url}{wh.RESET}")
        ###continue
        
        try:
            driver.get(url)
            wh.wait_for_page_has_loaded(driver)
            content = driver.page_source
        except Exception as e:
            print(f"{wh.RED}\t ERROR: GET url: {url} {wh.RESET}")     
        #print(driver.page_source)   
                        
    # # -----------------------------------------
    # # index.html
    # # -----------------------------------------   
    # files = wh.collect_files_endswith(config.project_folder, ["index.html"])         
    # for count, file in enumerate(files):
        
    #     file = wh.to_posix(os.path.abspath(file))
        
    #     wh.progress(count / len(files), verbose_string="TOTAL", VT=wh.CYAN, n=66)
    #     print()
    #     print(f"{wh.CYAN}[{(time.time() - start_secs)/60.0:.1f} m] url: {file}{wh.RESET}")        
        
    #     try:
    #         driver.get("file:///" + file)
    #         wh.wait_for_page_has_loaded(driver)
    #         content = driver.page_source
    #     except Exception as e:
    #         print(f"{wh.RED}\t ERROR: GET url: {file} {wh.RESET}")     
    #     #print(driver.page_source)          
        
        # regular images
        print("\t", "driver.find_elements: By.CSS_SELECTOR", flush=True)
        for e in driver.find_elements(By.CSS_SELECTOR, "img"):
            append_image_sizes(
                e.get_attribute("src"), 
                e
            )
            
        # style background
        print("\t", "driver.find_elements: By.XPATH", flush=True)
        for e in driver.find_elements(By.XPATH, "//div[contains(@style, 'background-image')]"):
            append_image_sizes(
                extract_url(e.get_attribute("style")), 
                e
            )  
    ### for />      
        
    driver.close()
    driver.quit()
    
    print("image_sizes", *image_sizes, sep="\n\t")
    
    wh.string_to_file("name,width,height,naturalWidth,naturalHeight\n", config.path_image_sizes, mode="w")
    wh.list_to_file(image_sizes, config.path_image_sizes, mode="a")
    
    wh.log("all done: duration: {:.1f}m".format((time.time() - start_secs)/60.0), filepath=config.path_log_params)