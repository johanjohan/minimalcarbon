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
            
def append_to_image_size_tuples(collected, url, bases, e, vt=wh.MAGENTA, pre="\t\t"):
    
    if not url:
        print(pre, "ignore:", "None:", wh.RED, url, wh.RESET)
        return collected
    
    # external? bases: accept 127.0.0.1 or karlsruhe.digital as valid
    bases = list(bases)
    protocol, loc, path = wh.url_split(url)
    if not any([(loc in b) for b in bases]):
        print(pre, "ignore:", "external:", wh.RED, url, wh.RESET)
        return collected
    
    if e and url:
        url = '/' + path # no loc as we already have proven it is internal
        url = wh.get_path_local_root_subdomains(url, base)
        name, ext = os.path.splitext(url)
        tpl  = (
            name, # no ext
            url, 
            e.size['width'],                # size in web doc
            e.size['height'], 
            e.get_attribute("naturalWidth"), # size on disk
            e.get_attribute("naturalHeight")
        )        
        
        list_tpl = list(tpl)
        # # # print(wh.YELLOW, "list_tpl :", list_tpl,  wh.RESET)
        # # # print(wh.YELLOW, "collected:", collected, wh.RESET)
        if not list_tpl in collected:
            line = ','.join([str(value) for value in tpl])
            print(pre, vt, line, wh.RESET)
            collected.append(list_tpl)
    else:
        print(wh.RED, "e  :", e,    wh.RESET)
        print(wh.RED, "url:", url,  wh.RESET)
        
    return collected
            
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
      
def find_all_image_size_tuples(driver, b_scan_srcset=False, pre="\t"):
    
    print(pre, "find_all_image_size_tuples: driver       :", driver)
    print(pre, "find_all_image_size_tuples: b_scan_srcset:", b_scan_srcset)
    pre += "\t"
    
    eu = set()
    
    def add(e, url, eu):
        eu.add(tuple([e, url]))
        print('.', end='', flush=True)
    
    # regular images
    print(pre, "driver.find_elements: By.CSS_SELECTOR", flush=True)
    print(pre, wh.CYAN, end='')
    for e in driver.find_elements(By.CSS_SELECTOR, "img"):
        url = e.get_attribute("src")
        add(e, url, eu)
    print(wh.RESET)
        
    # srcset
    if b_scan_srcset:
        """
        srcset="https://karlsruhe.digital/wp-content/uploads/2022/07/Bunte-Nacht-der-Digitalisierung-2022.jpeg 1500w, https://karlsruhe.digital/wp-content/uploads/2022/07/Bunte-Nacht-der-Digitalisierung-2022-300x200.jpeg 300w, https://karlsruhe.digital/wp-content/uploads/2022/07/Bunte-Nacht-der-Digitalisierung-2022-768x512.jpeg 768w, https://karlsruhe.digital/wp-content/uploads/2022/07/Bunte-Nacht-der-Digitalisierung-2022-1024x683.jpeg 1024w, https://karlsruhe.digital/wp-content/uploads/2022/07/Bunte-Nacht-der-Digitalisierung-2022-75x50.jpeg 75w"
        <source srcset="/images/cereal-box.avif" type="image/avif" />
        """
        print(pre, "driver.find_elements: srcset", flush=True)
        print(pre, wh.CYAN, end='')
        for e in driver.find_elements(By.XPATH, "//*[@srcset]"):
            url     = e.get_attribute("srcset")
            links   = url.split(',')
            for link in links:
                subs = link.split(' ')
                url  = ' '.join(sub for sub in subs[:-1]) # except last
                add(e, url, eu)
        print(wh.RESET)

    # traverse body: all elements for styles attached
    print(pre, "driver.find_elements: By.XPATH body", flush=True)
    print(pre, wh.CYAN, end='')
    for e in driver.find_elements(By.XPATH, "//body//*"):
        imgpath = e.value_of_css_property("background-image")
        if imgpath != "none" and "url" in imgpath:
            url = extract_url(imgpath)
            add(e, url, eu)
    print(wh.RESET)

    # style background: already caught above
    if False:
        print(pre, "driver.find_elements: By.XPATH", flush=True)
        print(pre, wh.CYAN, end='')
        #for e in driver.find_elements(By.XPATH, "//*[contains(@style, 'background-image')]"):
        for e in driver.find_elements(By.XPATH, "//*[contains(@style, 'url')]"):
            print("\t\t", wh.YELLOW, e.get_attribute("style"), wh.RESET)
            url = extract_url(e.get_attribute("style"))
            add(e, url, eu)
        print(wh.RESET)
            
    print(pre, "len(eu):", len(eu))
            
    image_tuples = []
    for e, url in eu:
        #print(wh.GRAY, e, url, image_tuples, wh.RESET)
        image_tuples = append_to_image_size_tuples(
            image_tuples,
            url, 
            [base, config.base],
            e,
            vt=wh.MAGENTA
        )     

    return image_tuples
        

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
    
    # # # # DEBUG!!!
    urls = ["/index.html", "/blog/index.html"] # DEBUG find bgimage in style 
    
    image_size_tuples = []

    for count, url in enumerate(urls):
        
        local   = wh.get_path_local_root_subdomains(url, config.base)
        base    = "http://127.0.0.1/"
        url     = base + local.lstrip('/')

        wh.progress(count / len(urls), verbose_string="TOTAL", VT=wh.CYAN, n=66)
        print()
        print(f"{wh.CYAN}[{(time.time() - start_secs)/60.0:.1f} m] url: {url}{wh.RESET}")
        
        try:
            driver.get(url)
            wh.wait_for_page_has_loaded_hash(driver)
            content = driver.page_source
        except Exception as e:
            print(f"{wh.RED}\t ERROR: GET url: {url} {wh.RESET}")     
            
        image_size_tuples.extend(
            find_all_image_size_tuples(driver, pre="\t")
        )
        print("len(image_size_tuples):", len(image_size_tuples))
        
        if b_take_snapshot:
            path_snap = config.path_snapshots + "snap_full_" + wh.url_to_filename(local) + ".tif" # webp avif png tif
            fullpage_screenshot(driver, path_snap, ["navbar", "banner_header", "vw-100"])            
            
    ### for />      
        
    driver.close()
    driver.quit()
    
    #print("image_size_tuples", *image_size_tuples, sep="\n\t")
    
    wh.string_to_file("\nbasename,name,width,height,naturalWidth,naturalHeight\n", config.path_image_sizes, mode="w")
    wh.list_to_file(image_size_tuples, config.path_image_sizes, mode="a")
    
    wh.log("all done: duration: {:.1f}m".format((time.time() - start_secs)/60.0), filepath=config.path_log_params)