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

start_secs          = time.time()
image_sizes         = []
b_take_snapshot     = False 
b_scan_image_sizes  = True

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
            

if __name__ == "__main__":
    
    wh.logo_filename(__file__)
    wh.log("__file__", __file__, filepath=config.path_log_params)
    
    # -----------------------------------------
    # index.html
    # -----------------------------------------   
    image_paths = []
    with open(config.path_image_sizes, mode="r", encoding="utf-8") as fp:
        for line in fp:
            if line.startswith('/'):
                c_base, c_path, wdom, hdom, nw, nh, c_url = line.split(',')
                image_paths.append(list(line.rstrip('\n').split(',')))
                
    print("image_paths", *image_paths, sep="\n\t")
    assert image_paths
    
    # # # # DEBUG!!!
    ####urls = ["/index.html", "/index.html", "/blog/index.html", "/blog/index.html", "/blog/index.html"] # DEBUG find bgimage in style 
    

    for count, item in enumerate(image_paths):
        
        c_base, c_path, wdom, hdom, nw, nh, c_url = item
        print(c_base, c_path, wdom, hdom, nw, nh, c_url)
        
        local   = wh.get_path_local_root_subdomains(c_path, config.base)
        base    = config.base
        url     = base + local.lstrip('/')
        
        print(url)

        wh.progress(count / len(image_paths), verbose_string="TOTAL", VT=wh.CYAN, n=66)
        print()
        print(f"{wh.CYAN}[{(time.time() - start_secs)/60.0:.1f} m] url: {url}{wh.RESET}")
        
       
            
    ### for />      
        

    
    wh.log("all done: duration: {:.1f}m".format((time.time() - start_secs)/60.0), filepath=config.path_log_params)