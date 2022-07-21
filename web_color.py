"""
https://docs.python.org/3/library/colorsys.html

The colorsys module defines bidirectional conversions of color values between 
colors expressed in the RGB (Red Green Blue) color space used in computer monitors 
and three other coordinate systems: YIQ, HLS (Hue Lightness Saturation) and HSV (Hue Saturation Value). 
Coordinates in all of these color spaces are floating point values. In the YIQ space, 
the Y coordinate is between 0 and 1, but the I and Q coordinates can be positive or negative. 
In all other spaces, the coordinates are all between 0 and 1.


colorsys.rgb_to_yiq(r, g, b)¶

    Convert the color from RGB coordinates to YIQ coordinates.

colorsys.yiq_to_rgb(y, i, q)

    Convert the color from YIQ coordinates to RGB coordinates.

colorsys.rgb_to_hls(r, g, b)

    Convert the color from RGB coordinates to HLS coordinates.

colorsys.hls_to_rgb(h, l, s)

    Convert the color from HLS coordinates to RGB coordinates.

colorsys.rgb_to_hsv(r, g, b)

    Convert the color from RGB coordinates to HSV coordinates.

colorsys.hsv_to_rgb(h, s, v)

    Convert the color from HSV coordinates to RGB coordinates.

..............................................
Hex triplet
threedigit 
sixdigit   

named colors
pip install webcolors
https://webcolors.readthedocs.io/en/1.3.1/


    Six-digit hexadecimal.
    Three-digit hexadecimal.
    Integer rgb() triplet.
    Percentage rgb() triplet.
    Varying selections of predefined color names.

..............................................
HTML
The <body> tag has following attributes which can be used to set different colors −

    bgcolor − sets a color for the background of the page.

    text − sets a color for the body text.

    alink − sets a color for active links or selected links.

    link − sets a color for linked text.

    vlink − sets a color for visited links − that is, for linked text that you have already clicked on.

        <body text = "blue" bgcolor = "green">
        
        <font color = "#FFFFFF">


    rgb(0,0,0)
    <body text = "rgb(0,0,255)" bgcolor = "rgb(0,255,0)">
..............................................
CSS
Using CSS

CSS can be added to HTML documents in 3 ways:

    Inline      - by using the style attribute inside HTML elements
    Internal    - by using a <style> element in the <head> section
    External    - by using a <link> element to link to an external CSS file




<h1 style="background-color:DodgerBlue;">Hello World</h1>
<style="color:Tomato;"
<style="border:2px solid Tomato;">


rgb(255, 99, 71)
#ff6347
hsl(9, 100%, 64%)


rgba(255, 99, 71, 0.5)
hsla(9, 100%, 64%, 0.5)


..............................................
https://pillow-lut-tools.readthedocs.io/en/latest/
pillow_lut.load_cube_file(lines, target_mode=None, cls=<class 'PIL.ImageFilter.Color3DLUT'>)
pillow_lut.sample_lut_linear(lut, point)
pillow_lut.sample_lut_cubic(lut, point)

 pillow_lut.rgb_color_enhance(source, brightness=0, exposure=0, contrast=0, warmth=0, saturation=0, vibrance=0, hue=0, gamma=1.0, linear=False, cls=<class 'PIL.ImageFilter.Color3DLUT'>)
 
 
..............................................
..............................................
..............................................
..............................................
..............................................
..............................................
..............................................
..............................................

"""


import colorsys
from distutils.cygwinccompiler import CygwinCCompiler
import helpers_web as wh
import helpers_web as hw
import config
import cssutils
import time
import pillow_lut 
import webcolors
import colorsys

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
def lut_convert_rgb_tuple(lut, rgb):
    norm    = tuple(c/255.0 for c in rgb) 
    cnorm   = pillow_lut.sample_lut_cubic(lut, norm)
    crgb    = tuple(round(c * 255.0) for c in cnorm) 
    return crgb
    
def lut_convert_rgb(lut, r,g,b):
    return lut_convert_rgb_tuple(lut, (r,g,b))
    
# if is_transp:
#     image = image.convert("RGBA")
# else:
#     image = image.convert("RGB")
# image = image.filter(lut)

