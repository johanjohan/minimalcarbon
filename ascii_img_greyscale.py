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

julia_mantel = "V:/00download/manteljulia_271367352_343627254254777_2341924037822352416_n.jpg"

def main():
    # create parser
    descStr = "This program converts an image into ASCII art."
    
    parser = argparse.ArgumentParser(description=descStr)
    # add expected arguments
    parser.add_argument('--file', dest='imgFile', default=julia_mantel, required=False)
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


# call main
if __name__ == '__main__':
    main()
