# Import the necessary packages
import imutils
import cv2 as cv

# Load the image, convert it to grayscale and blur it slightly
img = cv.imread('Plant.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
gray = cv.GaussianBlur(gray, (5, 5), 0)

# Threshold the image, then perform a series of erosions & dilations to remove any small regions of noise
thresh = cv.threshold(gray, 45, 255, cv.THRESH_BINARY)[1]
thresh = cv.erode(thresh, None, iterations=2)
thresh = cv.dilate(thresh, None, iterations=2)

# Find contours in thresholded image, then grab the largest one
contours = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
c = max(contours, key=cv.contourArea)

# Draw contours
cv.drawContours(img, [c], -1, (0,255,0), 2)

# Calculate plant surface area
i=0
perimeter = 0
while i < len(contours):
    cnt = contours[i]
    perimeter = perimeter + cv.arcLength(cnt, True)
    i = i + 1

# Convert plant perimeter from pixels to mm
# The formula is: mm = (pixels * 25.4) / DPI
perimeter = (perimeter * 25.4) / 129.5;

# Convert plant perimeter from mm to cm
perimeter = perimeter / 10;

# Print perimeter
strPerimeter = "Plant Perimeter is: "+str(perimeter)+" cm"
print(strPerimeter)

# Show the output image
cv.imshow("Plant Perimeter", img)
cv.waitKey(0)



#===============================================================================
# area = cv.contourArea(cnt)
# print(area)
# perimeter = cv.arcLength(cnt,True)
# print(perimeter)
#===============================================================================