# https://developer.mozilla.org/en-US/docs/Web/CSS/color
def property_is_color_XXX1(property):
    # inherit none transparent, variables
    return any(e in property.value for e in ['#', 'rgb', 'hsl', 'rgba', 'hsla', 'hwb']) # may as well be a named color

def property_is_color(property):
    b = any(e in property.name for e in ['color', 'border']) # may as well be a named color
    return b
    
def get_color_start(value):
    for start in ['#', 'rgba(', 'hsla(', 'rgb(', 'hsl(']: # could as well be a named webcolor!!!!
        if start in value:
            print("found:", start)
            return start
    return None

def color_from_string(value):
    color = None
    
    
    #  rgba(43, 51, 63, 0.7)
    def pack(r,g,b,a):
        color = (round(r),round(g),round(b),round(a))
        return color
    
    def unnormalize(r,g,b,a):
        color = pack(r,g,b,a)
        color = tuple(round(c * 255.0) for c in color)
        return color
    
    try:
        if '#' in value: # --> RGBA
            hex = value.split('#')[1]
            r,g,b = webcolors.hex_to_rgb('#' + hex)
            color = (r,g,b, 255)
            print(value, '#', type(color), wh.GREEN, color, wh.RESET)
            
        #elif any(key in value for key in ['rgba(', 'hsla(', 'rgb(', 'hsl(']):
        else:
            color = None
            
            # rgb Each parameter (red, green, and blue) defines the intensity of the color between 0 and 255.
            # hsl: hsl(0, 100%, 50%)

            if any(key in value for key in ['rgb(', 'hsl(', 'hwb(']):
                
                for key in ['rgb(', 'hsl(', 'hwb(']:
                    if key in value:
                        values = value.split(key)[1].replace('(','').split(')')[0]
                        print(type(values), values)
                        values = tuple(map(float, values.split(',')))
                        print(type(values), values)

                        if key == 'rgb(':
                            r,g,b = values
                            color = pack(r,g,b,255)
                        elif key == 'hsl(':
                            h,s,l = values 
                            r,g,b = colorsys.hls_to_rgb(h/360.0, l/100.0, s/100.0) # why is this reversed? Hue Lightness Saturation  
                            color = unnormalize(r,g,b,1)
                        else:
                            print(wh.RED, "color_from_string: not supported: key", key, wh.RESET)  
                            exit(1)   
                    
                        print(value, key, type(color), wh.GREEN, color, wh.RESET)
                        
                        break
                    
                    
            elif any(key in value for key in ['rgba(', 'hsla(']):            
                for key in ['rgba(', 'hsla(']: # colorsys.hsv_to_rgb(1,1,1)
                    if key in value:
                        values = value.split(key)[1].replace('(','').split(')')[0]
                        #print(type(values), values)
                        values = tuple(map(float, values.split(',')))
                        #print(type(values), values)
                        
                        if key == 'rgba(':
                            r,g,b,a = values
                            print("r,g,b,a", r,g,b,a)
                            color = pack(r,g,b,a*255.0)
                        elif key == "hsla(":
                            h,s,l,a = values 
                            r,g,b = colorsys.hls_to_rgb(h/360.0, l/100.0, s/100.0) # why is this reversed? Hue Lightness Saturation                  
                            color = unnormalize(r,g,b,a)
                        else:
                            print(wh.RED, "color_from_string: not supported: key", key, wh.RESET)  
                            exit(1)  
                            
                                                    
                        print(value, key, type(color), wh.GREEN, color, wh.RESET)
                        break

                
    except Exception as e:
        color = None
        print(wh.RED, "ERR", e, wh.RESET)
        
            
    if not color:
        # check for webcolors
        print("named", value)
        try:
            values = value.split(' ')[-1]
            print(type(values), values)
            r,g,b = webcolors.name_to_rgb(values.strip())
            color = pack(r,g,b,255.0)
            print(value, "named", type(color), wh.GREEN, color, wh.RESET)
        except Exception as e:
            color = None
            print(wh.RED, "color_from_string:", e, wh.RESET)  

    return color

