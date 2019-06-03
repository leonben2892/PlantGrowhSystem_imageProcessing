# import the necessary packages
from PlantCalculations import *

def bamboo_front(image_name):
    image_and_sortedcnts = image_contours(image_name, 0)
    cntsSorted = image_and_sortedcnts[0]
    image = image_and_sortedcnts[1]
    
    # Bound the ruler in a rectangle in order to calculate the bamboo height & length in pixels
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
    
    length = round((percentage_length/100)*12.5, 2) 
    height = round((percentage_height/100)*12.5, 2)
    
    length_pixel = wP2+wP1-15
    height_pixel = hP1;
    
    plant_data_list = []
    plant_data_list.append(draw_image_midpoints(image, 0, (xP2,yP1), (xP2+wP2+wP1-15, yP1), (xP2, yP1+hP1), (xP2+wP2+wP1-15, yP1+hP1), height, length))
    plant_data_list.extend([length, length_pixel, height, height_pixel])
    return plant_data_list

def bamboo_side(image_name):
    image_and_sortedcnts = image_contours(image_name, 0)
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
    percentage_width = round(((wP-60)/hR)*100, 2)
    
    width = round((percentage_width/100)*12.5, 2) 
    
    width_pixel = wP-60
    
    plant_data_list = []
    plant_data_list.append(draw_image_midpoints(image, 1, (xP+45,yP), (xP+wP-15, yP), (xP+45, yP+hP), (xP+wP-15, yP+hP), 0, 0, width))
    plant_data_list.extend([width, width_pixel])
    return plant_data_list

def bamboo_volume(image_name, height, height_pixel, length, length_pixel, width, width_pixel):
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
    precentage_plant_of_cube = 100 - (plant_volume_pixel / cube_around_plant_volume_pixel)*100
    
    cube_around_plant_volume_cm = length * height * width
    volume = round((precentage_plant_of_cube/100)*cube_around_plant_volume_cm, 2)
    return [image, volume]