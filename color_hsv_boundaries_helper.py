import cv2
import numpy as np


def trackbar_callback(x):
    pass


# Load the image
image = cv2.imread("Images/sample_img_1.png")

# Create a window to display the image
cv2.namedWindow('image')

# Create trackbars to adjust the HSV values
cv2.createTrackbar('Hue Min', 'image', 0, 179, trackbar_callback)
cv2.createTrackbar('Saturation Min', 'image', 0, 255, trackbar_callback)
cv2.createTrackbar('Value Min', 'image', 0, 255, trackbar_callback)
cv2.createTrackbar('Hue Max', 'image', 0, 179, trackbar_callback)
cv2.createTrackbar('Saturation Max', 'image', 0, 255, trackbar_callback)
cv2.createTrackbar('Value Max', 'image', 0, 255, trackbar_callback)

# Set default values for maximum HSV trackbars
cv2.setTrackbarPos('Hue Max', 'image', 179)
cv2.setTrackbarPos('Saturation Max', 'image', 255)
cv2.setTrackbarPos('Value Max', 'image', 255)

# Initialize HSV min/max values
h_min = s_min = v_min = h_max = s_max = v_max = 0
prev_h_min = prev_s_min = prev_v_min = prev_h_max = prev_s_max = prev_v_max = 0

while True:
    # Get current positions of all trackbars
    h_min = cv2.getTrackbarPos('Hue Min', 'image')
    s_min = cv2.getTrackbarPos('Saturation Min', 'image')
    v_min = cv2.getTrackbarPos('Value Min', 'image')
    h_max = cv2.getTrackbarPos('Hue Max', 'image')
    s_max = cv2.getTrackbarPos('Saturation Max', 'image')
    v_max = cv2.getTrackbarPos('Value Max', 'image')

    # Set the minimum and maximum HSV values to display
    lower_hsv = np.array([h_min, s_min, v_min])
    upper_hsv = np.array([h_max, s_max, v_max])

    # Convert the image to HSV format and apply color thresholding
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_image, lower_hsv, upper_hsv)
    result = cv2.bitwise_and(image, image, mask=mask)

    # Print if there is a change in the HSV values
    if (prev_h_min != h_min) or (prev_s_min != s_min) or (prev_v_min != v_min) \
            or (prev_h_max != h_max) or (prev_s_max != s_max) or (prev_v_max != v_max):
        print("(Hue Min = %d, Saturation Min = %d, Value Min = %d), "
              "(Hue Max = %d, Saturation Max = %d, Value Max = %d)" % (
                  h_min, s_min, v_min, h_max, s_max, v_max))
        prev_h_min = h_min
        prev_s_min = s_min
        prev_v_min = v_min
        prev_h_max = h_max
        prev_s_max = s_max
        prev_v_max = v_max

    # Display the resulting image
    cv2.imshow('image', result)

    # Check for key press (press q to abort)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Close all windows
cv2.destroyAllWindows()
