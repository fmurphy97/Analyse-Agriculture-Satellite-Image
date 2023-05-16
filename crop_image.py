import cv2
import numpy as np
from matplotlib import pyplot as plt
import tkinter as tk

from tkinter import Tk, filedialog
from PIL import Image, ImageTk

# Define the global variables
points = []
img = None
canvas = None

def mouse_callback(event, x, y, flags, param):
    global points, img, canvas

    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(img, (x, y), 3, (0, 255, 0), -1)
        cv2.imshow('Image', img)

    elif event == cv2.EVENT_RBUTTONDOWN:
        if len(points) > 0:
            points.pop()
            img = cv2.imread('Images/sample_img_1.png')
            for point in points:
                cv2.circle(img, point, 3, (0, 255, 0), -1)
            cv2.imshow('Image', img)

def create_polygon(image_path):
    global points, img, canvas

    img = cv2.imread(image_path)
    clone = img.copy()

    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', mouse_callback)

    while True:
        cv2.imshow('Image', img)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('r'):
            img = clone.copy()
            points = []

        elif key == ord('c'):
            break

    cv2.destroyAllWindows()

    # Create a mask based on the selected points
    mask = np.zeros_like(clone[:, :, 0])
    points = np.array(points, dtype=np.int32)
    cv2.fillPoly(mask, [points], (255, 255, 255))

    # Apply the mask to the original image
    result = cv2.bitwise_and(clone, clone, mask=mask)

    #
    cv2.imwrite("Images/Output.png", result)

    # Display the result
    # plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    # plt.axis('off')
    # plt.show()

# Create a Tkinter window to open the file dialog
root = tk.Tk()
root.withdraw()

# Open the file dialog to select the image
image_path = filedialog.askopenfilename()

# Call the function to create the polygon and remove everything outside
create_polygon(image_path)