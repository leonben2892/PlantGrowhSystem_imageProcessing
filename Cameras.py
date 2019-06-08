from cv2 import *

def image_capture(camera_index):
    # Initialize the camera
    cam = VideoCapture(camera_index)   # camera_index is used to decide which camera to use
    # Focus webcam
    focus = 0  # min: 0, max: 255, increment:5
    cam.set(cv2.CAP_PROP_FOCUS, focus) 
    # Capture image
    ret, img = cam.read()
    if ret:    # If image captured without any errors
        imshow("cam-test",img)
        if camera_index == 0:
                imwrite("CapturedImage0.jpg",img) # Save image
        else:
                imwrite("CapturedImage1.jpg",img) # Save image

def crop_image(x, y, w, h, image_name):
    img = cv2.imread(image_name)
    # Crop the image with the given coordinates
    crop_img = img[y:y+h, x:x+w]
    cv2.imshow("cropped", crop_img)
    cv2.waitKey(0)
    imwrite("CroppedImage.jpg",crop_img) # Save image


def resize_image(scale_percent, image_name):
    img = cv2.imread(image_name)
    # Set new image size based on given percentage
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # Resize the image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    cv2.imshow("Resized Image", resized)
    imwrite("ResizedImage.jpg",resized) # Save image

def capture_and_set_images():
    # Capture image from camera #1 (Front of the plant)
    # Capture image from camera #2 (Side of the plant)
    # Resize images (ONLY IF NECCESSERY!!!)
    # Crop the plant's front image to create a new image without the ruler in order to calculate the front surface area
    None