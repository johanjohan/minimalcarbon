"""
TODO
may better split image sizes files for keeping track of parent_urls
the list is getting very large right now


"""

import chromedriver_binary  # pip install chromedriver-binary-auto
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver  # pip install selenium
from selenium.webdriver.chrome.options import Options

###from Screenshot import Screenshot_clipping # pip install Selenium-Screenshot
# https://www.browserstack.com/guide/take-screenshot-with-selenium-python

import config
import helpers_web as wh
import helpers_web as hw
import time
import os
import requests

import urllib
import urllib.parse # selenium seems to urlencode results

#-----------------------------------------
# 
#-----------------------------------------            
def __append_to_image_size_tuples(collected, url, base, bases, e, vt=wh.MAGENTA, pre="\t\t"):
    
    if not url:
        print(pre, "ignore:", "None:", wh.RED, url, wh.RESET)
        return
    
    # ignore external? accept bases
    protocol, loc, path = wh.url_split(url)
    bases               = list(bases)
    if not any([(loc in b) for b in bases]):
        print(pre, "ignore:", "external:", wh.RED, url, wh.RESET)
        return 
    
    if e and url:

        # TODO should broken down to 
        ###local = '/' + path # no loc as we already have proven it is internal
        local           = wh.get_path_local_root_subdomains(url, base)
        local_name, ext = os.path.splitext(local)
        
        tpl  = [
            local_name,                         # no ext
            local, 
            e.size['width'],                    # size in web doc
            e.size['height'], 
            e.get_attribute("naturalWidth"),    # size on disk
            e.get_attribute("naturalHeight"),
            url,
            "x"
        ]    
        
        if False:
            print(wh.YELLOW, "url       :", url,        wh.RESET)
            print(wh.YELLOW, "base      :", base,       wh.RESET)
            print(wh.YELLOW, "   gplrs():", wh.get_path_local_root_subdomains(url, base),       wh.RESET)
            print(wh.YELLOW, "bases     :", bases,      wh.RESET)
            print(wh.YELLOW, "local     :", local,      wh.RESET)
            print(wh.YELLOW, "local_name:", local_name, wh.RESET)
            print()
        
        if not tpl in collected: 
            print(pre, vt + str(url), e.size['width'], e.size['height'], wh.RESET)
            collected.append(tpl)
        
    else:
        print(wh.RED, "e  :", e,    wh.RESET)
        print(wh.RED, "url:", url,  wh.RESET)
