# import the necessary packages
from PlantCalculations import *
import random

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

    def calculate_pixels_count(self, image_name):
        # Load the image, convert it to grayscale and blur it slightly
        image = cv2.imread(image_name)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        # Threshold the image, then perform a series of erosions + dilations to remove any small regions of noise
        thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)
        # Calculate the number of non-black pixels
        total_nz_pixels = cv2.countNonZero(thresh)
#         cv2.imshow("Thresh Image", thresh)
        return [total_nz_pixels, thresh]

    def proccess_ruler(self, image_name):
        image_and_sortedcnts = image_contours(image_name)
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
        # Calculate plant side pixels count
        plant_side_pixel_count, image = self.calculate_pixels_count(image_name)
        # Convert plant side pixels count to square cm
        self.plant_side_area_in_square_cm =  plant_side_pixel_count / self.pixels_in_square_cm
#         cv2.imshow("Side Area", image)

    def proccess_plant_height(self, image_name):
        image_and_sortedcnts = image_contours(image_name)
        cntsSorted = image_and_sortedcnts[0]
        image = image_and_sortedcnts[1]
        # Calculate the plant height in pixels
        plant = cntsSorted[len(cntsSorted)-1]
        xP,yP,wP,hP = cv2.boundingRect(plant)
        cv2.rectangle(image, (xP,yP), (xP+wP,yP+hP), (0, 255, 0), 2)
        # Calculate the plant height in cm
        self.plant_height = (hP/self.ruler_height_in_pixels)*17
#         cv2.imshow("Side Height", image)

    def calculate_effective_width(self, image_name):
        plant_front_pixel_count, image = self.calculate_pixels_count(image_name)
        # Convert plant front pixels count to square cm
        plant_front_area_in_square_cm =  plant_front_pixel_count / self.pixels_in_square_cm
        # Calculating effective width
        self.effective_width = plant_front_area_in_square_cm / self.plant_height
        # cv2.imshow("Front - Effective width", image)

    def calculate_plant_data(self):
        self.proccess_ruler("Ruler.jpg")
        self.process_plant_side_area("Front.jpg")
        self.proccess_plant_height("Front.jpg")
        self.calculate_effective_width("Side.jpg")
        self.plant_volume = self.plant_side_area_in_square_cm * self.effective_width

            
            
        