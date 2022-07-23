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
import datetime
import shutil
import os

from pyrsistent import v
#from distutils.cygwinccompiler import CygwinCCompiler
import helpers_web as wh
import helpers_web as hw
import helpers_lut as hl
import config
import cssutils
import time
import pillow_lut 
import webcolors
#import colorsys
from selenium.webdriver.support.color import Color
import re
import copy
import cssbeautifier


#-----------------------------------------
# selenium 
#-----------------------------------------
"""
special case: 

linear-gradient(direction, color-stop1, color-stop2, ...); 
linear-gradient(red, yellow, green); 
radial-gradient(shape size at position, start-color, ..., last-color);
conic-gradient([from angle] [at position,] color [degree], color [degree], ...);

normal case
color: currentcolor
text-shadow: 2px 2px red;
box-shadow: 10px 10px lightblue;
["-gradient"]

the combinators of the defined values which might simply be space or comma or slash.

color: lab(67.5345% -8.6911 -41.6019 / 100%);
https://dev.to/alvaromontoro/the-ultimate-guide-to-css-colors-2020-edition-1bh1
"""

# the combinators of the defined values which might simply be space or comma or slash.

# def string_has_color(__value):
#     for val in property_value_split(__value):
#         #print("\t\t\t\t\t", wh.GRAY, val, wh.RESET)
#         # https://dev.to/alvaromontoro/the-ultimate-guide-to-css-colors-2020-edition-1bh1
#         if any(key in val for key in ['#', 'rgb', 'hsl', 'hwb', 'lab', 'lch', 'device-cmyk', 'color']) or string_is_named_color(val):
#            return True            
#     return False

# def property_has_color(property):
#     return string_has_color(property.value)

def string_named_color_to_rgba(named_color_string):
    try:
        r,g,b = webcolors.name_to_rgb(named_color_string.strip())
        return (r,g,b,255)
    except Exception as e:
        #print(wh.RED, "is_named_color:", e, wh.RESET) 
        return None    
     
def string_is_named_color(cstring):
    return False if not string_named_color_to_rgba(cstring) else True

def selenium_color_to_string(color):
    return f"rgba({color.red},{color.green},{color.blue},{color.alpha})"


#-----------------------------------------
# 
#-----------------------------------------
def string_has_parenthesis(s):
    return all(key in s for key in ['(', ')'])

def string_extract_parenthesis(s):
    ret = s[s.find("(")+1:s.rfind(")")] 
    #print(wh.YELLOW, "string_extract_parenthesis:", s, "-->", ret, wh.RESET)
    return ret
#-----------------------------------------
# 
#-----------------------------------------
def string_to_selenium_color(string, pre="\t"*1):
    try:
        col = Color.from_string(string) # selenium eats it all ! wow
        print(pre, wh.dq(string), "-->", wh.GREEN, col.rgba, "[", col.hex, "]", col.red, col.green, col.blue, col.alpha, "\n\n", wh.RESET)
        return col
    except Exception as e:
        #print(wh.RED, "string_to_selenium_color:", e, wh.RESET)
        # if string_has_color(string):
        #     print(wh.RED, "string_to_selenium_color: STRANGE:", wh.dq(string), wh.RESET)
        #     print(wh.RED, "string_to_selenium_color: STRANGE: has_color: ", e, wh.RESET)
        #     exit(1)
        return None
    
def string_is_color(string):
    try:
        col = Color.from_string(string) # selenium eats it all ! wow
        return True
    except:
        return False

#-----------------------------------------
# 
#-----------------------------------------

# https://stackoverflow.com/questions/26633452/how-to-split-by-commas-that-are-not-within-parentheses
def string_split_at_delim_outside_parenthesis(value, delim):
    #ret = re.split(r',\s*(?![^()]*\))', value) # ok"
    ret = re.split(rf"{delim}(?![^(]*\))", value)
    print("string_split_at_comma_outside_parenthesis:", wh.dq(delim), wh.GREEN, ret, wh.RESET)
    return ret

def string_split_at_comma_outside_parenthesis(value):
    return string_split_at_delim_outside_parenthesis(value, delim=',')
        
        
# # # def string_extract_selenium_colors(__value):
    
# # #     # a useless function<<<<<<<<<<<<<<<<<<<<<<<<<

