# import the necessary packages
from imutils import contours
import imutils
import cv2

images_names = ['Big.jpg', 'Medium.jpg', 'Small.jpg']
processed_images = []

def process_image():
    # Calculate the midpoint between 2 given points
    def midpoint(ptA, ptB):
        return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

    for image_name in images_names:
        # Load the image, convert it to grayscale, and blur it slightly
        image = cv2.imread(image_name)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        
        # Perform edge detection, then perform a dilation & erosion to close gaps in between object edges
        edged = cv2.Canny(gray, 50, 100)
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)
        
        # Find contours in the edge map
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        
        # Sort the contours from left-to-right
        (cnts, _) = contours.sort_contours(cnts)
        
        phoneRectangle = cnts[len(cnts)-1]
        rollerRectangle = cnts[0]
          
        # Bound the phone in a rectangle in order to calculate the phone width and height in pixels
        x1,y1,w1,h1 = cv2.boundingRect(phoneRectangle)
        cv2.rectangle(image, (x1,y1), (x1+w1,y1+h1), (0, 255, 0), 2) 
          
        # Bound the ruler in a rectangle in order to calculate the ruler height in pixels
        x2,y2,w2,h2 = cv2.boundingRect(rollerRectangle)
        cv2.rectangle(image, (x2,y2), (x2+w2,y2+h2), (0, 255, 0), 2) 
        
        # Calculate phone width and height in reference to the ruler height
        percentage_height = round((h1/h2)*100, 2)
        percentage_length = round((w1/h2)*100, 2)
        stringHeight = "Percentage of phone height from ruler height is: "+str(percentage_height)+"%"
        stringWidth = "Percentage of phone width from ruler height is: "+str(percentage_length)+"%"
        print(stringHeight)
        print(stringWidth)
        phoneHeight = round((percentage_height/100)*17 , 2)
        phoneWidth = round((percentage_length/100)*17, 2) 
        stringHeightCm = "Phone height is: "+str(phoneHeight)+" cm"
        stringWidthCm = "Phone width is: "+str(phoneWidth)+" cm"
        print(stringHeightCm)
        print(stringWidthCm)
         
        # Phone points: top-left, top-right, bottom-left, bottom-right
        tl = (x1,y1)
        tr = (x1+w1, y1)
        bl = (x1, y1+h1)
        br = (x1+w1, y1+h1)
         
        # Compute the midpoint between the top-left and top-right coordinates 
        # Followed by the midpoint between bottom-left and bottom-right coordinates
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)
         
        # Compute the midpoint between the top-left and bottom-left coordinates,
        # Followed by the midpoint between the top-right and bottom-right
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)
         
        # Draw the midpoints on the image
        cv2.circle(image, (int(tltrX), int(tltrY)), 6, (255, 255, 255), -1)
        cv2.circle(image, (int(blbrX), int(blbrY)), 6, (255, 255, 255), -1)
        cv2.circle(image, (int(tlblX), int(tlblY)), 6, (255, 255, 255), -1)
        cv2.circle(image, (int(trbrX), int(trbrY)), 6, (255, 255, 255), -1)
         
        # Draw lines between the midpoints
        cv2.line(image, (int(tltrX), int(tltrY+4)), (int(blbrX), int(blbrY-4)), (0, 0, 255), 2)
        cv2.line(image, (int(tlblX+4), int(tlblY)), (int(trbrX-4), int(trbrY)), (255, 0, 0), 2)
         
        # Draw the object sizes on the image
        # Draw phone height
        cv2.putText(image, "{:.2f}cm".format(phoneHeight), (int(tltrX - 30), int(tltrY - 10)), cv2.FONT_ITALIC, 0.65, (0, 0, 255), 2)
        # Draw phone width
        cv2.putText(image, "{:.2f}cm".format(phoneWidth), (int(trbrX + 10), int(trbrY+5)), cv2.FONT_ITALIC, 0.65, (255, 0, 0), 2)
        
        # Add processed image to processed images list
        processed_images.append(image)
        
if __name__ == "__main__":
    process_image()
    # Show the output images
    cv2.imshow("Big Picture: Phone Width & Height", processed_images[0])
    cv2.imshow("Medium Picture: Phone Width & Height", processed_images[1])
    cv2.imshow("Small Picture: Phone Width & Height", processed_images[2])
    cv2.waitKey(0)

