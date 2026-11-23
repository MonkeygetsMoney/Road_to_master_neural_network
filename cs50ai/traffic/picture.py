import cv2 as cv
import sys
import os

# read an image
img = cv.imread('traffic/ousucks.jpg')

print(img.shape)
path = 'home/Users/text.txt'
print(os.sep) # is the separator '/' on Mac or '\' on window

path = path.split(os.sep)
print(os.path.join(*path))
