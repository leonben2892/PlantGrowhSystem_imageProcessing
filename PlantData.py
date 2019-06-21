# import the necessary packages
from PlantCalculations import *

class PlantData():
    def __init__(self):
        self.ruler_height_in_pixels = 0
        self.pixels_in_square_cm = 0
        self.plant_side_area_in_square_cm = 0
        self.effective_width = 0
        self.plant_height = 0
        self.plant_volume = 0       
               
    def __str__(self):
        return "Plant Height: {} cm\nPlant Volume: {} cm^3\n".format(self.plant_height, self.plant_volume)

    def proccess_ruler(self, image_name):
        image_and_sortedcnts = image_contours(image_name, 0)
        cntsSorted = image_and_sortedcnts[0]
        image = image_and_sortedcnts[1]
        # Calculate the ruler height in pixels
        ruler = cntsSorted[len(cntsSorted)-1]
        xR,yR,wR,hR = cv2.boundingRect(ruler)
        cv2.rectangle(image, (xR,yR), (xR+wR,yR+hR), (0, 255, 0), 2)
        self.ruler_height_in_pixels = hR
        # Calculate how many pixels are there in square cm
        self.pixels_in_square_cm = (hR/17)**2
        # cv2.imshow("Ruler", image)
        
    def process_plant_side_area(self, image_name):
        image_and_sortedcnts = image_contours(image_name, 1)
        cntsSorted = image_and_sortedcnts[0]
        image = image_and_sortedcnts[1]
        # Draw area contours
        cv2.drawContours(image, cntsSorted, -1, (0,255,0), 2)
        # Calculate plant side surface area
        plant_side_surface_area = 0
        for i in range(len(cntsSorted)):
            cnt = cntsSorted[i]
            plant_side_surface_area = plant_side_surface_area + cv2.contourArea(cnt)
        # Convert plant side area from pixels to square cm
        self.plant_side_area_in_square_cm =  plant_side_surface_area / self.pixels_in_square_cm
        # cv2.imshow("Side Area", image)

    def proccess_plant_height(self, image_name):
        image_and_sortedcnts = image_contours(image_name, 0)
        cntsSorted = image_and_sortedcnts[0]
        image = image_and_sortedcnts[1]
        # Calculate the plant height in pixels
        plant = cntsSorted[len(cntsSorted)-2]
        xP,yP,wP,hP = cv2.boundingRect(plant)
        cv2.rectangle(image, (xP,yP-310), (xP+wP,yP+hP), (0, 255, 0), 2)
        self.plant_height = ((hP+310)/self.ruler_height_in_pixels)*17
        # cv2.imshow("Side Height", image)

    def calculate_effective_width(self, image_name):
        image_and_sortedcnts = image_contours(image_name, 1)
        cntsSorted = image_and_sortedcnts[0]
        image = image_and_sortedcnts[1]
        # Draw area contours
        cv2.drawContours(image, cntsSorted, -1, (0,255,0), 2)
        plant_front_surface_area = 0
        for i in range(len(cntsSorted)):
            cnt = cntsSorted[i]
            plant_front_surface_area = plant_front_surface_area + cv2.contourArea(cnt)
        # Convert plant front area from pixels to square cm
        plant_front_area_in_square_cm =  plant_front_surface_area / self.pixels_in_square_cm
        self.effective_width = plant_front_area_in_square_cm / self.plant_height
        # cv2.imshow("Front - Effective width", image)

    def calculate_plant_data(self):
        self.proccess_ruler("Ruler.jpg")
        self.process_plant_side_area("Front.jpg")
        self.proccess_plant_height("Front.jpg")
        self.calculate_effective_width("Side.jpg")
        self.plant_volume = self.plant_side_area_in_square_cm * self.effective_width

            
            
        