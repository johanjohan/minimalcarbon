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
from PIL import Image
import pillow_avif

import requests

start_secs          = time.time()
image_sizes         = []
b_take_snapshot     = False 
b_scan_image_sizes  = True
b_download_images   = True

#-----------------------------------------
# 
#-----------------------------------------
def download_asset(abs_src, local_path, max_tries=10, sleep_secs_on_failure=2, pre="\t"):
    
    # # # print(pre, "download_asset:", "abs_src   :", wh.GRAY, abs_src,      wh.RESET)
    # # # print(pre, "download_asset:", "local_path:", wh.GRAY, local_path,   wh.RESET)
    
    print(pre, "download_asset:")
    pre += "\t"
    print(pre, wh.CYAN, abs_src,    wh.RESET, "-->")
    print(pre, wh.GRAY, local_path, wh.RESET)
    
    ret = True

    pre += "\t"
    wh.make_dirs(local_path)
    if not wh.file_exists_and_valid(local_path):

        # may_be_a_folder(abs_src):  # folders may get exception below?
        if wh.url_is_assumed_file(abs_src):

            wh.sleep_random(config.wait_secs, verbose_string=local_path, prefix="\t\t ") 

            # GET the file via session requests
            for cnt in range(max_tries):
                try:
                    print(pre, f"{wh.CYAN}\t\t [{cnt}] session.get: {abs_src}{wh.RESET}")
                    session = requests.Session()
                    session.get(base)  # sets cookies
                    res = session.get(abs_src)
                    ret = True
                    break
                except Exception as e:
                    print("\n"*4)
                    print(pre, f"{wh.RED}\t\t ERROR {cnt} session.get: {abs_src}...sleep... {wh.RESET}")
                    time.sleep(sleep_secs_on_failure)
                    ret = False
            ### for />
                    
            # SAVE the file binary to disk local
            try:
                with open(local_path, 'wb') as fp:
                    fp.write(res.content)
                    print(pre, f"{wh.GREEN}wrote OK: {local_path}{wh.RESET}")
                      
                assert wh.file_exists_and_valid(local_path)
                ret = True
            except:
                print(pre, f"{wh.RED}local_path may be a directory?: {local_path}{wh.RESET}")
                ret = False
        else:
            print(pre, f"{wh.RED}abs_src may be a directory?: {abs_src}{wh.RESET}")
            ret = False
    else:
        print(pre, f"{wh.RED}already exists: {os.path.basename(local_path)}{wh.RESET}")  
        ret = True 
        
    return ret        
### def />


#-----------------------------------------
# 
#-----------------------------------------
# https://stackoverflow.com/questions/41721734/take-screenshot-of-full-page-with-selenium-python-with-chromedriver
def fullpage_screenshot(driver, file, classes_to_hide=None, pre="\t"):
    
    classes_to_hide = list(classes_to_hide)

    print(pre + "fullpage_screenshot:", wh.YELLOW + file, wh.RESET) # , wh.RESET)
    print(pre + "fullpage_screenshot:", "classes_to_hide:", classes_to_hide, wh.GRAY) 

    total_width     = driver.execute_script("return document.body.offsetWidth")
    total_height    = driver.execute_script("return document.body.parentNode.scrollHeight")
    viewport_width  = driver.execute_script("return document.body.clientWidth")
    viewport_height = driver.execute_script("return window.innerHeight")
    print(pre + "\t", f"total: ({total_width}, {total_height}), Viewport: ({viewport_width},{viewport_height})")
    rectangles = []

    y = 0
    while y < total_height:
        x = 0
        top_height = y + viewport_height

        if top_height > total_height:
            top_height = total_height

        while x < total_width:
            top_width = x + viewport_width

            if top_width > total_width:
                top_width = total_width

            print(pre + "\t", f"appending rectangle ({x},{y},{top_width},{top_height})")
            rectangles.append((x, y, top_width,top_height))

            x = x + viewport_width

        y = y + viewport_height
    ### while

    stitched_image = Image.new('RGB', (total_width, total_height))
    previous = None
    part = 0
    
    for rectangle in rectangles:
        if not previous is None:
            driver.execute_script(f"window.scrollTo({rectangle[0]}, {rectangle[1]})")
            time.sleep(0.2)
            
            # driver.execute_script("document.getElementById('topnav').setAttribute('style', 'position: absolute; top: 0px;');")
            # time.sleep(0.2)
            
            if classes_to_hide:
                for hide_class in classes_to_hide:
                    
                    # check whether CLASS_NAME is available
                    if driver.find_elements(By.CLASS_NAME, hide_class):
                        driver.execute_script(f"document.getElementsByClassName('{hide_class}')[0].setAttribute('style', 'position: absolute; top: 0px;');")
                        
                        if rectangle[1] > 0:
                            driver.execute_script(f"document.getElementsByClassName('{hide_class}')[0].setAttribute('style', 'display: none;');")
                            
                    time.sleep(0.2)
                ### for
            ### if
            
            print(pre + "\t\t", f"scrolled To ({rectangle[0]},{rectangle[1]})")
            time.sleep(0.2)
        ### if not previous is None

        file_name = f"__tmp_ssnap_part_{part}.png"
        print(pre + "\t\t", f"capturing {file_name} ...")
        driver.get_screenshot_as_file(file_name)
        screenshot = Image.open(file_name)

        if rectangle[1] + viewport_height > total_height:
            offset = (rectangle[0], total_height - viewport_height)
        else:
            offset = (rectangle[0], rectangle[1])

        print(pre + "\t\t", f"adding to stitched image with offset ({offset[0]}, {offset[1]})")
        stitched_image.paste(screenshot, offset)

        del screenshot
        os.remove(file_name)
        part = part + 1
        previous = rectangle
        
    ### for rectangles

    wh.make_dirs(path_snap)
    stitched_image.save(file, optimize=True, lossless=True) # , quality=100
    #stitched_image.save(file, optimize=True, quality=50) # , quality=100
    
    # # # cmd = f"""
    
    # # #     {os.path.abspath("avif/avifenc.exe")} 
    # # #     --speed {0} 
    # # #     --jobs  {8} 
        
    # # #     --lossless
        
    # # #     {os.path.abspath(__image_smaller_png_path)} 
    # # #     {os.path.abspath(path_snap)} 
        
    # # # """
    # # # ##md = f""" {os.path.abspath("avif/avifenc.exe")} --help """
    # # # cmd = wh.string_remove_whitespace(cmd)
    # # # print(wh.CYAN, end='')
    # # # print(cmd)
    # # # ret = os.system(wh.dq(cmd))    
    
    
    
    print(pre + "\t", "finishing chrome full page screenshot workaround...", wh.RESET)
    return True

