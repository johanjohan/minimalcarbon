
import config
import helpers_web as wh
import helpers_web as hw

import os
from PIL import Image, ImageOps

if __name__ == "__main__":
    def test_compression():
        out_exts = [".webp", ".avif", ".png"]
        image_paths = [
            config.project_folder + "wp-content/themes/karlsruhe-digital/images/beitragsseite_hero_slider.jpg",
            # config.project_folder + "wp-content/themes/karlsruhe-digital/images/programm_hero.jpg",
            #config.project_folder + "wp-content/themes/karlsruhe-digital/images/bloguebersichtseite_hero_slider.jpg",
            # config.project_folder + "wp-content/themes/karlsruhe-digital/images/suchseite_hero_slider.jpg",
            # config.project_folder + "wp-content/themes/karlsruhe-digital/images/suchergebnisse_hero_slider.jpg",
            config.project_folder + "wp-content/uploads/2019/08/1-IT-Cluster-in-Europa.png",
            #"__tmp__images_compression/__girl.png",
        ]
        for path in image_paths:
            for quality in range(0, 101, 10):
                
                print("\n"*4 + "#"*88) 
                
                image       = Image.open(path)
                is_transp   = wh.image_has_transparency(image)
                
                old_size = image.size
                image.thumbnail((1600, 1600), resample=Image.Resampling.LANCZOS)
                
                #__image_smaller_png_path = os.path.abspath("__smaller.png")
                # if os.path.isfile(__image_smaller_png_path):
                #     os.remove(__image_smaller_png_path)
                    
                import tempfile
                __image_smaller_png_path = tempfile.NamedTemporaryFile(suffix='.png').name
                image.save(__image_smaller_png_path, format="png")

                for new_ext in out_exts:
                    print("-"*66)
                    name, ext = os.path.splitext(path)
                    base = os.path.basename(name)
                    q = f"_q{quality:03d}"
                    out_path    = "__tmp__images_compression/_PIL/" + base + q + "_PIL" + new_ext
                    out_path_IM = "__tmp__images_compression/_IMA/" + base + q + "_IMA" + new_ext
                    out_path_AV = "__tmp__images_compression/_AVE/" + base + q + "_AVE" + new_ext
                    out_path_LL = "__tmp__images_compression/_LLS/" + base + q + "_LLS" + new_ext
                    wh.make_dirs(out_path)
                    wh.make_dirs(out_path_IM)
                    wh.make_dirs(out_path_AV)
                    wh.make_dirs(out_path_LL)
                    
                    print("", "quality:", wh.YELLOW, quality, wh.MAGENTA, out_path, wh.RESET)
                    # print("\t", "is_transp:", is_transp)
                    # print("\t", "size     :", old_size, "-->", image.size)                    
                    
                    format = new_ext.lstrip('.') 
                    # if is_transp:
                    #     image.save(out_path, format=format, optimize=True, lossless=True) # !!! need great alpha
                    # else:
                    image.save(out_path, format=format, optimize=True, quality=quality) 

                    # lossless
                    image.save(out_path_LL, format=format, optimize=True, lossless=True)

                    print("-"*66)
                    # magick -quality 40 -define heic:speed=0 test.jpg test.avif
                    # https://askubuntu.com/questions/1411869/creating-avif-or-heic-images-with-transparency-does-not-work-with-imagemagick-in
                    import subprocess
                    print("magick...")
                    subprocess.call([
                        "magick", "convert",
                        "-quality", str(quality),       # https://imagemagick.org/script/command-line-options.php#quality
                        os.path.abspath(__image_smaller_png_path),
                        os.path.abspath(out_path_IM)
                    ])
                    print("magick: done")
                    
                    """
                    <picture>
                        <source srcset="image.avif" type="image/avif">
                        <source srcset="image.webp" type="image/webp">
                        <source srcset="image.jpg" type="image/jpeg">
                        <img src="image.jpeg" alt="Description of the image">
                    </picture>        
                    """
                    # #./avifenc [options] input.file output.avif
                    # # https://web.dev/compress-images-avif/
                    # assert os.path.isfile(os.path.abspath("avif/avifenc.exe"))
                    # assert os.path.isfile(os.path.abspath(path))
                    # color QP [0 (Lossless) <-> 63 (Worst)], 
                    # alpha QP [0 (Lossless) <-> 63 (Worst)]
                    # https://medium.com/yavar/avif-the-nextgen-image-format-91162caf32d2
                    
                    if format == "avif":
                        print("-"*66)
                        print(wh.YELLOW, "avifenc...", format, wh.RESET)
                        min_val = 0
                        max_val = 63
                        q_av = int(wh.map(quality, 0, 100, max_val, min_val))
                        print("q_av", q_av)
                        
                        """
 
                            --advanced color:cq-level={q_av}    # does NOT work
                            --advanced alpha:cq-level=10        # does NOT work
                            --advanced cq-level=10

                            --advanced cq-level={q_av}

                        """
                        # avifenc [options] input.[jpg|jpeg|png|y4m] output.avif
                        cmd = f"""
                        
                            {os.path.abspath("avif/avifenc.exe")} 
                            --speed {5} 
                            --jobs  {8} 
                            
                            --min       {min_val} --max        {max_val}   
                            --minalpha  {min_val} --maxalpha   {max_val}   

                            --advanced end-usage=q
                            --advanced cq-level={q_av}
                                                        
                            --advanced tune=ssim
                            --advanced sharpness=0 
                        
                            {os.path.abspath(__image_smaller_png_path)} 
                            {os.path.abspath(out_path_AV)} 
                            
                        """
                        ##md = f""" {os.path.abspath("avif/avifenc.exe")} --help """
                        cmd = wh.string_remove_whitespace(cmd)
                        print(wh.CYAN, end='')
                        print(cmd)
                        ret = os.system(wh.dq(cmd))
                        print(wh.RESET, end='')
                    
                    print("-"*66)   
                    wh.image_show_file(out_path, secs=0)
                    
                os.remove(__image_smaller_png_path)     
            
    test_compression()       
    exit(0)   