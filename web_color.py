"""

linear-gradient(180deg, rgba(0, 0, 0, 0.8), rgba(255, 255, 255, 0))



-------------------------------------------------------------------------



import js2py

squareofNum = "function f(x) {return x*x;}"

result = js2py.eval_js(squareofNum)

print(result(5))

pip install js2py
-------------------------------------------------------------------------
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


#import colorsys
import shutil
import os
#from distutils.cygwinccompiler import CygwinCCompiler
import helpers_web as wh
import helpers_web as hw
import config
import cssutils
import time
import pillow_lut 
import webcolors
#import colorsys
from selenium.webdriver.support.color import Color
import re


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
    print("lut_convert_rgb_tuple: rgb:", rgb)
    norm    = tuple(c/255.0 for c in rgb) 
    cnorm   = pillow_lut.sample_lut_cubic(lut, norm)
    crgb    = tuple(round(c * 255.0) for c in cnorm) 
    return Color(red=crgb[0], green=crgb[1], blue=crgb[2], alpha=1) # .rgba # alpha: hmmmm
    
def lut_convert_rgb(lut, r,g,b):
    print("lut_convert_rgb: r,g,b:", r,g,b)
    return lut_convert_rgb_tuple(lut, (r,g,b))
    
# https://www.selenium.dev/documentation/webdriver/additional_features/colors/
# rgba(255,255,255,1)
def lut_convert_selenium_color(lut, color):
    assert lut
    assert color
    
    print("lut_convert_selenium_color: color:", color, "r,g,b:", color.red, color.green, color.blue)
    l = lut_convert_rgb(lut, color.red, color.green, color.blue)
    return Color(red=l.red, green=l.green, blue=l.blue, alpha=color.alpha) # .rgba     # preserve alpha

def lut_convert_image(lut, image):
    if wh.image_has_transparency(image):
        image = image.convert("RGBA")
    else:
        image = image.convert("RGB")
    image = image.filter(lut)
    return image
#-----------------------------------------
# 
#-----------------------------------------
def __property_color_cleanup(value):
    value = wh.string_remove_control_characters(value)
    value = wh.string_remove_multiple_spaces(value)
    for fr, to in [(', ', ','), (';', ' '), ('( ', '('), (' )', ')')]:
        value = value.replace(fr, to)
    # # # #print("\t\t\t\t", wh.CYAN, value, wh.RESET)
    return value
    
def property_has_color(property):
    value = __property_color_cleanup(property.value)
    #print("\t\t\t\t", wh.CYAN, value, wh.RESET)
    for val in value.split(' '):
        #print("\t\t\t\t\t", wh.GRAY, val, wh.RESET)
        if any(key in val for key in ['#', 'rgb', 'hsl', 'hwb']) or is_named_color(val):
           return True            
    return False

#-----------------------------------------
# seleniumm cannot 
#-----------------------------------------
def named_color_to_rgba(named_color_string):
    try:
        r,g,b = webcolors.name_to_rgb(named_color_string.strip())
        return (r,g,b,255)
    except Exception as e:
        #print(wh.RED, "is_named_color:", e, wh.RESET) 
        return None    
     
def is_named_color(cstring):
    return False if not named_color_to_rgba(cstring) else True
#-----------------------------------------
# 
#-----------------------------------------
def string_has_parenthesis(s):
    return any(key in s for key in ['(', ')'])

def string_extract_parenthesis(s):
    ###ret = s[s.find("(")+1:s.find(")")]
    ret = s[s.find("(")+1:s.rfind(")")] # fix
    print(wh.YELLOW, "string_extract_parenthesis:", s, "-->", ret, wh.RESET)
    return ret

def string_to_selenium_color(string, pre="\t"*1):
    try:
        col = Color.from_string(string) # selenium eats it all ! wow
        print(pre, wh.dq(string), "-->", wh.GREEN, col.rgba, "[", col.hex, "]", col.red, col.green, col.blue, col.alpha, "\n\n", wh.RESET)
        return col
    except Exception as e:
        #print(wh.RED, "string_to_selenium_color:", e, wh.RESET)
        return None
        
def string_extract_selenium_colors(value):
    
    """
    special case: 
    linear-gradient(direction, color-stop1, color-stop2, ...); 
    linear-gradient(red, yellow, green); 
    radial-gradient(shape size at position, start-color, ..., last-color);
    conic-gradient([from angle] [at position,] color [degree], color [degree], ...);
    currentcolor
    text-shadow: 2px 2px red;
    box-shadow: 10px 10px lightblue;
    ["-gradient"]
    
    """
    rgba = [] # TODO may be multiple cols in string
    value = __property_color_cleanup(value)
    print("\t"*0, "string_extract_selenium_colors", wh.MAGENTA, value, wh.RESET)
    for val in value.split(' '):
        if col := string_to_selenium_color(val):
             rgba.append(col) 
       
    print("selenium *rgba[]", wh.GREEN, *rgba, wh.RESET, sep="\n"+"\t"*2)  
    ##print("selenium color", wh.GREEN, color, wh.RESET) 
    
    assert rgba # DEBUG
       
    return rgba if rgba else None # TODO ??? or []

# https://stackoverflow.com/questions/26633452/how-to-split-by-commas-that-are-not-within-parentheses
def string_split_at_delim_outside_parenthesis(value, delim):
    #ret = re.split(r',\s*(?![^()]*\))', value) # ok
    ret = re.split(rf"{delim}(?![^(]*\))", value)
    print("string_split_at_comma_outside_parenthesis:", wh.dq(delim), wh.GREEN, ret, wh.RESET)
    return ret

def string_split_at_comma_outside_parenthesis(value):
    return string_split_at_delim_outside_parenthesis(value, delim=',')

def property_value_apply_lut(value, lut):
    value = __property_color_cleanup(value)
    print("\t"*0, "property_value_apply_lut", wh.MAGENTA, value, wh.RESET)
    
    delim = ' '
    if any(key in value for key in ["-gradient"]):
        value = string_extract_parenthesis(value) # 
        delim = ','

    values = string_split_at_delim_outside_parenthesis(value, delim=delim)
        
    for val in values:
        print("\t"*1, val)
        if col := string_to_selenium_color(val):
            print(col)
             
                
    return value
    
    
    
#-----------------------------------------
# 
#-----------------------------------------
def path_split(file):
    file        = wh.to_posix(file)
    dir         = os.path.dirname(file)
    head, tail  = os.path.split(file)
    base, ext   = os.path.splitext(tail)      

    if True:
        print("file:", file)
        print("dir:", dir)
        print("head:", head) # same as dir
        print("tail:", tail)
        print("base:", base)
        print("ext:", ext)            
    
    return dir, base, ext
        
def path_file_add_postfix(file, postfix):
    dir, base, ext = path_split(file)
    ret = wh.add_trailing_slash(dir) + base + postfix + ext
    print("ret:", ret)
    return ret
#-----------------------------------------
# 
#-----------------------------------------        
# https://colour.readthedocs.io/en/develop/generated/colour.LUT3D.html

# https://pythonhosted.org/cssutils/docs/utilities.html
if __name__ == "__main__":
    
    lut = None
    lut = pillow_lut.load_cube_file(
        "D:/__BUP_V_KOMPLETT/X/111_BUP/22luts/LUT cube/LUTs Cinematic Color Grading Pack by IWLTBAP/__xIWL_zM_Creative/Creative/xIWL_B-7040-STD.cube" # xIWL_C-9730-STD.cube
    )
    # for r in range(256):
    #      for g in range(256):      
    #           for b in range(256):    
    #               rgb =  (r,g,b)
    #               norm = tuple(c/255.0 for c in rgb) 
    #               cnorm = pillow_lut.sample_lut_cubic(lut, norm)      
    #               crgb = tuple(round(c * 255.0) for c in cnorm) 
    #               print(rgb, "-->", norm, "-->", cnorm, "-->",  crgb, "|", lut_convert_rgb(lut, r,g,b))    
    # exit(0)  
        
    import chromato 
    
    strings = [
               "#ff0000",
               "#f00",
               "background: border-box #f00;",
               "background: \t rgba(0,0,\t  255,1);\n\t\t\t\t\t\t",
               "background: blue;",
               "background: purple;",
               "unknown_color",
               "background: rgba(0,0,255,0.5);",
               "some ramp: #f00 to #0f0 to #00f",
               "background-image: url('paper.gif');",
               "background-color: #cccccc;",
               "linear-gradient(180deg, rgba(0, 0, 0, 0.8), rgba(255, 255, 255, 0))",
               "linear-gradient(red, yellow, green, purple, #123456, #987654, rgb(255,128,96), rgba(255,128,96,1)); ",
               ]

    
    
    for s in strings:
        #print( string_extract_selenium_colors(s) )
        property_value_apply_lut(s, lut)
        print()
    exit(0)
    
    # https://pypi.org/project/Js2Py/
    # https://github.com/PiotrDabkowski/Js2Py
    import js2py
    js2py.eval_js('console.log( "Hello World!" )')
    add = js2py.eval_js('function add(a, b) {return a + b}')
    result = add(1, 2) + 3
    print("result", result)
    squareofNum = js2py.eval_js("function f(x) {return x*x;}")
    print("result", squareofNum(5))
    #exit(0)
    

    import logging
    cssutils.log.setLevel(logging.CRITICAL)
    
    postfix_bup     = "_bup_"
    postfix_orig    = "_orig_"
    
    files = wh.collect_files_endswith(config.project_folder, [".css"])
    files = wh.links_remove_excludes(files, [postfix_bup, "202207"])
    print("files", *files, sep="\n\t")
    
    # def property_value_is_color(val):
    #     return any(e in val for e in ['#', 'rgb', 'hsl', 'rgba', 'hsla']) # may as well be a named color
    
    # # pip install chromato
    # # https://github.com/vikpe/chromato/blob/f11556bde953fd6999187774a3de1e978f32b06c/README.md
    # from chromato.spaces import Color
    # import chromato 
    # red = Color(255, 0, 0)
    # print(red.cmyk )   
    # print(red.hex )   
    # print(red.rgb, red.rgb.r )   
    # print(red.hsl )   
    # print(red.hsv )   
    # #exit(0)
    
    
    colors = []
    for file in files:
        
        print("-"*88)
        
        # orig: save or restore
        orig_path = path_file_add_postfix(file, postfix_orig + config.dt_now_string)
        if wh.file_exists_and_valid(orig_path):
            shutil.copy(orig_path, file)
        else:
            shutil.copy(file, orig_path)
        
        # make a bup
        bup_path = path_file_add_postfix(file, postfix_bup + config.dt_now_string)
        shutil.copy(file, bup_path)
                
        print("\t"*0, wh.CYAN, file, wh.RESET)
        try:
            sheet = cssutils.parseFile(file)
            # combine all linked sheets
            sheet = cssutils.resolveImports(sheet, target=None)
            
            print("\t"*1, wh.MAGENTA, cssutils.getUrls(sheet) , wh.RESET)
            
            for rule in sheet: # .cssRules:       
                print("\t"*2, rule.type, cssutils.css.CSSRule._typestrings[rule.type])
                
                if rule.type in [cssutils.css.CSSRule.STYLE_RULE]:
                    print("\t"*3,   rule.selectorText )       
                    for property in rule.style:
                        print("\t"*4,   property.name , end=' ')       
                        if property_has_color(property):
                            print("property.value:",  wh.GREEN, property.value, wh.RESET)
                            color   = string_extract_selenium_colors(property.value)[0] # TODO what about possible others? may be NONE TODO
                            assert color
                            print("color:",  wh.GREEN, color, wh.RESET)
                            assert lut
                            lutted  = lut_convert_selenium_color(lut, color)
                            print("lutted:", property.value, wh.GRAY, color, "-->", wh.GREEN, lutted, wh.RESET)
                        else:
                            print(wh.GRAY, property.value, wh.RESET)
                            pass
                            
                        # if 'color' in property.name:
                        #     color = property.value
                        # elif property.name == 'background':
                        #     values = property.value.split(' ')
                        #     color = property.value
                        
                        # print("\t"*3, wh.CYAN, property.name, wh.RESET, property.value, wh.RESET)
                        # if property_is_color(property):
                        #     print("\t"*4, wh.YELLOW, property.value, wh.RESET)
                        #     colors.append((property.name, property.value, color_from_string(property.value)))
                            
                        #     ## now isolate that color, convert via lut and replace
                            
                        #     property_to_color(property)
                            
                            
 
                                                            
        except Exception as e:
            print(f"{wh.RED} css: {e} {wh.RESET}")
            time.sleep(2)
            exit(1)
            
    print("colors", *colors, sep="\n\t")