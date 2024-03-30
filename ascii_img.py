"""
TODO
this creates
a python file or raw string
holding the layers of the main color clustrers
which will be css/html to replace images

https://stackoverflow.com/questions/30097953/ascii-art-sorting-an-array-of-ascii-characters-by-brightness-levels-c-c
$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'.

could do RLE
https://stackoverflow.com/questions/18948382/run-length-encoding-in-python

from re import sub

def encode(text):
    '''
    Doctest:
        >>> encode('WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW')
        '12W1B12W3B24W1B14W'    
    '''
    return sub(r'(.)\1*', lambda m: str(len(m.group(0))) + m.group(1),
               text)

def decode(text): 
    '''
    Doctest:
        >>> decode('12W1B12W3B24W1B14W')
        'WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW'
    '''
    return sub(r'(\d+)(\D)', lambda m: m.group(2) * int(m.group(1)),
               text)

textin = "WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW"
assert decode(encode(textin)) == textin
"""

# great turning ascii earth
# https://speckyboy.com/css-javascript-ascii-artwork-snippets/
# https://www.jonathan-petitcolas.com/ascii-art-converter/

# better overlay several colored pre tags

# https://www.geeksforgeeks.org/converting-image-ascii-image-python/
# Python code to convert an image to ASCII image.
import sys
import random
import argparse
import numpy as np
import math

import PIL
from PIL import Image, ImageOps

"""
https://stackoverflow.com/questions/3241929/python-find-dominant-most-common-color-in-an-image

Here's code making use of Pillow and Scipy's cluster package.

For simplicity I've hardcoded the filename as "image.jpg". 
Resizing the image is for speed: if you don't mind the wait, 
comment out the resize call. 
When run on this sample image of blue peppers it usually says the dominant colour is #d8c865, 
which corresponds roughly to the bright yellowish area to the lower left of the two peppers. 
I say "usually" because the clustering algorithm used has a degree of randomness to it. 
There are various ways you could change this, but for your purposes it may suit well. 
(Check out the options on the kmeans2() variant if you need deterministic results.)
"""
import binascii
import scipy
import scipy.misc
import scipy.cluster

import cssbeautifier

import helpers_web as hw

from re import sub

def rle_encode(text):
    return sub(r'(.)\1*', lambda m: str(len(m.group(0))) + m.group(1),
               text)

def rle_decode(text):
    return sub(r'(\d+)(\D)', lambda m: m.group(2) * int(m.group(1)),
               text)
    

pfx = "ascii-"

body_start  = lambda : f"""
    <html>
        <head>
            <title>test</title>
        </head>
        <body>
    """
body_end    = lambda : """</body></html>"""

div_start   = lambda id : f"<div id='{id}' class='{pfx}parent'>"
div_end     = lambda : "</div>"

cdata_start = lambda : "<![CDATA["
cdata_end   = lambda : "]]>"

pre_start   = lambda n : f"<pre class='{pfx}child {pfx}child-{n} {pfx}art' id='{pfx}layer-{n}'>"
pre_end     = lambda : "</pre>"


def sanitize_cdata(s):
    s = s.replace(cdata_end(), "??i") # "]]>"
    for c in ('&', '<', '>', ']'):
        s = s.replace(c, "?")
    return s

# https://stackoverflow.com/questions/2784183/what-does-cdata-in-xml-mean
#  however, I can't use the CEND sequence. 
# If I need to use CEND I must escape one of the brackets or the greater-than sign using concatenated CDATA sections


def style(colors, bg_color=[0,255,0], font_size="2vw", line_height="1.2em"):
    
    def child(num, top, left, color):
        return f"""
            .{pfx}child-{num} {{
                color:  {rgb_to_hex(color)};
            }}  

            """
        return f"""
            .{pfx}child-{num} {{
                left:   {left};
                top:    {top};
                color:  {rgb_to_hex(color)};
            }}  

            """
    
    colors = list(colors)
    html = f"""
    <style>
    
    
    body {{

        background-color: black; 
        margin:0; padding:0;
        color:white;
        font-family: sans-serif;
    }}
    
    
            .{pfx}parent {{
                position:   relative;
                margin:     0;   
                padding:    0;
                width:      100%;
                height:     700;
                background-color: {rgb_to_hex(bg_color)};
                z-index:        -2000;
            }}
            
            .{pfx}art {{
                font-family:    monospace;
                white-space:    pre;
                font-size:      {font_size};
                font-weight:    700;
                line-height:    {line_height};
                z-index:        -1000;
            }}
        
            .{pfx}child {{
                margin:0;   padding:0;
                position:   absolute;
                left:       0;
                top:        0;
            }}
        
    """
    
    for i, color in enumerate(colors):
        html += child(i, 0, 0, color) # i*2, i*2
        
    html += """
    
    </style>
    
    """
    
    return cssbeautifier.beautify(html)
 
