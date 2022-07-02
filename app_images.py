# https://stackoverflow.com/questions/3964681/find-all-files-in-a-directory-with-extension-txt-in-python
""" 
font  s .ttf .woff

<div class="footer-social-links d-flex justify-content-center">
<a href="https://twitter.com/KA_digital" target="_blank" rel="nofollow noopener" class="tgwf_grey"><i class="fab fa-twitter"></i></a><a href="https://www.facebook.com/karlsruhe.digital" target="_blank" rel="nofollow noopener" class="tgwf_green" data-hasqtip="10"><i class="fab fa-facebook-square"></i></a><a href="https://www.instagram.com/karlsruhe.digital/" target="_blank" rel="nofollow noopener" class="tgwf_green" data-hasqtip="11"><i class="fab fa-instagram"></i></a><a href="https://de.linkedin.com/company/karlsruhedigital" target="_blank" rel="nofollow noopener" class="tgwf_grey"><i class="fab fa-linkedin"></i></a><a href="mailto:info@karlsruhe.digital"><i class="fas fa-envelope"></i></a></div>

<i class="fas fa-search"></i>

<div class="owl-nav d-flex justify-content-center align-items-center"><a class="owl-prev d-flex mr-4"><img src="/wp-content/themes/karlsruhe-digital/images/Pfeil_Links.png"></a><span class="swiper-item-number">01</span><a class="owl-next d-flex ml-4"><img src="/wp-content/themes/karlsruhe-digital/images/Pfeil_Rechts.png"></a></div>

<span class="swiper-item-number">01</span>
"""
import glob, os
from posixpath import splitext
from re import X
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


import chromedriver_binary  # pip install chromedriver-binary-auto
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver  # pip install selenium
from selenium.webdriver.chrome.options import Options
#-----------------------------------------
# 
#-----------------------------------------

def image_has_transparency(img):
    if img.info.get("transparency", None) is not None:
        return True
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True

    return False

def image_show(path, secs=1):
    path = os.path.normpath(path)
    #print("image_show:", path)
    assert os.path.isfile(path)
    
    import subprocess
    import time
    # https://www.etcwiki.org/wiki/IrfanView_Command_Line_Options
    p = subprocess.Popen(["C:/Program Files/IrfanView/i_view64.exe", path])
    time.sleep(secs)
    p.kill()
    
    # from PIL import Image
    # img = Image.open(path)
    # img.show()    
    

#-----------------------------------------
# 
#-----------------------------------------
def save_conversions(path_conversions, conversions, mode='w'):
    
    # make unique # remove redundancies    
    prev = load_conversions(path_conversions)
    conversions.extend(prev) 
    conversions = wh.links_make_unique(conversions)
    ################os.remove(path_conversions)
    
    if conversions:    
        print("save_conversions:", wh.YELLOW + path_conversions + wh.RESET)
        with open(path_conversions, mode, encoding="utf-8") as fp:
            for conversion in conversions:
                fr, to = conversion        
                fp.write(fr.strip() +  "," + to.strip() + "\n")    
        print("save_conversions: len(conversions):", len(conversions))
                
