"""
TODO
this creates
a python file or raw string
holding the layers of the main color clustrers
which will be css/html to replace images

https://stackoverflow.com/questions/30097953/ascii-art-sorting-an-array-of-ascii-characters-by-brightness-levels-c-c
$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'.
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

from PIL import Image, ImageOps

# gray scale level values from:
# http://paulbourke.net/dataformats/asciiart/

# 70 levels of gray
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. " # 70 levels

# 10 levels of gray
gscale2 = '@%#*+=-:. '
gscale2 = 'MX#*+=-:. '

def map(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def getAverageL(image):
    """
    Given PIL Image, return average value of grayscale value
    """
    # get image as numpy array
    im = np.array(image)

    # get shape
    w, h = im.shape

    # get average
    return np.average(im.reshape(w*h))


def covertImageToAscii(image, cols, scale, moreLevels):
    """
    Given Image and dims (rows, cols) returns an m*n list of Images
    """
    # declare globals
    global gscale1, gscale2
    
    image = image.convert('L')
    # store dimensions
    W, H = image.size[0], image.size[1]
    print("input image dims: %d x %d" % (W, H))

    # compute width of tile
    w = W/cols

    # compute tile height based on aspect ratio and scale
    h = w/scale

    # compute number of rows
    rows = int(H/h)

    print("cols: %d, rows: %d" % (cols, rows))
    print("tile dims: %d x %d" % (w, h))
    if moreLevels:
        print("gscale1")
    else:
        print("gscale2")

    # check if image size is too small
    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)

    # ascii image is a list of character strings
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

            # crop image to tile
            x1 = int(i*w)
            x2 = int((i+1)*w)

            # correct last tile
            if i == cols-1:
                x2 = W

            # crop image to extract tile
            img = image.crop((x1, y1, x2, y2))

            # get average luminance
            avg = int(getAverageL(img))

            # look up ascii char
            if moreLevels:
                gsval = gscale1[int((avg*69)/255)]
            else:
                gsval = gscale2[int((avg*9)/255)]

            # append ascii char to string
            aimg[j] += gsval

    # return txt image
    return aimg

# main() function

# https://www.geeksforgeeks.org/extract-dominant-colors-of-an-image-using-python/

#julia_mantel    = "V:/00download/manteljulia_271367352_343627254254777_2341924037822352416_n.jpg"
rainbow         = "D:/__BUP_V_KOMPLETT/X/111_BUP/33projects/2022/2022-karlsruhe.digital/2022/beautiful-girl-flower-rainbow-background-22116179.jpg"

def main():
    # create parser
    descStr = "This program converts an image into ASCII art."
    
    parser = argparse.ArgumentParser(description=descStr)
    # add expected arguments
    parser.add_argument('--file', dest='imgFile', default=rainbow, required=False)
    parser.add_argument('--scale', dest='scale', default=0.5, required=False) # 0.43 aspect
    parser.add_argument('--out', dest='outFile', default="__out.txt", required=False)
    parser.add_argument('--cols', dest='cols', default=100, required=False) # 80
    parser.add_argument('--morelevels', dest='moreLevels', default=False,action='store_true')

    # parse args
    args = parser.parse_args()

    imgFile = args.imgFile

    # set output file
    outFile = args.outFile

    # set scale default as 0.43 which suits
    # a Courier font
    scale = float(args.scale)

    # set cols
    cols = int(args.cols)
    
    num_layers = 3
    assert num_layers > 1
    min_bright = 35
    max_bright = 210
    
    step = math.floor(max_bright/(num_layers))
    
    print('generating ASCII art...')
    # convert image to ascii txt
    root_image = Image.open(imgFile)
    root_image = ImageOps.equalize(root_image)
    root_image.show()
    
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
        
    
        aimg = covertImageToAscii(image, cols, scale, args.moreLevels)
        for row in aimg:
            print(row)
        print()
        image.show()

    # # open file
    # with open(outFile, 'w') as f:
    #     # write to file
    #     for row in aimg:
    #         f.write(row + '\n')
            
    #     print("ASCII art written to %s" % outFile)

def clamp(x): 
  return max(0, min(x, 255))

# call main
if __name__ == '__main__':
    pass
    
    ##main()
    
    # https://stackoverflow.com/questions/3241929/python-find-dominant-most-common-color-in-an-image
    """
        
    Here's code making use of Pillow and Scipy's cluster package.

    For simplicity I've hardcoded the filename as "image.jpg". Resizing the image is for speed: if you don't mind the wait, comment out the resize call. When run on this sample image of blue peppers it usually says the dominant colour is #d8c865, which corresponds roughly to the bright yellowish area to the lower left of the two peppers. I say "usually" because the clustering algorithm used has a degree of randomness to it. There are various ways you could change this, but for your purposes it may suit well. (Check out the options on the kmeans2() variant if you need deterministic results.)

    """
    
    #from __future__ import print_function
    import binascii
    import struct
    from PIL import Image
    import numpy as np
    import scipy
    import scipy.misc
    import scipy.cluster
    
    def pil_image_segmentation(image, num_clusters):
        image   = image.convert("RGB")
        ar      = np.asarray(image)
        shape   = ar.shape
        ar      = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)
    
        # codes are float rgb colors
        codes, dist = scipy.cluster.vq.kmeans(ar, num_clusters)
        print('codes: cluster centres:\n', *codes, sep="\n\t")
        print('codes: dist:', dist)
        
        
    ###########################
    
    NUM_CLUSTERS = 32

    print('reading image')
    im      = Image.open(rainbow)
    im      = im.convert("RGB")
    #im = im.resize((150, 150))      # optional, to reduce time
    ar      = np.asarray(im)
    shape   = ar.shape
    ar      = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)
    

    # PIL_image = Image.fromarray(np.uint8(numpy_image)).convert('RGB')
    # PIL_image = Image.fromarray(numpy_image.astype('uint8'), 'RGB')
    
# 0163 8008662 carolin brandl

    print('finding clusters')
    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
    # codes are float rgb colors
    print("dist:", dist)
    print("len(codes):", len(codes))
    print('codes: cluster centres:\n', *codes, sep="\n\t")
    
    # convert to 8 bit rgb, TODO could even reduce to #FFF
    colors = []
    for code in codes:
        r,g,b = code
        colors.append("#{:02x}{:02x}{:02x}".format(clamp(round(r)), clamp(round(g)), clamp(round(b))))
    colors = sorted(colors)
    print("colors", *colors, sep="\n\t")

    vecs, dist      = scipy.cluster.vq.vq(ar, codes)         # assign codes
    counts, bins    = np.histogram(vecs, len(codes))

    index_max   = np.argmax(counts)                    # find most frequent
    peak        = codes[index_max]
    colour      = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
    print('most frequent is %s (#%s)' % (peak, colour))

    # bonus: save image using only the NUM_CLUSTERS most common colours
    __cluster_path = '__clusters.png'
    import imageio
    c = ar.copy()
    for i, code in enumerate(codes):
        c[scipy.r_[np.where(vecs==i)],:] = code
        
    import os
    if os.path.isfile(__cluster_path):
        os.remove(__cluster_path)
    imageio.imwrite(__cluster_path, c.reshape(*shape).astype(np.uint8))
    print('saved clustered image')
    
    im = Image.open(__cluster_path)
    im.show()
    
    