def script(num_layers, start_layer=0, fps=12):
    
    assert start_layer < num_layers
        
    html = f"""

    <script>

        var fps = {fps} // change on mobile
        var startTime = new Date();
        var myVar = setInterval(div_set_pos, (1.0/fps) * 1000);
        
        function div_set_pos() {{

            elapsed = (new Date() - startTime) / 1000.0; // secs
            fade    = Math.min(1, elapsed / 3.0)
            
            for (let i = {start_layer}; i < {num_layers}; i++) {{
                
                irev = {start_layer} -1 - i;

                let scale   = 1;
                let speed   = 2; // 0.44
                //let radius  = Math.sin(i/3.0) * scale; //1 + i*0.333
                let radius  = i * scale; // 1 + i*0.333

                layer_id    = "{pfx}layer-" + parseInt(i)
                let layer   = document.getElementById(layer_id);

                x = elapsed * speed / (irev * 1)
                posx = Math.cos(x) * radius
                posy = Math.sin(x) * radius;
                
                layer.style.position    = "absolute";
                layer.style.left        = (fade * posx)+'px';
                layer.style.top         = (fade * posy)+'px';

                console.log(elapsed, fade, layer_id, x, layer.style.left, layer.style.top);
            }}


        }}
    </script>

    """
    #print(html)
    return html

# gray scale level values from:
# http://paulbourke.net/dataformats/asciiart/
# 70 levels of gray

gNoCDATA    = "$@B%8WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}?-_+~i!lI;:,\"^`'. " # no []
g70         = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. " # 70 levels
g10         = '@%#*+=-:. ' # 10 levels of gray
g95         = "@MBHENR#KWXDFPQASUZbdehx*8Gm&04LOVYkpq5Tagns69owz$CIu23Jcfry%1v7l+it[] {}?j|()=~!-/<>\"^_';,:`. " # 96 levels
g2          = '@*+-. '
gXX         = "@MBHENR#KWXDFPQASUZbdehx*8Gm&04LOVYkpq5Tagns69owz$CIu23Jcfry%1v7l+it{}?j|()=~!-/\"^_';,:`. " # 90 levels

gKapital    = hw.string_reverse(""" .-°,:'^;_ι/r!"}?()jLτ+={Yv•citγ7T]F3ελυJfxyu%V[lnszîoο1çh9CI½ekUü5«»¼ùη2PöΠXûζπχωOSaαZw£ôA*H08KÜèé&ρEGbÖêdDRÄàá46pßqâämÉNQδgMB§W""")
gJap        = hw.string_reverse(" ヽゝノぃっイトょとてウグちぁわガ木ゟ允中五乞共全丹史拉争仲体命串典例係孤商戚侵侮勲凝喚属彙審鍵鎌籠騰欄")
gJap        = hw.string_reverse("二了人上六寸少勺仁夕乃木今牛示占女打丘乞代企全先作世伏幸封乱仲伎参佐侍享堂侃例剝員喪勅候便事侵側偶唱個像劇墨属健憾簡儀瞬圏髄籠謄糧欄")
gUtf        = hw.string_reverse(""" ˙˺.˘,:ʳ;_×¡?¿iFuo95O*EDÀÅgMǿ§WǌǢǾ∯ѨℕǊǄѬ┣ℍℌ╫⅀Ⅷℜ◉▥▃▨▍◕▣◚▩●▀▌■∎▅▋◼▊◘▇▉▓█""")
gUtf        = hw.string_reverse(""" ˙⁻ˈ˺¨`.˔◝˘-¯,¹҇:'²ʳ^‸;˭⁝_|ˠ×/r¡\!?(<¿+Yiº7F3Ju%lo1h9eU5$XOZA*0&EÒdD4pÀqmÅÃNg@ĒMĎÆǿ#Ń§ģƣWÑğǌƁὪǢǲƢǾǱᾪ∯₨ŴѨᾮ⋓ℕ⇯∰Ǌ₰ǆǄ▬ⅅѬ‣ↇ┣Ѽ┫ℍℝℹℌ◑╫⁑⅀Ⅷℜ◉▤▥▃▧▨ↈ▍◕▣◚▦◛▩●▀▚▌■∎▅▋◼▆▒▊▙▛◘▇▉▓◙█""")


