import numpy as np
import sys
import cv2
import math



#load image
#img_size  = int(sys.argv[1])
def create_gaussian(width,height,sigma,fname_out):
    #真っ黒な画像を作成
    img = np.zeros((height, width), dtype = np.uint8)

    for x in range(width):
        for y in range(height):
            img[y,x]=177*math.exp(-( ((x-width//2)**2)/(2*sigma**2) + ((y-height//2)**2)/(2*sigma**2) ))

    cv2.imwrite(fname_out, img )

#create_gaussian(620,465,6,"gaussian.png")