# # #     rgba = [] 
    
# # #     for val in property_value_split(__value):
# # #         if col := string_to_selenium_color(val):
# # #              rgba.append(col) 
# # #     print("selenium *rgba[]", wh.GREEN, *rgba, wh.RESET, sep="\n"+"\t"*2)  
    
# # #     assert rgba # DEBUG
    
# # #     return rgba if rgba else None # TODO ??? or []



#-----------------------------------------
# 
#-----------------------------------------

#__combinators = [' ', ',', '/']

def __css_function_cleanup(__value):
    
    value = wh.string_remove_control_characters(__value)
    
    for fr, to in [
        (';', ' ; '),
        ('/', ' / '),
    ]: 
        value = value.replace(fr, to)
        
    value = wh.string_remove_multiple_spaces(value)    
    
    for fr, to in [
        (' ,', ','), 
        (', ', ','), 
        ('( ', '('), 
        (' (', '('), 
        (' )', ')'), 
    ]: 
        value = value.replace(fr, to)
        
    #print("\t\t\t\t", wh.GRAY, __value, "-->", wh.YELLOW, value, wh.RESET)
    return value
    
# function: "linear-gradient(red, yellow, green, purple, #123456, #987654, rgb(255,128,96), rgba(255,128,96,1)); "   
def function_split_traverse_apply_lut(__value, lut):   
    
    #print("function_split_traverse_apply_lut:", __value)
    
    assert string_has_parenthesis(__value)
    
    value   = __css_function_cleanup(__value)
    name    = value.split('(')[0]
    args    = string_split_at_delim_outside_parenthesis(
        string_extract_parenthesis(value), 
        ','
    )
    # print("\t", "name:", name)
    # print("\t", "args:", args)
    
    # these are the comma-separated args: ['to right top', 'rgba(123,234,210,1)', '#004d7a', '#008793', '#00bf72', '#a8eb12']
    new_args = []
    for arg in args:
        pv = cssutils.css.PropertyValue(arg)
        #print("\t\t\t", "pv:", pv, pv.length)
        if pv.length > 1:
            new_args.append(pv.cssText) # all together 'to right top' (length 3)
        elif pv.length == 1:
            v = pv[0]
            if v.type == cssutils.css.Value.COLOR_VALUE:
                lut_col         = hl.lut_convert_rgb(lut, v.red, v.green, v.blue)
                lut_col.alpha   = v.alpha # restore original
                new_args.append( selenium_color_to_string(lut_col) ) # rgba(...)
            else:
                new_args.append(pv.cssText) # whatever
        else:
            assert False
    ### for args />  
    
    return f"{name}({', '.join(new_args)})" # the new function
 
def property_traverse_apply_lut(__value, __lut):

    #print("\t"*4, "property_traverse_apply_lut", wh.MAGENTA, __value, wh.RESET)
    ret = []
    for v in cssutils.css.PropertyValue(__value):
        
        if v.type == cssutils.css.Value.COLOR_VALUE:
            lut_col         = hl.lut_convert_rgb(__lut, v.red, v.green, v.blue)
            lut_col.alpha   = v.alpha # restore original
            ret.append(selenium_color_to_string(lut_col))                                
        elif v.type == cssutils.css.Value.FUNCTION:
            new_func = function_split_traverse_apply_lut(v.value, __lut)
            ret.append(new_func)
        else:
            ret.append(str(v.cssText)) # IDENT DIMENSION...
        
    ### for />                    
    return ' '.join(ret)   
   
# # "linear-gradient(red, yellow, green, purple, #123456, #987654, rgb(255,128,96), rgba(255,128,96,1)); "
# def property_value_split(__value):
#     ret = []
#     value = __css_function_cleanup(__value)
#     delim = ' '
#     if any(key in value for key in ["-gradient"]):
        
#         # store key
#         if string_has_parenthesis(__value):
#             key = __value.split('(')[0]
#             ret.append(key)
                    
#         value = string_extract_parenthesis(value) 
#         delim = ','    
        
#         values = string_split_at_delim_outside_parenthesis(string_extract_parenthesis(value), delim=',')

        
#     ret.extend(string_split_at_delim_outside_parenthesis(value, delim=delim))
#     print("property_value_split:", wh.GRAY, __value, "-->", wh.RESET, ret)
#     return ret
    