g = g70
g = g2
g = gXX
g = "01010101010101010101010101010101010101010101010101010101010101010101010101 "
g = "KARLSRUHEdigital."
g = gNoCDATA
g = g10
g = gKapital

def clamp(x): 
  return max(0, min(x, 255))

def rgb_to_hex(rgb): # [r,g,b] --> #rrggbb
    r,g,b = rgb
    return "#{:02x}{:02x}{:02x}".format( clamp(round(r)), clamp(round(g)), clamp(round(b)) )

def rgb_to_luminance(rgb):
    #print("rgb", rgb)
    r,g,b = rgb
    return round(0.2126*r + 0.7152*g + 0.0722*b) # / 255.0

def map(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def get_average_l(image):
    """
    Given PIL Image, return average value of grayscale value
    """
    # get image as numpy array
    im = np.array(image)

    # get shape
    w, h = im.shape

    # get average
    return np.average(im.reshape(w*h))

# full_image may be None
def convert_image_to_ascii(layer, cols, scale, gscale=gNoCDATA, reverse_gscale=False, full_image=None):
    """
    Given Image and dims (rows, cols) returns an m*n list of Images
    """

    print("convert_image_to_ascii:", "cols  :", cols)
    print("convert_image_to_ascii:", "scale :", scale)
    print("convert_image_to_ascii:", "gscale:", len(gscale), gscale)
    
    if full_image:
        ####full_image = full_image.convert('L')
        print("\t", "using full_image as avg ref!!!!")
        
    # declare globals
    len_gscale_1 = len(gscale) - 1
    
    layer = layer.convert('L')
    # store dimensions
    W, H = layer.size ### [0], layer.size[1]
    print("\t", "input layer dims: %d x %d" % (W, H))

    # compute width of tile
    assert cols > 0
    w = W/cols

    # compute tile height based on aspect ratio and scale
    assert scale > 0
    h = w/scale

    # compute number of rows
    assert h > 0
    rows = int(H/h)

    print("\t", "cols: %d, rows: %d" % (cols, rows))
    print("\t", "tile dims: %d x %d" % (w, h))

    # check if layer size is too small
    if cols > W or rows > H:
        print("ERROR: Image layer too small for specified cols!")
        exit(0)

    # ascii layer is a list of character strings
    aimg = []
    # generate list of dimensions
    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)

        # correct last tile
        if j == rows-1:
            y2 = H

        # append an empty string
        aimg.append("")

        for i in range(cols):

            # crop layer to tile
            x1 = int(i*w)
            x2 = int((i+1)*w)

            # correct last tile
            if i == cols-1:
                x2 = W
                
            # crop layer to extract tile
            # # if full_image:
            # #     img = full_image.crop((x1, y1, x2, y2))
            # # else:
            img = layer.crop((x1, y1, x2, y2))

            # get average luminance
            avg = int(get_average_l(img))
                        
            g       = gscale
            g_index = -1 # last
            if reverse_gscale:
                g       = ''.join(reversed(gscale))
                g_index = 0 # first
            
            # look up
            if full_image:
                # look up instead in full_image
                gsval = g[int((avg * len_gscale_1) / 255)]
                if gsval != g[g_index]: # the last & empty element
                    gsval = full_image[j][i]
            else:
                # look up ascii char
                gsval = g[int((avg * len_gscale_1) / 255)]

            # append ascii char to string
            aimg[j] += gsval
            #print("\t\t", j, aimg[j]) # row, aimg[j] is growing

    # return txt image
    return aimg, cols, rows

