"""
TODO
may better split image sizes files for keeping track of parent_urls
the list is getting very large right now


"""

import chromedriver_binary  # pip install chromedriver-binary-auto
#from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.support.expected_conditions import visibility_of_element_located
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.common.by import By
from selenium import webdriver  # pip install selenium
#from selenium.webdriver.chrome.options import Options

###from Screenshot import Screenshot_clipping # pip install Selenium-Screenshot
# https://www.browserstack.com/guide/take-screenshot-with-selenium-python

import config
import helpers_web as wh
import helpers_web as hw
import time
import urllib.parse # selenium seems to urlencode results

#-----------------------------------------
# 
#-----------------------------------------
if __name__ == "__main__":
        
    start_secs          = time.time()
    urls_visited        = []
    b_take_snapshot     = True 

    
    wh.logo_filename(__file__)
    wh.log("__file__", __file__, filepath=config.path_log_params)
    
    if b_take_snapshot:
        
        wh.log("b_take_snapshot",       b_take_snapshot,    filepath=config.path_log_params)
        
        start_secs = time.time()
        
        # -----------------------------------------
        # chrome init
        # -----------------------------------------    
        driver = None        
        for tries in range(10):
            try:
                print(f"[{tries}] webdriver.Chrome()...")
                print(f"[{tries}] {config.options}")
                driver = webdriver.Chrome(options=config.options)
                driver.implicitly_wait(config.implicit_wait) #  An implicit wait tells WebDriver to poll the DOM for a certain amount of time when trying to find any element (or elements) not immediately available. The default setting is 0 (zero). Once set, the implicit wait is set for the life of the WebDriver object.
                break
            except Exception as e:
                print(f"{wh.RED} {e} {wh.RESET}")
                time.sleep(3)

        # -----------------------------------------
        # index.html
        # -----------------------------------------   
        wh.file_make_unique(config.path_sitemap_links_internal, sort=True)
        urls = config.path_sitemap_links_internal         
        urls = wh.list_from_file(urls)
        urls = wh.links_remove_comments(urls, '#')
        urls = wh.links_replace(urls, config.replacements_pre)
        urls = wh.links_remove_externals(urls, config.base)
        urls = wh.links_strip_query_and_fragment(urls)
        urls = wh.links_make_absolute(urls, config.base)
        urls = wh.links_sanitize(urls)
        
        wh.file_make_unique(config.path_image_snaps_visited, sort=True)
        urls_visited = wh.list_from_file(config.path_image_snaps_visited)

        base = wh.add_trailing_slash("http://127.0.0.1") # config.base --> given arg
        
        for count, url in enumerate(urls):
            
            if (url in urls_visited):
                print("already visited:", wh.GRAY, url, wh.RESET)    
                continue
            
            protocol, loc, path = wh.url_split(url)
            local_url           = path.lstrip('/')
            abs_url             = base + local_url
            print("", "abs_url", abs_url)
            
            print()
            wh.progress(count / len(urls), verbose_string="TOTAL", VT=wh.CYAN, n=66)
            print()
            print(f"{wh.CYAN}[{(time.time() - start_secs)/60.0:.1f} m] abs_url: {abs_url} {wh.RESET}")
            
            # driver GET
            max_tries = 10
            for i in range(max_tries):
                try:
                    driver.get(abs_url)
                    wh.wait_for_page_has_loaded_hash(driver)
                    content = driver.page_source
                    break
                except Exception as e:
                    print(f"{wh.RED}\t [{i}] ERROR: GET abs_url: {abs_url} {wh.RESET}")     
                    time.sleep(2)
            ### max tries />
                
            # lossless
            protocol, loc, path = wh.url_split(abs_url)
            path_snap = config.path_snapshots + loc + "/snap_full_" + wh.url_to_filename(local_url) + ".webp" # webp avif png tif
            print("path_snap", path_snap)
            if not wh.file_exists_and_valid(path_snap):
                wh.fullpage_screenshot(driver, path_snap, classes_to_hide=["navbar", "banner_header", "vw-100"])   
            else:
                print("already exists:",  wh.GRAY, path_snap, wh.RESET)
                
            # visited to file       
            urls_visited.append(url)
            ####urls_visited = sorted(wh.links_make_unique(urls_visited))
            try:
                wh.list_to_file(url, config.path_image_snaps_visited, mode="a")
            except Exception as e:
                print(wh.RED, e, wh.RESET)     
                       
        ### for url />      
            
        driver.close()
        driver.quit()
        
        wh.file_make_unique(config.path_image_snaps_visited, sort=True)
        wh.log("b_take_snapshot: all done: duration: {:.1f}m".format((time.time() - start_secs)/60.0), filepath=config.path_log_params)
        