# # def property_value_apply_lut(__value, lut):

# #     s_out = ""
# #     for val in property_value_split(__value):
# #         print("\t"*1, val)
# #         if col := string_to_selenium_color(val):
# #             lutted = lut_convert_selenium_color(lut, col)
# #             print("property_value_apply_lut:", col, "-->", lutted)
# #             s_out += selenium_color_to_string(lutted)
# #         else:
# #             s_out += val
             
# #     print("property_value_apply_lut:", wh.GRAY, __value, wh.RESET, "-->", wh.GREEN, s_out, wh.RESET)
                
# #     return s_out # a new property value
 

    
#-----------------------------------------
# 
#-----------------------------------------        
# https://colour.readthedocs.io/en/develop/generated/colour.LUT3D.html

# https://pythonhosted.org/cssutils/docs/utilities.html
if __name__ == "__main__":
    
    lut = None
    lut = pillow_lut.load_cube_file(
        #"D:/__BUP_V_KOMPLETT/X/111_BUP/22luts/LUT cube/LUTs Cinematic Color Grading Pack by IWLTBAP/__xIWL_zM_Creative/Creative/xIWL_B-7040-STD.cube" # xIWL_C-9730-STD.cube
        "docs/identity.cube"
    )
    assert lut
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
    
    assert string_has_parenthesis("s") == False
    assert string_has_parenthesis("s(") == False
    assert string_has_parenthesis("s)") == False
    assert string_has_parenthesis("s()") == True

    
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

    
    
    # for s in strings:
    #     print("-"*88)
    #     #string_extract_selenium_colors(s)
    #     property_value_apply_lut(s, lut)
    #     print()
    # exit(0)
    
    # # https://pypi.org/project/Js2Py/
    # # https://github.com/PiotrDabkowski/Js2Py
    # import js2py
    # js2py.eval_js('console.log( "Hello World!" )')
    # add = js2py.eval_js('function add(a, b) {return a + b}')
    # result = add(1, 2) + 3
    # print("result", result)
    # squareofNum = js2py.eval_js("function f(x) {return x*x;}")
    # print("result", squareofNum(5))
    # #exit(0)
    

    import logging
    cssutils.log.setLevel(logging.CRITICAL)

    files = wh.collect_files_endswith(config.project_folder, [".css"], pre="")
    files = wh.files_backup_or_restore_and_exclude(files, postfix_orig=config.postfix_orig, postfix_bup="")
    
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
    
    # https://pythonhosted.org/cssutils/docs/css.html#values
    colors = []
    for file in files:
        
        print("-"*88)
                
        print("\t"*0, wh.CYAN, file, wh.RESET)
        try:
            sheet = cssutils.parseFile(file)
            sheet = cssutils.resolveImports(sheet, target=None) # combine all linked sheets
            
            #print("\t"*1, wh.MAGENTA, cssutils.getUrls(sheet) , wh.RESET) # try out cssutils.getUrls(sheet)
            
            for rule in sheet: # .cssRules:      
                print("\t"*2, ":"*66) 
                print("\t"*2, rule.type, cssutils.css.CSSRule._typestrings[rule.type])
                
                if rule.type in [cssutils.css.CSSRule.STYLE_RULE]:
                    print("\t"*3, "rule.selectorText:", rule.selectorText )   
                        
                    for property in rule.style:
                        print("\t"*4, "property.name", property.name) #  , end=' ')       

                        new_pv = property_traverse_apply_lut(property.value, lut)
                        print("\t"*4, wh.GRAY, property.value, "-->", wh.GREEN, wh.dq(new_pv), wh.RESET)
                        property.value = new_pv
                        ##time.sleep(1)
                            
            ### for rule />                
                            
            print(wh.GREEN, cssbeautifier.beautify(sheet.cssText.decode("utf-8")), wh.RESET)
            
            # save back
            if True:
                wh.string_to_file(
                    cssbeautifier.beautify(sheet.cssText.decode("utf-8")), 
                    file
                )
                                                            
        except Exception as e:
            print(f"{wh.RED} css: {e} {wh.RESET}")
            time.sleep(2)
            exit(1)
            
    print("colors", *colors, sep="\n\t")