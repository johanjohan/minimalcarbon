# https://stackoverflow.com/questions/3964681/find-all-files-in-a-directory-with-extension-txt-in-python



import config
import helpers_web as wh



def image_show(path, secs=1):
    import subprocess
    import time
    p = subprocess.Popen(["C:\Program Files\IrfanView\i_view64.exe", path])
    time.sleep(secs)
    p.kill()

def saved_percent(size_orig, size_new):
    assert size_orig > 0
    perc = 100 - (size_new/size_orig*100)
    return perc


def saved_percent_string(size_orig, size_new):
    return "{:.1f}%".format(saved_percent(size_orig, size_new))

if __name__ == "__main__":
    
    import glob, os
    import PIL
    from PIL import Image, ImageOps
    
    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#webp
    project_folder  = os.path.abspath(config.project_folder)
    quality         = 66
    max_dim         = (1000, 1000) # (1280, 720) # (1200, 600)
    force_write     = True
    show_nth_image  = 20 # 0 is off
    resample        = Image.Resampling.LANCZOS
    
    print("quality    ", quality)
    print("max_dim    ", max_dim)
    print("force_write", force_write)
    
    images = []
    for root, dirs, files in os.walk(project_folder):
        for file in files:
            if any(file.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif']): # , '.webp'
                path = os.path.abspath(os.path.join(root, file))
                #print("\t", os.path.basename(path))
                images.append(path)
                
    # convert
    perc_avg = 0.0
    for cnt, path in enumerate(images):
                
        name, ext = os.path.splitext(path) # ('my_file', '.txt')
        out_path = name + '.webp'       
                    
        if force_write or not wh.file_exists_and_valid(out_path):
        
            print("\t", "{}/{}:".format(cnt+1, len(images)), os.path.basename(path))
            print("\t\t", wh.progress_string(cnt / len(images), verbose_string="", VT=wh.CYAN, n=33))
            
            size_orig = os.path.getsize(path)
            image = Image.open(path)
            image = image.convert('RGB')
            wh_orig = image.size
            
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
                        
            # colorize
            if True:
                image = image.convert("L")
                image = ImageOps.colorize(image, black ="#003300", white ="white")
                
            image = image.convert('RGB')
            image.save(out_path, 'webp', optimize=True, quality=quality)
            print("\t\t", "quality:", quality)
            print("\t\t", "wh     :", wh_orig, "-->", image.size, "| max_dim:", max_dim)
            
            size_new = os.path.getsize(out_path)
            print("\t\t", "saved  :", wh.GREEN + saved_percent_string(size_orig, size_new) + wh.RESET, os.path.basename(out_path))
            perc_avg += saved_percent(size_orig, size_new)
            
            if show_nth_image > 0 and not (cnt%show_nth_image):
                image_show(out_path, secs=0.5)
            
        else:
            print("\t\t", "already exists:", os.path.basename(path))
                                                        
    perc_avg /= len(images)  
    perc_avg = round(perc_avg, 1)  
    print("perc_avg:", wh.GREEN + str(perc_avg) + wh.RESET)
    print("all done.")
                
                