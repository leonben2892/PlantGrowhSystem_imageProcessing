# import the necessary packages
from BambooCalculations import *

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


    def calculate_plant_data(self, plant_type):
        calculated_plant_data = []
        if plant_type == "Bamboo":
            calculated_plant_data.extend(bamboo_front("BambooFront.jpg"))
            calculated_plant_data.extend(bamboo_side("BambooSide.jpg"))
            self.front_image, self.length, self.length_pixel, self.height, self.height_pixel, self.side_image, self.width, self.width_pixel = calculated_plant_data
            calculated_plant_data.clear()
            calculated_plant_data.extend(bamboo_volume("BambooVolume.jpg", self.height, self.height_pixel, self.length, self.length_pixel, self.width, self.width_pixel))
            self.plant_area_image, self.volume = calculated_plant_data
        