import cv2
import numpy as np
import matplotlib.pyplot as plt

from image_cropper import ImageCropper



class ImageAnalyser:

    COLOR_HSV_RANGES = [(37, 52, 68), (94, 255, 139)]

    def __init__(self, input_image_path):
        self.filepath = input_image_path
        self.img = None

        self.img = None
        self.overlay_img = None

        self.color_mask = None
        self.lot_mask = None

        self.color_ratio = 0.0

        self.analyse_img()

    def create_color_mask(self):
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, ImageAnalyser.COLOR_HSV_RANGES[0], ImageAnalyser.COLOR_HSV_RANGES[1])
        self.color_mask = mask

    def create_lot_mask(self):
        img_cropper = ImageCropper(self.filepath)
        img_cropper.run()
        self.lot_mask = img_cropper.mask

    def analyse_img(self):
        self.img = cv2.imread(self.filepath)
        self.create_color_mask()
        self.create_lot_mask()
        self.calculate_color_ratio()
        self.create_overlay_img()

    def calculate_color_ratio(self):
        relevant_area = self.color_mask[self.lot_mask > 0]

        color_ratio = np.count_nonzero(relevant_area) / relevant_area.shape[0]
        self.color_ratio = color_ratio

    def create_overlay_img(self):
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



