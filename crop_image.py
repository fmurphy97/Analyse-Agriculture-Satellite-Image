import cv2
import numpy as np
from matplotlib import pyplot as plt
from tkinter import Tk, filedialog

# Define the global variables
points = []
lines = []
img = None
canvas = None

def mouse_callback(event, x, y, flags, param):
    global points, lines, img, canvas

    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(img, (x, y), 3, (0, 255, 0), -1)
        cv2.imshow('Image', img)

        if len(points) > 1:
            prev_point = points[-2]
            curr_point = points[-1]
            lines.append((prev_point, curr_point))
            cv2.line(img, prev_point, curr_point, (0, 255, 0), 1)
            cv2.imshow('Image', img)

    elif event == cv2.EVENT_RBUTTONDOWN:
        if len(points) > 0:
            points.pop()
            img = cv2.imread(image_path)
            for point in points:
                cv2.circle(img, point, 3, (0, 255, 0), -1)

            lines.clear()
            for i in range(len(points) - 1):
                cv2.line(img, points[i], points[i + 1], (0, 255, 0), 1)

            cv2.imshow('Image', img)

def create_polygon(image_path):
    global points, lines, img, canvas

    img = cv2.imread(image_path)
    clone = img.copy()

    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', mouse_callback)

    while True:
        cv2.imshow('Image', img)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('r'):
            img = clone.copy()
            points.clear()
            lines.clear()

        elif key == ord('c'):
            break

    cv2.destroyAllWindows()

    # Create a mask based on the selected points
    mask = np.zeros_like(clone[:, :, 0])
    points = np.array(points, dtype=np.int32)
    cv2.fillPoly(mask, [points], (255, 255, 255))

    # Apply the mask to the original image
    result = cv2.bitwise_and(clone, clone, mask=mask)

    cv2.imwrite("output.png", result)

# Create a Tkinter window to open the file dialog
root = Tk()
root.withdraw()

# Open the file dialog to select the image
image_path = filedialog.askopenfilename()

# Call the function to create the polygon and remove everything outside
create_polygon(image_path)