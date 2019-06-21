from cv2 import *
import requests
import numpy as np

IMAGE_EXTENSION = ".jpg"

def image_capture_from_phone(direction):
        if direction == "Front":
                url = "http://192.168.1.41:8080/shot.jpg"
                img_resp = requests.get(url)
                img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
                img = cv2.imdecode(img_arr, -1)
                cv2.imshow("Front", img)
                imwrite("Front"+IMAGE_EXTENSION, img)
        elif direction == "Side":
                url = "http://192.168.1.45:8080/shot.jpg"
                img_resp = requests.get(url)
                img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
                img = cv2.imdecode(img_arr, -1)
                cv2.imshow("Side", img)  
                imwrite("Side"+IMAGE_EXTENSION, img)

def resize_image(scale_percent, image_name):
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

def image_capture(camera_index):
    # Initialize the camera
    cam = VideoCapture(camera_index)   # camera_index is used to decide which camera to use
    # Focus webcam
    focus = 0  # min: 0, max: 255, increment:5
    cam.set(28, focus) 
    # Capture image
    ret, img = cam.read()
    if ret:    # If image captured without any errors
        # imshow("cam-test",img)
        if camera_index == 0:
                imwrite("CapturedImage0.jpg",img) # Save image
        else:
                imwrite("CapturedImage1.jpg",img) # Save image

def capture_and_set_images():
    image_capture_from_phone("Front")
    image_capture_from_phone("Side")
    resize_image(70, "Front")
    resize_image(70, "Side")
    crop_image("Front", 250, 20,815, 690, "Ruler")
    crop_image("Front", 250, 20,815, 690, "Front")
    crop_image("Side", 250, 20,815, 690, "Side")