def property_to_color(property):

    # if 'color' in property.name:
    #     delim = get_color_start(property.value)
    # elif 'border' in property.name:
    #     pass

    
        
    # if '#' in property.value:
    #     pass
    # elif 'rgb' in property.value:
    #     pass
    # elif 'hsl' in property.value:
    #     pass
    # elif 'hwb' in property.value:
    #     pass
    # else:
    #     pass
    
    # for hint in ['#', 'rgba(', 'hsla(', 'rgb(', 'hsl(']: # could as well be a named webcolor!!!!
    #     if hint in property.value:
    #         print("found:", hint)
    #         break
    # ### for
    
    pass

    

#-----------------------------------------
# 
#-----------------------------------------
#-----------------------------------------
# 
#-----------------------------------------
#-----------------------------------------
# 
#-----------------------------------------    

# That function expects decimal for s (saturation) and v (value), not percent. Divide by 100.
# test_color = colorsys.hsv_to_rgb(359,100,100)
# --> colorsys.hsv_to_rgb(1,1,1)
# test_color = colorsys.hsv_to_rgb(359/360.0, 1, 1)

# def hsv2rgb(h,s,v):
#     return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

# def hsv_to_rgb(h, s, v):
#         if s == 0.0: return (v, v, v)
#         i = int(h*6.) # XXX assume int() truncates!
#         f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
#         if i == 0: return (v, t, p)
#         if i == 1: return (q, v, p)
#         if i == 2: return (p, v, t)
#         if i == 3: return (p, q, v)
#         if i == 4: return (t, p, v)
#         if i == 5: return (v, p, q)
        

#-----------------------------------------
# 
#-----------------------------------------        
# from matplotlib.colors import hsv_to_rgb
# rgb = hsv_to_rgb(hsv)

# https://colour.readthedocs.io/en/develop/generated/colour.LUT3D.html

# https://pythonhosted.org/cssutils/docs/utilities.html
if __name__ == "__main__":
    
    # lut = pillow_lut.load_cube_file(
    #     "D:/__BUP_V_KOMPLETT/X/111_BUP/22luts/LUT cube/LUTs Cinematic Color Grading Pack by IWLTBAP/__xIWL_zM_Creative/Creative/xIWL_B-7040-STD.cube" # xIWL_C-9730-STD.cube
    # )
    # for r in range(256):
    #      for g in range(256):      
    #           for b in range(256):    
    #               rgb =  (r,g,b)
    #               norm = tuple(c/255.0 for c in rgb) 
    #               cnorm = pillow_lut.sample_lut_cubic(lut, norm)      
    #               crgb = tuple(round(c * 255.0) for c in cnorm) 
    #               print(rgb, "-->", norm, "-->", cnorm, "-->",  crgb, "|", lut_convert_rgb(lut, r,g,b))    
    # exit(0)  
    
    import logging
    cssutils.log.setLevel(logging.CRITICAL)
    
    files = wh.collect_files_endswith(config.project_folder, [".css"])
    
    # def property_value_is_color(val):
    #     return any(e in val for e in ['#', 'rgb', 'hsl', 'rgba', 'hsla']) # may as well be a named color
    
    colors = []
    for file in files:
        print("\t"*0, wh.CYAN, file, wh.RESET)
        try:
            sheet = cssutils.parseFile(file)
            sheet = cssutils.resolveImports(sheet, target=None)
            
            print("\t"*1, wh.MAGENTA, cssutils.getUrls(sheet) , wh.RESET)
            
            for rule in sheet.cssRules:       
                print("\t"*2, rule.type, cssutils.css.CSSRule._typestrings[rule.type])
                
                if rule.type in [cssutils.css.CSSRule.STYLE_RULE, cssutils.css.CSSRule.STYLE_RULE]:
                                
                    for property in rule.style:
                        print("\t"*3, wh.CYAN, property.name, wh.RESET, property.value, wh.RESET)
                        if property_is_color(property):
                            print("\t"*4, wh.YELLOW, property.value, wh.RESET)
                            colors.append((property.name, property.value, color_from_string(property.value)))
                            
                            ## now isolate that color, convert via lut and replace
                            
                            property_to_color(property)
                            
                            
 
                                                            
        except Exception as e:
            print(f"{wh.RED} css: {e} {wh.RESET}")
            time.sleep(2)
            
    print("colors", *colors, sep="\n\t")