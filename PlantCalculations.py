import imutils
import cv2

def image_contours(image_name):
    # Load the image, convert it to grayscale, and blur it slightly
    image = cv2.imread(image_name)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # Perform edge detection, then perform a dilation & erosion to close gaps in between object edges
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    
    # Find contours in the edge map (for max size)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
   
    # Sort contours by area
    cntsSorted = sorted(cnts, key=lambda x: cv2.contourArea(x))
    return [cntsSorted,image]

def draw_image_midpoints(image, draw_flg, parm_tl, parm_tr, parm_bl, parm_br, height = 0, length = 0, width = 0):
    
    def midpoint(ptA, ptB):
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
    if draw_flg == 0:
        cv2.circle(image, (int(tltrX), int(tltrY)), 6, (255, 255, 255), -1) # Top 
    cv2.circle(image, (int(tlblX), int(tlblY)), 6, (255, 255, 255), -1) # Left
    cv2.circle(image, (int(trbrX), int(trbrY)), 6, (255, 255, 255), -1) # Right
      
    # Draw lines between the midpoints
    if draw_flg == 0:
        cv2.line(image, (int(tltrX), int(tltrY+4)), (int(blbrX), int(blbrY)), (0, 0, 255), 2) # Height
    cv2.line(image, (int(tlblX+4), int(tlblY)), (int(trbrX-4), int(trbrY)), (255, 0, 0), 2) # Length / Width (depends on draw_flg)
      
    # Draw the object sizes on the image
    if draw_flg == 0:
        # Draw plant height
        cv2.putText(image, "{:.2f}cm".format(height), (int(tltrX - 30), int(tltrY - 10)), cv2.FONT_ITALIC, 0.65, (0, 0, 255), 2)
        # Draw plant length
        cv2.putText(image, "{:.2f}cm".format(length), (int(trbrX + 10), int(trbrY+5)), cv2.FONT_ITALIC, 0.65, (255, 0, 0), 2)
    else:
        # Draw plant width
        cv2.putText(image, "{:.2f}cm".format(width), (int(trbrX + 10), int(trbrY+5)), cv2.FONT_ITALIC, 0.65, (255, 0, 0), 2)
    
    if draw_flg == 0:
        front_image = image 
        return front_image
    else:
        side_image = image
        return side_image