def scipy_to_pil(np_image, shape, mode='RGB'): # None
    # print("scipy_to_pil: shape:", shape)
    # print("scipy_to_pil: mode :", mode)
    image = Image.fromarray(
        np.uint8(
            np_image.reshape(*shape).astype(np.uint8) # c.reshape(*shape).astype(np.uint8))
        )
    )
    return image.convert(mode) if mode else image

def pil_image_threshold(image, threshold):
    return image.point( lambda p: 255 if p > threshold else 0 )
    
def pil_image_segmentation(image, num_clusters):

        print("pil_image_segmentation: num_clusters:", num_clusters)
        
        image   = image.convert("RGB")
        ar      = np.asarray(image)
        shape   = ar.shape # store original
        ar      = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)
    
        # colors are float rgb colors
        print("\t", "kmeans...")
        colors, dist = scipy.cluster.vq.kmeans(ar, num_clusters)
        colors = [[round(num) for num in color] for color in colors] # to ints
        #print('colors: dist:', dist, *colors, sep="\n\t")
        
        vecs,   dist    = scipy.cluster.vq.vq(ar, colors)         # assign colors
        #print("\t", "vecs", len(vecs), vecs)
        #print("\t", "dist", len(dist), dist)
        counts, bins    = np.histogram(vecs, len(colors))
        #print("\t", "counts", len(counts), counts)
        #print("\t", "bins  ", len(bins), bins)
     
        index_max   = np.argmax(counts)                    # find most frequent
        peak        = colors[index_max]
        colour      = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
        print("\t", 'most frequent is %s (#%s)' % (peak, colour))
        
        # layers
        layers = []
        for i, color in enumerate(colors):
            #print("\t\t", "color:", color)
            c = ar.copy()
            c.fill(0)
            c[scipy.r_[np.where(vecs==i)],:] = color
            PIL_image = scipy_to_pil(c, shape, 'RGB') 
            layers.append(PIL_image)
            #PIL_image.save("__layer_" + str(i) + ".png")
            
        # composite
        c = ar.copy()
        c.fill(0)
        for i, color in enumerate(colors):
            c[scipy.r_[np.where(vecs==i)],:] = color
        composite = scipy_to_pil(c, shape, 'RGB') 
        
        assert (len(layers) == len(colors) == len(counts))
        
        print("pil_image_segmentation: all done.")
        
        return composite, layers, colors, counts
    
# https://www.geeksforgeeks.org/extract-dominant-colors-of-an-image-using-python/

