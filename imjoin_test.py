# coding: utf-8

import sys
from stitcher.image import SphereImageGenerator

import cv2

argvs = []

img_num = int(input())
argvs.append(img_num)
print("file_num: " + str(img_num))

i = 0
while (i < img_num):
    fname = input()
    argvs.append(fname)
    i = i + 1

i = 0
while (i < img_num):
    adjnum = int(input())
    argvs.append(adjnum)
    adjs = input()
    argvs.append(adjs)
    i = i + 1

sip = SphereImageGenerator();
result = sip.stitch(argvs);