### def />        
#-----------------------------------------
"""
srcset="https://karlsruhe.digital/wp-content/uploads/2022/07/Bunte-Nacht-der-Digitalisierung-2022.jpeg 1500w, 
        https://karlsruhe.digital/wp-content/uploads/2022/07/Bunte-Nacht-der-Digitalisierung-2022-300x200.jpeg 300w, 
        https://karlsruhe.digital/wp-content/uploads/2022/07/Bunte-Nacht-der-Digitalisierung-2022-768x512.jpeg 768w, 
        https://karlsruhe.digital/wp-content/uploads/2022/07/Bunte-Nacht-der-Digitalisierung-2022-1024x683.jpeg 1024w, 
        https://karlsruhe.digital/wp-content/uploads/2022/07/Bunte-Nacht-der-Digitalisierung-2022-75x50.jpeg 75w"
<source srcset="/images/cereal-box.avif" type="image/avif" />
"""   
def find_all_image_size_tuples(
    collected, 
    driver, 
    base, 
    bases, 
    b_scan_srcset, 
    pre="\t", 
    turns_for_slow_funcs=config.turns_for_slow_funcs
    ):
        
    print(pre, "find_all_image_size_tuples: b_scan_srcset:", wh.CYAN, str(b_scan_srcset), wh.RESET)
    print(pre, "find_all_image_size_tuples: driver       :", wh.GRAY, str(driver), wh.RESET)
    print(pre, "find_all_image_size_tuples: base         :", wh.GRAY, base,  wh.RESET)
    print(pre, "find_all_image_size_tuples: bases        :", wh.GRAY, bases, wh.RESET)
    print(pre, "find_all_image_size_tuples: counter      :", wh.GRAY, find_all_image_size_tuples.counter, wh.RESET)
    pre += "\t"
    
    eu      = set()   
    bases   = list(bases)
    
    def __add(e, url, eu):
        url = urllib.parse.unquote(url) # << !
        eu.add(tuple([e, url]))
        print(wh.CYAN + '.', end='', flush=True)
        
    # NOTE findElements waits for at least one element or until timeout which is defined by the implicit wait setting
    # find urls in driver 
    # NOTE selenium returns url encoded strings --> urllib.parse.unquote(url)
    try:
        # regular images
        print(pre, "driver.find_elements: By.CSS_SELECTOR", flush=True)
        print(pre, wh.CYAN, end='')
        for e in driver.find_elements(By.CSS_SELECTOR, "img"):
            url = e.get_attribute("src")
            __add(e, url, eu)
        print(wh.RESET)
            
        # srcset
        if b_scan_srcset:
            print(pre, "driver.find_elements: srcset", flush=True)
            print(pre, wh.CYAN, end='')
            for e in driver.find_elements(By.XPATH, "//*[@srcset]"):
                url     = e.get_attribute("srcset")
                links   = url.split(',')
                for link in links:
                    subs = link.split(' ')
                    url  = ' '.join(sub for sub in subs[:-1]) # except last
                    __add(e, url, eu)
            print(wh.RESET)

        
        # TODO these could only be traversed once or twice !!!!!!!!!!!!!!!!!!!!!!!!
        # traverse body: all elements for styles attached, a bit slow but effective
        if find_all_image_size_tuples.counter < turns_for_slow_funcs:
            xpath_css = "//body//*"
            print(pre, f"driver.find_elements: By.XPATH {xpath_css}", flush=True)
            print(pre, wh.CYAN, end='')
            for e in driver.find_elements(By.XPATH, xpath_css):
                
                imgpath = e.value_of_css_property("background-image") 
                if imgpath != "none" and "url" in imgpath:
                    url = wh.extract_url(imgpath)
                    __add(e, url, eu)
                    
                imgpath = e.value_of_css_property("content")
                if imgpath != "none" and "url" in imgpath:
                    print(wh.YELLOW, "content", imgpath, wh.RESET) # <<<<<<<<<<<<< 
                    time.sleep(3)
                    url = wh.extract_url(imgpath)
                    __add(e, url, eu)

            print(wh.RESET)
        
        # favicon
        if find_all_image_size_tuples.counter < turns_for_slow_funcs:
            xpath_css = "//link[contains(@rel, 'icon')]"
            print(pre, f"driver.find_elements: By.XPATH {xpath_css}", flush=True)
            print(pre, wh.CYAN, end='')
            for e in driver.find_elements(By.XPATH, xpath_css):
                url = e.get_attribute("href")
                print(wh.YELLOW, url, wh.RESET)
                __add(e, url, eu)
            print(wh.RESET)      
        
        # # # # # # # style background: already caught above
        # # # # # # if False:
        # # # # # #     print(pre, "driver.find_elements: By.XPATH", flush=True)
        # # # # # #     print(pre, wh.CYAN, end='')
        # # # # # #     #for e in driver.find_elements(By.XPATH, "//*[contains(@style, 'background-image')]"):
        # # # # # #     for e in driver.find_elements(By.XPATH, "//*[contains(@style, 'url')]"):
        # # # # # #         print("\t\t", wh.YELLOW, e.get_attribute("style"), wh.RESET)
        # # # # # #         url = extract_url(e.get_attribute("style"))
        # # # # # #         __add(e, url, eu)
        # # # # # #     print(wh.RESET)
        
    except Exception as e:
        print(pre, wh.RED, "ERROR", e, wh.RESET)
            
    print(pre, "len(eu):", len(eu))
            
    # append to image_tuples
    for e, url in eu:        
        __append_to_image_size_tuples(
            collected,
            urllib.parse.unquote(url), # safety
            base,
            bases,
            e,
            vt=wh.GREEN
        ) 
        
    find_all_image_size_tuples.counter += 1
    
### /> def
find_all_image_size_tuples.counter = 0    
        
#-----------------------------------------
# 
#-----------------------------------------
def file_image_sizes_make_unique(b_sort=True, b_sort_reverse=True):
    
    print("file_image_sizes_make_unique:", wh.GRAY + config.path_image_sizes, wh.RESET)
    
    if not os.path.isfile(config.path_image_sizes):
        return
    
    res = []
    with open(config.path_image_sizes, mode="r", encoding="utf-8") as fp:
        for line in fp:
            if line.startswith('/'):
                subs = line.rstrip('\n').split(',')
                res.append(list(subs))
    
    len_orig = len(res)            
    res = [list(x) for x in set(tuple(x) for x in res)] # https://stackoverflow.com/questions/3724551/python-uniqueness-for-list-of-lists
    
    if b_sort:
        res = sorted(res, reverse=b_sort_reverse) # reverse we can skip searching after first hit which is highest size
        
    print("file_image_sizes_make_unique: removed:", len(res) - len_orig, "items") 
    
    #print("res", *res, sep="\n\t")   
    
    wh.string_to_file("localbasename,localname,width,height,naturalWidth,naturalHeight,url,url_parent\n", config.path_image_sizes, mode="w")
    wh.list_to_file(res, config.path_image_sizes, mode="a")            
    
#-----------------------------------------
def file_image_sizes_get_index(index):
    res = []
    
    if os.path.isfile(config.path_image_sizes):
        with open(config.path_image_sizes, mode="r", encoding="utf-8") as fp:
            for line in fp:
                if line.startswith('/'):
                    subs = line.rstrip('\n').split(',')
                    assert index < len(subs), f"{index} < {len(subs)}"
                    res.append(subs[index])
             
    res = wh.links_make_unique(res) 
    res = sorted(res)          
    #print("res", *res, sep="\n\t")    
    return res