# call main
if __name__ == '__main__':
    
    def image_show(image, secs=0.25):
        path = "__tmp.png"
        image.save(path)
        import subprocess
        import time
        # https://www.etcwiki.org/wiki/IrfanView_Command_Line_Options
        p = subprocess.Popen(["C:/Program Files/IrfanView/i_view64.exe", path])
        time.sleep(secs)
        p.kill()
        import os
        os.remove(path)
    
    image_path = "V:/00download/manteljulia_271367352_343627254254777_2341924037822352416_n.jpg"
    image_path = "D:/__BUP_V_KOMPLETT/X/111_BUP/33projects/2022/2022-karlsruhe.digital/2022/beautiful-girl-flower-rainbow-background-22116179.jpg"
    image_path = "Header-1.jpg"
    image_path = "bunte_nacht_der_digitalisierung_hero_slider.jpg"
    image_path = "bunte_nacht_der_digitalisierung_hero_slider_unpowered.webp"
    image_path = "kai.jpg"
    image_path = "__ascii/kai.jpg"

    descStr = "This program converts an image into ASCII art."
    
    
    
    parser = argparse.ArgumentParser(description=descStr)
    # add expected arguments
    parser.add_argument('--file', dest='imgFile', type=str, default=image_path, required=False)
    parser.add_argument('--scale', dest='scale', type=float, default=0.5, required=False) # 0.43 aspect
    parser.add_argument('--out', dest='outFile', default="__out.txt", required=False)
    parser.add_argument('--cols', dest='cols', type=int, default=150, required=False) # 80
    parser.add_argument('--num_clusters', type=int, default=16, required=False) # 80 len(g)
    args = parser.parse_args()
    

    if args.num_clusters > len(g):
        args.num_clusters = min(args.num_clusters, len(g))
        print("args.num_clusters: fced to:", args.num_clusters)

    print(descStr)
    root_image = Image.open(args.imgFile)
    root_image.thumbnail((args.cols, args.cols), resample=Image.Resampling.LANCZOS) # save time, look better!
    #root_image = ImageOps.equalize(root_image, mask = None)
    root_image = ImageOps.autocontrast(root_image, mask = None)
    root_aimg, cols, rows = convert_image_to_ascii(root_image, args.cols, args.scale, gscale=g)  
    root_aimg_string = "\n".join(root_aimg)
    with open("__out_root.html", mode="w", encoding="utf-8") as fp:
        fp.write("<pre>" + root_aimg_string + "</pre>")
    #root_image.show()
    image_show(root_image)
    ##print(root_aimg) # list of row strings
    
   
   
    
    if False:
        
        num_layers = 3
        assert num_layers > 1
        min_bright = 35
        max_bright = 210
        step = math.floor(max_bright/(num_layers))        
        
        cnt = 0
        for i in range(num_layers):
            cnt += 1
            print(cnt, "-"*88)
            
            #threshold = map(i, 0, num_layers-1, min_bright, max_bright)
            threshold = map(i, 0, num_layers-1, max_bright, min_bright)
            print("threshold:", threshold)
            
            # ImageOps.posterize(simg, bits=i)
            
            image = root_image.copy()
            image = image.point( lambda p: 255 if p > threshold else 0 )
            aimg = convert_image_to_ascii(image, args.cols, args.scale)
            for row in aimg:
                print(row)
            print()
            image.show()


    composite, layers, colors, counts = pil_image_segmentation(root_image, num_clusters=args.num_clusters)
    image_show(composite)
 

    def color_darkest(colors, key=lambda x:rgb_to_luminance(x), reverse=False):
        print(*colors, sep="\n\t")
        colors = sorted(colors, key=key, reverse=reverse)
        print(*colors, sep="\n\t")
        return colors[0]
    
    sort_by_count = lambda x : x[2]
    sort_by_color = lambda x : x[1]
    sort_by_lum   = lambda x : rgb_to_luminance(x[1])
        
    zipped = zip(layers, colors, counts)
    # # zipped = list(zipped) # needed for sorting
    # # zipped = sorted(zipped, key = sort_by_count, reverse=False)
    # # print("before sort:", *zipped, sep="\n\t")
    # # zipped = sorted(zipped, key = sort_by_lum, reverse=False)
    # # print("after sort:", *zipped, sep="\n\t")
    
    html = body_start()
    html += style(colors, bg_color=color_darkest(colors), font_size="1.3vw", line_height="1.2em")
    html += div_start(id="ascii-div") + "\n"
    
    for i, (layer, color, count) in enumerate(zipped):
        
        print("\n"*3)
        print(round(i/(args.num_clusters-1),2), "-"*88)
        print("\t", i, count, color)
        
        html += pre_start(i) 
        
        print("rgb_to_luminance:", round(rgb_to_luminance(color), 3), rgb_to_hex(color), color, "count:", count)
        ##layer = pil_image_threshold(layer.convert("RGB"), 0)
        
        threshold = 0
        layer_neg = layer #.copy().point( lambda p: 0 if p > threshold else 255 )
        
        aimg, cols, rows = convert_image_to_ascii(layer_neg, args.cols, args.scale, gscale=g, reverse_gscale=True, full_image=root_aimg) # root_image       
        #print(aimg)
        aimg_string = "\n".join(aimg)
        aimg_string = sanitize_cdata(aimg_string)
        #print(aimg_string)
            
        ###html += cdata_start()+ "\n" + aimg_string + cdata_end() + "\n"
        html += "\n" + aimg_string + "\n"
        
        image_show(layer)
        
        html += pre_end() + "\n"
    ### for />
    
    html += div_end() + "\n"
    html += script(args.num_clusters, start_layer=0, fps=25)
    html += body_end()
    
    if True:
        from bs4 import BeautifulSoup as bs
        soup = bs(html, 'html.parser')  
        html = soup.prettify()
    
    #print(html)
    import datetime
    date_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = f"__ascii/__acsii_test_{date_time}.html"
    
    with open(out_path, mode="w", encoding="utf-8") as fp:
        fp.write(html)
    
    with open(out_path + "_RLE.html", mode="w", encoding="utf-8") as fp:
        fp.write(rle_encode(html))
    
    print("\n"*3)
    


    