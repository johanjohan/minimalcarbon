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
from re import X
import PIL
from PIL import Image, ImageOps
import halftone as ht # https://pypi.org/project/halftone/

import config
import helpers_web as wh
import time
import pathlib
import pyautogui as pag
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

def saved_percent(size_orig, size_new):
    assert size_orig > 0
    perc = 100 - (size_new/size_orig*100)
    return perc

def saved_percent_string(size_orig, size_new):
    pct = saved_percent(size_orig, size_new)
    vt  = wh.RED if pct <= 0 else wh.GREEN
    return "{}{:+.1f}%{}".format(vt, pct, wh.RESET)
#-----------------------------------------
# 
#-----------------------------------------
def save_conversions(path_conversions, conversions, mode='w'):
    
    # make unique
    conversions.extend(load_conversions(path_conversions))
    conversions = list(set(conversions)) # unique
    
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
    with open(path_conversions, 'r', encoding="utf-8") as fp:
        for line in fp:
            subs = line.split(',')
            conversions.append((subs[0].strip(), subs[1].strip()))
            
    print("load_conversions: len(conversions):", len(conversions))
    conversions = list(set(conversions)) # unique
    print("load_conversions: unique len(conversions):", len(conversions))
    return conversions

#-----------------------------------------
# 
#-----------------------------------------
def to_posix(filepath):
    return pathlib.Path(filepath).as_posix()
 
def get_size(start_path):
    print("get_size:", wh.CYAN, start_path, wh.RESET)
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    print("get_size: total_size:", round(total_size / (1024*1024), 1), "MB")
    return total_size
           
