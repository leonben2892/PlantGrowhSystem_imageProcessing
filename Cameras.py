from cv2 import *

def image_capture(camera_index):
    # Initialize the camera
    cam = VideoCapture(camera_index)   # camera_index is used to decide which camera to use
    ret, img = cam.read()
    if ret:    # If image captured without any errors
        namedWindow("cam-test",CV_WINDOW_AUTOSIZE)
        imshow("cam-test",img)
        waitKey(0)
        destroyWindow("cam-test")
        imwrite("filename.jpg",img) # Save image

def crop_image(x, y, w, h):
    img = cv2.imread("TestImage.jpg")
    # Crop the image with the given coordinates
    crop_img = img[y:y+h, x:x+w]
    cv2.imshow("cropped", crop_img)
    cv2.waitKey(0)
    imwrite("filename.jpg",crop_img)