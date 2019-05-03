import cv2

# Load the image, convert it to grayscale and blur it slightly
image = cv2.imread('PlantArea.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)
 
# Perform edge detection, then perform a dilation & erosion to close gaps in between object edges
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)
 
# Find contours in thresholded image
contours,_ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours
cv2.drawContours(image, contours, -1, (0,255,0), 2)
 
# Calculate plant front surface area
plant_front_surface_area = 0
for i in range(len(contours)):
    cnt = contours[i]
    plant_front_surface_area = plant_front_surface_area + cv2.contourArea(cnt)
   
# Print area
print("Plant Area is: {} pixels".format(plant_front_surface_area))
 
# Show the output image
cv2.imshow("Plant Area", image)
cv2.waitKey(0)