#-----------------------------------------
# 
#-----------------------------------------
if __name__ == "__main__":
    
    project_folder              = to_posix(os.path.abspath(config.project_folder))
    path_conversions            = config.data_folder + config.base_netloc + "_image_conversions.csv"

    b_perform_conversion        = True
    b_perform_pdf_compression   = b_perform_conversion
    b_perform_replacement       = True
     
    b_delete_originals          = False
        
    if b_delete_originals:
        if "Cancel" == pag.confirm(text=f"b_delete_originals: {b_delete_originals}"):
            exit(0)

    conversions = []
    
    #-----------------------------------------
    # 
    #-----------------------------------------
    dir_size_orig = get_size(config.project_folder)
            
    #-----------------------------------------
    # 
    #-----------------------------------------
    if b_perform_pdf_compression:
        import ghostscript as gs
        csuffix = "_compressed.pdf"
        
        pdfs = wh.collect_files_endswith(project_folder, [".pdf"])
        pdfs = [pdf for pdf in pdfs if not csuffix in pdf] # no compressed files
        #print("pdfs", *pdfs, sep="\n\t")
        for i, pdf in enumerate(pdfs):
            
            print("-"*88)
            
            orig_path = pdf
            new_path  = pdf + csuffix
            
            if not wh.file_exists_and_valid(new_path):
                gs.compress_pdf(orig_path, new_path, res=config.pdf_res)
                
            if wh.file_exists_and_valid(new_path):
                size_orig = os.path.getsize(orig_path)
                size_new  = os.path.getsize(new_path)
                print("\t", "saved:", saved_percent_string(size_orig, size_new), os.path.basename(new_path))
                if size_new < size_orig:
                    conversions.append((orig_path, new_path))     
                    print("\t\t", "added to conversions.")           
                
        ### for />
                 
        if conversions:
            save_conversions(path_conversions, conversions)  
    ### b_perform_pdf_compression />   

    #-----------------------------------------
    # 
    #-----------------------------------------
    if b_perform_conversion:   
        
        # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#webp
        quality         = 50 # 66
        max_dim         = (1000, 1000) # (1280, 720) # (1200, 600)
        show_nth_image  = 11 # 0 is off, 1 all
        resample        = Image.Resampling.LANCZOS
        b_colorize      = True
        halftone        = None # (4, 30) # or None
        b_force_write   = True
        b_blackwhite    = False
        b_use_palette   = False
        blend_alpha     = 0.9
        
        image_exts = ['.jpg', '.jpeg', '.png', '.gif']
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
                     
        # convert images
        
        perc_avg = 0.0
        for cnt, path in enumerate(images):
            
            print("-"*88)
            path        = os.path.normpath(path) # to_posix(path)
            name, ext   = os.path.splitext(path) # ('my_file', '.txt')
            out_path    = name + '.webp' 
            out_path    = os.path.normpath(out_path) # to_posix(out_path)
            
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
                    image = ImageOps.colorize(image, black=black, white="#eeeeee")
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
                print("\t\t", "saved  :", saved_percent_string(size_orig, size_new), os.path.basename(out_path))
                perc_avg += saved_percent(size_orig, size_new)
                
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
    ### b_perform_conversion />

    #-----------------------------------------
    # better use a list in case above finds no more erased images....
    # TODO need to create /wp paths from these images...rel to project folder and using / 
    # https://www.geeksforgeeks.org/python-os-path-relpath-method/
    #-----------------------------------------
    #-----------------------------------------
    # 
    #-----------------------------------------
    
    def replace_all_conversions_in_file(filename, conversions):
        
        print("\t", "replace_all_conversions_in_file:", wh.CYAN, filename, wh.RESET)
        print("\t", wh.GRAY, end='')
        
        fp = open(filename, "r", encoding="utf-8")
        html = fp.read()
        
        # replace
        for i, conversion in enumerate(conversions):
            fr, to = conversion
            
            if wh.file_exists_and_valid(to):    
                
                # rel paths from root /
                wp_fr = to_posix('/' + os.path.relpath(fr, project_folder))
                wp_to = to_posix('/' + os.path.relpath(to, project_folder))
                
                # cnt = html.count(wp_fr)
                # print("\t\t cnt:", cnt, "|", wp_fr)
                
                if False and not (i%11):
                    #print("\t\t replace:", os.path.basename(fr), wh.CYAN, "with", wh.RESET, os.path.basename(to))    
                    #print("\t\t replaced:", os.path.basename(fr), wh.CYAN, "-->", wh.RESET, wp_to)    
                    #print("\t\t replaced:", wh.CYAN, wp_to, wh.RESET)    
                    print('.', end='')
                
                html = wh.replace_all(html, wp_fr, wp_to) 
                    
            else:
                print("\t\t\t", "does not exist: to:", to)
        ### for conversion />
        
        print(wh.RESET)   
        fp.close()
        
        #open the input file in write mode
        fp = open(filename, "w", encoding="utf-8")
        fp.write(html)
        fp.close()


    if b_perform_replacement:
        conversions = load_conversions(path_conversions)    
        #print(*conversions, sep="\n\t")      
                                
        html_files = wh.collect_files_endswith(project_folder, ["index.html", "index_pretty.html"])
        for i, html_file in enumerate(html_files):
            print("\t", "-"*88)
            print("\t", i+1, "/", len(html_files), os.path.basename(html_file))
            
            if False:
                replace_all_conversions_in_file(html_file, conversions)
            else:
                conversions_exts = []
                for q in ["\"", "\'"]:
                    for ext in image_exts:
                        conversions_exts.append((ext + q, ".webp" + q))
                        
                        wh.replace_all_in_file(html_file, ext + q, ".webp" + q)
                
                #replace_all_conversions_in_file(html_file, conversions_exts)
                                              
        ### for /> 
    ### b_perform_replacement />            
            
            
    if b_delete_originals:
        print("b_delete_originals")
        conversions = load_conversions(path_conversions)    
        
        for conversion in conversions:
            fr, to = conversion
            if wh.file_exists_and_valid(fr):
                print("\t", wh.RED, "removing:", os.path.basename(fr), wh.RESET)
                os.remove(fr)
                
        dir_size_new = get_size(config.project_folder)
        print("saved:", saved_percent_string(dir_size_orig, dir_size_new), config.project_folder)
  
    #-----------------------------------------
    # 
    #-----------------------------------------
    print("all done.")
                
    # https://www.thepythoncode.com/article/compress-pdf-files-in-python
    # https://blog.finxter.com/how-to-compress-pdf-files-using-python/
                