#-----------------------------------------
# def file_image_sizes_get_url_parents():
#     return file_image_sizes_get_index(7)
#-----------------------------------------
# get the urls as they appeared in the document
def file_image_sizes_get_urls():
    return file_image_sizes_get_index(6)
#-----------------------------------------
# 
#-----------------------------------------

if __name__ == "__main__":
    
    print("do not use")
    exit(0)
    
    
    start_secs          = time.time()
    ###image_sizes         = []
    urls_visited        = []
    b_take_snapshot     = False 
    b_scan_image_sizes  = True
    b_download_images   = True  # TODO make own program

    
    wh.logo_filename(__file__)
    wh.log("__file__", __file__, filepath=config.path_log_params)
    
    if b_scan_image_sizes or b_take_snapshot:
        
        wh.logo("b_scan_image_sizes")
        wh.log("b_scan_image_sizes",    b_scan_image_sizes, filepath=config.path_log_params)
        wh.log("b_take_snapshot",       b_take_snapshot,    filepath=config.path_log_params)
        
        start_secs          = time.time()
        
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
        

        image_size_tuples = []
        file_image_sizes_make_unique()
        
        wh.file_make_unique(config.path_image_sizes_visited, sort=True)
        urls_visited = wh.list_from_file(config.path_image_sizes_visited)

        for count, url in enumerate(urls):
        
            base        = config.base
            bases       = [config.base, "https://kadigital.s3-cdn.welocal.cloud/", "https://media.karlsruhe.digital/"]
            local_url   = wh.get_path_local_root_subdomains(url, config.base)
            abs_url     = wh.link_make_absolute(url, base)

            print()
            wh.progress(count / len(urls), verbose_string="TOTAL", VT=wh.CYAN, n=66)
            print()
            print(f"{wh.CYAN}[{(time.time() - start_secs)/60.0:.1f} m] abs_url: {abs_url} {wh.RESET}")
            
            if not (url in urls_visited) or b_take_snapshot:
                
                # driver GET
                if b_scan_image_sizes or b_take_snapshot:
                    max_tries = 10
                    for i in range(max_tries):
                        try:
                            driver.get(abs_url)
                            wh.wait_for_page_has_loaded_hash(driver)
                            content = driver.page_source
                            break
                        except Exception as e:
                            print(f"{wh.RED}\t [{i}] ERROR: GET url: {url} {wh.RESET}")     
                            time.sleep(2)
                    
                if b_scan_image_sizes:
                    find_all_image_size_tuples(
                        image_size_tuples, 
                        driver, 
                        base,
                        bases, 
                        b_scan_srcset=False, 
                        pre="\t"
                    )
                    print("len(image_size_tuples):", len(image_size_tuples))
                    
                    # to file
                    try:
                        # TODO at the very end create header nd make unique
                        wh.list_to_file(image_size_tuples, config.path_image_sizes, mode="a")
                    except Exception as e:
                        print(wh.RED, e, wh.RESET)

                            
                if b_take_snapshot:
                    path_snap = config.path_snapshots + "snap_full_" + wh.url_to_filename(local_url) + ".webp" # webp avif png tif
                    if not wh.file_exists_and_valid(path_snap):
                        wh.fullpage_screenshot(driver, path_snap, ["navbar", "banner_header", "vw-100"])   
                    else:
                        print("already exists:",  wh.GRAY, path_snap, wh.RESET)
                 
                # visited to file       
                urls_visited.append(url)
                urls_visited = sorted(wh.links_make_unique(urls_visited))
                try:
                    wh.list_to_file(urls_visited, config.path_image_sizes_visited, mode="a")
                except Exception as e:
                    print(wh.RED, e, wh.RESET)     
                       
            else:
                print("already listed:", wh.GRAY, url, wh.RESET)
                
            # # # # # # DEBUG
            # # # # # if count > 12:
            # # # # #     print(wh.YELLOW, "DEBUG break", wh.RESET)
            # # # # #     break         
                
        ### for url />      
            
        driver.close()
        driver.quit()
        
        file_image_sizes_make_unique()
        wh.file_make_unique(config.path_image_sizes_visited, sort=True)
            
        wh.log("b_scan_image_sizes: all done: duration: {:.1f}m".format((time.time() - start_secs)/60.0), filepath=config.path_log_params)
        
    #-----------------------------------------
    # download  
    #-----------------------------------------    
    if b_download_images:
        
        start_secs = time.time()
        
        wh.logo("b_download_images")
        wh.log("b_download_images", b_download_images, filepath=config.path_log_params)
                
        image_paths = file_image_sizes_get_urls()
        print("image_paths", *image_paths, sep="\n\t")
    
        for abs_src in image_paths:
            
            local_path  = config.project_folder + wh.get_path_local_root_subdomains(abs_src, config.base).lstrip('/')
            ret         = wh.download_asset(abs_src, local_path, config.base, max_tries=10) # also same func in 100_selenium TODO
            #assert ret
            assert wh.file_exists_and_valid(local_path)

    
    wh.log("b_download_images: all done: duration: {:.1f}m".format((time.time() - start_secs)/60.0), filepath=config.path_log_params)