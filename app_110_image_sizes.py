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

start_secs      = time.time()
image_sizes     = []
b_take_snapshot = False

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
    
# # https://stackoverflow.com/questions/41721734/take-screenshot-of-full-page-with-selenium-python-with-chromedriver
# def save_screenshot(driver, path) -> None:
#     # Ref: https://stackoverflow.com/a/52572919/
#     original_size   = driver.get_window_size()
#     required_width  = driver.execute_script('return document.body.parentNode.scrollWidth')
#     required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
#     driver.set_window_size(required_width, required_height)

#     scheight = .1
#     while scheight < 9.9:
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
#         scheight += .01    
    
#     # driver.save_screenshot(path)  # has scrollbar
#     driver.find_element(By.TAG_NAME, 'body').screenshot(path)  # avoids scrollbar
#     driver.set_window_size(original_size['width'], original_size['height'])
 

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
                    driver.execute_script(f"document.getElementsByClassName('{hide_class}')[0].setAttribute('style', 'position: absolute; top: 0px;');")
                    
                    if rectangle[1] > 0:
                        driver.execute_script(f"document.getElementsByClassName('{hide_class}')[0].setAttribute('style', 'display: none;');")
                time.sleep(0.2)
            
            print(pre + "\t\t", f"scrolled To ({rectangle[0]},{rectangle[1]})")
            time.sleep(0.2)

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
            #driver.implicitly_wait(1) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
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
        
        local = url
        
        # replace for localhost
        url = "http://127.0.0.1/" + local.lstrip('/')
        url = "http://127.0.0.1/" + local.lstrip('/')

        wh.progress(count / len(urls), verbose_string="TOTAL", VT=wh.CYAN, n=66)
        print()
        print(f"{wh.CYAN}[{(time.time() - start_secs)/60.0:.1f} m] url: {url}{wh.RESET}")
        ###continue
        
        try:
            driver.get(url)
            wh.wait_for_page_has_loaded_hash(driver)
            content = driver.page_source
        except Exception as e:
            print(f"{wh.RED}\t ERROR: GET url: {url} {wh.RESET}")     
        #print(driver.page_source)   
        
        
        if b_take_snapshot:

            path_snap = config.path_snapshots + "snap_full_" + wh.url_to_filename(local) + ".tif" # webp avif png tif
            fullpage_screenshot(driver, path_snap, ["navbar", "banner_header", "vw-100"])
        
                        
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