
import pillow_lut 
from selenium.webdriver.support.color import Color
import helpers_web as wh

#-----------------------------------------
# 
#-----------------------------------------
"""
    lut = pillow_lut.load_cube_file(
        "D:/__BUP_V_KOMPLETT/X/111_BUP/22luts/LUT cube/LUTs Cinematic Color Grading Pack by IWLTBAP/__xIWL_zM_Creative/Creative/xIWL_B-7040-STD.cube" # xIWL_C-9730-STD.cube
    )
    for r in range(256):
         for g in range(256):      
              for b in range(256):    
                  rgb =  (r,g,b)
                  norm = tuple(c/255.0 for c in rgb) 
                  cnorm = pillow_lut.sample_lut_cubic(lut, norm)      
                  crgb = tuple(round(c * 255.0) for c in cnorm) 
                  print(rgb, "-->", norm, "-->", cnorm, "-->",  crgb, "|", lut_convert_rgb(lut, r,g,b))  
"""
# https://www.selenium.dev/documentation/webdriver/additional_features/colors/
# rgba(255,255,255,1)

def lut_convert_rgb_tuple(lut, rgb):
    #print("lut_convert_rgb_tuple: rgb:", rgb)
    norm    = tuple(c/255.0 for c in rgb) 
    cnorm   = pillow_lut.sample_lut_cubic(lut, norm)
    crgb    = tuple(round(c * 255.0) for c in cnorm) 
    return  Color(red=crgb[0], green=crgb[1], blue=crgb[2], alpha=1) # .rgba # alpha: hmmmm
    
def lut_convert_rgb(lut, r,g,b):
    #print("lut_convert_rgb: r,g,b:", r,g,b)
    return lut_convert_rgb_tuple(lut, (r,g,b))
    
def lut_convert_selenium_color(lut, color):
    #print("lut_convert_selenium_color: color:", color, "r,g,b:", color.red, color.green, color.blue)
    l = lut_convert_rgb(lut, color.red, color.green, color.blue)
    return Color(red=l.red, green=l.green, blue=l.blue, alpha=color.alpha) # .rgba     # preserve alpha

def lut_convert_image(lut, image):
    if wh.image_has_transparency(image):
        image = image.convert("RGBA")
    else:
        image = image.convert("RGB")
    image = image.filter(lut)
    return image
