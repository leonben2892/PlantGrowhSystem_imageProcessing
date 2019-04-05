# Import the necessary packages
import cv2 as cv

# Load the image, convert it to grayscale and blur it slightly
img = cv.imread('Plant.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
gray = cv.GaussianBlur(gray, (5, 5), 0)

# Threshold the image, then perform a series of erosions & dilations to remove any small regions of noise
thresh = cv.threshold(gray, 45, 255, cv.THRESH_BINARY)[1]
thresh = cv.erode(thresh, None, iterations=2)
thresh = cv.dilate(thresh, None, iterations=2)

# Find contours in thresholded image
contours, hierarchy = cv.findContours(thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# Draw contours
cv.drawContours(img, contours, -1, (0,255,0), 2)

# Calculate plant surface area
i=0
area = 0
while i < len(contours):
    cnt = contours[i]
    area = area + cv.contourArea(cnt)
    i = i + 1

# Print area
strArea = "Plant Area is: "+str(area)+" pixels"
print(strArea)

# Show the output image
cv.imshow("Plant Area", img)
cv.waitKey(0)

