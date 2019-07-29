# import the necessary packages
from cv2 import *
import requests
import numpy as np

IMAGE_EXTENSION = ".jpg"

def image_capture_from_phone(direction):
    """
    Capture an image
    
    Parameters
    ----------
    direction: string
        Which camera to capture
        
    Returns
    ----------
    Nothing
    """
    if direction == "Side":
            url = "http://192.168.43.158:8080/shot.jpg"
            img_resp = requests.get(url)
            img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
            img = cv2.imdecode(img_arr, -1)
            # cv2.imshow("Side", img)
            imwrite("Side"+IMAGE_EXTENSION, img)
    elif direction == "Front":
            url = "http://192.168.43.243:8080/shot.jpg"
            img_resp = requests.get(url)
            img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
            img = cv2.imdecode(img_arr, -1)
            # cv2.imshow("Front", img)  
            imwrite("Front"+IMAGE_EXTENSION, img)

def resize_image(scale_percent, image_name):
    """
    Resize an image
    
    Parameters
    ----------
    scale_percent: int
        the new size of the image in percentage
    
    image_name: string
        The name of the image you want to resize
        
    Returns
    ----------
    Nothing
    """
    img = cv2.imread(image_name+IMAGE_EXTENSION)
    # Set new image size based on given percentage
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # Resize the image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    # cv2.imshow("Resized Image", resized)
    imwrite(image_name+IMAGE_EXTENSION, resized) # Save image

def crop_image(x, y, w, h, image_name, object):
    """
    Crop an image
    
    Parameters
    ----------
    x: int
        The starting x coordinate of the crop 
    
    y: int
        The starting y coordinate of the crop
    
    w: int
        The width of the crop
    
    h: int
        The height of the crop
    
    image_name: string
        The name of the image you want to crop
    
    object: string
        The object you are cropping from the image
        
    Returns
    ----------
    Nothing
    """
    img = cv2.imread(image_name+IMAGE_EXTENSION)
    # Crop the image with the given coordinates
    crop_img = img[y:y+h, x:x+w]
    # cv2.imshow("cropped", crop_img)
    if object == "Ruler":
        imwrite("Ruler"+IMAGE_EXTENSION,crop_img) # Save image
    elif object == "Front":
        imwrite("Front"+IMAGE_EXTENSION,crop_img) # Save image
    elif object == "Side":
        imwrite("Side"+IMAGE_EXTENSION,crop_img) # Save image

def capture_and_set_images():
    """
    Capture, resize and crop images to prepare them for image processing
    
    Parameters
    ----------
    Nothing
        
    Returns
    ----------
    Nothing
    """
    image_capture_from_phone("Front")
    image_capture_from_phone("Side")
    resize_image(70, "Front")
    resize_image(70, "Side")
    crop_image(350, 0,720, 450, "Front", "Ruler")
    crop_image(700, 20,1000, 570,"Front", "Front")
    crop_image(250, 20,815, 690, "Side", "Side")