def load_conversions(path_conversions):
    
    print("load_conversions:", wh.YELLOW + path_conversions + wh.RESET)
    
    conversions = []
    if os.path.isfile(path_conversions):
        with open(path_conversions, 'r', encoding="utf-8") as fp:
            for line in fp:
                subs = line.split(',')
                if len(subs) >= 2:
                    conversions.append(tuple([subs[0].strip(), subs[1].strip()])) # a tuple
        conversions = wh.links_make_unique(conversions)
            
    print("load_conversions: len(conversions):", len(conversions))
    return conversions


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
    # 
    #-----------------------------------------
    project_folder                          = wh.to_posix(os.path.abspath(config.project_folder))
    path_conversions                        = config.data_folder + config.base_netloc + "_image_conversions.csv"

    b_append_custom_css                     = True
    b_perform_pdf_compression               = False 
    b_perform_image_conversion              = True
    b_convert_list_images_written           = False
    b_convert_all_links_from_lists_to_local = False # make all links to local
    b_perform_replacement_conv  = False
    b_fix_xml_elements                      = False
    b_minify                                = False
     
    # TODO some images have sanitized names like r:xxx --> r_xxx
    # del with warning
    conversions = []
    b_delete_conversion_originals   = False
    if b_delete_conversion_originals:
        if "Cancel" == pag.confirm(text=f"b_delete_conversion_originals: {b_delete_conversion_originals}"):
            exit(0)

    #-----------------------------------------
    # 
    #-----------------------------------------
    dir_size_orig = wh.get_directory_total_size(config.project_folder)

    #-----------------------------------------
    # 
    #-----------------------------------------
    # append css
    if b_append_custom_css:
        with open(config.path_stylesheet, 'a', encoding="utf-8") as outfile:
            with open(config.path_custom_css, 'r', encoding="utf-8") as infile:
                data = infile.read()
                if not config.custom_css_marker in data:
                    wh.logo("b_append_custom_css")
                    outfile.write(data)
                    print("appended custom css to", config.path_stylesheet)
    
    #-----------------------------------------
    # replace via karlsruhe.digital_images_written.csv
    #-----------------------------------------
    if b_convert_all_links_from_lists_to_local:
        wh.logo("b_convert_all_links_from_lists_to_local")
        
        # load ALL lists
        func=lambda file : any(file.lower().endswith(ext) and '_links_' in file.lower() for ext in [".txt"])
        link_files = wh.collect_files_func(config.data_folder, func)        
        print(link_files)

        # read into links
        links = []
        for file in link_files:
            links.extend(wh.list_from_file(file))
            
        links = wh.links_make_unique(links)
        links = wh.links_remove_externals(links, config.base)
        links = wh.links_remove_nones(links)
        links  = sorted(links)
        wh.list_to_file(links, config.data_folder + "__links.txt") 
        #print(*links, sep="\n\t")
        
        tuples = []
        for fr in links:
            to = wh.get_path_local_root_subdomains(fr, config.base, True)  
            tuples.append(tuple([fr.strip(), to.strip()]))  
            
        wh.list_to_file(tuples, config.data_folder + "__tuples.txt") 

        # collect html                
        files = wh.collect_files_endswith(project_folder, [ ".css", ".html" ])
        
        # # # read triples from data\karlsruhe.digital_images_written.csv
        # # with open(config.path_image_tuples_written, "r", encoding="utf-8") as fp:
        # #     lines = fp.read().splitlines() 
        # #     triples = [tuple(line.split(',')) for line in lines]
        # #     print(*triples, sep="\n\t")
        
        # # for file in files:
        # #     wh.replace_all_in_file_tuples(file, triples)
        
        # # # # # with open(config.data_folder + "karlsruhe.digital_links_img.txt", "r", encoding="utf-8") as fp:
        # # # # #     lines = fp.read().splitlines()   
        # # # # #     lines = wh.links_make_unique(lines)
        # # # # #     lines = sorted(lines)
        # # # # #     #print(*lines, sep="\n\t")
            
        # # # # #     tuples = []
        # # # # #     for fr in lines:
        # # # # #         #print("\t", wh.sq(fr))
        # # # # #         to = wh.get_path_local_root_subdomains(fr, config.base, True)  
        # # # # #         tuples.append(tuple([fr, to]))     
            
            
        #print(*tuples, sep="\n\t")
        print(len(tuples), "tuples")
        time.sleep(2)
        
        for i, file in enumerate(files):
            #print()
            wh.progress((i+1)/len(files), verbose_string="replace_all_in_file_tuples", VT=wh.MAGENTA, n=66, prefix="")
            #print()
            replace_all_in_file_tuples(file, tuples)
        pass

    if b_convert_list_images_written:
        wh.logo("b_convert_images_written")
        lines = wh.list_from_file(config.path_image_tuples_written)
        lines = wh.links_sanitize(lines)
        
        def to_duple(line):
            subs = line.split(',')
            assert len(subs) >= 2
            return tuple(subs[:2])
        
        def to_duple_webp(line):
            subs = line.split(',')
            if len(subs) < 2:
                return None
            
            fr = subs[0]
            name, ext = os.path.splitext(subs[1])
            to = wh.get_path_local_root_subdomains(name + config.suffix_compressed + ".webp", config.base)
            return tuple([fr, to])
        
        def to_triple(line):
            subs = line.split(',')
            assert len(subs) >= 3
            return tuple(subs[:3])
        
        tuples = [to_duple_webp(line) for line in lines]
        
        files = wh.collect_files_endswith(project_folder, [ ".css", ".html" ])
        for i, file in enumerate(files):
            #print()
            wh.progress((i+1)/len(files), verbose_string="replace_all_in_file_tuples", VT=wh.MAGENTA, n=66, prefix="")
            #print()
            replace_all_in_file_tuples(file, tuples)    
                
    #-----------------------------------------
    # 
    #-----------------------------------------
    if b_perform_pdf_compression:
        wh.logo("b_perform_pdf_compression")
        import ghostscript as gs

        compression='/screen'
        compression_path = "_" + "cmp_" + compression.lstrip('/')
        #csuffix = config.suffix_compressed + compression_path + ".pdf" # "_unpowered"
        
        pdfs = wh.collect_files_endswith(project_folder, [".pdf"])
        pdfs = [pdf for pdf in pdfs if not compression_path in pdf] # remove already compressed
        print("pdfs", *pdfs, sep="\n\t")
        for i, pdf in enumerate(pdfs):
            
            print("-"*88)
            
            orig_path = pdf
            ##new_path  = pdf + csuffix
            new_path  = orig_path + compression_path + ".pdf"
            
            if not wh.file_exists_and_valid(new_path):
                gs.compress_pdf(orig_path, new_path, compression=compression, res=config.pdf_res)
                
                if wh.file_exists_and_valid(new_path):
                    size_orig = os.path.getsize(orig_path)
                    size_new  = os.path.getsize(new_path)
                    print("\t", "saved:", wh.vt_saved_percent_string(size_orig, size_new), os.path.basename(new_path))
                    
                    if size_new >= size_orig:
                        import shutil
                        shutil.copyfile(orig_path, new_path) # restore original
                        print("\t\t", "copying original:", os.path.basename(orig_path))
                    
                    conversions.append((orig_path, new_path))     
                    print("\t\t", "added to conversions:", os.path.basename(new_path))  
                    
                    # delete conv later
                    # if b_delete_conversion_originals:
                    #     print("\t\t", "removing orig_path:", wh.RED + orig_path, wh.RESET) 
                    #     os.remove(orig_path) 
            else:
                print("already exists:", os.path.basename(new_path))
                            
        ### for />
                 
        if conversions:
            save_conversions(path_conversions, conversions)  
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
        b_force_write   = False
        b_blackwhite    = False
        b_use_palette   = False
        blend_alpha     = 0.7


        if b_force_write and "Cancel" == pag.confirm(text=f"b_force_write: {b_force_write}"):
            exit(0)
            
        image_exts = config.image_exts
        #image_exts = ['.png', '.gif']
        
        print("image_exts   :", image_exts)
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
        images = wh.collect_files_endswith(project_folder, image_exts)
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
                is_transp   = image_has_transparency(image)
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
                    image_show(out_path, secs=0.5)
                
            else:
                print("\t\t", "already exists:", os.path.basename(out_path))
        ### for images />
            
        if images:                                                
            perc_avg /= len(images)  
            perc_avg = round(perc_avg, 1)  
            print("perc_avg:", wh.GREEN + str(perc_avg) + wh.RESET + "%")
    

         #print(*conversions, sep="\n\t")
        if conversions:
            save_conversions(path_conversions, conversions)   
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
        print("\t", wh.GRAY, end='')
        
        fp = open(filename, "r", encoding="utf-8")
        html = fp.read()
        
        # replace
        for i, conversion in enumerate(conversions):
            fr, to = conversion
            
            if wh.file_exists_and_valid(to):    
                
                # rel paths from root /
                wp_fr = wh.to_posix('/' + os.path.relpath(fr, project_folder))
                wp_to = wh.to_posix('/' + os.path.relpath(to, project_folder))
                
                # cnt = html.count(wp_fr)
                # print("\t\t cnt:", cnt, "|", wp_fr)
                
                if not (i%11):
                    #print("\t\t replace:", os.path.basename(fr), wh.CYAN, "with", wh.RESET, os.path.basename(to))    
                    #print("\t\t replaced:", os.path.basename(fr), wh.CYAN, "-->", wh.RESET, wp_to)    
                    #print("\t\t replaced:", wh.CYAN, wp_to, wh.RESET)    
                    print('.', end='')
                
                html = wh.replace_all(html, wp_fr, wp_to) 
                    
            else:
                print("\t\t\t", wh.RED, "does not exist: to:", to, wh.RESET, end='\r')
        ### for conversion />
        
        print(wh.RESET)   
        fp.close()
        
        #open the input file in write mode
        fp = open(filename, "w", encoding="utf-8")
        fp.write(html)
        fp.close()

    #-----------------------------------------
    # 
    #-----------------------------------------
    if b_perform_replacement_conv:
        
        wh.logo("b_perform_replacement_conv")
        
        conversions = load_conversions(path_conversions)    
        #print(*conversions, sep="\n\t")      
                                
        html_files = wh.collect_files_endswith(project_folder, ["index.html", "index_pretty.html", "style.css"])
        for i, html_file in enumerate(html_files):
            #print("\t", "-"*88)
            print("\n"*1)
            wh.progress(i / len(html_files), verbose_string="TOTAL", VT=wh.CYAN, n=80, prefix="\t ")
            print("\n"*1)
            print("\t", i+1, "/", len(html_files), os.path.basename(html_file))
            
            if True:
                replace_all_conversions_in_file(html_file, conversions)
                
            # # whatever is left like /wp-content/themes/karlsruhe-digital/images/Pfeil_Links.png
            # # replace image extensions
            # if True:
            #     conversions_exts = []
            #     for q in ["\"", "\'"]:
            #         for ext in image_exts:
            #             wh.replace_all_in_file(html_file, ext + q, ".webp" + q)
                
             
            # # # # # extras replacements_post   
            # # # # wh.replace_all_in_file(html_file, " srcset=", " XXXsrcset=")
            # # # # wh.replace_all_in_file(html_file, " sizes=", " XXXsizes=")
                                              
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
        

        for file in files_index_html:
            
            print("-"*80)
            print("file", wh.CYAN + file + wh.RESET)
            wp_path     = wh.to_posix('/' + os.path.relpath(file, project_folder))
            base_path   = config.base + wh.to_posix(os.path.relpath(file, project_folder)).replace("index.html", "")
            same_page_link = f"""<a href="{base_path}">{config.base_netloc}</a>"""
            
            if "/en/" in wp_path:
                banner_header_text = f"This is the Low Carbon Website Version of {same_page_link}"
                banner_footer_text = f"Proudly unpowered by {config.html_infossil_link} saving 23 kWh per year. logo. certificate. codex. mission. {config.date_time2}"
            else:
                banner_header_text = f"Dies ist die Low Carbon Website von {same_page_link}"
                banner_footer_text = f"Proudly unpowered by {config.html_infossil_link}. Die Einsparung beträgt 23 kWh pro Jahr. logo. certificate. codex. mission. {config.date_time2}"
                
            tree = lxml.html.parse(file) # lxml.html.fromstring(content)
            
            # start the hocus pocus in focus
            # use section-1 from original site as frag
            if False and False:
                hx.replace_xpath_with_fragment_from_file(
                    tree, 
                    "//section[@id='section-1']", 
                    "data/karlsruhe.digital_fragment_section1.html" # frag_file_path
                )
            
            if True: # +++
                # TODO must be /en/ and not depending on wp_path /en/
                banner_header = hx.banner_header(banner_header_text)
                hx.remove_by_xpath(tree, "//div[@class='banner_header']")
                print("\t adding banner_header")                    
                tree.find(".//header").insert(0, banner_header)    
                
                banner_footer = hx.banner_footer(banner_footer_text)
                hx.remove_by_xpath(tree, "//div[@class='banner_footer']")
                print("\t adding banner_footer")  
                tree.find(".//footer").append(banner_footer) # ".//body"

            # image attributes srcset
            tree = hx.remove_attributes(tree, "img", ["srcset", "sizes", "xxxsrcset", "xxxsizes", "XXXsrcset", "XXXsizes"])

            # remove logo in footer: body > footer > div.footer-top > div > div > div.col-xl-4
            hx.remove_by_xpath(tree, "//div[@class='footer-top']//a[@class='logo']")

            # search in menu
            if True:
                hx.remove_by_xpath(tree, "//li[@id='menu-item-136']") # search in menu
            else:
                #hx.replace_by_xpath(tree, "//i[contains(@class, 'fa-search')]", "<span>SUCHE</span")
                pass

            # all fa font awesome TODO also gets rid of dates etc...
            # hx.remove_by_xpath(tree, "//i[contains(@class, 'fa-')]")

            # <span class="swiper-item-number">6</span>
            # if True:
            #     #hx.remove_by_xpath(tree, "//span[@class='swiper-item-number']")
            #     hx.remove_by_xpath(tree, "//div[@id='hero-swiper']//span[@class='swiper-item-number']")
            #     hx.remove_by_xpath(tree, "//div[@id='hero-swiper']//span[@class='color-white']")
            
            
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
            
            # twitter feeds
            hx.remove_by_xpath(tree, "//section[contains(@class,'social-media-feed')]")
            
            # social media footer
            footer_social_html = """
            <div id="unpowered-social-media-footer">
                <a href="https://twitter.com/KA_digital" rel="nofollow noopener" target="_blank" class="tgwf_grey">
                twitter
                </a>
                <a href="https://www.facebook.com/karlsruhe.digital" rel="nofollow noopener" target="_blank" class="tgwf_green" data-hasqtip="8" aria-describedby="qtip-8">
                facebook
                </a>
                <a href="https://www.instagram.com/karlsruhe.digital/" rel="nofollow noopener" target="_blank" class="tgwf_green" data-hasqtip="9">
                instagram
                </a>
                <a href="https://de.linkedin.com/company/karlsruhedigital" rel="nofollow noopener" target="_blank" class="tgwf_grey">
                linkedin
                </a>
                <a href="mailto:info@karlsruhe.digital">
                mail
                </a>
            </div>
            """
            hx.replace_xpath_with_fragment(tree, "//div[contains(@class, 'footer-bottom' )]//div[contains(@class, 'footer-social-links' )]", footer_social_html)
            hx.replace_xpath_with_fragment(tree, "//div[@id='unpowered-social-media-footer']", footer_social_html)

            # swipers
            # //div[contains(@id, 'blog-swiper' )]//div[contains(@class, 'owl-nav' )][last()]
            ###hx.remove_by_xpath(tree, "//div[contains(@id, 'blog-swiper' )]//div[contains(@class, 'owl-nav' )][last()]")
            hx.remove_by_xpath(tree, "//div[contains(@id, 'blog-swiper' )]//div[contains(@class, 'owl-nav' )][1]")
            hx.remove_by_xpath(tree, "//div[contains(@id, 'hero-swiper' )]//div[contains(@class, 'owl-nav' )][1]")
            hx.remove_by_xpath(tree, "//div[contains(@id, 'testimonial-swiper' )]//div[contains(@class, 'owl-nav' )][1]")
            hx.remove_by_xpath(tree, "//div[contains(@id, 'theses-swiper' )]//div[contains(@class, 'owl-nav' )][1]")
            
            

            # save to html
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
        conversions = load_conversions(path_conversions)    
        
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
    # 
    #-----------------------------------------
    wh.get_project_total_size(config.project_folder)

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