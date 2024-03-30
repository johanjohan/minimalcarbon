"""

linear-gradient(180deg, rgba(0, 0, 0, 0.8), rgba(255, 255, 255, 0))

https://gist.github.com/mitchellrj/8472092
take an HTML document and replace all CSS with inline styles, accounting
for all precedence rules. Requires cssutils, cssselect and lxml.Does not
work with pseudo-elements, @font-face, @page and CSS variables as these
cannot be represented by inline CSS.

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

import lxml.html
from lxml import etree
import helpers_lxml as hx

#-----------------------------------------
# selenium 
#-----------------------------------------
"""
    .mick {
        color: black;
    }

    .mick2 {
        color: #000;
    }
    .mick3 {
        color: #000FFF;
    }

    .lucy {
        color: red;
        border:  1px solid purple;
    }

    .lucy2 {
        color: white;
        border-bottom:  1px solid green;
    }

    .hsla {
        color: hsla(100, 100%, 50%, 1)
        /* #55ff00 rgb(85,255,0) */
    }

    .hsla2 {
        color: hsla(235, 100%, 50%, .5)
        /* #0015ff with 50% opacity  0, 21, 255 */
    }

    .hsl {
        color: hsl(100, 100%, 50%)
        /* #0015ff rgb(85,255,0) */
    }

    .ramp {
        background-image: linear-gradient(to right top, rgba(123,234,210,1), #004d7a, #008793, #00bf72, #a8eb12);
    }

    .ramp {
        background-image: repeating-radial-gradient(powderblue, powderblue 8px, white 8px, white 16px);
    }

    .ramp {
        background-image: conic-gradient(from 90deg at 0 0, blue, red);
    }


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

def string_to_selenium_color(string, pre="\t"*1):
    try:
        col = Color.from_string(string) # selenium eats it all ! wow
        print(pre, wh.dq(string), "-->", wh.GREEN, col.rgba, "[", col.hex, "]", col.red, col.green, col.blue, col.alpha, "\n\n", wh.RESET)
        return col
    except Exception as e:
        # print(wh.RED, "string_to_selenium_color: e:", e, wh.RESET)
        # print(wh.RED, "string_to_selenium_color: string:", string, wh.RESET)
        return None
    
def string_is_color(string):
    return True if string_to_selenium_color(string) else False

#-----------------------------------------
# 
#-----------------------------------------
def string_has_parenthesis(s):
    return all(key in s for key in ['(', ')'])

# https://en.wikipedia.org/wiki/Bracket
def string_extract_fore_back(s, fore, back):
    ret = s[s.find(fore)+1:s.rfind(back)] 
    #print(wh.YELLOW, "string_extract_fore_back:", fore, back, ":", s, "-->", ret, wh.RESET)
    return ret

def string_extract_parentheses(s):
    return string_extract_fore_back(s, '(', ')')

def string_extract_braces(s):
    return string_extract_fore_back(s, '{', '}')

def string_extract_brackets(s):
    return string_extract_fore_back(s, '[', ']')

def string_extract_chevrons(s):
    return string_extract_fore_back(s, '<', '>')

def string_embrace_fore_back(s, fore, back):
    return fore + str(s) + back

def string_get_head(s, delim):
    if s is not None:
        ret = s.split(delim)[0]
        print("string_get_head: ret:", ret)
        return ret
    else:
        print(wh.RED, "string_get_head: s is None", wh.RESET)
        exit(1)

# https://stackoverflow.com/questions/26633452/how-to-split-by-commas-that-are-not-within-parentheses
def string_split_at_delim_outside_parenthesis(value, delim):
    #ret = re.split(r',\s*(?![^()]*\))', value) # ok"
    ret = re.split(rf"{delim}(?![^(]*\))", value)
    print("string_split_at_comma_outside_parenthesis:", wh.dq(delim), wh.MAGENTA, ret, wh.RESET)
    return ret

def string_split_at_comma_outside_parenthesis(value):
    return string_split_at_delim_outside_parenthesis(value, delim=',')
        
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
    
# linear-gradient(red, yellow, green, purple, #123456, #987654, rgb(255,128,96), rgba(255,128,96,1)); 
# linear-gradient(to right, #60c7f2 0%, #00a5e6 100%)
#  args_comma:  ['to right', '#60c7f2 0%', '#00a5e6 100%']
def function_split_traverse_apply_lut(__value, lut):   
    
    #print("function_split_traverse_apply_lut:", __value)
    
    assert  string_has_parenthesis(__value)
    value   = __css_function_cleanup(__value)
    name    = value.split('(')[0]
    args_comma    = string_split_at_delim_outside_parenthesis(
        string_extract_parentheses(value), 
        ','
    )
    print("\t\t\t", wh.GRAY, "name:", wh.MAGENTA, name, wh.RESET)
    print("\t\t\t", wh.GRAY, "args_comma:", wh.CYAN,    args_comma, wh.RESET)
    
    # these are the comma-separated args_comma: ['to right top', 'rgba(123,234,210,1)', '#004d7a', '#008793', '#00bf72', '#a8eb12']
    new_args_comma = []
    for arg in args_comma:
        try:
            pv = cssutils.css.PropertyValue(arg)
            print("\t\t\t", "pv:", pv.length, pv)
            
            if pv.length > 1:
                # split by space
                args_space    = string_split_at_delim_outside_parenthesis(
                    pv.cssText, 
                    ' '
                )    
                print("\t\t\t\t", wh.GRAY, "args_space:", wh.CYAN, args_space, wh.RESET)
                new_args_space = []
                for arg_space in args_space:
                    if v := string_to_selenium_color(arg_space):
                        lut_col         = hl.lut_convert_rgb(lut, v.red, v.green, v.blue)
                        lut_col.alpha   = v.alpha # restore original
                        new_args_space.append( selenium_color_to_string(lut_col) ) # rgba(...)
                    else:
                        new_args_space.append(arg_space)
                ## for args_space />
                
                new_args_space_joined = ' '.join(new_args_space)
                print("\t\t\t\t\t", wh.GRAY, "new_args_space_joined:", wh.CYAN, new_args_space_joined, wh.RESET)
                
                # recombine space-split items
                new_args_comma.append(
                    new_args_space_joined
                )
                  
            elif pv.length == 1:
                v = pv[0]
                if v.type == cssutils.css.Value.COLOR_VALUE:
                    lut_col         = hl.lut_convert_rgb(lut, v.red, v.green, v.blue)
                    lut_col.alpha   = v.alpha # restore original
                    new_args_comma.append( selenium_color_to_string(lut_col) ) # rgba(...)
                else:
                    new_args_comma.append(pv.cssText) # whatever
            else:
                assert False
        except Exception as e: # cssutils.css.PropertyValue # can be MSValue...
            print("\t\t\t", wh.YELLOW, "ISSUE:", e, wh.RESET, "--> will append arg directly:", wh.dq(arg))
            new_args_comma.append(arg)
            time.sleep(0)
    ### for args_comma />  
    
    ret = f"{name}({','.join(new_args_comma)})"
    
    print("function_split_traverse_apply_lut: ret:", ret)
    
    return ret # the new function: linear-gradient(to right top, rgba(123, 234, 210, 1), rgba(0, 77, 122, 1), rgba(0, 135, 147, 1), rgba(0, 191, 114, 1), rgba(168, 235, 18, 1))
 
def property_traverse_apply_lut(__value, __lut):

    print("\t"*4, "property_traverse_apply_lut", wh.MAGENTA, __value, wh.RESET)
    ret = []
    for v in cssutils.css.PropertyValue(__value):
        
        #print("\t"*4, "v:", wh.MAGENTA, v, wh.RESET)
        
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
        
    # # # import chromato 
    
    # # assert string_has_parenthesis("s") == False
    # # assert string_has_parenthesis("s(") == False
    # # assert string_has_parenthesis("s)") == False
    # # assert string_has_parenthesis("s()") == True
    
    # # string_extract_braces("""
                          
    
    # # "glossary": {
    # #     "title": "example glossary",
	# # 	"GlossDiv": {
    # #         "title": "S",
	# # 		"GlossList": {
    # #             "GlossEntry": {
    # #                 "ID": "SGML",
	# # 				"SortAs": "SGML",
	# # 				"GlossTerm": "Standard Generalized Markup Language",
	# # 				"Acronym": "SGML",
	# # 				"Abbrev": "ISO 8879:1986",
	# # 				"GlossDef": {
    # #                     "para": "A meta-markup language, used to create markup languages such as DocBook.",
	# # 					"GlossSeeAlso": ["GML", "XML"]
    # #                 },
	# # 				"GlossSee": "markup"
    # #             }
    # #         }
    # #     }
    # # }
                   
                          
                          
    # #                       """)
    # # exit(0)

    # # # strings = [
    # # #            "#ff0000",
    # # #            "#f00",
    # # #            "background: border-box #f00;",
    # # #            "background: \t rgba(0,0,\t  255,1);\n\t\t\t\t\t\t",
    # # #            "background: blue;",
    # # #            "background: purple;",
    # # #            "unknown_color",
    # # #            "background: rgba(0,0,255,0.5);",
    # # #            "some ramp: #f00 to #0f0 to #00f",
    # # #            "background-image: url('paper.gif');",
    # # #            "background-color: #cccccc;",
    # # #            "linear-gradient(180deg, rgba(0, 0, 0, 0.8), rgba(255, 255, 255, 0))",
    # # #            "linear-gradient(red, yellow, green, purple, #123456, #987654, rgb(255,128,96), rgba(255,128,96,1)); ",
    # # #            ]

    
    
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
    
    s = """
@supports (-webkit-text-stroke: thin) {
    .gradient-color {
        background: linear-gradient(to right, #60c7f2 0%, #00a5e6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text
        }
    }    
    
    """
    
    # string_get_head(s, "{")
    # string_get_head("xxx", "{")
    # string_get_head("", "{")
    # string_get_head(None, "{")
    # exit(0)
    

    import logging
    cssutils.log.setLevel(logging.CRITICAL)

    #-----------------------------------------
    # 
    #----------------------------------------- 
    files = wh.collect_files_endswith(config.project_folder, [".css"], excludes=config.excludes_postfix, pre="")
    ######files = wh.files_backup_or_restore_and_exclude(files, postfix_orig=config.postfix_orig, postfix_bup="")
    #files = []
    #print("files", *files, sep="\n\t")
    
    # https://pythonhosted.org/cssutils/docs/css.html#values
    #-----------------------------------------
    # external stylesheets .css
    #----------------------------------------- 
    """
    @supports (-webkit-text-stroke: thin) {
        gradient-color {
            background: linear-gradient(to right, #60c7f2 0%, #00a5e6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text
        }
    }
    """
    if True:
        for file in files:
            
            print("-"*88)
                    
            print("\t"*0, wh.CYAN, file, wh.RESET)
            try:
                sheet = cssutils.parseFile(file)
                sheet = cssutils.resolveImports(sheet, target=None) # combine all linked sheets
                
                #print("\t"*1, wh.MAGENTA, cssutils.getUrls(sheet) , wh.RESET) # TODO CHECK NOTE cssutils.getUrls(sheet)
                
                for rule in sheet.cssRules:      
                    print("\t"*2, wh.BLUE, "::", os.path.basename(file), ":"*66, wh.RESET) 
                    print("\t"*2, "rule     :", rule )   
                    print("\t"*2, "rule.type:", rule.type, cssutils.css.CSSRule._typestrings[rule.type])
                    
                    if rule.type in [cssutils.css.CSSRule.STYLE_RULE]:
                        
                        print("\t"*3, "rule.style:", rule.style )   
                        print("\t"*3, "rule.selectorText:", rule.selectorText )   
                    
                        for property in rule.style:
                            print("\t"*4, "property.name    :", wh.CYAN, wh.dq(property.name) ,    wh.RESET)     
                            print("\t"*4, "property.value   :", wh.CYAN, wh.dq(property.value),    wh.RESET)      
                            print("\t"*4, "property.priority:", wh.CYAN, wh.dq(property.priority), wh.RESET)        

                            new_pv = property_traverse_apply_lut(property.value, lut)
                            print("\t"*4, wh.GRAY, wh.dq(property.value), "-->", wh.RESET)
                            print("\t"*4, wh.GREEN, wh.dq(new_pv), wh.RESET)
                            property.value = new_pv
                            ##time.sleep(1)
                            
                    # ITERATIVE FOCUS POCUS FOCUS         
                            
                    elif rule.type in [cssutils.css.CSSRule.MEDIA_RULE]:
                        print("\t"*3, "rule.cssText :", rule.cssText )   
                        print("\t"*3, "rule.cssRules:", rule.cssRules )   
                        
                        for property in rule.cssRules[0].style:
                            print("\t"*4, "property.name    :", wh.CYAN, wh.dq(property.name) ,    wh.RESET)     
                            print("\t"*4, "property.value   :", wh.CYAN, wh.dq(property.value),    wh.RESET)      
                            print("\t"*4, "property.priority:", wh.CYAN, wh.dq(property.priority), wh.RESET)        

                            new_pv = property_traverse_apply_lut(property.value, lut)
                            print("\t"*4, wh.GRAY, wh.dq(property.value), "-->", wh.RESET)
                            print("\t"*4, wh.GREEN, wh.dq(new_pv), wh.RESET)
                            property.value = new_pv                        
                        
                    elif False and rule.type in [cssutils.css.CSSRule.UNKNOWN_RULE]: 
                        
                        
                        # <<<<<<<<< TODO <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                        print(wh.YELLOW, "GLITCHY!!! bad {} {}")
                        
                        print("\t"*3, wh.YELLOW, "UNKNOWN_RULE: rule.cssText:", rule.cssText , wh.RESET)   
                        time.sleep(1)
                        
                        name0       = string_get_head(rule.cssText, "{")
                        inner0      = string_extract_braces(rule.cssText)
                        name1       = string_get_head(inner0, "{")
                        inner1      = string_extract_braces(inner0)
                        inner1_list = wh.string_remove_whitespace(inner1).split(';')
                        
                        print(wh.MAGENTA)
                        print("name0      :", name0)     # @supports (-webkit-text-stroke: thin)
                        print("inner0     :", inner0)    # . gradient-color {...}
                        print("name1      :", name1)     # . gradient-color
                        print("inner1     :", inner1)    # ...
                        print("inner1_list:", inner1_list)
                        print(wh.RESET)
                        
                        for i, cssText in enumerate(inner1_list):
                            style = cssutils.css.CSSStyleDeclaration(cssText=cssText) # item
                            for key in style.keys():
                                value           = style.getPropertyValue(key)
                                inner1_list[i]  = f"{key}: " + property_traverse_apply_lut(value, lut) # https://stackoverflow.com/questions/4081217/how-to-modify-list-entries-during-for-loop
                                #print("\t", key, ":",  value, "-->", inner1_list[i])
                                
                        print("inner1_list: after:", inner1_list)
                        
                        rule_text = f"""
                            {name0} {{
                                {name1} {{
                                    {'; '.join(inner1_list)}
                                }}
                            }}
                        """
                        print("rule_text", wh.MAGENTA, cssbeautifier.beautify(rule_text), wh.RESET)
                        
                        # # ss = cssutils.css.CSSRule(rule_text)
                        # # print("ss", ss)
                        
                        
                        
                       
                        # https://github.com/jaraco/cssutils/issues/6
                        
                        
                        # # # # new_rule = cssutils.css.CSSStyleDeclaration(cssText=rule_text)
                        # # # # new_rule = cssutils.css.CSSMediaRuleRule(cssText=rule_text)
                        # # # # print("new_rule", new_rule)
                        
                        #######rule.style = ss
                                
                        sheet.add(rule_text)        
                                
                ### for rule />      
                
                
                                
                print(wh.GREEN, cssbeautifier.beautify(sheet.cssText.decode("utf-8")), wh.RESET)
                time.sleep(1)
                
                # save back
                if True:
                    wh.string_to_file(
                        cssbeautifier.beautify(sheet.cssText.decode("utf-8")), 
                        file
                    )
                
                ####exit(0)
                                                                
            except Exception as e:
                print(f"{wh.RED} css: {e} {wh.RESET}")
                time.sleep(2)
                exit(1)

    #-----------------------------------------
    # index.html: internal stylesheets and style-attributes
    #-----------------------------------------  
    files = wh.collect_files_endswith(config.project_folder, ["index.html"], excludes=config.excludes_postfix, pre="")
    ########files = wh.files_backup_or_restore_and_exclude(files, postfix_orig=config.postfix_orig, postfix_bup="")
    #print("files", *files, sep="\n\t")
    ##files = []           
    
    # https://pythonhosted.org/cssutils/docs/css.html#values
    for file in files:
        
        print("#"*99)
        print("file:", file)
                
        content = wh.string_from_file(file)
        tree    = lxml.html.fromstring(content)
        
        # all tags with style attributes
        if True:
            #for node in  tree.xpath("//*/@style[not(.="")]"): # all tages with @style and not empty # ERR
            for node in  tree.xpath("//*/@style"): # all tages with @style and not empty # ERR
                
                print("\t", ":"*88)
                try:
                    style_text = node.attrib['style'] ## TODO getProperty()
                except:
                    continue
                
                if not style_text:
                    continue
                                
                print(wh.MAGENTA, wh.dq(style_text), wh.RESET)
                print(wh.CYAN, cssbeautifier.beautify(style_text), wh.RESET)
                
                style = cssutils.parseStyle(style_text) 
                print(style)
                print ("\t\t", "style.cssText:", wh.MAGENTA, wh.dq(style.cssText), wh.RESET)
                
                for property in style:
                    print("\t"*4, "property.name    :", wh.CYAN, wh.dq(property.name) ,    wh.RESET)     
                    print("\t"*4, "property.value   :", wh.CYAN, wh.dq(property.value),    wh.RESET)      
                    print("\t"*4, "property.priority:", wh.CYAN, wh.dq(property.priority), wh.RESET)      

                    new_pv = property_traverse_apply_lut(property.value, lut)
                    print("\t"*4, wh.GRAY,  wh.dq(property.value), "-->", wh.RESET)
                    print("\t"*4, wh.GREEN, wh.dq(new_pv), wh.RESET)
                    property.value = new_pv
                        
                # assign style back to lxml
                node.attrib['style'] =  property.cssText
                #print("\t\t", wh.GREEN, node.attrib['style'], wh.RESET)
            
        ### for node
        
        # all internal style sheets
        if False:
            for node in tree.xpath("//style"):
                print("\t", "|"*88)
                style_text = node.text_content()
                print(wh.CYAN, cssbeautifier.beautify(style_text), wh.RESET)
                
                sheet = cssutils.parseString(style_text) 
                print ("\t\t", "style.cssText:", wh.MAGENTA, sheet.cssText, wh.RESET)
                
                for rule in sheet:
                    if rule.type in [cssutils.css.CSSRule.STYLE_RULE]:
                        for property in rule.style:
                            print(property)
                            print("\t"*4, "property.name    :", wh.CYAN, wh.dq(property.name) ,    wh.RESET)     
                            print("\t"*4, "property.value   :", wh.CYAN, wh.dq(property.value),    wh.RESET)      
                            print("\t"*4, "property.priority:", wh.CYAN, wh.dq(property.priority), wh.RESET)      

                            new_pv = property_traverse_apply_lut(property.value, lut)
                            print("\t"*4, wh.GRAY,  wh.dq(property.value), "-->", wh.RESET)
                            print("\t"*4, wh.GREEN, wh.dq(new_pv), wh.RESET)
                            property.value = new_pv
                                
                # assign style back to lxml
                node.text =  sheet.cssText.decode("utf-8") 
                print(wh.GREEN, cssbeautifier.beautify(node.text_content()), wh.RESET)
            ### for node
                
        
        content = etree.tostring(tree, pretty_print=True).decode("utf-8")
        print(wh.GREEN, content, wh.RESET)
        if True:
            print("string_to_file", wh.GRAY, file, wh.RESET)
            wh.string_to_file(
                content, 
                file
            )    
            
    ### for file
        
    print("all done.")
    
    #-----------------------------------------
    # 
    #----------------------------------------- 