# import the necessary packages
import imutils
import cv2

class PlantData():
    
    def __init__(self):
        self.length_pixel = 0
        self.length = 0
        
        self.height_pixel = 0
        self.height = 0
        
        self.width_pixel = 0
        self.width = 0
        
        self.volume = 0
        
        self.front_image = None
        self.side_image = None
        self.plant_area_image = None
        
        
    def __str__(self):
        return "Plant Length: {} cm\nPlant Height: {} cm\nPlant Width: {} cm\nPlant Volume: {} cm^3".format(self.length,self.height,self.width,self.volume)
    
    def image_contours(self, image_name, calculation_flg):
        # Load the image, convert it to grayscale, and blur it slightly
        image = cv2.imread(image_name)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        
        # Perform edge detection, then perform a dilation & erosion to close gaps in between object edges
        edged = cv2.Canny(gray, 50, 100)
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)
        
        if calculation_flg == 0:
            # Find contours in the edge map
            cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
        else:
            # Find contours in thresholded image
            cnts,_ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Sort contours by area
        cntsSorted = sorted(cnts, key=lambda x: cv2.contourArea(x))
        return [cntsSorted,image]

    def plant_front(self, image_name):
        
        # Calculate the height of the plant in adnier in pixels unit
        def plant_height_in_adnier_pixels(plant_in_adnier, plant_out_adnier, plant_out_adnier_pixels):
            plant_height_in_adnier_precentage = ((plant_in_adnier/plant_out_adnier)*100)
            return round((plant_height_in_adnier_precentage/100) * plant_out_adnier_pixels, 2)
        
        image_and_sortedcnts = self.image_contours(image_name, 0)
        cntsSorted = image_and_sortedcnts[0]
        image = image_and_sortedcnts[1]
        
        # Bound the ruler in a rectangle in order to calculate the phone width and height in pixels
        ruler = cntsSorted[len(cntsSorted)-1]
        xR,yR,wR,hR = cv2.boundingRect(ruler)
        cv2.rectangle(image, (xR,yR), (xR+wR,yR+hR), (0, 255, 0), 2) 
        
        # Calculate the first plant points (x, y, width, height)
        front_plant1 = cntsSorted[len(cntsSorted)-2]
        _,yP1,wP1,hP1 = cv2.boundingRect(front_plant1)
         
        # Calculate the second plant points (x, y, width, height)
        front_plant2 = cntsSorted[len(cntsSorted)-3]
        xP2,_,wP2,_ = cv2.boundingRect(front_plant2)
        
        # Bound both plants in a rectangle in order to calculate the plant length and height in pixels
        cv2.rectangle(image, (xP2,yP1), (xP2+wP2+wP1-15,yP1+hP1), (0, 255, 0), 2) 
         
        # Calculate plant front length and height in reference to the ruler height
        percentage_height = round((hP1/hR)*100, 2)
        percentage_length = round(((wP2+wP1-15)/hR)*100, 2)
        
        # Variable to hold the fixed height of the plant in the adnier
        plant_height_in_adnier = 7.5
        
        self.length = round((percentage_length/100)*12.5, 2) 
        self.height = round((percentage_height/100)*12.5 + plant_height_in_adnier, 2)
        
        self.length_pixel = wP2+wP1-15
        self.height_pixel = int(plant_height_in_adnier_pixels(plant_height_in_adnier, self.height-7.5, hP1) + hP1)
        
        self.draw_image_midpoints(image, 0, (xP2,yP1), (xP2+wP2+wP1-15, yP1), (xP2, yP1+hP1), (xP2+wP2+wP1-15, yP1+hP1))
        
    def plant_side(self, image_name):
        image_and_sortedcnts = self.image_contours(image_name, 0)
        cntsSorted = image_and_sortedcnts[0]
        image = image_and_sortedcnts[1]
        
        # Bound the ruler in a rectangle in order to calculate the phone width and height in pixels
        ruler = cntsSorted[len(cntsSorted)-1]
        xR,yR,wR,hR = cv2.boundingRect(ruler)
        cv2.rectangle(image, (xR,yR), (xR+wR-55,yR+hR), (0, 255, 0), 2) 
        
        
        # Calculate the first plant points (x, y, width, height)
        side_plant = cntsSorted[len(cntsSorted)-2]
        xP,yP,wP,hP = cv2.boundingRect(side_plant)
        cv2.rectangle(image, (xP+45,yP), (xP+wP-15,yP+hP), (0, 255, 0), 2)
        
        # Calculate plant side width in reference to the ruler height
        percentage_length = round(((wP-60)/hR)*100, 2)

        
        self.width = round((percentage_length/100)*12.5, 2) 
        self.width_pixel = wP-60
        
        self.draw_image_midpoints(image, 1, (xP+45,yP), (xP+wP-15, yP), (xP+45, yP+hP), (xP+wP-15, yP+hP))
    
    def draw_image_midpoints(self, image, draw_flg, parm_tl, parm_tr, parm_bl, parm_br):
        
        def midpoint(ptA, ptB):
            return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)
        
        # Plant points: top-left, top-right, bottom-left, bottom-right
        tl = parm_tl
        tr = parm_tr
        bl = parm_bl
        br = parm_br
          
        # Compute the midpoint between the top-left and top-right coordinates 
        # Followed by the midpoint between bottom-left and bottom-right coordinates
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)
          
        # Compute the midpoint between the top-left and bottom-left coordinates,
        # Followed by the midpoint between the top-right and bottom-right
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)
          
        # Draw the midpoints on the image
        if draw_flg == 0:
            cv2.circle(image, (int(tltrX), int(tltrY)), 6, (255, 255, 255), -1) # Top 
        cv2.circle(image, (int(tlblX), int(tlblY)), 6, (255, 255, 255), -1) # Left
        cv2.circle(image, (int(trbrX), int(trbrY)), 6, (255, 255, 255), -1) # Right
          
        # Draw lines between the midpoints
        if draw_flg == 0:
            cv2.line(image, (int(tltrX), int(tltrY+4)), (int(blbrX), int(blbrY)), (0, 0, 255), 2) # Height
        cv2.line(image, (int(tlblX+4), int(tlblY)), (int(trbrX-4), int(trbrY)), (255, 0, 0), 2) # Length / Width (depends on draw_flg)
          
        # Draw the object sizes on the image
        if draw_flg == 0:
            # Draw plant height
            cv2.putText(image, "{:.2f}cm".format(self.height), (int(tltrX - 30), int(tltrY - 10)), cv2.FONT_ITALIC, 0.65, (0, 0, 255), 2)
            # Draw plant length
            cv2.putText(image, "{:.2f}cm".format(self.length), (int(trbrX + 10), int(trbrY+5)), cv2.FONT_ITALIC, 0.65, (255, 0, 0), 2)
        else:
            # Draw phone width
            cv2.putText(image, "{:.2f}cm".format(self.width), (int(trbrX + 10), int(trbrY+5)), cv2.FONT_ITALIC, 0.65, (255, 0, 0), 2)
        
        if draw_flg == 0:
            self.front_image = image 
        else:
            self.side_image = image
            
    def plant_volume(self, image_name):
        image_and_sortedcnts = self.image_contours(image_name, 1)
        cntsSorted = image_and_sortedcnts[0]
        image = image_and_sortedcnts[1]
        # Draw contours
        cv2.drawContours(image, cntsSorted, -1, (0,255,0), 2)
         
        # Calculate plant front surface area
        plant_front_surface_area = 0
        for i in range(len(cntsSorted)):
            cnt = cntsSorted[i]
            plant_front_surface_area = plant_front_surface_area + cv2.contourArea(cnt)
             
        plant_volume_pixel = (plant_front_surface_area+14000) * self.width_pixel
        cube_around_plant_volume_pixel = self.length_pixel * self.height_pixel * self.width_pixel
        precentage_plant_of_cube = 100 - (plant_volume_pixel / cube_around_plant_volume_pixel)*100
         
        cube_around_plant_volume_cm = self.length * self.height * self.width
        self.volume = round((precentage_plant_of_cube/100)*cube_around_plant_volume_cm, 2)
        self.plant_area_image = image