#-----------------------------------------
# 
#-----------------------------------------            
def __append_to_image_size_tuples(collected, url_parent, url, bases, e, vt=wh.MAGENTA, pre="\t\t"):
    
    if not url:
        print(pre, "ignore:", "None:", wh.RED, url, wh.RESET)
        return
    
    # external? bases: accept 127.0.0.1 or karlsruhe.digital as valid
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
            url_parent
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
        
            
def extract_url(style_string):
    
    if not style_string:
        return None
    
    if "url" in style_string:
        url = style_string
        url = url.split('url')[-1]
        url = url.split(')')[0]
        url = url.strip().lstrip('(')
        for q in ["\"", "\'"]:
            url = url.strip().lstrip(q).rstrip(q)
        #print(style_string, YELLOW, url, RESET)
        return url
    else:
        print(wh.RED, "url NOT found in ", style_string, wh.RESET)
        return style_string

"""
srcset="https://karlsruhe.digital/wp-content/uploads/2022/07/Bunte-Nacht-der-Digitalisierung-2022.jpeg 1500w, 
        https://karlsruhe.digital/wp-content/uploads/2022/07/Bunte-Nacht-der-Digitalisierung-2022-300x200.jpeg 300w, 
        https://karlsruhe.digital/wp-content/uploads/2022/07/Bunte-Nacht-der-Digitalisierung-2022-768x512.jpeg 768w, 
        https://karlsruhe.digital/wp-content/uploads/2022/07/Bunte-Nacht-der-Digitalisierung-2022-1024x683.jpeg 1024w, 
        https://karlsruhe.digital/wp-content/uploads/2022/07/Bunte-Nacht-der-Digitalisierung-2022-75x50.jpeg 75w"
<source srcset="/images/cereal-box.avif" type="image/avif" />
"""   
def find_all_image_size_tuples(collected, driver, url_parent, bases, b_scan_srcset, pre="\t"):
        
    print(pre, "find_all_image_size_tuples: b_scan_srcset:", wh.CYAN, str(b_scan_srcset), wh.RESET)
    print(pre, "find_all_image_size_tuples: driver       :", wh.GRAY, str(driver), wh.RESET)
    print(pre, "find_all_image_size_tuples: bases        :", wh.GRAY, bases, wh.RESET)
    print(pre, "find_all_image_size_tuples: url_parent   :", wh.GRAY, url_parent, wh.RESET)
    
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

        # traverse body: all elements for styles attached
        xpath_css = "//body//*"
        print(pre, f"driver.find_elements: By.XPATH {xpath_css}", flush=True)
        print(pre, wh.CYAN, end='')
        for e in driver.find_elements(By.XPATH, xpath_css):
            imgpath = e.value_of_css_property("background-image")
            if imgpath != "none" and "url" in imgpath:
                url = extract_url(imgpath)
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
            url_parent,
            url, 
            bases,
            e,
            vt=wh.GREEN
        )     
        
#-----------------------------------------
# 
#-----------------------------------------
def file_image_sizes_get_index(index):
    res = []
    with open(config.path_image_sizes, mode="r", encoding="utf-8") as fp:
        for line in fp:
            if line.startswith('/'):
                #c_base, c_path, wdom, hdom, nw, nh, c_url, c_url_parent = line.rstrip('\n').split(',')
                subs = line.rstrip('\n').split(',')
                assert index < len(subs), f"{index} < {len(subs)}"
                res.append(subs[index])
             
    res = wh.links_make_unique(res) 
    res = sorted(res)          
    #print("res", *res, sep="\n\t")    
    return res

