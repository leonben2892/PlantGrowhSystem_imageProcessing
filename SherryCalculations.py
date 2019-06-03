# import the necessary packages
from PlantCalculations import *

def sherry_front(image_name):
    image_and_sortedcnts = image_contours(image_name, 0)
    cntsSorted = image_and_sortedcnts[0]
    image = image_and_sortedcnts[1]
    # Bound the sherry_plant in a rectangle in order to calculate the phone width and height in pixels
    sherry_plant = cntsSorted[len(cntsSorted)-1]
    xP,yP,wP,hP = cv2.boundingRect(sherry_plant)
    cv2.rectangle(image, (xP,yP), (xP+wP,yP+hP), (0, 255, 0), 2) 
      
    # Calculate the first ruler points (x, y, width, height)
    ruler = cntsSorted[len(cntsSorted)-2]
    xR,yR,wR,hR = cv2.boundingRect(ruler)
    cv2.rectangle(image, (xR,yR), (xR+wR,yR+hR), (0, 255, 0), 2) 
       
    # Calculate ruler front length and height in reference to the ruler height
    percentage_length = round((wP/hR)*100, 2)
    percentage_height = round((hP/hR)*100, 2)
    
    length = round((percentage_length/100)*17, 2) 
    height = round((percentage_height/100)*17, 2)
    
    length_pixel = xP
    height_pixel = hP
    
    plant_data_list = []
    plant_data_list.append(draw_image_midpoints(image, 0, (xP, yP), (xP+wP, yP), (xP, yP+hP), (xP+wP, yP+hP), height, length))
    plant_data_list.extend([length, length_pixel, height, height_pixel])
    return plant_data_list
    
def sherry_side(image_name):
    image_and_sortedcnts = image_contours(image_name, 0)
    cntsSorted = image_and_sortedcnts[0]
    image = image_and_sortedcnts[1]   
    # Bound the ruler in a rectangle in order to calculate the phone width and height in pixels
    ruler = cntsSorted[len(cntsSorted)-1]
    xR,yR,wR,hR = cv2.boundingRect(ruler)
    cv2.rectangle(image, (xR,yR), (xR+wR,yR+hR), (0, 255, 0), 2) 
      
    # Calculate the first sherry_plant points (x, y, width, height)
    sherry_plant = cntsSorted[len(cntsSorted)-2]
    xP,yP,wP,hP = cv2.boundingRect(sherry_plant)
    cv2.rectangle(image, (xP,yP), (xP+wP,yP+hP), (0, 255, 0), 2) 
       
    # Calculate sherry_plant side width in reference to the ruler height
    percentage_width = round((wP/hR)*100, 2)

    width = round((percentage_width/100)*17, 2) 
    
    width_pixel = wP
    
    plant_data_list = []
    plant_data_list.append(draw_image_midpoints(image, 1, (xP, yP), (xP+wP, yP), (xP, yP+hP), (xP+wP, yP+hP), 0, 0, width))
    plant_data_list.extend([width, width_pixel])
    return plant_data_list

def sherry_volume(image_name, height, height_pixel, length, length_pixel, width, width_pixel):
    image_and_sortedcnts = image_contours(image_name, 1)
    cntsSorted = image_and_sortedcnts[0]
    image = image_and_sortedcnts[1]
    # Draw contours
    cv2.drawContours(image, cntsSorted, -1, (0,255,0), 2)
    
    # Calculate plant front surface area
    plant_front_surface_area = 0
    for i in range(len(cntsSorted)):
        cnt = cntsSorted[i]
        plant_front_surface_area = plant_front_surface_area + cv2.contourArea(cnt)
    
    plant_volume_pixel = plant_front_surface_area * width_pixel
    cube_around_plant_volume_pixel = length_pixel * height_pixel * width_pixel
    precentage_plant_of_cube = (plant_volume_pixel / cube_around_plant_volume_pixel)*100

    
    cube_around_plant_volume_cm = length * height * width
    volume = round((precentage_plant_of_cube/100)*cube_around_plant_volume_cm, 2)
    return [image, volume]