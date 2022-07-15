""" 
# https://stackoverflow.com/questions/3964681/find-all-files-in-a-directory-with-extension-txt-in-python


"""
import glob, os
from posixpath import splitext
from re import X
from urllib.parse import urljoin
import PIL
from PIL import Image, ImageOps
import halftone as ht # https://pypi.org/project/halftone/

import config
import helpers_web as wh
import helpers_web as hw
import time
import pathlib
import pyautogui as pag


from bs4 import BeautifulSoup as bs

import lxml.html
import helpers_lxml as hx
import conversions as conv


import chromedriver_binary  # pip install chromedriver-binary-auto
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver  # pip install selenium
from selenium.webdriver.chrome.options import Options

import shutil

# https://github.com/homm/pillow-lut-tools
# https://pillow-lut-tools.readthedocs.io/en/latest/
# pip install pillow_lut
# pillow_lut.load_cube_file(lines, target_mode=None, cls=<class 'PIL.ImageFilter.Color3DLUT'>)
import pillow_lut 
import pillow_avif

#-----------------------------------------
# 
#-----------------------------------------
if __name__ == "__main__":
    
    #-----------------------------------------
    # alert
    #-----------------------------------------    
    pag.alert("make sure to also change backgrond image extensions in style.css...", timeout=10000)
    pag.alert("also change navText hardcoded in scripts...", timeout=10000)
        
    #-----------------------------------------
    # logo
    #-----------------------------------------               
    wh.logo_filename(__file__)
    wh.log("__file__:", __file__, filepath=config.path_log_params)
    
    #-----------------------------------------
    # dir_size_orig
    #-----------------------------------------
    dir_size_orig = wh.get_directory_total_size(config.project_folder)

    #pag.alert(text=f"good time to backup htdocs!", timeout=2000)
    #-----------------------------------------
    # get sizes
    #-----------------------------------------    
    b_get_project_total_size_use_pdf = False
    perc100_saved, total_size_originals, total_size_unpowered = wh.get_project_total_size(
        config.project_folder, 
        prefix=config.base_netloc,
        use_pdf=b_get_project_total_size_use_pdf
    )
    #exit(0)            
    #-----------------------------------------
    # 
    #-----------------------------------------
    params = {
        "project_folder":                       wh.to_posix(os.path.abspath(config.project_folder)),
        "path_conversions":                     config.path_conversions,

        "b_append_custom_css":                  True,
        "b_copy_custom_script":                 True,
        "b_remove_fonts_css":                   True,
        
        "b_perform_pdf_compression":            True ,
        "b_perform_pdf_compression_force":            False, # <<<<<<<<<<<<<<<<<<<<      
        
        "b_perform_image_conversion":           True,
        "images": {
            "b_force_write":        True,   # <<<<<<<<<<<<<<<<<<<<        
            "show_nth_image":       37, # 0 is off, 1 all
            
            "quality":              60, # 66 55
            
            ##"max_dim":            (500, 500), # could make smaller with avif --> func_size
            "size_thresh":          1000, 
            "size_large":           (1400, 1400), 
            "size_small":           (553, 553),
            
            "resample":             Image.Resampling.LANCZOS, 
            "resample_comment":     "Image.Resampling.LANCZOS", # verbose only
            
            "halftone":             None, # (4, 30) or None # ht.euclid_dot(spacing=halftone[0], angle=halftone[1])

            #"cube_lut_path":        "D:/__BUP_V_KOMPLETT/X/111_BUP/22luts/LUT cube/LUTs Cinematic Color Grading Pack by IWLTBAP/__xIWL_zM_Creative/Creative/xIWL_C-6730-STD.cube", # may be empty string
            #"cube_lut_path":        "D:/__BUP_V_KOMPLETT/X/111_BUP/22luts/LUT cube/LUTs Cinematic Color Grading Pack by IWLTBAP/__xIWL_zM_Creative/Creative/xIWL_B-7040-STD.cube", # may be empty string
            #"cube_lut_path":        "D:/__BUP_V_KOMPLETT/X/111_BUP/22luts/LUT cube/LUTs Cinematic Color Grading Pack by IWLTBAP/__xIWL_zM_Creative/Creative/xIWL_C-9730-STD.cube", # may be empty string
            "cube_lut_path":        None, # may be empty string or None
            
            "b_colorize":           True,
            "blend_alpha":          0.6, # 0.666 0.8 0.75  
            "b_enhance_transp":     True,         
            
            ###"b_1bit":               False,  # very bad
            "b_greyscale":          False,
            "b_use_palette":        False,
        },        
        
        "b_replace_conversions":                True, # <<<<<<<<<<<<<<<<<<<<      
        
        "b_minify1":                            True,
        "b_fix_xml_elements":                   True,
        "b_hide_media_subdomain":                   True,
        "b_minify2":                            True,
        "b_export_site":                        True, 
        "b_export_site_force":                      True,    
    }
    
    import json
    wh.log(json.dumps(params, indent=4), filepath=config.path_log_params, echo=False)
    wh.log(wh.format_dict(params), filepath=config.path_log_params)
        
    # del with warning
    conversions = []
    b_delete_conversion_originals   = False
    if b_delete_conversion_originals:
        if "Cancel" == pag.confirm(text=f"b_delete_conversion_originals: {b_delete_conversion_originals}"):
            exit(0)
            
    #-----------------------------------------
    # remove path_conversions
    #-----------------------------------------
    wh.logo("remove path_conversions")        
    if os.path.isfile(params.get("path_conversions")):
        os.remove(params.get("path_conversions"))

    #-----------------------------------------
    # copy icons
    #-----------------------------------------
    wh.logo("copy icons")
    hw.make_dirs(config.path_dst_icons)
    shutil.copytree(config.path_src_icons, config.path_dst_icons, dirs_exist_ok=True)

    #-----------------------------------------
    # b_append_custom_css
    #-----------------------------------------
    # append css before fonts will be replaced after
    if params.get("b_append_custom_css"):
        wh.logo("b_append_custom_css")
        data_stylesheet = wh.string_from_file(config.path_stylesheet)
        print("count:", data_stylesheet.count(config.custom_css_marker))
        data_stylesheet = data_stylesheet.split(config.custom_css_marker)[0]
        data_stylesheet += wh.string_from_file(config.path_custom_css)
        wh.string_to_file(data_stylesheet, config.path_stylesheet)
        print("appended custom css to", config.path_stylesheet)
        print("count:", data_stylesheet.count(config.custom_css_marker))
        
    #-----------------------------------------
    # b_copy_custom_script
    #-----------------------------------------
    if params.get("b_copy_custom_script"):
        wh.logo("b_copy_custom_script")
        if config.path_new_script:
            shutil.copy(config.path_new_script, config.path_script)
            print("copied", config.path_new_script, "to", config.path_script)
    
    #-----------------------------------------
    # fonts
    #-----------------------------------------
    if params.get("b_remove_fonts_css"):
        wh.logo("b_remove_fonts_css")
        # https://pythonhosted.org/cssutils/
        # https://pythonhosted.org/cssutils/
        # https://github.com/jaraco/cssutils
        # https://cthedot.de/cssutils/
        # https://stackoverflow.com/questions/59648732/replace-uri-value-in-a-font-face-css-rule-with-cssutils
        # https://groups.google.com/g/cssutils?pli=1
        # https://www.fullstackpython.com/cascading-style-sheets.html
        import cssutils
        import logging
        import cssbeautifier
        from lxml import etree

        def save_css_changed(orig_path, text, conversions):
            name, ext = os.path.splitext(orig_path)
            new_path  = name + config.suffix_compressed + ext
            wh.string_to_file(
                text,
                new_path
            )
            conversions.append((orig_path, new_path))     
            print("\t\t", "added to conversions:", wh.CYAN, os.path.basename(new_path), wh.RESET)  
                    
        cssutils.log.setLevel(logging.CRITICAL)
            
        #-----------------------------------------
        # download fonts from stylesheets
        #-----------------------------------------
        # TODO save fonts locally
        print("downloading fonts...")
        files = wh.collect_files_endswith(params.get("project_folder"), [".css"])
        files = wh.links_remove_excludes(files, [config.suffix_compressed])
        #print(wh.CYAN, *files, wh.RESET, sep="\n\t")
        
        font_urls = []
        for file in files:
            print("", wh.CYAN, file, wh.RESET)
            try:
                sheet = cssutils.parseFile(file)
                for rule in sheet:                    
                    if rule.type in [cssutils.css.CSSFontFaceRule.FONT_FACE_RULE]:
                        print("\t", rule)  
                        for property in rule.style:
                            if property.name == 'src': # 'font-family':
                                print("\t\t", hw.CYAN, property.name, property.value, hw.RESET)  
                                if "url" in property.value:
                                    url = property.value.replace("(", "").replace(")", "")
                                    url = url.strip().lstrip("url")
                                    print("\t\t\t", hw.CYAN, url, hw.RESET)
                                    subs = url.split(',')
                                    for sub in subs:
                                        font_url = sub.strip().lstrip("url")
                                        font_url = font_url.split(" ")[0]
                                        font_url = hw.strip_query_and_fragment(font_url)
                                        font_url = font_url.replace("../", "/wp-content/themes/karlsruhe-digital/")
                                        font_url = urljoin(config.base, font_url)
                                        print("\t\t\t\t", hw.MAGENTA, font_url, hw.RESET)
                                        
                                        local_path = config.project_folder + wh.get_path_local_root_subdomains(font_url, config.base).lstrip('/')
                                        
                                        if not os.path.isfile(local_path):
                                            wh.make_dirs(local_path)
                                            response = hw.get_response(font_url)
                                            with open(local_path, "wb") as fp:
                                                fp.write(response.read())
                                        
                                        font_urls.append((font_url, local_path))
                                                              
            except Exception as e:
                print(f"{wh.RED} css: {e} {wh.RESET}")
                time.sleep(2)
                
        ### for file   
        #print(*font_urls, sep="\n\t")

        #-----------------------------------------
        # remove fonts from stylesheets
        #-----------------------------------------
        for file in files:
            b_file_has_changed = False
            print("", wh.CYAN, file, wh.RESET)
            try:
                sheet = cssutils.parseFile(file)
                #print("before", wh.GRAY, cssbeautifier.beautify(sheet.cssText.decode("utf-8")), wh.RESET)       
                sheet = wh.css_sheet_delete_rules(
                    sheet, 
                    [
                        cssutils.css.CSSFontFaceRule.FONT_FACE_RULE, 
                        ###cssutils.css.CSSFontFaceRule.COMMENT
                    ])

                # reset fonts
                for rule in sheet:
                    
                    assert rule.type != cssutils.css.CSSFontFaceRule.FONT_FACE_RULE # removed above
                    
                    if rule.type in [cssutils.css.CSSFontFaceRule.STYLE_RULE]:
                        for property in rule.style:
                            #print("\t\t\t", property.name)
                            if property.name == 'font-family':
                                property.value = config.font_sans
                                b_file_has_changed = True
                                
                            # # https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/src
                            # assert property.name != 'src'
                            # if property.name == 'src':
                            #     property.value = "XXX"
                            #     b_file_has_changed = True
                                
                #print("after", wh.GREEN, cssbeautifier.beautify(sheet.cssText.decode("utf-8")), wh.RESET)
                ###save_css_changed(file, cssbeautifier.beautify(sheet.cssText.decode("utf-8")), conversions)
                if b_file_has_changed:
                    wh.string_to_file(
                        cssbeautifier.beautify(sheet.cssText.decode("utf-8")), 
                        file
                    )
                   
            except Exception as e:
                print(f"{wh.RED} css: {e} {wh.RESET}")
                time.sleep(2)
        ### for file
        conv.save(params.get("path_conversions"), conversions)  
            
        #-----------------------------------------
        # replace fonts in tag styles   
        #-----------------------------------------  
        files = wh.collect_files_endswith(params.get("project_folder"), ["index.htm","index.html"])
        files = wh.links_remove_excludes(files, [config.suffix_compressed])
        #print(wh.MAGENTA, *files, wh.RESET, sep="\n\t")
        
        for file in files:
            b_file_has_changed = False
            #print(file)
            content = wh.string_from_file(file)
            tree = lxml.html.fromstring(content)
            for node in  tree.xpath("//*[@style]"):
                #print("\t", node)
                style_text = node.attrib['style']
                #print("\t\t", style_text)
                style = cssutils.parseStyle(style_text) # <<<
                #print ("\t\t", "style.cssText:", wh.MAGENTA, style.cssText, wh.RESET)
                for property in style:
                    if property.name == 'font-family':
                        print(file)
                        property.value = config.font_sans 
                        b_file_has_changed = True
                        print ("\t\t", wh.YELLOW, style.cssText, wh.RESET)   
                                                  
                    # # # if property.name == 'background-image':
                    # # #     print ("\t\t", wh.MAGENTA, style.cssText, wh.RESET) 
                    # # #     pass
                        
                # assign style back to lxml
                node.attrib['style'] =  property.cssText 
                #print("\t\t", wh.GREEN, node.attrib['style'], wh.RESET)
                
            ### for node
            
            content = etree.tostring(tree, pretty_print=True).decode("utf-8")
            #print(wh.GREEN, content, wh.RESET)
            ###save_css_changed(file, content, conversions)
            if b_file_has_changed:
                wh.string_to_file(
                    content, 
                    file
                )    
        ### for file
        conv.save(params.get("path_conversions"), conversions)  
         
    #-----------------------------------------
    # 
    #-----------------------------------------
    if params.get("b_perform_pdf_compression"):
        
        b_force_write = params.get("b_perform_pdf_compression_force")
        
        if b_force_write and "Cancel" == pag.confirm(text=f"PDF: b_force_write: {b_force_write}", timeout=2000):
            exit(0)        
        
        wh.logo("b_perform_pdf_compression")
        import ghostscript as gs
        
        pdfs = wh.collect_files_endswith(params.get("project_folder"), [".pdf"])
        pdfs = [pdf for pdf in pdfs if not config.pdf_compression_suffix in pdf] # remove already compressed
        print("pdfs", *pdfs, sep="\n\t")
        for i, pdf in enumerate(pdfs):
            
            print("-"*88)
            
            orig_path = pdf
            name, ext = os.path.splitext(orig_path)
            new_path  = name + config.pdf_compression_suffix + ext
            
            conversions.append((orig_path, new_path))     
            print("\t\t", "added to conversions:", os.path.basename(new_path)) 
                                
            if not wh.file_exists_and_valid(new_path) or b_force_write:
                gs.compress_pdf(orig_path, new_path, compression=config.pdf_compression, res=config.pdf_res)
                
                if wh.file_exists_and_valid(new_path):
                    size_orig = os.path.getsize(orig_path)
                    size_new  = os.path.getsize(new_path)
                    wh.log("\t", "saved:", 
                           wh.vt_saved_percent_string(size_orig, size_new), 
                           os.path.basename(new_path), 
                           filepath=config.path_log_params
                    )
                    
                    if size_new >= size_orig:
                        shutil.copyfile(orig_path, new_path) # restore original
                        print("\t\t", "copying original:", os.path.basename(orig_path))
                    
 
                    
                    # delete conv later
                    # if b_delete_conversion_originals:
                    #     print("\t\t", "removing orig_path:", wh.RED + orig_path, wh.RESET) 
                    #     os.remove(orig_path) 
            else:
                print("already exists:", os.path.basename(new_path))
                            
        ### for />
                 
        conv.save(params.get("path_conversions"), conversions)  
    ### b_perform_pdf_compression />   

    #-----------------------------------------
    # 
    #-----------------------------------------
    if params.get("b_perform_image_conversion"):   
        
        wh.logo("b_perform_image_conversion")
        
        # # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#webp
        # quality         = 66 # 66 55
        # max_dim         = (1000, 1000) # (1280, 720) # (1200, 600)
        # show_nth_image  = 30 # 0 is off, 1 all
        # resample        = Image.Resampling.LANCZOS
        # halftone        = None # (4, 30) # or None
        # b_colorize      = True
        # b_force_write   = params.get("b_perform_image_conversion_force")
        # b_greyscale    = False
        # b_use_palette   = False
        # blend_alpha     = 0.8 # 0.666 0.8
        
        pimages         = params.get("images")
        
        quality         = pimages.get("quality")  # 66 # 66 55
        ##max_dim         = pimages.get("max_dim")  # (1000, 1000) # (1280, 720) # (1200, 600)
        show_nth_image  = pimages.get("show_nth_image")  # 30 # 0 is off, 1 all
        resample        = pimages.get("resample")  # Image.Resampling.LANCZOS
        halftone        = pimages.get("halftone")  # None # (4, 30) # or None
        b_colorize      = pimages.get("b_colorize")  # True
        b_force_write   = pimages.get("b_force_write")  # params.get("b_perform_image_conversion_force")
        ###b_1bit          = pimages.get("b_1bit")
        b_greyscale     = pimages.get("b_greyscale")  # False
        b_use_palette   = pimages.get("b_use_palette")  # False
        blend_alpha     = pimages.get("blend_alpha")  # 0.8 # 0.666 0.8
        cube_lut_path   = pimages.get("cube_lut_path")
        
        if cube_lut_path:
            shutil.copy(cube_lut_path, config.path_stats)
        
        if b_force_write and "Cancel" == pag.confirm(text=f"images: b_force_write: {b_force_write}", timeout=2000):
            exit(0)
            
        print(wh.format_dict(params["images"]))
        time.sleep(3)
        
        #-----------------------------------------
        # 
        #-----------------------------------------
        images = wh.collect_files_endswith(params.get("project_folder"), config.image_exts)        
        images = [img for img in images if not config.suffix_compressed in img]
        print("images",  hw.GRAY, *images, hw.RESET, sep = "\n\t")
        #wh.log("images", *[f"\n\t{x}" for x in images], filepath=config.path_log_params, echo=False)

        if cube_lut_path:
            print("loading lut:", wh.CYAN, cube_lut_path, wh.RESET)
            lut = pillow_lut.load_cube_file(cube_lut_path)
        else:
            lut = None
            
        new_ext = config.target_image_ext
                                         
        # convert images
        perc_avg = 0.0
        for cnt, path in enumerate(images):
            
            print("-"*88)
            path        = os.path.normpath(path) # wh.to_posix(path)
            name, _     = os.path.splitext(path) # ('my_file', '.txt')
            out_path    = name + config.suffix_compressed + new_ext 
            out_path    = os.path.normpath(out_path) # wh.to_posix(out_path)
            
            conversions.append((path, out_path))
                        
            if b_force_write or not wh.file_exists_and_valid(out_path):
            
                print("\t", "{}/{}:".format(cnt+1, len(images)), os.path.basename(path))
                print("\t\t", wh.progress_string(cnt / len(images), verbose_string="", VT=wh.CYAN, n=33))
                print("\t\t", "new_ext:", new_ext)
                
                size_orig   = os.path.getsize(path)
                image       = Image.open(path)
                is_transp   = wh.image_has_transparency(image)
                #image      = image.convert('RGBA' if is_transp else 'RGB')
                wh_orig     = image.size
                
                old_mode    = image.mode
                
                # colorize png?
                enhance_transp = True if (pimages.get("b_enhance_transp") and is_transp) else False
                print("\t\t", "enhance_transp:", wh.YELLOW, enhance_transp, wh.RESET)
                #wh.log("enhance_transp:", enhance_transp, filepath=config.path_log_params, echo=False)
                
                # NEW put this in app_110 TODO
                def func_size(path, csv_path, size_thresh, size_large, size_small):
                    
                    # could read this to ram beforehand TODO

                    relpath = wh.to_posix('/' + os.path.relpath(path, config.project_folder))
                    relpath = wh.get_path_local_root_subdomains(relpath, config.base)
                    relname, ext = os.path.splitext(relpath)
                                        
                    # look through all paths in csv and get size in page
                    found   = False
                    w,h     = 0,0
                    with open(csv_path, mode="r", encoding="utf-8") as fp:
                        for line in fp:
                            if line.startswith('/'):
                                c_base, c_path, c_w, c_h, c_nw, c_nh, c_url, c_url_parent = line.split(',')
                                if relname == c_base:
                                    found = True
                                    w = max(int(c_w), w)
                                    h = max(int(c_h), h)
                                    print("\t\t", wh.GREEN, "found:", c_base, w, h, c_nw, c_nh, wh.RESET)
                                    #break # can find multiple entries per image --> accumulate bigger w then
                                    
                    if not found:
                        print("\t\t", wh.RED, "NOT found:", relname, w, h, wh.RESET)
                    
                    if (w >= size_thresh or h >= size_thresh) or (not found):
                        return size_large
                    else:
                        return size_small
                                
                new_dim = func_size(
                    path, 
                    csv_path=config.path_image_sizes, 
                    size_thresh=pimages.get("size_thresh"), 
                    size_large=pimages.get("size_large"),
                    size_small=pimages.get("size_small")
                ) 
                image.thumbnail(new_dim, resample=resample)
                image_orig = image.copy()
                #image_orig  = ImageOps.autocontrast(image_orig.convert("RGB"))
                    
                # https://jdhao.github.io/2019/03/07/pillow_image_alpha_channel/
                def get_mask_rgba(image):
                    
                    if not wh.image_has_transparency(image):
                        print(wh.YELLOW, "image has no tranparency...None", wh.RESET)
                        return None
                    
                    mask    = image.convert("RGBA").copy()
                    mixels  = mask.load() 
                    
                    width, height   = image.size
                    for x in range(width):
                        for y in range(height):
                            r,g,b,a     = tuple(mixels[x,y])
                            mixels[x,y] = tuple([a,a,a,a])
                            
                    return mask
                    
                def apply_mask_rgba(image, mask):
                    
                    assert image
                    assert mask
                    
                    assert image.size == mask.size   
                    assert mask.mode  == "RGBA",  mask.mode 
                    
                    image   = image.convert("RGBA")
                    pixels  = image.load() # this is not a list, nor is it list()'able
                    mixels  = mask.load()      
                    
                    width, height = image.size    
                    for x in range(width):
                        for y in range(height):
                            r,g,b,a     = tuple(pixels[x,y])
                            a           = mixels[x,y][0]
                            pixels[x,y] = tuple([r,g,b,a])
                            
                    return image
                    #return image.putalpha(mask.convert("L"))
                            
                if enhance_transp:
                    mask  = get_mask_rgba(image) # after resizing
                    ###mask.save(path + "__mask__.png", 'png', optimize=True, lossless=True) # debug
                else:
                    mask = None
                
                #if (b_colorize and not is_transp) or enhance_transp: 
                if b_colorize and (not is_transp or enhance_transp): 
                    image = image.convert("L") # L only !!! # LA L 1
                    black = "#003300"
                    black = "#002200"
                    #black = "#001733"
                    white = "#eeeeee"
                    white = "#ffffff"
                    image = ImageOps.colorize(image, black=black, white=white)
                    ####image = ImageOps.autocontrast(image)
                    
                # blend: 0 returns orig, 1 new
                if (blend_alpha > 0.0) and (not is_transp or enhance_transp):  # ???? 0 or 1 TODO
                    ###assert image.mode == image_orig.mode
                    image = Image.blend(
                        image_orig.convert("RGB"), 
                        image.convert("RGB"), 
                        blend_alpha
                    )

                if enhance_transp:
                    image = image.convert("RGBA")
                    image = apply_mask_rgba(image, mask)
                    
                if lut and (not is_transp or enhance_transp):
                    print("\t\t", "lut      :", wh.CYAN, os.path.basename(cube_lut_path), wh.RESET)
                    if is_transp:
                        image = image.convert("RGBA")
                    else:
                        image = image.convert("RGB")
                    image = image.filter(lut)
                    
                if halftone and not is_transp:
                    image = image.convert("L")
                    image = ht.halftone(image, ht.euclid_dot(spacing=halftone[0], angle=halftone[1]))
                    assert isinstance(image, PIL.Image.Image)
                            
                    
                # image modes
                # if b_1bit and not is_transp:
                #         image = image.convert("1", dither=Image.Dither.FLOYDSTEINBERG)
                                        
                if b_greyscale:
                    if is_transp:
                        image = image.convert("LA")
                    else:
                        image = image.convert("L")
                    
                # looking terrible
                if b_use_palette and not is_transp:
                    dither  = None # Image.NONE # NONE FLOYDSTEINBERG None
                    palette = Image.ADAPTIVE # WEB ADAPTIVE
                    colors  = 256 # Number of colors to use for the ADAPTIVE palette. Defaults to 256.
                    if is_transp:
                        #image = image.convert("PA", dither=dither, palette=palette, colors=colors ) # NONE FLOYDSTEINBERG
                        pass
                    else:
                        image = image.convert("P",  dither=dither, palette=palette, colors=colors)
                        
                format = new_ext.lstrip('.')    
                if is_transp:
                    image.save(out_path, format=format, optimize=True, lossless=True) # !!!
                else:
                    image.save(out_path, format=format, optimize=True, quality=quality) 
                    
                print("\t\t", "format     :", format)
                print("\t\t", "quality    :", quality)
                print("\t\t", "wh         :", wh_orig, "-->", image.size, "| new_dim:", new_dim)
                print("\t\t", "is_transp  :", wh.vt_b(is_transp))
                print("\t\t", "mode       :", old_mode, "-->", image.mode)
                print("\t\t", "blend_alpha:", blend_alpha)
            
                size_new = os.path.getsize(out_path)
                print("\t\t", "saved  :", wh.vt_saved_percent_string(size_orig, size_new), os.path.basename(out_path))
                perc_avg += wh._saved_percent(size_orig, size_new)
                
                if show_nth_image > 0 and not (cnt%show_nth_image):
                    wh.image_show_file(out_path, secs=0.5)
                
            else:
                print("\t\t", "already exists:", os.path.basename(out_path))
        ### for images />
            
        if images:                                                
            perc_avg /= len(images)  
            perc_avg = round(perc_avg, 1)  
            vt = wh.GREEN if perc_avg >= 0 else wh.RED
            print("perc_avg:",vt + str(perc_avg) + "%" + wh.RESET)
            time.sleep(3)
    

         #print(*conversions, sep="\n\t")
        if conversions:
            conv.save(params.get("path_conversions"), conversions)   
    ### b_perform_image_conversion />

    #-----------------------------------------
    # better use a list in case above finds no more erased images....
    # TODO need to create /wp paths from these images...rel to project folder and using / 
    # https://www.geeksforgeeks.org/python-os-path-relpath-method/
    #-----------------------------------------
    #-----------------------------------------
    # 
    #-----------------------------------------
    def replace_all_conversions_in_file(filename, conversions):
        
        #print("\t", "replace_all_conversions_in_file:", wh.CYAN, filename, wh.RESET)
        
        # # fp = open(filename, "r", encoding="utf-8")
        # # html = fp.read()
        
        html = wh.string_from_file(filename)
        
        # replace
        #print("\t\t", end='')
        for i, conversion in enumerate(conversions):
            fr, to = conversion
            
            if wh.file_exists_and_valid(to):    
                
                # rel paths from root /
                wp_fr = wh.to_posix('/' + os.path.relpath(fr, params.get("project_folder")))
                wp_to = wh.to_posix('/' + os.path.relpath(to, params.get("project_folder")))
                
                cnt = html.count(wp_fr)
                if cnt > 0:
                    
                    # print(
                    #     "\t\t", "cnt:", cnt,  
                    #     wh.CYAN, "wp_fr", wh.GRAY, wp_fr, 
                    #     wh.CYAN, "wp_to", wh.GRAY, wp_to, 
                    #     wh.RESET
                    # )
                    
                    # if not (i%1):
                    #     #print(str(cnt) + ' ', end='')
                    #     pass
                    
                    
                    # compressor for html may strip quotes....
                    no_f = lambda s: s # dangerous! as quotes may be removed by html-minify
                    # NEW try all TODO with quotes
                    for f in [ wh.dq,  wh.sq,  wh.pa,  wh.qu]: ## , no_f]: # dangerous! as quotes may be removed by html-minify
                        #print(f"{ wh.GRAY}\t\t\t replace_all: {f(wp_fr)} {wh.RESET}") 
                        html = wh.replace_all(html,  f(wp_fr),  f(wp_to) )    
            else:
                print("\t\t\t", wh.RED, "does not exist: to:", to, wh.RESET, end='\r')
        ### for conversion />
        
        wh.string_to_file(html, filename)
        
        # # # fp.close()
        
        # # # #open the input file in write mode
        # # # fp = open(filename, "w", encoding="utf-8")
        # # # fp.write(html)
        # # # fp.close()

    #-----------------------------------------
    # 
    #-----------------------------------------
    if params.get("b_replace_conversions"):
        wh.logo("b_replace_conversions")
        
        conversions = conv.load(params.get("path_conversions"))    
        #print(*conversions, sep="\n\t")     
                                
        html_files = wh.collect_files_endswith( params.get("project_folder") , ["index.html", ".css", ".js"])
        for i, html_file in enumerate(html_files):
            verbose_string = f"\t {i+1}/{len(html_files)} {os.path.basename(html_file)}"
            wh.progress(i / len(html_files), verbose_string=verbose_string, VT=wh.CYAN, n=80, prefix="")
            
            replace_all_conversions_in_file(html_file, conversions)
              
            # DANGEROUS!!!
            if False:
                # TODO why are these still here?
                # replace left over image extensions
                for q_end in ["\"", "\'", ")"]:
                    for ext in config.image_exts_no_target:
                        wh.file_replace_all(html_file, ext + q_end, config.target_image_ext + q_end)        
                                     
        ### for /> 
    ### b_perform_replacement />            
            
                
    # # # # #-----------------------------------------
    # # # # # b_fix_xml
    # # # # #-----------------------------------------
    # # # # if b_fix_xml_elements:
    # # # #     wh.logo("b_fix_xml_elements")
        
    # # # #     func=lambda s : True # finds all
    # # # #     func=lambda file : any(file.lower().endswith(ext) for ext in config.image_exts)
    # # # #     func=lambda file : file.lower().endswith("index.html")
    # # # #     files_index_html = wh.collect_files_func(project_folder, func=func)
    # # # #     #print(*files_index_html, sep="\n\t")
        
    # # # #     color = "darkseagreen"
    # # # #     svg_percircle = f"""<div class="percircle"><svg viewBox="0 0 500 500" role="img" xmlns="http://www.w3.org/2000/svg">
    # # # #         <g id="myid">
    # # # #             <circle stroke="{color}"
    # # # #                     stroke-width="12px"
    # # # #                     fill="none"
    # # # #                     cx="250"
    # # # #                     cy="250"
    # # # #                     r="222" />
    # # # #             <text style="font: bold 12rem sans-serif;"
    # # # #                 text-anchor="middle"
    # # # #                 dominant-baseline="central"
    # # # #                 x="50%"
    # # # #                 y="50%"
    # # # #                 fill="{color}">{perc100_saved:.0f}%</text> 
    # # # #         </g>     
    # # # #     </svg></div>"""


    # # # #     for file in files_index_html:
            
    # # # #         print("-"*80)
    # # # #         print("file", wh.CYAN + file + wh.RESET)
    # # # #         wp_path     = wh.to_posix('/' + os.path.relpath(file, project_folder))
    # # # #         base_path   = config.base + wh.to_posix(os.path.relpath(file, project_folder)).replace("index.html", "")
    # # # #         same_page_link = f"""<a href="{base_path}">{config.base_netloc}</a>"""
            
    # # # #         """
    # # # #         Dies ist die energie-effiziente
    # # # #         energie optimierte 
    # # # #         Dies ist die Low Carbon Website
    # # # #         Dies ist die Low Carbon Website
    # # # #         This is the environmentally aware version of 
    # # # #         Dies ist die umweltbewusste Seite
    # # # #         This is the environmentally friendly twin of 
    # # # #         .<br/>The energy consumption of this website was reduced by {saved_string}.
    # # # #         .<br/>Der Energieverbrauch dieser Website wurde um {saved_string} reduziert.
    # # # #         """
    # # # #         # https://babel.pocoo.org/en/latest/dates.html
    # # # #         from babel.dates import format_date, format_datetime, format_time
    # # # #         dt = config.date_time_now
    # # # #         format='full' # long
    # # # #         saved_string = f"<span style=''>{perc100_saved:.1f}%</span>"
    # # # #         if "/en/" in wp_path:
    # # # #             dt_string = format_date(dt, format=format, locale='en')
    # # # #             banner_header_text = f"This is the Low Carbon proxy of {same_page_link}" # <br/>{svg_percircle}
    # # # #             banner_footer_text = f"{svg_percircle}<br/>unpowered by {config.html_infossil_link}" # <br/>{dt_string}
    # # # #         else:
    # # # #             dt_string = format_date(dt, format=format, locale='de_DE')
    # # # #             banner_header_text = f"Dies ist der Low Carbon Proxy von {same_page_link}"
    # # # #             banner_footer_text = f"{svg_percircle}<br/>unpowered by {config.html_infossil_link}" # <br/>{dt_string}
                
    # # # #         #---------------------------
    # # # #         # lxml
    # # # #         #---------------------------    
    # # # #         tree = lxml.html.parse(file) # lxml.html.fromstring(content)
            
    # # # #         # start the hocus pocus in focus
    # # # #         # use section-1 from original site as frag
    # # # #         if False and False:
    # # # #             hx.replace_xpath_with_fragment_from_file(
    # # # #                 tree, 
    # # # #                 "//section[@id='section-1']", 
    # # # #                 "data/karlsruhe.digital_fragment_section1.html" # frag_file_path
    # # # #             )
            
    # # # #         #---------------------------
    # # # #         # banners
    # # # #         #---------------------------    
    # # # #         if True: # +++
    # # # #             # TODO must be /en/ and not depending on wp_path /en/
    # # # #             banner_header = hx.banner_header(banner_header_text)
    # # # #             hx.remove_by_xpath(tree, "//div[@class='banner_header']")
    # # # #             print("\t adding banner_header")    
    # # # #             try:                
    # # # #                 tree.find(".//header").insert(0, banner_header)    
    # # # #             except Exception as e:
    # # # #                 print("\t", wh.RED, e, wh.RESET)
    # # # #                 exit(1)

    # # # #             """ 
    # # # #             media
    # # # #             <footer id="colophon" class="site-footer with-footer-logo" role="contentinfo"><div class="footer-container"><div class="logo-container"><a href="https://media.karlsruhe.digital/" title="" rel="home" class="footer-logo tgwf_green" data-hasqtip="14"><img src="https://kadigital.s3-cdn.welocal.cloud/sources/5ffed45149921.svg" alt=""></a></div><div class="footer-nav"><div class="menu-footer-container"><ul id="menu-footer" class="footer-menu"><li id="menu-item-551" class="menu-item menu-item-type-custom menu-item-object-custom menu-item-551"><a target="_blank" rel="noopener" href="/impressum/index.html">Impressum</a></li><li id="menu-item-550" class="menu-item menu-item-type-custom menu-item-object-custom menu-item-550"><a target="_blank" rel="noopener" href="/datenschutz/index.html">Datenschutz</a></li></ul></div> </div></div><div class="footer-socials-wrapper"><ul class="footer-socials"><li><a href="https://www.facebook.com/karlsruhe.digital" target="" rel="nofollow" class="social ss-facebook tgwf_green" data-hasqtip="15"><span>Facebook</span></a></li><li><a href="https://twitter.com/KA_digital" target="" rel="nofollow" class="social ss-twitter tgwf_grey"><span>Twitter</span></a></li><li><a href="https://www.instagram.com/karlsruhe.digital/" target="" rel="nofollow" class="social ss-instagram tgwf_green" data-hasqtip="16"><span>Instagram</span></a></li><li><a href="mailto:info@karlsruhe.digital" target="" rel="nofollow" class="social ss-mail"><span>Mail</span></a></li></ul></div></footer>

    # # # #             """                
    # # # #             banner_footer = hx.banner_footer(banner_footer_text)
    # # # #             hx.remove_by_xpath(tree, "//div[@class='banner_footer']")
    # # # #             print("\t adding banner_footer")  
    # # # #             try:
    # # # #                 footer = tree.find(".//footer") # ".//body"
    # # # #                 if not footer:
    # # # #                     footer = tree.find(".//body")
    # # # #                 footer.append(banner_footer)
    # # # #             except Exception as e:
    # # # #                 print("\t", wh.RED, e, wh.RESET)    
    # # # #                 exit(1)                

    # # # #         #---------------------------
    # # # #         # image attributes srcset
    # # # #         #---------------------------    
    # # # #         tree = hx.remove_attributes(tree, "img", ["srcset", "sizes", "xxxsrcset", "xxxsizes", "XXXsrcset", "XXXsizes"])

    # # # #         # remove logo in footer: body > footer > div.footer-top > div > div > div.col-xl-4
    # # # #         hx.remove_by_xpath(tree, "//div[@class='footer-top']//a[@class='logo']")

    # # # #         #---------------------------
    # # # #         # menu
    # # # #         #---------------------------    
    # # # #         b_hide_search = True
    # # # #         if b_hide_search:
    # # # #             hx.remove_by_xpath(tree, "//li[@id='menu-item-136']") # search in menu
    # # # #         else:
    # # # #             #hx.replace_by_xpath(tree, "//i[contains(@class, 'fa-search')]", "<span>SUCHE</span")
    # # # #             pass
            
    # # # #         if b_hide_media_subdomain:
    # # # #             hx.remove_by_xpath(tree, "//li[@id='menu-item-3988']") # media submenu --> no media.

    # # # #         # all fa font awesome TODO also gets rid of dates etc...
    # # # #         # hx.remove_by_xpath(tree, "//i[contains(@class, 'fa-')]")

    # # # #         # <span class="swiper-item-number">6</span>
    # # # #         # if True:
    # # # #         #     #hx.remove_by_xpath(tree, "//span[@class='swiper-item-number']")
    # # # #         #     hx.remove_by_xpath(tree, "//div[@id='hero-swiper']//span[@class='swiper-item-number']")
    # # # #         #     hx.remove_by_xpath(tree, "//div[@id='hero-swiper']//span[@class='color-white']")
            

    # # # #         #---------------------------
    # # # #         # scripts
    # # # #         #---------------------------                      
    # # # #         # //script[normalize-space(text())]
    # # # #         hx.remove_by_xpath(tree, "//script[contains(normalize-space(text()), '_wpemojiSettings' )]")
    # # # #         hx.remove_by_xpath(tree, "//script[contains(normalize-space(text()), 'ftsAjax' )]")
    # # # #         hx.remove_by_xpath(tree, "//script[contains(normalize-space(text()), 'checkCookie' )]")
            
    # # # #         hx.remove_by_xpath(tree, "//head//script[contains(@src, 'google-analytics' )]")
    # # # #         hx.remove_by_xpath(tree, "//head//script[contains(@src, 'wp-emoji-release' )]")
    # # # #         hx.remove_by_xpath(tree, "//head//script[contains(@src, 'feed-them-social' )]")
            
    # # # #         hx.remove_by_xpath(tree, "//head//script[contains(@src, 'jquery-migrate' )]")
    # # # #         #hx.remove_by_xpath(tree, "//head//script[contains(@src, 'jquery.js' )]") >> needed for menu !!!
            
    # # # #         hx.remove_by_xpath(tree, "//head//script[@async]")
    # # # #         hx.remove_by_xpath(tree, "//head//script[@defer]")
            
    # # # #         # hx.remove_by_xpath(tree, "//head//script[@src='https://www.google-analytics.com/analytics.js']")
    # # # #         # hx.remove_by_xpath(tree, "//head//script[@src='https://www.google-analytics.com/analytics.js']")
    # # # #         # hx.remove_by_xpath(tree, "//head//script[@src='/wp-includes/js/wp-emoji-release.min.js']")
    # # # #         # hx.remove_by_xpath(tree, "//head//script[@src='/wp-includes/js/wp-emoji-release.min.js']")
            
    # # # #         #hx.remove_by_xpath(tree, "//body//script[contains(@src, 'bootstrap' )]")
    # # # #         #hx.remove_by_xpath(tree, "//body//script[contains(@src, 'owl.carousel' )]")
    # # # #         ####hx.remove_by_xpath(tree, "//body//script[contains(@src, 'script.js' )]") NO!!
    # # # #         hx.remove_by_xpath(tree, "//body//script[contains(@src, 'wp-embed' )]")
    # # # #         hx.remove_by_xpath(tree, "//body//script[contains(@src, 'googletagmanager' )]")
    # # # #         hx.remove_by_xpath(tree, "//body//script[contains(text(), 'gtag' )]")
            
    # # # #         #---------------------------
    # # # #         # twitter feeds
    # # # #         #---------------------------   
    # # # #         hx.remove_by_xpath(tree, "//section[contains(@class,'social-media-feed')]")
            
    # # # #         #---------------------------
    # # # #         # social media footer
    # # # #         #--------------------------- 
    # # # #         hx.replace_xpath_with_fragment(tree, "//div[contains(@class, 'footer-bottom' )]//div[contains(@class, 'footer-social-links' )]", config.footer_social_html)
    # # # #         hx.replace_xpath_with_fragment(tree, "//div[@id='unpowered-social-media-footer']", config.footer_social_html)

    # # # #         #---------------------------
    # # # #         # swipers
    # # # #         #--------------------------- 
    # # # #         # //div[contains(@id, 'blog-swiper' )]//div[contains(@class, 'owl-nav' )][last()]
    # # # #         ###hx.remove_by_xpath(tree, "//div[contains(@id, 'blog-swiper' )]//div[contains(@class, 'owl-nav' )][last()]")
    # # # #         hx.remove_by_xpath(tree, "//div[contains(@id, 'blog-swiper' )]//div[contains(@class, 'owl-nav' )][1]")
    # # # #         hx.remove_by_xpath(tree, "//div[contains(@id, 'hero-swiper' )]//div[contains(@class, 'owl-nav' )][1]")
    # # # #         hx.remove_by_xpath(tree, "//div[contains(@id, 'testimonial-swiper' )]//div[contains(@class, 'owl-nav' )][1]")
    # # # #         hx.remove_by_xpath(tree, "//div[contains(@id, 'theses-swiper' )]//div[contains(@class, 'owl-nav' )][1]")
            
    # # # #         #---------------------------
    # # # #         # video/media player
    # # # #         #---------------------------          
    # # # #         hx.remove_by_xpath(tree, "//div[contains(@class, 'wp-video' )]")            
    # # # #         hx.remove_by_xpath(tree, "//div[contains(@class, 'mejs-video' )]")            

    # # # #         #---------------------------
    # # # #         # save
    # # # #         #--------------------------- 
    # # # #         out_path = file # + "__test.html"
    # # # #         print("writing:", out_path)
    # # # #         tree.write(
    # # # #             out_path, 
    # # # #             pretty_print=True, 
    # # # #             xml_declaration=False,   
    # # # #             encoding="utf-8",   # !!!!
    # # # #             method='html'       # !!!!
    # # # #         )
        
    
    # # # #     # files_index_html = wh.collect_files_endswith(project_folder, ["index.html"])
    # # # #     # for file in files_index_html:
    # # # #     #     print("-"*80)
    # # # #     #     content = wh.string_from_file(file, sanitize=False)
    # # # #     #     soup    = bs(content)
    # # # #     #     content = soup.prettify()
    # # # #     #     print(content)
                      
    #-----------------------------------------
    # 
    #-----------------------------------------
    if b_delete_conversion_originals:
        if "Cancel" == pag.confirm(text=f"b_delete_conversion_originals: {b_delete_conversion_originals}"):
            exit(0)
            
        wh.logo("b_delete_conversion_originals")
        conversions = conv.load(params.get("path_conversions"))    
        for conversion in conversions:
            fr_to_delete, __to = conversion
            if wh.file_exists_and_valid(fr_to_delete):
                print("\t", wh.RED, "removing:", os.path.basename(fr_to_delete), wh.RESET)
                os.remove(fr_to_delete)
                

    #-----------------------------------------
    # TODO collect files and make sitemap
    #-----------------------------------------  
    b_sitemap_xml = True
    if b_sitemap_xml:
        wh.logo("sitemap")
        
        urls = []
        for file in wh.collect_files_endswith(config.project_folder, ["index.html"]):
            urls.append(
                wh.to_posix(config.target_base + os.path.relpath(file, config.project_folder))           
            )
        #print(*urls, sep="\n\t")
        import sitemap
        sitemap.sitemap_xml_from_list(urls, out_xml_path=config.path_htdocs_sitemap)
        
        # gzip
        wh.gzip_file(config.path_htdocs_sitemap, config.path_htdocs_sitemap_gz)
        os.remove(config.path_htdocs_sitemap)
        
        # robots.txt https://en.wikipedia.org/wiki/Robots_exclusion_standard
        robots_text = f"User-agent: *\nDisallow: \nSitemap: {config.target_base}{config.filename_sitemap_gz}\n"  
        wh.string_to_file(robots_text, config.path_htdocs_robots)
        
        print("written:", config.path_htdocs_sitemap_gz)
        print("written:", config.path_htdocs_robots)
        
       
     
    #-----------------------------------------
    # 
    #-----------------------------------------  
    # rm xmlrpc.ph   
    wh.logo("rm xmlrpc.ph")
    xmlrpc_path = config.project_folder+"xmlrpc.php"
    if os.path.isfile(xmlrpc_path):
        os.remove(xmlrpc_path)

    #-----------------------------------------
    # b_minify1
    #-----------------------------------------
    def minify(title="minify"):
        
        wh.logo(title)
        
        for file in wh.collect_files_endswith(config.project_folder, ["index.html"]):
            wh.html_minify_on_disk(file)
            
        for file in wh.collect_files_endswith(config.project_folder, [".css"]):
            wh.css_minify_on_disk(file)
            
        for file in wh.collect_files_endswith(config.project_folder, [".js"]):
            wh.js_minify_on_disk(file)
            
    if params.get("b_minify1"):
        minify("b_minify1")

    #-----------------------------------------
    # get_project_total_size
    #-----------------------------------------
    wh.logo("get_project_total_size")
    perc100_saved, total_size_originals, total_size_unpowered = wh.get_project_total_size(
        config.project_folder, 
        prefix=config.base_netloc,
        use_pdf=b_get_project_total_size_use_pdf
        )
                
    #-----------------------------------------
    # b_fix_xml
    #-----------------------------------------
    if params.get("b_fix_xml_elements"):
        wh.logo("b_fix_xml_elements")
        
        # func=lambda s : True # finds all
        # func=lambda file : any(file.lower().endswith(ext) for ext in config.image_exts)
        func=lambda file : file.lower().endswith("index.html")
        files_index_html = wh.collect_files_func(params.get("project_folder"), func=func)
        #print(*files_index_html, sep="\n\t")
        
        svg_percircle = f"""
        <div class="percircle"><svg viewBox="0 0 500 500" role="img" xmlns="http://www.w3.org/2000/svg">
            <g id="myid">
                <circle stroke="{config.svg_color}"
                        stroke-width="30px"
                        fill="none"
                        cx="250"
                        cy="250"
                        r="230" />
                <text style="font: bold 11.1rem sans-serif;"
                    text-anchor="middle"
                    dominant-baseline="central"
                    x="50%"
                    y="50%"
                    fill="{config.svg_color}">
                    <tspan font-size="1.0em">{round(perc100_saved):.0f}</tspan><tspan font-size="0.9em">％</tspan>
                </text> 
            </g>     
        </svg>
        <span>saved</span>
        </div> """
        # % ﹪ ％ # 15.1rem 1.0em 0.5em # 11.1rem 1 1 #

        for file in files_index_html:
            
            print("-"*80)
            print("file", wh.CYAN + file + wh.RESET)
            wp_path     = wh.to_posix('/' + os.path.relpath(file, params.get("project_folder")))
            base_path   = config.base + wh.to_posix(os.path.relpath(file, params.get("project_folder"))).replace("index.html", "")
            same_page_link = f""" <a href="{base_path}" class="same_page_link">{config.base_netloc}</a> """
            
            """
            Zero Fossil Site
            Zero Carbon Site
            Zero Energy Site
            Minimal Carbon Site
            Dies ist die energie-effiziente
            energie optimierte 
            Dies ist die Low Carbon Website
            Dies ist die Low Carbon Website
            This is the environmentally aware version of 
            Dies ist die umweltbewusste Seite
            This is the environmentally friendly twin of 
            .<br/>The energy consumption of this website was reduced by {saved_string}.
            .<br/>Der Energieverbrauch dieser Website wurde um {saved_string} reduziert.
            This is the Low Carbon proxy of {same_page_link}
            """
            # https://babel.pocoo.org/en/latest/dates.html
            from babel.dates import format_date, format_datetime, format_time
            dt = config.date_time_now
            format='full' # long
            saved_string = f"<span style=''>{perc100_saved:.1f}%</span>"
            if "/en/" in wp_path:
                dt_string = format_date(dt, format=format, locale='en')
                banner_header_text = f"<a href='http://openresource.1001suns.com'>{config.svg_leaf_img}</a> This is the Minimal Carbon Site {same_page_link}" # <br/>{svg_percircle}  <sup>{config.html_by_infossil_link}</sup>
                banner_footer_text = f"unpowered by <a href='https://1001suns.com'>infossil<br/>{svg_percircle}</a>" # <br/>{dt_string}
            else:
                dt_string = format_date(dt, format=format, locale='de_DE')
                banner_header_text = f"<a href='http://openresource.1001suns.com'>{config.svg_leaf_img}</a> Dies ist die Minimal Carbon Site {same_page_link}"
                banner_footer_text = f"unpowered by <a href='https://1001suns.com'>infossil<br/>{svg_percircle}</a>" # <br/>{dt_string}
                
            #---------------------------
            # lxml
            #---------------------------    
            tree = lxml.html.parse(file) # lxml.html.fromstring(content)
            
            # start the hocus pocus in focus
            # use section-1 from original site as frag
            if False and False:
                hx.replace_xpath_with_fragment_from_file(
                    tree, 
                    "//section[@id='section-1']", 
                    "data/karlsruhe.digital_fragment_section1.html" # frag_file_path
                )
                
            # # section 1 unneeded
            # hx.remove_by_xpath(tree, "//section[@id='section-1']//div[contains(@class, 'owl-dots' )]")
            # hx.remove_by_xpath(tree, "//section[@id='section-1']//div[contains(@class, 'owl-nav'  )]")
            
            # set first item zo 07
            # //div[@id='testimonial-swiper']//span[contains(@class, 'swiper-item-number' )]
            hx.set_text_by_xpath(
                tree, 
                "//div[@id='testimonial-swiper']//span[contains(@class, 'swiper-item-number' )]", 
                "07"
            )
            
            # ###OK!!!!!!!!!!!
            # hx.set_text_by_xpath(
            #     tree, 
            #     "//li[@id='menu-item-2675']/a", 
            #     "was struktur now replaced yyyy<<<<<"
            # )
            
            # # last slide from hero-swiper
            # # //section[@id='section-1']//div[contains(@class, 'owl-item'  )][last()]
            # hx.remove_by_xpath(tree, "//section[@id='section-1']//div[contains(@class, 'owl-item'  )][last()]")
            
            #---------------------------
            # banners
            #---------------------------    
            if True: # +++
                # TODO must be /en/ and not depending on wp_path /en/
                banner_header = hx.banner_header(banner_header_text)
                hx.remove_by_xpath(tree, "//div[@class='banner_header']")
                print("\t adding banner_header")    
                try:                
                    tree.find(".//header").insert(0, banner_header)    
                except Exception as e:
                    print("\t", wh.RED, e, wh.RESET)
                    exit(1)

                """ 
                media
                <footer id="colophon" class="site-footer with-footer-logo" role="contentinfo"><div class="footer-container"><div class="logo-container"><a href="https://media.karlsruhe.digital/" title="" rel="home" class="footer-logo tgwf_green" data-hasqtip="14"><img src="https://kadigital.s3-cdn.welocal.cloud/sources/5ffed45149921.svg" alt=""></a></div><div class="footer-nav"><div class="menu-footer-container"><ul id="menu-footer" class="footer-menu"><li id="menu-item-551" class="menu-item menu-item-type-custom menu-item-object-custom menu-item-551"><a target="_blank" rel="noopener" href="/impressum/index.html">Impressum</a></li><li id="menu-item-550" class="menu-item menu-item-type-custom menu-item-object-custom menu-item-550"><a target="_blank" rel="noopener" href="/datenschutz/index.html">Datenschutz</a></li></ul></div> </div></div><div class="footer-socials-wrapper"><ul class="footer-socials"><li><a href="https://www.facebook.com/karlsruhe.digital" target="" rel="nofollow" class="social ss-facebook tgwf_green" data-hasqtip="15"><span>Facebook</span></a></li><li><a href="https://twitter.com/KA_digital" target="" rel="nofollow" class="social ss-twitter tgwf_grey"><span>Twitter</span></a></li><li><a href="https://www.instagram.com/karlsruhe.digital/" target="" rel="nofollow" class="social ss-instagram tgwf_green" data-hasqtip="16"><span>Instagram</span></a></li><li><a href="mailto:info@karlsruhe.digital" target="" rel="nofollow" class="social ss-mail"><span>Mail</span></a></li></ul></div></footer>

                """                
                banner_footer = hx.banner_footer(banner_footer_text)
                hx.remove_by_xpath(tree, "//div[@class='banner_footer']")
                print("\t adding banner_footer")  
                try:
                    footer = tree.find(".//footer") # ".//body"
                    if not footer:
                        footer = tree.find(".//body")
                    footer.append(banner_footer)
                except Exception as e:
                    print("\t", wh.RED, e, wh.RESET)    
                    exit(1)                

            #---------------------------
            # image attributes srcset
            #---------------------------    
            tree = hx.remove_attributes(tree, "img", ["srcset", "sizes", "xxxsrcset", "xxxsizes", "XXXsrcset", "XXXsizes"])

            # remove logo in footer: body > footer > div.footer-top > div > div > div.col-xl-4
            hx.remove_by_xpath(tree, "//div[@class='footer-top']//a[@class='logo']")

            #---------------------------
            # menu
            #---------------------------    
            b_hide_search = True
            if b_hide_search:
                hx.remove_by_xpath(tree, "//li[@id='menu-item-136']") # search in menu
            else:
                #hx.replace_by_xpath(tree, "//i[contains(@class, 'fa-search')]", "<span>SUCHE</span")
                pass
            
            if params.get("b_hide_media_subdomain"):
                hx.remove_by_xpath(tree, "//li[@id='menu-item-3988']") # media submenu --> no media.

            # all fa font awesome TODO also gets rid of dates etc...
            # hx.remove_by_xpath(tree, "//i[contains(@class, 'fa-')]")

            # <span class="swiper-item-number">6</span>
            # if True:
            #     #hx.remove_by_xpath(tree, "//span[@class='swiper-item-number']")
            #     hx.remove_by_xpath(tree, "//div[@id='hero-swiper']//span[@class='swiper-item-number']")
            #     hx.remove_by_xpath(tree, "//div[@id='hero-swiper']//span[@class='color-white']")
            

            #---------------------------
            # scripts
            #---------------------------                      
            # //script[normalize-space(text())]
            hx.remove_by_xpath(tree, "//script[contains(normalize-space(text()), '_wpemojiSettings' )]")
            hx.remove_by_xpath(tree, "//script[contains(normalize-space(text()), 'ftsAjax' )]")
            hx.remove_by_xpath(tree, "//script[contains(normalize-space(text()), 'checkCookie' )]")
            
            hx.remove_by_xpath(tree, "//head//script[contains(@src, 'google-analytics' )]")
            hx.remove_by_xpath(tree, "//head//script[contains(@src, 'wp-emoji-release' )]")
            hx.remove_by_xpath(tree, "//head//script[contains(@src, 'feed-them-social' )]")
            
            hx.remove_by_xpath(tree, "//head//script[contains(@src, 'jquery-migrate' )]")
            #hx.remove_by_xpath(tree, "//head//script[contains(@src, 'jquery.js' )]") >> needed for menu !!!
            
            hx.remove_by_xpath(tree, "//head//script[@async]")
            hx.remove_by_xpath(tree, "//head//script[@defer]")
            
            # hx.remove_by_xpath(tree, "//head//script[@src='https://www.google-analytics.com/analytics.js']")
            # hx.remove_by_xpath(tree, "//head//script[@src='https://www.google-analytics.com/analytics.js']")
            # hx.remove_by_xpath(tree, "//head//script[@src='/wp-includes/js/wp-emoji-release.min.js']")
            # hx.remove_by_xpath(tree, "//head//script[@src='/wp-includes/js/wp-emoji-release.min.js']")
            
            #hx.remove_by_xpath(tree, "//body//script[contains(@src, 'bootstrap' )]")
            #hx.remove_by_xpath(tree, "//body//script[contains(@src, 'owl.carousel' )]")
            ####hx.remove_by_xpath(tree, "//body//script[contains(@src, 'script.js' )]") NO!!
            hx.remove_by_xpath(tree, "//body//script[contains(@src, 'wp-embed' )]")
            hx.remove_by_xpath(tree, "//body//script[contains(@src, 'googletagmanager' )]")
            hx.remove_by_xpath(tree, "//body//script[contains(text(), 'gtag' )]")
            
            #---------------------------
            # twitter feeds ERASE
            #---------------------------   
            # COMPLETELY remove twitter social feeds
            # hx.remove_by_xpath(tree, "//section[contains(@class,'social-media-feed')]") # can actually leave this

            #---------------------------
            # twitter feeds KEEP
            #---------------------------   
            xp_twitter_feed = "//section[contains(@class,'social-media-feed')]"
            
            # remove twitter images # popup-gallery-twitter
            hx.remove_by_xpath(tree, "//section[contains(@class,'social-media-feed')]//div[contains(@class, 'popup-gallery-twitter')]")
            
            # clear our former repair
            hx.remove_by_xpath(tree, "//section[contains(@class,'social-media-feed')]//img")
            
            # add image for twitter logo
            for logo in ["twitter"]:
                html_img = f"{config._html_icon_img(f'{logo}', f'icon-white icon-{logo}', 'display:inline-block !important')}"
                hx.append_xpath_with_fragment(
                    tree, 
                    f"{xp_twitter_feed}//div[contains(@class,'fts-mashup-twitter-icon')]/a", 
                    html_img                  
                )
            
            for share in ["facebook", "twitter"]:

                # remove FAwesome nongo
                hx.remove_by_xpath(
                    tree, 
                    f"{xp_twitter_feed}//i[contains(@class,'fa-{share}')]"
                    )
                
                html_img = config._html_icon_img(f'{share}', f'icon-white-smaller icon-{share}', 'display:inline-block !important') # class style
                # append our svg
                hx.append_xpath_with_fragment(
                    tree, 
                    f"{xp_twitter_feed}//a[contains(@class, 'ft-gallery{share}')]", 
                    html_img                  
                )
                
           
            #---------------------------
            # social media footer
            #--------------------------- 
            hx.replace_xpath_with_fragment(tree, "//div[contains(@class, 'footer-bottom' )]//div[contains(@class, 'footer-social-links' )]", config.footer_social_html)
            hx.replace_xpath_with_fragment(tree, "//div[@id='unpowered-social-media-footer']", config.footer_social_html)

            #---------------------------
            # swipers
            #--------------------------- 
            # //div[contains(@id, 'blog-swiper' )]//div[contains(@class, 'owl-nav' )][last()]
            ###hx.remove_by_xpath(tree, "//div[contains(@id, 'blog-swiper' )]//div[contains(@class, 'owl-nav' )][last()]")
            hx.remove_by_xpath(tree, "//div[contains(@id, 'blog-swiper' )]//div[contains(@class, 'owl-nav' )][1]")
            hx.remove_by_xpath(tree, "//div[contains(@id, 'hero-swiper' )]//div[contains(@class, 'owl-nav' )][1]")
            hx.remove_by_xpath(tree, "//div[contains(@id, 'testimonial-swiper' )]//div[contains(@class, 'owl-nav' )][1]")
            hx.remove_by_xpath(tree, "//div[contains(@id, 'theses-swiper' )]//div[contains(@class, 'owl-nav' )][1]")
            
            #---------------------------
            # video/media player
            #---------------------------          
            hx.remove_by_xpath(tree, "//div[contains(@class, 'wp-video' )]")            
            hx.remove_by_xpath(tree, "//div[contains(@class, 'mejs-video' )]")            

            #---------------------------
            # save
            #--------------------------- 
            out_path = file # + "__test.html"
            print("writing:", out_path)
            tree.write(
                out_path, 
                pretty_print=True, 
                xml_declaration=False,   
                encoding="utf-8",   # !!!!
                method='html'       # !!!!
            )
        
    
        # files_index_html = wh.collect_files_endswith(project_folder, ["index.html"])
        # for file in files_index_html:
        #     print("-"*80)
        #     content = wh.string_from_file(file, sanitize=False)
        #     soup    = bs(content)
        #     content = soup.prettify()
        #     print(content)

    #-----------------------------------------
    # b_minify2
    #-----------------------------------------
    if params.get("b_minify2"):
        minify("b_minify2")
       
    #-----------------------------------------
    # export
    #-----------------------------------------
    if params.get("b_export_site"):
        wh.logo("b_export_site")
        
        def _export(func, excludes, target_folder, b_export_site_force):
            
            print("_export:", target_folder)
            print("_export:", "b_export_site_force", b_export_site_force)
            wh.make_dirs(target_folder)
            
            files = wh.collect_files_func(config.project_folder, func=func)
            files = wh.links_remove_excludes(files, excludes)
            files = wh.links_sanitize(files)
            total_size = 0
            
            for file in files:
                
                total_size += os.path.getsize(file)
                
                wp_src  = wh.to_posix(os.path.relpath(file, config.project_folder))
                dst     = wh.add_trailing_slash(target_folder) + wp_src
                
                
                if b_export_site_force or not os.path.isfile(dst):
                    print(".", end='', flush=True)
                    #print("\t", dst)
                    wh.make_dirs(dst)
                    shutil.copy(file, dst)
                    
            print()
            return total_size
                    
        # # # f_unpowered=lambda file : any(file.lower().endswith(ext) for ext in [
        # # #     ".xml", 
        # # #     ".css", 
        # # #     ".js", 
        # # #     config.suffix_compressed + config.target_image_ext, 
        # # #     config.pdf_compression_suffix + ".pdf", 
        # # #     "index.html"
        # # # ])
        
        # remove config.path_exported
        if os.path.isdir(config.folder_exported):
            shutil.rmtree(config.folder_exported)
                
        total_size = _export(
            config.f_unpowered, 
            [], 
            config.folder_exported,
            b_export_site_force=params.get("b_export_site_force")
        )     
        
        ######shutil.copy(config.path_log_params, config.path_exported)       

    #-----------------------------------------
    # 
    #-----------------------------------------
    dir_size_new = wh.get_directory_total_size(config.project_folder)
    print("saved dir_size_new:", wh.vt_saved_percent_string(dir_size_orig, dir_size_new), config.project_folder)
  
    #-----------------------------------------
    # get_project_total_size
    #-----------------------------------------
    wh.logo("get_project_total_size")
    perc100_saved, total_size_originals, total_size_unpowered = wh.get_project_total_size(
        config.project_folder, 
        prefix=config.base_netloc,
        use_pdf=b_get_project_total_size_use_pdf
        )
       
    wh.log(None,                                             filepath=config.path_log_params, echo=True)
    wh.log("perc100_saved       :", perc100_saved,           filepath=config.path_log_params, echo=True)
    wh.log("total_size_originals:", total_size_originals,    filepath=config.path_log_params, echo=True)
    wh.log("total_size_unpowered:", total_size_unpowered,    filepath=config.path_log_params, echo=True)
    #-----------------------------------------
    # 
    #-----------------------------------------   
    print("all done.")
                
    # https://www.thepythoncode.com/article/compress-pdf-files-in-python
    # https://blog.finxter.com/how-to-compress-pdf-files-using-python/
                
                
 