def file_image_sizes_get_url_parents():
    return file_image_sizes_get_index(7)

def file_image_sizes_get_urls():
    return file_image_sizes_get_index(6)

#-----------------------------------------
# 
#-----------------------------------------

if __name__ == "__main__":
    
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
        urls = config.path_sitemap_links_internal         
        urls = wh.list_from_file(urls)
        urls = wh.links_remove_comments(urls, '#')
        urls = wh.links_replace(urls, config.replacements_pre)
        urls = wh.links_remove_externals(urls, config.base)
        urls = wh.links_strip_query_and_fragment(urls)
        urls = wh.links_make_absolute(urls, config.base)
        urls = wh.links_sanitize(urls)
        
        # # DEBUG!!!
        # urls = [
        #     "https://karlsruhe.digital/", 
        #     "https://karlsruhe.digital/", 
        #     "https://karlsruhe.digital/blog/", 
        #     "https://karlsruhe.digital/blog/", 
        #     "https://media.karlsruhe.digital/"
        # ] 
    
        image_size_tuples = []
        url_parents = file_image_sizes_get_url_parents()
        print("url_parents", *url_parents, sep="\n\t")

        for count, url in enumerate(urls):
            
            url_parent  = url
            
            base        = config.base
            bases       = [config.base, "https://kadigital.s3-cdn.welocal.cloud/", "https://media.karlsruhe.digital/"]
            local_url   = wh.get_path_local_root_subdomains(url, config.base)
            abs_url     = wh.link_make_absolute(url, base)

            wh.progress(count / len(urls), verbose_string="TOTAL", VT=wh.CYAN, n=66)
            print()
            print(f"{wh.CYAN}[{(time.time() - start_secs)/60.0:.1f} m] abs_url: {abs_url} {wh.RESET}")
            
            if not (url_parent in url_parents):
                
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
                        url_parent,    # for the record
                        bases, 
                        b_scan_srcset=False, 
                        pre="\t"
                    )
                    print("len(image_size_tuples):", len(image_size_tuples))
                    
                    # to file
                    try:
                        # TODO at the very end create header nd make unique
                        ###wh.string_to_file("\nlocalbasename,localname,width,height,naturalWidth,naturalHeight,url,url_parent\n", config.path_image_sizes, mode="w")
                        wh.list_to_file(image_size_tuples, config.path_image_sizes, mode="a")
                    except Exception as e:
                        print(wh.RED, e, wh.RESET)

                            
                if b_take_snapshot:
                    path_snap = config.path_snapshots + "snap_full_" + wh.url_to_filename(local_url) + ".webp" # webp avif png tif
                    if not wh.file_exists_and_valid(path_snap):
                        fullpage_screenshot(driver, path_snap, ["navbar", "banner_header", "vw-100"])   
                    else:
                        print("already exists:",  wh.GRAY, path_snap, wh.RESET)
                
            else:
                print("already listed:", wh.GRAY, url_parent, wh.RESET)
                
                
            # DEBUG
            if count > 12:
                print(wh.YELLOW, "DEBUG break", wh.RESET)
                break         
                
        ### for url />      
            
        driver.close()
        driver.quit()
        
        #print("image_size_tuples", *image_size_tuples, sep="\n\t")
        
        # if b_scan_image_sizes:
        #     wh.string_to_file("\nlocalbasename,localname,width,height,naturalWidth,naturalHeight,url\n", config.path_image_sizes, mode="w")
        #     wh.list_to_file(image_size_tuples, config.path_image_sizes, mode="a")
            
        wh.log("all done: duration: {:.1f}m".format((time.time() - start_secs)/60.0), filepath=config.path_log_params)
        
    #-----------------------------------------
    # download  
    #-----------------------------------------    
   
    if b_download_images:
        
        start_secs = time.time()
        
        wh.logo("b_download_images")
        wh.log("b_download_images", b_download_images, filepath=config.path_log_params)
                
        image_paths = file_image_sizes_get_urls()
        # # # # # # with open(config.path_image_sizes, mode="r", encoding="utf-8") as fp:
        # # # # # #     for line in fp:
        # # # # # #         if line.startswith('/'):
        # # # # # #             c_base, c_path, wdom, hdom, nw, nh, c_url, c_url_parent = line.rstrip('\n').split(',')
        # # # # # #             image_paths.append(c_url)
                    
        print("image_paths", *image_paths, sep="\n\t")
    
        for abs_src in image_paths:
            
            local_path = config.project_folder + wh.get_path_local_root_subdomains(abs_src, config.base).lstrip('/')
            
            ret = download_asset(abs_src, local_path, max_tries=10) # also same func in 100_selenium TODO
            assert ret

    
    wh.log("all done: duration: {:.1f}m".format((time.time() - start_secs)/60.0), filepath=config.path_log_params)