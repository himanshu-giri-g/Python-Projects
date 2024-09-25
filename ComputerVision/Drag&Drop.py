import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np

# Set up the video capture and hand detector
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set width
cap.set(4, 720)   # Set height
detector = HandDetector(detectionCon=0.8)  # Initialize hand detector with confidence
colorR = (255, 0, 255)

# Class definition for draggable rectangles
class DragRect:
    def __init__(self, posCenter, size=[200, 200]):
        if len(posCenter) != 2:
            raise ValueError("posCenter must be a list or tuple of two elements.")
        self.posCenter = tuple(posCenter)  # Ensure it's a tuple
        self.size = size

    def update(self, cursor):
        if len(cursor) != 2:
            raise ValueError("Cursor must be a list or tuple of two elements.")
        self.posCenter = tuple(cursor)  # Ensure it remains a tuple
        cx, cy = self.posCenter  # This should now always work
        w, h = self.size

        # If the index finger tip is in the rectangle region, update the position
        if cx - w // 2 < cursor[0] < cx + w // 2 and \
                cy - h // 2 < cursor[1] < cy + h // 2:
            self.posCenter = cursor

# Create multiple draggable rectangles
rectList = []
for x in range(5):
    rectList.append(DragRect([x * 250 + 150, 150]))  # Initialize each rectangle correctly

def new_func(detector, img):
    hands, img = detector.findHands(img)  # Detect hands
    if hands:
        lmList = hands[0]['lmList']  # Extract landmark list from the first hand
        return lmList
    return None  # Return None if no hands are detected

while True:
    success, img = cap.read()  # Capture a frame
    img = cv2.flip(img, 1)  # Flip the image horizontally for a natural view
    lmList = new_func(detector, img)  # Get hand landmarks

    if lmList:
        # Get coordinates of index finger (landmark 8)
        x1, y1 = lmList[8][0], lmList[8][1]  # Coordinates of index finger tip

        cursor = [x1, y1]  # Create cursor from index finger tip coordinates
        print("Cursor coordinates:", cursor)  # Debugging print

        # Measure distance between index finger (8) and middle finger (12)
        if len(lmList) > 12:  # Ensure there are enough landmarks
            x2, y2 = lmList[12][0], lmList[12][1]  # Coordinates of middle finger tip
            l, info, img = detector.findDistance([x1, y1], [x2, y2], img)
            print("Distance:", l)  # Print distance for debugging
            
            if l < 30:  # If distance is less than 30, consider it a click or grab
                for rect in rectList:  # Update position of rectangles based on finger movement
                    rect.update(cursor)

    # Create a transparent image to draw the rectangles
    imgNew = np.zeros_like(img, np.uint8)
    for rect in rectList:
        cx, cy = rect.posCenter  # Unpack the center position
        w, h = rect.size
        cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2),
                      (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
        cvzone.cornerRect(imgNew, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)

    # Merge the original image and the transparent image
    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

    # Display the final output
    cv2.imshow("Image", out)
    cv2.waitKey(1)
