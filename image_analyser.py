import cv2
import numpy as np

from image_cropper import ImageCropper


class ImageAnalyser:
    COLOR_HSV_RANGES = [(37, 52, 68), (94, 255, 139)]

    def __init__(self, input_image_path):
        """Class in charge of analysing the image, making masks, calculating color ratios, and generate overlay output
        image"""
        self.filepath = input_image_path

        self.img = None  # input image
        self.overlay_img = None  # final image with colors on top

        self.color_mask = None  # mask, values >0 mean that the pixel is within the selected color range
        self.lot_mask = None  # mask, values > 0 mean that the pixel is within the selected area

        self.color_ratio = 0.0  # ratio of pixels that have the selected color and are in the selected range

    def create_color_mask(self):
        """Based on HSV color ranges creates an image mask"""
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, ImageAnalyser.COLOR_HSV_RANGES[0], ImageAnalyser.COLOR_HSV_RANGES[1])
        self.color_mask = mask

    def calculate_color_ratio(self):
        """Calculate the ratio of pixels that have the selected color within the selected range"""
        relevant_area = self.color_mask[self.lot_mask > 0]

        color_ratio = np.count_nonzero(relevant_area) / relevant_area.shape[0]
        self.color_ratio = color_ratio

    def create_overlay_img(self):
        """Creates image that hase the original image as base, the ignored areas in black, the desired areas in green"""
        final_img = self.img.copy()

        # Highlight greens
        mask_indices = self.color_mask > 0
        opacity = 0.2
        final_img[mask_indices] = ((1 - opacity) * final_img[mask_indices] + opacity * np.array([0, 255, 0]))

        # Dim Unwanted areas
        mask_indices = (self.lot_mask == 0)
        opacity = 0.7
        final_img[mask_indices] = ((1 - opacity) * final_img[mask_indices] + opacity * np.array([0, 0, 0]))

        self.overlay_img = final_img

    def create_lot_mask(self):
        """Prompt the user to select an area and creates a mask based on it"""
        img_cropper = ImageCropper(self.filepath)
        img_cropper.run()
        self.lot_mask = img_cropper.mask

    def analyse_img(self):
        """Runs all the image processing"""
        self.img = cv2.imread(self.filepath)
        self.create_color_mask()
        self.create_lot_mask()
        self.calculate_color_ratio()
        self.create_overlay_img()
