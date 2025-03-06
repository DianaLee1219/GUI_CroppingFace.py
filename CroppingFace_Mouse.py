import cv2 # type: ignore
import time  # For delaying window closing

image = cv2.imread("sample.jpg",1)

# Make a dummy image, will be useful to clear the drawing
dummy = image.copy()
cv2.namedWindow("Window")

# restore points
pt1 = None
pt2 = None

# Cropped image status
cropped = False 

k = 0

def drawRectangular(action, x, y, flags, userdata):
    # Referencing global variables 
    global pt1, pt2, k, cropped

    # Action to be taken when left mouse button is pressed
    if action==cv2.EVENT_LBUTTONDOWN:
        pt1=(x,y)
        # Mark the point
        cv2.circle(image, pt1, 2, (255,255,0), 2)

    # Action to be taken when left mouse button is released
    elif action==cv2.EVENT_LBUTTONUP:
        pt2=(x,y)
        # Mark the rectangle
        cv2.rectangle(image, pt1, pt2, (255,255,0), 2)
        cv2.imshow("Window",image)

    # Save the cropped region
    if pt1 and pt2:
        x1, y1 = min(pt1[0], pt2[0]), min(pt1[1], pt2[1])
        x2, y2 = max(pt1[0], pt2[0]), max(pt1[1], pt2[1])

        cropped_image = dummy[y1:y2, x1:x2]  # Crop from original image

        if cropped_image.size > 0:  # Ensure valid cropping
            cv2.imwrite("cropped_image.jpg", cropped_image)
            cropped = True

# Set mouse callback function
cv2.setMouseCallback("Window", drawRectangular)

while k != 27:  # Press 'Esc' to exit
    cv2.imshow("Window", image)
    cv2.putText(image, "Choose top left corner, and drag?",
               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    k = cv2.waitKey(20) & 0xFF

    # If cropping is done, wait 1 second then close
    if cropped:
        cv2.waitKey(1000)  # Wait 1 second
        break

cv2.destroyAllWindows()
