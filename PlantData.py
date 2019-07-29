# import the necessary packages
import cv2
import imutils
import random

class PlantData():
    """
    A class used to represent plant data
    
    Attributes
    ----------
    ruler_height_in_pixels: int
        The ruler's height in pixels unit
        
    pixels_in_square_cm: int
        The number of pixels in square cm (cm^2)
        
    plant_side_area_int_square_cm: double
        The plant's side view area in square cm units 
        
    effective_width: double
        The plant's effective width in cm units
        
    plant_height: double
        The plant's height in cm units
    
    plant_volume: double
        The plant's volume estimation in cm^3 units
        
    Methods
    ----------
    draw_image_midpoints(image, parm_tl, parm_tr, parm_bl, parm_br, height = 0, length = 0, width = 0)
        Draw midpoints on a given image
        
    calculate_pixels_count(image_name)
        Calculates the number of non-black pixels in an image
        
    proccess_ruler(image_name)
        Calculates the number of pixels in square cm (cm^2)
        
    process_plant_side_area(image_name)
        Calculates the area of the plant from a side view
        
    proccess_plant_height(image_name)
        Calculates the plant's height
        
    calculate_effective_width(image_name)
        Calculates the plant's effective width
    
    calculate_plant_volume()
        Estimating plant's volume
    """
    def __init__(self):
        self.ruler_height_in_pixels = 0
        self.pixels_in_square_cm = 0
        self.plant_side_area_in_square_cm = 0
        self.effective_width = 0
        self.plant_height = 0
        self.plant_volume = 0       
               
    def __str__(self):
        return "Plant Height: {} cm\nPlant Volume: {} cm^3\n".format(self.plant_height, self.plant_volume)

    def draw_image_midpoints(self, image_name, parm_tl, parm_tr, parm_bl, parm_br, plant_height):
        """
        Draw midpoints on a given image
        
        Parameters
        ----------
        image_name: string
            The name of the image we want to draw midpoints on
        
        parm_tl: coordinate
            Top-left coordinate of the image
        
        parm_tr: coordinate
            Top-right coordinate of the image
        
        parm_bl: coordinate
            Bottom-left coordinate of the image
        
        parm_br: coordinate
            Bottom-right coordinate of the image
        
        plant_height: double
            The plant's height
            
        Returns
        ----------
        string: The name if the image we just added midpoint on
        """
        def midpoint(ptA, ptB):
            """
            Determine the midpoint of the given points
            
            Parameters
            ----------
            ptA: coordinate
                The first point
                
            ptB: coordinate
                The second point
                
            Returns
            ----------
            coordinate: The coordinate of the midpoint of the 2 given points
            """
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
        cv2.circle(image_name, (int(tltrX), int(tltrY)), 6, (255, 255, 255), -1) # Top 
      
        # Draw a line between 2 midpoints
        cv2.line(image_name, (int(tltrX), int(tltrY+4)), (int(blbrX), int(blbrY)), (0, 0, 255), 2) # Height
    
        # Write the the height of the plant next to the top midpoint
        cv2.putText(image_name, "{:.2f}cm".format(plant_height), (int(tltrX - 30), int(tltrY - 10)), cv2.FONT_ITALIC, 0.65, (0, 0, 255), 2)
    
        return image_name
    
    def calculate_pixels_count(self, image_name):
        """
        Calculates the number of non-black pixels in an image
        
        Parameters
        ----------
        image_name: string
            The name of the image we want to calculates the number of non-black pixels

        Returns
        ----------
        list: The list consist of - total of non-black pixels, the image after image processing & the image contours sorted by contour area
        """
        # Load the image, convert it to grayscale and blur it slightly
        image = cv2.imread(image_name)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        # Threshold the image, then perform a series of erosions & dilations to remove any small regions of noise
        thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)
        # Grab all the contours in an image and sort them by size
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts_sorted = sorted(cnts, key=lambda x: cv2.contourArea(x))
        # Calculate the number of non-black pixels
        total_nz_pixels = cv2.countNonZero(thresh)
#         cv2.imshow("Thresh Image", thresh)
        return [total_nz_pixels, thresh, cnts_sorted]

    def proccess_ruler(self, image_name):
        """
        Calculates the number of pixels in square cm (cm^2)
        
        Parameters
        ----------
        image_name: string
            The name of the image from which we calculate the number of pixels in square cm

        Returns
        ----------
        Nothing
        """
        _, image, cnts_sorted = self.calculate_pixels_count(image_name)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        # Calculate the ruler height in pixels
        ruler = cnts_sorted[len(cnts_sorted)-1]
        xR,yR,wR,hR = cv2.boundingRect(ruler)
        cv2.rectangle(image, (xR,yR), (xR+wR,yR+hR), (0, 255, 0), 2)
        self.ruler_height_in_pixels = hR
        # Calculate how many pixels are there in square cm
        self.pixels_in_square_cm = (hR/17)**2
#         cv2.imshow("Ruler", image)
        
    def process_plant_side_area(self, image_name):
        """
        Calculates the area of the plant from a side view
        
        Parameters
        ----------
        image_name: string
            The name of the image from which we calculate the area of the plant from a side view

        Returns
        ----------
        Nothing
        """
        # Calculate plant side pixels count
        plant_side_pixel_count, image, _ = self.calculate_pixels_count(image_name)
        # Convert plant side pixels count to square cm
        self.plant_side_area_in_square_cm =  plant_side_pixel_count / self.pixels_in_square_cm
#         cv2.imshow("Side Area", image)

    def proccess_plant_height(self, image_name):
        """
        Calculates the plant's height
        
        Parameters
        ----------
        image_name: string
            The name of the image from which we calculate the plant's height

        Returns
        ----------
        Nothing
        """
        _, image, cnts_sorted = self.calculate_pixels_count(image_name)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        # Calculate the plant height in pixels
        plant = cnts_sorted[len(cnts_sorted)-1]
        xP,yP,wP,hP = cv2.boundingRect(plant)
        cv2.rectangle(image, (xP,yP), (xP+wP,yP+hP), (0, 255, 0), 2)
        # Calculate the plant height in cm
        self.plant_height = (hP/self.ruler_height_in_pixels)*17
        # Draw height line on the image
        image = self.draw_image_midpoints(image, (xP,yP), (xP+wP, yP), (xP, yP+hP), (xP+wP,yP+hP), self.plant_height)
#         cv2.imshow("Side Height", image)

    def calculate_effective_width(self, image_name):
        """
        Calculates the plant's effective width
        
        Parameters
        ----------
        image_name: string
            The name of the image from which we calculate the plant's effective width

        Returns
        ----------
        Nothing
        """
        plant_front_pixel_count, image, _ = self.calculate_pixels_count(image_name)
        # Convert plant front pixels count to square cm
        plant_front_area_in_square_cm =  plant_front_pixel_count / self.pixels_in_square_cm
        # Calculating effective width
        self.effective_width = plant_front_area_in_square_cm / self.plant_height
#         cv2.imshow("Front - Effective width", image)

    def calculate_plant_volume(self):
        """
        Estimating plant's volume
        
        Parameters
        ----------
        Nothing

        Returns
        ----------
        Nothing
        """
        self.proccess_ruler("Ruler.jpg")
        self.process_plant_side_area("Front.jpg")
        self.proccess_plant_height("Front.jpg")
        self.calculate_effective_width("Side.jpg")
        self.plant_volume = self.plant_side_area_in_square_cm * self.effective_width

            
            
        