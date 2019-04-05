# Import the necessary packages
import imutils
import cv2
from win32api import GetSystemMetrics
from cmath import sqrt
  
# Load the image, convert it to grayscale, and blur it slightly
image = cv2.imread("Plant.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
  
# Threshold the image, then perform a series of erosions & dilations to remove any small regions of noise
thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.erode(thresh, None, iterations=2)
thresh = cv2.dilate(thresh, None, iterations=2)
  
# Find contours in thresholded image, then grab the largest one
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
c = max(cnts, key=cv2.contourArea)

# Bound the plant in a rectangle in order to calculate the plant width and height
x,y,w,h = cv2.boundingRect(c)
cv2.rectangle(image, (x,y), (x+w,y+h), (255,255,255), 1) 

# Calculate width and height of the plant in pixels
distanceX = x+w
distanceY = y+h
 
# Calculating monitor DPI
# DPI = sqrt(WidthResolution^2+HeightResolution^2) / ScreenSize.
screenSize = 17 # Change this to your screen size!
widthResolution = GetSystemMetrics(0)
heightResolution = GetSystemMetrics(1)
diagonalResolution = sqrt(widthResolution**2 + heightResolution**2)
monitorDPI = round(diagonalResolution.real / screenSize, 2)

# Convert width and height from pixels to mm units
# The formula is: mm = (pixels * 25.4) / DPI
mmWidth = ((distanceX * 25.4) / monitorDPI) 
mmHeight = ((distanceY * 25.4) / monitorDPI) 

# Convert width and height from mm units to cm units
cmWidth = mmWidth / 10
cmHeight = mmHeight / 10

# Print width and height in cm units
stringWidth = "Plant width is: "+str(round(cmWidth, 2))+" cm"
stringHeight = "Plant height is: "+str(round(cmHeight, 2))+" cm"
print(stringWidth)
print(stringHeight)

# Determine the most extreme points along the contour
extLeft = tuple(c[c[:, :, 0].argmin()][0])
extRight = tuple(c[c[:, :, 0].argmax()][0])
extTop = tuple(c[c[:, :, 1].argmin()][0])
extBot = tuple(c[c[:, :, 1].argmax()][0])

# Draw each of the extreme points, where the left-most is red, right-most is green,
# top-most is blue, and bottom-most is yellow
cv2.circle(image, extLeft, 8, (0, 0, 255), -1)
cv2.circle(image, extRight, 8, (0, 255, 0), -1)
cv2.circle(image, extTop, 8, (255, 0, 0), -1)
cv2.circle(image, extBot, 8, (0, 255, 255), -1)
  
# Show the output image
cv2.imshow("Plant Width & Height", image)
cv2.waitKey(0)

