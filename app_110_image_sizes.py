"""
TODO
may better split image sizes files for keeping track of parent_urls
the list is getting very large right now


#-----------
    # images
    #-----------
    # driver.find_element_by_xpath('//a[@href="'+url+'"]')
    links_img  = h.xpath('//img/@src')
    links_img += h.xpath('//link[contains(@rel, "icon")]/@href')  # favicon
    links_img += wh.get_background_images_from_style_attribute(driver)
    # TODO need to replace these in css as well
    links_img += wh.get_background_images_from_stylesheet_file(style_path)
    
    for text in h.xpath("//style/text()"):
        links_img += wh.get_background_images_from_stylesheet_string(text)
    
    for text in  h.xpath("//div/@style"):
        links_img += wh.get_background_images_from_inline_style_tag(text)
    for text in  h.xpath("//video/@style"):
        links_img += wh.get_background_images_from_inline_style_tag(text)        
    # a lot of images in media.
    for text in  h.xpath("//*/@style"):
        links_img += wh.get_background_images_from_inline_style_tag(text)
    
    # media.ka    
    import json
    for jstring in  h.xpath("//*/@data-vjs_setup"):
        j = json.loads(jstring)
        #print(json.dumps(j, indent=4), sep="\n\t\t")
        print("\t\t\t", j.get("poster", None))
        links_img.append(j.get("poster", None))
        
    #### NEW!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if True:
        # traverse body: all elements for style NEW TODO SLOW!
        print("\t", "driver.find_elements: By.XPATH body", flush=True)
        for e in driver.find_elements(By.XPATH, "//body//*"):
            imgpath = e.value_of_css_property("background-image")
            if imgpath != "none" and "url" in imgpath:
                print("\t\t", wh.YELLOW, wh.dq(imgpath), wh.RESET)
                url = wh.extract_url(imgpath)
                links_img.append( url )
 
     


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


#-----------------------------------------
# 
#-----------------------------------------            
def __append_to_image_size_tuples(collected, url, bases, e, vt=wh.MAGENTA, pre="\t\t"):
    
    if not url:
        print(pre, "ignore:", "None:", wh.RED, url, wh.RESET)
        return
    
    # ignore external? bases: accept 127.0.0.1 or karlsruhe.digital as valid
    protocol, loc, path = wh.url_split(url)
    bases = list(bases)
    if not any([(loc in b) for b in bases]):
        print(pre, "ignore:", "external:", wh.RED, url, wh.RESET)
        return 
    
    if e and url:
        
        local = '/' + path # no loc as we already have proven it is internal
        local = wh.get_path_local_root_subdomains(local, base)
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
        
        if not tpl in collected: 
            #print(pre, vt, ','.join([str(value) for value in tpl]), wh.RESET)
            #print(pre, vt, url, e.size['width'], e.size['height'], wh.RESET)
            #print(pre, vt, ', '.join([str(tpl[i]) for i in range(1,6)]), wh.RESET)
            print(pre, vt + str(url), e.size['width'], e.size['height'], wh.RESET)
            collected.append(tpl)
        
    else:
        print(wh.RED, "e  :", e,    wh.RESET)
        print(wh.RED, "url:", url,  wh.RESET)
        


"""
srcset="https://karlsruhe.digital/wp-content/uploads/2022/07/Bunte-Nacht-der-Digitalisierung-2022.jpeg 1500w, 
        https://karlsruhe.digital/wp-content/uploads/2022/07/Bunte-Nacht-der-Digitalisierung-2022-300x200.jpeg 300w, 
        https://karlsruhe.digital/wp-content/uploads/2022/07/Bunte-Nacht-der-Digitalisierung-2022-768x512.jpeg 768w, 
        https://karlsruhe.digital/wp-content/uploads/2022/07/Bunte-Nacht-der-Digitalisierung-2022-1024x683.jpeg 1024w, 
        https://karlsruhe.digital/wp-content/uploads/2022/07/Bunte-Nacht-der-Digitalisierung-2022-75x50.jpeg 75w"
<source srcset="/images/cereal-box.avif" type="image/avif" />
"""   
def find_all_image_size_tuples(collected, driver, bases, b_scan_srcset, pre="\t"):
        
    print(pre, "find_all_image_size_tuples: b_scan_srcset:", wh.CYAN, str(b_scan_srcset), wh.RESET)
    print(pre, "find_all_image_size_tuples: driver       :", wh.GRAY, str(driver), wh.RESET)
    print(pre, "find_all_image_size_tuples: bases        :", wh.GRAY, bases, wh.RESET)
    
    pre += "\t"
    
    eu      = set()   
    bases   = list(bases)
    
    def __add(e, url, eu):
        eu.add(tuple([e, url]))
        print(wh.CYAN + '.', end='', flush=True)
        
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

        # traverse body: all elements for styles attached, a bit slow but effective
        xpath_css = "//body//*"
        print(pre, f"driver.find_elements: By.XPATH {xpath_css}", flush=True)
        print(pre, wh.CYAN, end='')
        for e in driver.find_elements(By.XPATH, xpath_css):
            
            imgpath = e.value_of_css_property("background-image") # may as well look for content:
            if imgpath != "none" and "url" in imgpath:
                url = wh.extract_url(imgpath)
                __add(e, url, eu)
                
            imgpath = e.value_of_css_property("content") # may as well look for content:
            if imgpath != "none" and "url" in imgpath:
                print(wh.YELLOW, "content", imgpath, wh.RESET) # <<<<<<<<<<<<< TRAY
                time.sleep(3)
                url = wh.extract_url(imgpath)
                __add(e, url, eu)

        print(wh.RESET)
        
        # favicon
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
        #print(wh.GRAY, e, url, image_tuples, wh.RESET)
        __append_to_image_size_tuples(
            collected,
            url, 
            bases,
            e,
            vt=wh.GREEN
        )     
        
#-----------------------------------------
# 
#-----------------------------------------


def file_image_sizes_make_unique():
    
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
    unique_data = [list(x) for x in set(tuple(x) for x in res)] # https://stackoverflow.com/questions/3724551/python-uniqueness-for-list-of-lists
    res = sorted(unique_data)
    print("file_image_sizes_make_unique: removed:", len(res) - len_orig, "items") 
    
    #print("res", *res, sep="\n\t")   
    
    wh.string_to_file("localbasename,localname,width,height,naturalWidth,naturalHeight,url,url_parent\n", config.path_image_sizes, mode="w")
    wh.list_to_file(res, config.path_image_sizes, mode="a")            
    
def file_image_sizes_get_index(index):
    res = []
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

# def file_image_sizes_get_url_parents():
#     return file_image_sizes_get_index(7)

def file_image_sizes_get_urls():
    return file_image_sizes_get_index(6)

#-----------------------------------------
# 
#-----------------------------------------

if __name__ == "__main__":
    
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
                driver.implicitly_wait(0) # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< An implicit wait tells WebDriver to poll the DOM for a certain amount of time when trying to find any element (or elements) not immediately available. The default setting is 0 (zero). Once set, the implicit wait is set for the life of the WebDriver object.
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