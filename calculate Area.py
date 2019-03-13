import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
img = cv.imread('plant1.png')
imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
cv.drawContours(img, contours, -1, (0,255,0), 3)
i=0
area = 0
while i < len(contours):
    cnt = contours[i]
    area = area + cv.contourArea(cnt)
    i = i + 1
print(area)
plt.imshow(img)
plt.show()