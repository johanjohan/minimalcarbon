# https://stackoverflow.com/questions/3964681/find-all-files-in-a-directory-with-extension-txt-in-python
""" 


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
#-----------------------------------------
# 
#-----------------------------------------


#-----------------------------------------
# 
#-----------------------------------------
def replace_all_in_file_tuples(filename, tuples):
    
    #print("replace_all_in_file_tuples:", filename)
    
    with open(filename, "r", encoding="utf-8") as fp:
        data = fp.read()
         
    for conversion in tuples:
        #print(YELLOW, conversion, RESET)
        fr, to = conversion
        
        fr = fr.strip()
        to = to.strip()
        print("replace_all_in_file_tuples: fr to", fr, to)
        
        name, ext = os.path.splitext(to)
        print("replace_all_in_file_tuples: name ext", name, ext)
        # assert name, "no name"
        # assert ext, "no ext"
        
        if ext in config.image_exts:
            to = wh.get_path_local_root_subdomains(name + config.suffix_compressed + ".webp", config.base)
        else:
            to = wh.get_path_local_root_subdomains(to, config.base)
        
        return tuple([fr, to])
        
        #print(YELLOW, fr, CYAN, "-->", YELLOW, to, RESET)
        
        data = replace_all(data, dq(fr), dq(to)) 
        data = replace_all(data, sq(fr), sq(to)) 
        data = replace_all(data, pa(fr), pa(to)) 
        #data = replace_all(data, fr, to) # ?????
    
    with open(filename, "w", encoding="utf-8") as fp:
        fp.write(data)
            
            
#-----------------------------------------
# 
#-----------------------------------------
if __name__ == "__main__":
    
    wh.logo_filename(__file__)
    
    #pag.alert(text=f"good time to backup htdocs!")
    #-----------------------------------------
    # get sizes
    #-----------------------------------------    
    perc100_saved, total_size_originals, total_size_unpowered = wh.get_project_total_size(config.project_folder)
                
    #-----------------------------------------
    # 
    #-----------------------------------------
    project_folder                      = wh.to_posix(os.path.abspath(config.project_folder))
    path_conversions                    = config.data_folder + config.base_netloc + "_conversions.csv"

    b_append_custom_css                 = False
    b_append_custom_script              = True
    b_remove_fonts_css                  = True
    
    b_perform_pdf_compression           = True 
    b_perform_image_conversion          = True
    b_perform_image_conversion_force        = False
    
    b_replace_conversions               = False
    b_fix_xml_elements                  = True
    b_hide_media_subdomain                  = True
    b_minify                            = True
    b_export_site                       = True 
        
    ###b_convert_list_images_written           = False
    ###b_convert_all_links_from_lists_to_local = False # make all links to local
    

    # TODO some images have sanitized names like r:xxx --> r_xxx
    # del with warning
    conversions = []
    b_delete_conversion_originals   = False
    if b_delete_conversion_originals:
        if "Cancel" == pag.confirm(text=f"b_delete_conversion_originals: {b_delete_conversion_originals}"):
            exit(0)
            
    # # if os.path.isfile(path_conversions):
    # #     os.remove(path_conversions)
    #-----------------------------------------
    # dir_size_orig
    #-----------------------------------------
    dir_size_orig = wh.get_directory_total_size(config.project_folder)

    #-----------------------------------------
    # copy icons
    #-----------------------------------------
    hw.make_dirs(config.path_dst_icons)
    shutil.copytree(config.path_src_icons, config.path_dst_icons, dirs_exist_ok=True)

    #-----------------------------------------
    # b_append_custom_css
    #-----------------------------------------
    # append css before fonts will be replaced after
    if b_append_custom_css:
        wh.logo("b_append_custom_css")
        data_stylesheet = wh.string_from_file(config.path_stylesheet)
        print("count:", data_stylesheet.count(config.custom_css_marker))
        data_stylesheet = data_stylesheet.split(config.custom_css_marker)[0]
        data_stylesheet += wh.string_from_file(config.path_custom_css)
        wh.string_to_file(data_stylesheet, config.path_stylesheet)
        print("appended custom css to", config.path_stylesheet)
        print("count:", data_stylesheet.count(config.custom_css_marker))
        
    #-----------------------------------------
    # b_append_custom_script
    #-----------------------------------------
    if b_append_custom_script:
        wh.logo("b_append_custom_script")
        if config.path_new_script:
            shutil.copy(config.path_new_script, config.path_script)
            print("copied", config.path_new_script, "to", config.path_script)
    
    #-----------------------------------------
    # fonts
    #-----------------------------------------
    if b_remove_fonts_css:
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
        files = wh.collect_files_endswith(project_folder, [".css"])
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
        conv.save(path_conversions, conversions)  
            
        #-----------------------------------------
        # replace fonts in tag styles   
        #-----------------------------------------  
        files = wh.collect_files_endswith(project_folder, ["index.htm","index.html"])
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
        conv.save(path_conversions, conversions)  
        
          
        
    # # # # # #-----------------------------------------
    # # # # # # replace via karlsruhe.digital_images_written.csv
    # # # # # #-----------------------------------------
    # # # # # if b_convert_all_links_from_lists_to_local:
    # # # # #     wh.logo("b_convert_all_links_from_lists_to_local")
        
    # # # # #     # load ALL lists
    # # # # #     func=lambda file : any(file.lower().endswith(ext) and '_links_' in file.lower() for ext in [".txt"])
    # # # # #     link_files = wh.collect_files_func(config.data_folder, func)        
    # # # # #     print(link_files)

    # # # # #     # read into links
    # # # # #     links = []
    # # # # #     for file in link_files:
    # # # # #         links.extend(wh.list_from_file(file))
            
    # # # # #     links = wh.links_make_unique(links)
    # # # # #     links = wh.links_remove_externals(links, config.base)
    # # # # #     links = wh.links_remove_nones(links)
    # # # # #     links  = sorted(links)
    # # # # #     wh.list_to_file(links, config.data_folder + "__links.txt") 
    # # # # #     #print(*links, sep="\n\t")
        
    # # # # #     tuples = []
    # # # # #     for fr in links:
    # # # # #         to = wh.get_path_local_root_subdomains(fr, config.base, True)  
    # # # # #         tuples.append(tuple([fr.strip(), to.strip()]))  
            
    # # # # #     wh.list_to_file(tuples, config.data_folder + "__tuples.txt") 

    # # # # #     # collect html                
    # # # # #     files = wh.collect_files_endswith(project_folder, [ ".css", ".html" ])
        
    # # # # #     # # # read triples from data\karlsruhe.digital_images_written.csv
    # # # # #     # # with open(config.path_image_tuples_written, "r", encoding="utf-8") as fp:
    # # # # #     # #     lines = fp.read().splitlines() 
    # # # # #     # #     triples = [tuple(line.split(',')) for line in lines]
    # # # # #     # #     print(*triples, sep="\n\t")
        
    # # # # #     # # for file in files:
    # # # # #     # #     wh.replace_all_in_file_tuples(file, triples)
        
    # # # # #     # # # # # with open(config.data_folder + "karlsruhe.digital_links_img.txt", "r", encoding="utf-8") as fp:
    # # # # #     # # # # #     lines = fp.read().splitlines()   
    # # # # #     # # # # #     lines = wh.links_make_unique(lines)
    # # # # #     # # # # #     lines = sorted(lines)
    # # # # #     # # # # #     #print(*lines, sep="\n\t")
            
    # # # # #     # # # # #     tuples = []
    # # # # #     # # # # #     for fr in lines:
    # # # # #     # # # # #         #print("\t", wh.sq(fr))
    # # # # #     # # # # #         to = wh.get_path_local_root_subdomains(fr, config.base, True)  
    # # # # #     # # # # #         tuples.append(tuple([fr, to]))     
            
            
    # # # # #     #print(*tuples, sep="\n\t")
    # # # # #     print(len(tuples), "tuples")
    # # # # #     time.sleep(2)
        
    # # # # #     for i, file in enumerate(files):
    # # # # #         #print()
    # # # # #         wh.progress((i+1)/len(files), verbose_string="replace_all_in_file_tuples", VT=wh.MAGENTA, n=66, prefix="")
    # # # # #         #print()
    # # # # #         replace_all_in_file_tuples(file, tuples)
    # # # # #     pass


                
    #-----------------------------------------
    # 
    #-----------------------------------------



    # # # if b_convert_list_images_written:
    # # #     wh.logo("b_convert_images_written")
    # # #     lines = wh.list_from_file(config.path_image_tuples_written)
    # # #     lines = wh.links_sanitize(lines)
        
    # # #     def to_duple(line):
    # # #         subs = line.split(',')
    # # #         assert len(subs) >= 2
    # # #         return tuple(subs[:2])
        
    # # #     def to_duple_webp(line):
    # # #         subs = line.split(',')
    # # #         if len(subs) < 2:
    # # #             return None
            
    # # #         fr = subs[0]
    # # #         name, ext = os.path.splitext(subs[1])
    # # #         to = wh.get_path_local_root_subdomains(name + config.suffix_compressed + ".webp", config.base)
    # # #         return tuple([fr, to])
        
    # # #     def to_triple(line):
    # # #         subs = line.split(',')
    # # #         assert len(subs) >= 3
    # # #         return tuple(subs[:3])
        
    # # #     tuples = [to_duple_webp(line) for line in lines]
    # # #     print(*tuples, sep="\n\t")
    # # #     exit(0)
        
    # # #     files = wh.collect_files_endswith(project_folder, [ ".css", ".html" ])
    # # #     for i, file in enumerate(files):
    # # #         #print()
    # # #         wh.progress((i+1)/len(files), verbose_string="replace_all_in_file_tuples", VT=wh.MAGENTA, n=66, prefix="")
    # # #         #print()
    # # #         replace_all_in_file_tuples(file, tuples)    
                
    #-----------------------------------------
    # 
    #-----------------------------------------
    if b_perform_pdf_compression:
        wh.logo("b_perform_pdf_compression")
        import ghostscript as gs
        
        pdfs = wh.collect_files_endswith(project_folder, [".pdf"])
        pdfs = [pdf for pdf in pdfs if not config.pdf_compression_suffix in pdf] # remove already compressed
        print("pdfs", *pdfs, sep="\n\t")
        for i, pdf in enumerate(pdfs):
            
            print("-"*88)
            
            orig_path = pdf
            name, ext = os.path.splitext(orig_path)
            new_path  = name + config.pdf_compression_suffix + ext
            
            conversions.append((orig_path, new_path))     
            print("\t\t", "added to conversions:", os.path.basename(new_path)) 
                                
            if not wh.file_exists_and_valid(new_path):
                gs.compress_pdf(orig_path, new_path, compression=config.pdf_compression, res=config.pdf_res)
                
                if wh.file_exists_and_valid(new_path):
                    size_orig = os.path.getsize(orig_path)
                    size_new  = os.path.getsize(new_path)
                    print("\t", "saved:", wh.vt_saved_percent_string(size_orig, size_new), os.path.basename(new_path))
                    
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
                 
        conv.save(path_conversions, conversions)  
    ### b_perform_pdf_compression />   

    #-----------------------------------------
    # 
    #-----------------------------------------
    if b_perform_image_conversion:   
        
        wh.logo("b_perform_image_conversion")
        
        # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#webp
        quality         = 66 # 66
        max_dim         = (1000, 1000) # (1280, 720) # (1200, 600)
        show_nth_image  = 30 # 0 is off, 1 all
        resample        = Image.Resampling.LANCZOS
        halftone        = None # (4, 30) # or None
        b_colorize      = True
        b_force_write   = b_perform_image_conversion_force
        b_blackwhite    = False
        b_use_palette   = False
        blend_alpha     = 0.666


        if b_force_write and "Cancel" == pag.confirm(text=f"b_force_write: {b_force_write}", timeout=10):
            exit(0)
            
        print("image_exts   :", config.image_exts)
        print("quality      :", quality)
        print("max_dim      :", max_dim)
        print("b_force_write:", b_force_write)
        print("b_colorize   :", b_colorize)
        print("halftone     :", halftone)
        print("b_use_palette:", b_use_palette)
        print("blend_alpha  :", blend_alpha)
        
        #-----------------------------------------
        # 
        #-----------------------------------------
        images = wh.collect_files_endswith(project_folder, config.image_exts)
        # # # # # # # func=lambda file : any(file.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif", ".svg"])
        # # # # # # # images = wh.collect_files_func(project_folder, func)
        
        # # # remove compressed
        # # images_no_compressed = [img for img in images if not config.suffix_compressed in img]
        # # removed = [item for item in images if item not in images_no_compressed]
        # # print("removed", hw.GRAY, *removed, hw.RESET, sep = "\n\t")
        # # print("images",  hw.GRAY, *images, hw.RESET, sep = "\n\t")
        
        
        images = [img for img in images if not config.suffix_compressed in img]
        print("images",  hw.GRAY, *images, hw.RESET, sep = "\n\t")
                     
        # convert images
        perc_avg = 0.0
        for cnt, path in enumerate(images):
            
            print("-"*88)
            path        = os.path.normpath(path) # wh.to_posix(path)
            name, ext   = os.path.splitext(path) # ('my_file', '.txt')
            out_path    = name + config.suffix_compressed + '.webp' 
            out_path    = os.path.normpath(out_path) # wh.to_posix(out_path)
            
            conversions.append((path, out_path))
                        
            if b_force_write or not wh.file_exists_and_valid(out_path):
            
                print("\t", "{}/{}:".format(cnt+1, len(images)), os.path.basename(path))
                print("\t\t", wh.progress_string(cnt / len(images), verbose_string="", VT=wh.CYAN, n=33))
                
                size_orig = os.path.getsize(path)
                image = Image.open(path)
                is_transp   = wh.image_has_transparency(image)
                #image       = image.convert('RGBA' if is_transp else 'RGB')
                wh_orig = image.size
                
                print("\t\t", "is_transp:", is_transp)
                print("\t\t", "mode     :", image.mode)
                print("\t\t", "size     :", image.size)
                
                if False:
                    w, h = image.size
                    print("\t\t", "size:", image.size)
                    assert h > 0 and w > 0
                    if w > max_dim[0] or h > max_dim[1]:
                        if w >= h:
                            image = image.resize((max_dim[0], round(h / w * max_dim[0])), resample=resample)
                        else:
                            image = image.resize((round(w / h * max_dim[1]), max_dim[1]), resample=resample)
                        print("\t\t", "new :", image.size)
                else:   
                    image.thumbnail(max_dim, resample=resample)
                    image_orig = image.copy()
                    #image_orig  = ImageOps.autocontrast(image_orig.convert("RGB"))
                            
                if halftone and not is_transp:
                    image = image.convert("L")
                    image = ht.halftone(image, ht.euclid_dot(spacing=halftone[0], angle=halftone[1]))
                    assert isinstance(image, PIL.Image.Image)
                
                if b_colorize and not is_transp: 
                    image = image.convert("L") # L only !!! # LA L 1
                    black = "#003300"
                    black = "#002200"
                    #black = "#001733"
                    white = "#eeeeee"
                    white = "#ffffff"
                    image = ImageOps.colorize(image, black=black, white=white)
                    ####image = ImageOps.autocontrast(image)
                    
                # blend
                if (not is_transp) and( blend_alpha < 1.0): 
                    ###assert image.mode == image_orig.mode
                    image = Image.blend(
                        image_orig.convert("RGB"), 
                        image.convert("RGB"), 
                        blend_alpha
                    )
                    
                if b_blackwhite:
                    if is_transp:
                        image = image.convert("LA")
                    else:
                        image = image.convert("L")
                        
                if b_use_palette:
                    if is_transp:
                        image = image.convert("PA")
                    else:
                        image = image.convert("P")
                    
                ###image = image.convert(rgb_mode)
                    
                if is_transp:
                    image.save(out_path, 'webp', optimize=True, lossless=True) # !!!
                else:
                    image.save(out_path, 'webp', optimize=True, quality=quality) 
                # print("\t\t", "is_transp:", is_transp)
                # print("\t\t", "mode     :", image.mode)
                print("\t\t", "quality  :", quality)
                print("\t\t", "wh       :", wh_orig, "-->", image.size, "| max_dim:", max_dim)
                
                size_new = os.path.getsize(out_path)
                print("\t\t", "saved  :", wh.vt_saved_percent_string(size_orig, size_new), os.path.basename(out_path))
                perc_avg += wh._saved_percent(size_orig, size_new)
                
                if show_nth_image > 0 and not (cnt%show_nth_image):
                    wh.image_show(out_path, secs=0.5)
                
            else:
                print("\t\t", "already exists:", os.path.basename(out_path))
        ### for images />
            
        if images:                                                
            perc_avg /= len(images)  
            perc_avg = round(perc_avg, 1)  
            print("perc_avg:", wh.GREEN + str(perc_avg) + wh.RESET + "%")
    

         #print(*conversions, sep="\n\t")
        if conversions:
            conv.save(path_conversions, conversions)   
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
        
        fp = open(filename, "r", encoding="utf-8")
        html = fp.read()
        
        # replace
        #print("\t\t", end='')
        for i, conversion in enumerate(conversions):
            fr, to = conversion
            
            if wh.file_exists_and_valid(to):    
                
                # rel paths from root /
                wp_fr = wh.to_posix('/' + os.path.relpath(fr, project_folder))
                wp_to = wh.to_posix('/' + os.path.relpath(to, project_folder))
                
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
                    
                    # NEW try all TODO with quotes
                    for f in [ wh.dq,  wh.sq,  wh.pa,  wh.qu]:
                        #print(f"{ wh.GRAY}\t\t\t replace_all: {f(wp_fr)} {wh.RESET}") 
                        html = wh.replace_all(html,  f(wp_fr),  f(wp_to) )
            
                    # # # # html = wh.replace_all(html,  wh.sq(wp_fr),  wh.sq(wp_to) ) 
                    # # # # html = wh.replace_all(html,  wh.dq(wp_fr),  wh.dq(wp_to) )
                    # # # # html = wh.replace_all(html,  wh.pa(wp_fr),  wh.pa(wp_to) )
                    # # # # html = wh.replace_all(html,  wh.qu(wp_fr),  wh.qu(wp_to) ) # &quot;https:\/\/media.karlsruhe.digital\/storage\/thumbs\/1920x\/r:1644340878\/659.jpg&quot;
                    
            else:
                print("\t\t\t", wh.RED, "does not exist: to:", to, wh.RESET, end='\r')
        ### for conversion />
        
        fp.close()
        
        #open the input file in write mode
        fp = open(filename, "w", encoding="utf-8")
        fp.write(html)
        fp.close()

    #-----------------------------------------
    # 
    #-----------------------------------------
    if b_replace_conversions:
        
        wh.logo("b_replace_conversions")
        
        conversions = conv.load(path_conversions)    
        #print(*conversions, sep="\n\t")     
                                
        html_files = wh.collect_files_endswith(project_folder, ["index.html", ".css"])
        for i, html_file in enumerate(html_files):
            #print("\t", "-"*88)
            ###print("\n"*1)
            verbose_string = f"\t {i+1}/{len(html_files)} {os.path.basename(html_file)}"
            wh.progress(i / len(html_files), verbose_string=verbose_string, VT=wh.CYAN, n=80, prefix="")
            ###print("\n"*1)
            ###print("\t", i+1, "/", len(html_files), os.path.basename(html_file))
            
            replace_all_conversions_in_file(html_file, conversions)
                
            # whatever is left like /wp-content/themes/karlsruhe-digital/images/Pfeil_Links.png
            # replace image extensions
            for q in ["\"", "\'"]:
                for ext in config.image_exts_no_webp:
                    wh.replace_all_in_file(html_file, ext + q, ".webp" + q)
                
             

                                              
        ### for /> 
    ### b_perform_replacement />            
            
                
    #-----------------------------------------
    # b_fix_xml
    #-----------------------------------------
    if b_fix_xml_elements:
        wh.logo("b_fix_xml_elements")
        
        func=lambda s : True # finds all
        func=lambda file : any(file.lower().endswith(ext) for ext in config.image_exts)
        func=lambda file : file.lower().endswith("index.html")
        files_index_html = wh.collect_files_func(project_folder, func=func)
        #print(*files_index_html, sep="\n\t")
        
        color = "darkseagreen"
        svg_percircle = f"""<div class="percircle"><svg viewBox="0 0 500 500" role="img" xmlns="http://www.w3.org/2000/svg">
            <g id="myid">
                <circle stroke="{color}"
                        stroke-width="30px"
                        fill="none"
                        cx="250"
                        cy="250"
                        r="222" />
                <text style="font: bold 12rem sans-serif;"
                    text-anchor="middle"
                    dominant-baseline="central"
                    x="50%"
                    y="50%"
                    fill="{color}">{perc100_saved:.0f}%</text> 
            </g>     
        </svg></div>"""


        for file in files_index_html:
            
            print("-"*80)
            print("file", wh.CYAN + file + wh.RESET)
            wp_path     = wh.to_posix('/' + os.path.relpath(file, project_folder))
            base_path   = config.base + wh.to_posix(os.path.relpath(file, project_folder)).replace("index.html", "")
            same_page_link = f"""<a href="{base_path}">{config.base_netloc}</a>"""
            
            """
            Dies ist die energie-effiziente
            energie optimierte 
            Dies ist die Low Carbon Website
            Dies ist die Low Carbon Website
            This is the environmentally aware version of 
            Dies ist die umweltbewusste Seite
            This is the environmentally friendly twin of 
            """
            # https://babel.pocoo.org/en/latest/dates.html
            from babel.dates import format_date, format_datetime, format_time
            dt = config.date_time_now
            format='full' # long
            saved_string = f"<span style=''>{perc100_saved:.1f}%</span>"
            if "/en/" in wp_path:
                dt_string = format_date(dt, format=format, locale='en')
                banner_header_text = f"This is the Low Carbon version of {same_page_link}.<br/>The energy consumption of this website was reduced by {saved_string}." # <br/>{svg_percircle}
                banner_footer_text = f"unpowered by {config.html_infossil_link}<br/>{svg_percircle}" # <br/>{dt_string}
            else:
                dt_string = format_date(dt, format=format, locale='de_DE')
                banner_header_text = f"Dies ist die Low Carbon Website von {same_page_link}.<br/>Der Energieverbrauch dieser Website wurde um {saved_string} reduziert."
                banner_footer_text = f"unpowered by {config.html_infossil_link}<br/>{svg_percircle}" # <br/>{dt_string}
                
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
            
            if b_hide_media_subdomain:
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
            # twitter feeds
            #---------------------------   
            hx.remove_by_xpath(tree, "//section[contains(@class,'social-media-feed')]")
            
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
    # 
    #-----------------------------------------
    if b_delete_conversion_originals:
        wh.logo("b_delete_conversion_originals")
        conversions = conv.load(path_conversions)    
        
        for conversion in conversions:
            fr_to_delete, __to = conversion
            if wh.file_exists_and_valid(fr_to_delete):
                print("\t", wh.RED, "removing:", os.path.basename(fr_to_delete), wh.RESET)
                os.remove(fr_to_delete)
                
    #-----------------------------------------
    # minify
    #-----------------------------------------
    if b_minify:
        wh.logo("b_minify")
        for file in wh.collect_files_endswith(config.project_folder, ["index.html"]):
            wh.minify_on_disk(file)
                
    #-----------------------------------------
    # 
    #-----------------------------------------
    dir_size_new = wh.get_directory_total_size(config.project_folder)
    print("saved dir_size_new:", wh.vt_saved_percent_string(dir_size_orig, dir_size_new), config.project_folder)
  
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
        sitemap.sitemap_xml_from_list(urls, out_xml_path=config.project_folder+'sitemap.xml')
     
    # rm  xmlrpc.ph   
    xmlrpc_path = config.project_folder+"xmlrpc.php"
    if os.path.isfile(xmlrpc_path):
        os.remove(xmlrpc_path)

    #-----------------------------------------
    # export
    #-----------------------------------------
   
    if b_export_site:
        wh.logo("b_export_site")
        
        force_write = False
        
        def _export(func, excludes, target_folder, force_write):
            
            print("_export:", target_folder)
            print("_export:", "force_write", force_write)
            wh.make_dirs(target_folder)
            
            files = wh.collect_files_func(config.project_folder, func=func)
            files = wh.links_remove_excludes(files, excludes)
            files = wh.links_sanitize(files)
            total_size = 0
            
            for file in files:
                
                total_size += os.path.getsize(file)
                
                wp_src  = wh.to_posix(os.path.relpath(file, config.project_folder))
                dst     = wh.add_trailing_slash(target_folder) + wp_src
                
                
                if force_write or not os.path.isfile(dst):
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
        # # #     config.suffix_compressed + ".webp", 
        # # #     config.pdf_compression_suffix + ".pdf", 
        # # #     "index.html"
        # # # ])
        
        total_size = _export(
            config.f_unpowered, 
            [], 
            config.project_folder + "../__exported/",
            force_write=force_write
        )            
    #-----------------------------------------
    # 
    #-----------------------------------------
    wh.logo("GREEN4matics")
    perc100_saved, total_size_originals, total_size_unpowered = wh.get_project_total_size(config.project_folder)

    #-----------------------------------------
    # 
    #-----------------------------------------   
    print("all done.")
                
    # https://www.thepythoncode.com/article/compress-pdf-files-in-python
    # https://blog.finxter.com/how-to-compress-pdf-files-using-python/
                
                
                
""" 
        # # options=config.options
        # # options.headless = False
        # # driver = webdriver.Chrome(options=options)
        # # driver.implicitly_wait(30)    

        for file in files_index_html:
            
            print("-"*80)
            
            tree = lxml.html.parse(file)
            #tree = lxml.html.fromstring(content)

            tree = hx.remove_attributes(tree, "img", ["srcset", "xxxsrcset", "sizes", "xxxsizes"])
        
            out_path = file + "_srcset.html"
            print("writing:", out_path)
            tree.write(out_path, pretty_print=True)
            
            # img_sizes = h.xpath('//img[@sizes or @xxxsizes]') 
            # print(img_sizes)

            # # # # # # # # # driver.get("file:///" + file)
            # # # # # # # # # wh.wait_for_page_has_loaded(driver)
            # # # # # # # # # content = driver.page_source
            
            # # # # # # # # # time.sleep(3)
            
            # # # # # # # # # #elements = driver.find_elements(By.TAG_NAME, "img")
            
            # # # # # # # # # #elements = driver.find_elements(By.XPATH, "//img[@srcset]")
            # # # # # # # # # elements = driver.find_elements(By.XPATH, "//img")
            # # # # # # # # # for element in elements:
            # # # # # # # # #     print("\t", element.tag_name, element.text)
            # # # # # # # # #     driver.execute_script("arguments[0].remove();", element)
                
            # # # # # # # # # driver.execute_script(
            # # # # # # # # #     ""
            # # # # # # # # #     var element = document.getElementById("Ebene_1");
            # # # # # # # # #     element.parentNode.removeChild(element);
            # # # # # # # # #     ""
            # # # # # # # # # )

                
            # # # # # # # # # #driver.refresh()
            # # # # # # # # # for i in range(7):
            # # # # # # # # #     time.sleep(1)
            # # # # # # # # #     print('.', end='', flush=True)
                
            # # # # content = wh.string_from_file(file, sanitize=False)
            # # # soup    = bs(content, "html.parser")
            # # # #content = soup.prettify()
            # # # for data in soup(['style', 'script']):
            # # #     # Remove tags
            # # #     print("\t", data)
            # # #     data.decompose()

            # # # # return data by retrieving the tag content
            # # # #content = ' '.join(soup.stripped_strings)        
            
            # # # #print(content)    
        
            # # # driver.get("data:text/html;charset=utf-8," + content)
            # # # wh.wait_for_page_has_loaded(driver)
            
            # # # for i in range(30):
            # # #     time.sleep(1)
            # # #     print('.', end='', flush=True)
                    
                    
        #print(*files_index_html, sep="\n\t")
        # 
        # 
        
        # driver.close()
        # driver.quit()
        
        
"""