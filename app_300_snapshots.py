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
 
    wh.logo_filename(__file__)
    wh.log("__file__", __file__, filepath=config.path_log_params)
    
    # TODO make args ###########################
    # args: take a list of urls file or string
    base                = wh.add_trailing_slash("http://127.0.0.1") # config.base --> given arg
    config.path_snapshots_visited = config.path_snapshots + wh.add_trailing_slash(wh.strip_protocol(base)) + wh.strip_protocol(base).rstrip('/') + "_300_image_snaps_visited.csv"
    excludes = ["media.karlsruhe.digital"]
    ####################################

    start_secs          = time.time()
    #urls_visited        = []
    b_take_snapshot     = True 

    if b_take_snapshot:
                        
        # -----------------------------------------
        # chrome init
        # -----------------------------------------    
        driver = None        
        for tries in range(10):
            try:
                print(f"[{tries}] webdriver.Chrome()...")
                print(f"[{tries}] {config.options}")
                driver = webdriver.Chrome(options=config.options)
                driver.implicitly_wait(5) #  An implicit wait tells WebDriver to poll the DOM for a certain amount of time when trying to find any element (or elements) not immediately available. The default setting is 0 (zero). Once set, the implicit wait is set for the life of the WebDriver object.
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
        urls = wh.links_remove_excludes(urls, excludes) # <<<
        urls = wh.links_replace(urls, config.replacements_pre)
        urls = wh.links_remove_externals(urls, config.base)
        urls = wh.links_strip_query_and_fragment(urls) # do not need for snaps
        urls = wh.links_make_absolute(urls, config.base)
        urls = wh.links_sanitize(urls)
        
        # change base here as necessary
        if base != config.base:
            new_urls = []
            for url in urls:
                protocol, loc, path = wh.url_split(url)
                new_url = wh.get_path_local_root_subdomains(url, config.base)
                new_url = base + new_url.lstrip('/')
                new_urls.append(new_url)
                print("\t", new_url, wh.GRAY, "[", url, "]", wh.RESET)
            urls = new_urls
        
        wh.make_dirs(config.path_snapshots_visited)
        wh.file_make_unique(config.path_snapshots_visited, sort=True)
        #urls_visited = wh.list_from_file(config.path_snapshots_visited)

        for count, abs_url in enumerate(urls):
                        
            print()
            wh.progress(count / len(urls), verbose_string="TOTAL", VT=wh.CYAN, n=66)
            print()
            print(f"{wh.CYAN}[{(time.time() - start_secs)/60.0:.1f} m] abs_url: {abs_url} {wh.RESET}")

            protocol, loc, path = wh.url_split(abs_url)
            path_snap_base  = config.path_snapshots + loc + "/snap_full_" + wh.url_to_filename(path)
            path_snap       = path_snap_base + ".webp"  # webp avif png tif
            path_snap_png   = path_snap_base + ".png"   # fallback for large dims
            wh.log("path_snap", path_snap, filepath=config.path_log_params)
            
            #if (abs_url in urls_visited) or wh.file_exists_and_valid(path_snap) or wh.file_exists_and_valid(path_snap_png) :
            if wh.file_exists_and_valid(path_snap) or wh.file_exists_and_valid(path_snap_png) :
                print("\t", wh.MAGENTA, "already visited:", wh.GRAY, abs_url, wh.RESET)    
                continue
                                  
            # driver GET
            #max_tries = 10
            for i in range(max_tries:=10):
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
            # The maximum pixel dimensions of a WebP image is 16383 x 16383
            if not wh.file_exists_and_valid(path_snap):
                wh.fullpage_screenshot(driver, path_snap, classes_to_hide=["navbar", "banner_header", "vw-100"])   
            else:
                print("already exists:",  wh.GRAY, path_snap, wh.RESET)
                
            # # visited to file       
            # urls_visited.append(abs_url)
            # try:
            #     wh.string_to_file(abs_url + "\n", config.path_snapshots_visited, mode="a")
            # except Exception as e:
            #     print(wh.RED, e, wh.RESET)     
                       
        ### for url />      
            
        driver.close()
        driver.quit()
        
        ####wh.file_make_unique(config.path_snapshots_visited, sort=True)
        wh.log("b_take_snapshot: all done: duration: {:.1f}m".format((time.time() - start_secs)/60.0), filepath=config.path_log_params)
        
