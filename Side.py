# # import the necessary packages
# import imutils
# import cv2
# from cv2 import contourArea
#   
# # Calculate the midpoint between 2 given points
# def midpoint(ptA, ptB):
#     return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)
#   
# # Load the image, convert it to grayscale, and blur it slightly
# image = cv2.imread("Side.jpg")
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# gray = cv2.GaussianBlur(gray, (7, 7), 0)
#   
# # Perform edge detection, then perform a dilation & erosion to close gaps in between object edges
# edged = cv2.Canny(gray, 50, 100)
# edged = cv2.dilate(edged, None, iterations=1)
# edged = cv2.erode(edged, None, iterations=1)
#   
# # Find contours in the edge map
# cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnts = imutils.grab_contours(cnts)
#   
# # Sort contours by area
# cntsSorted = sorted(cnts, key=lambda x: cv2.contourArea(x))
#   
# # Bound the ruler in a rectangle in order to calculate the phone width and height in pixels
# ruler = cntsSorted[len(cntsSorted)-1]
# xR,yR,wR,hR = cv2.boundingRect(ruler)
# cv2.rectangle(image, (xR,yR), (xR+wR-55,yR+hR), (0, 255, 0), 2) 
#   
#   
# # Calculate the first plant points (x, y, width, height)
# side_plant = cntsSorted[len(cntsSorted)-2]
# xP,yP,wP,hP = cv2.boundingRect(side_plant)
# cv2.rectangle(image, (xP+45,yP), (xP+wP-15,yP+hP), (0, 255, 0), 2)
#   
#   
# # Calculate plant side width in reference to the ruler height
# percentage_length = round(((wP-60)/hR)*100, 2)
# stringWidth = "Percentage of plant width from ruler height is: "+str(percentage_length)+"%"
# print(stringWidth)
# plant_width = round((percentage_length/100)*12.5, 2) 
# stringWidthCm = "Phone width is: "+str(plant_width)+" cm"
# print(stringWidthCm)
#   
# # Plant points: top-left, top-right, bottom-left, bottom-right
# tl = (xP+45,yP)
# tr = (xP+wP-15, yP)
# bl = (xP+45, yP+hP)
# br = (xP+wP-15, yP+hP)
#     
# # Compute the midpoint between the top-left and top-right coordinates 
# # Followed by the midpoint between bottom-left and bottom-right coordinates
# (tltrX, tltrY) = midpoint(tl, tr)
# (blbrX, blbrY) = midpoint(bl, br)
#     
# # Compute the midpoint between the top-left and bottom-left coordinates,
# # Followed by the midpoint between the top-right and bottom-right
# (tlblX, tlblY) = midpoint(tl, bl)
# (trbrX, trbrY) = midpoint(tr, br)
#     
# # Draw the midpoints on the image
# cv2.circle(image, (int(tlblX), int(tlblY)), 6, (255, 255, 255), -1) # Left
# cv2.circle(image, (int(trbrX), int(trbrY)), 6, (255, 255, 255), -1) # Right
#     
# # Draw lines between the width midpoints
# cv2.line(image, (int(tlblX+4), int(tlblY)), (int(trbrX-4), int(trbrY)), (255, 0, 0), 2) # Width
#     
# # Draw the object sizes on the image
# # Draw phone width
# cv2.putText(image, "{:.2f}cm".format(plant_width), (int(trbrX + 10), int(trbrY+5)), cv2.FONT_ITALIC, 0.65, (255, 0, 0), 2)
#   
# # Show the output image
# cv2.imshow("Plant Side", image)
# cv2.waitKey(0)