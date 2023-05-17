import cv2
import numpy as np
from tkinter import Tk, filedialog


class ImageCropper:
    def __init__(self, image_path=None):

        # Define the global variables
        self.points = []
        self.lines = []
        self.img = None
        self.canvas = None

        self.mask = None
        self.image_path = image_path

    def mouse_callback(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:
            self.points.append((x, y))
            cv2.circle(self.img, (x, y), 3, (0, 255, 0), -1)
            cv2.imshow('Image', self.img)

            if len(self.points) > 1:
                prev_point = self.points[-2]
                curr_point = self.points[-1]
                self.lines.append((prev_point, curr_point))
                cv2.line(self.img, prev_point, curr_point, (0, 255, 0), 1)
                cv2.imshow('Image', self.img)

        elif event == cv2.EVENT_RBUTTONDOWN:
            if len(self.points) > 0:
                self.points.pop()
                self.img = cv2.imread(self.image_path)
                for point in self.points:
                    cv2.circle(self.img, point, 3, (0, 255, 0), -1)

                self.lines.clear()
                for i in range(len(self.points) - 1):
                    cv2.line(self.img, self.points[i], self.points[i + 1], (0, 255, 0), 1)

                cv2.imshow('Image', self.img)

    def create_polygon(self, image_path):

        self.img = cv2.imread(image_path)
        clone = self.img.copy()

        cv2.namedWindow('Image')
        cv2.setMouseCallback('Image', self.mouse_callback)

        while True:
            cv2.imshow('Image', self.img)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('r'):
                self.img = clone.copy()
                self.points.clear()
                self.lines.clear()

            elif key == ord('c'):
                break

        cv2.destroyAllWindows()

        # Create a mask based on the selected points
        self.mask = np.zeros_like(clone[:, :, 0])
        self.points = np.array(self.points, dtype=np.int32)
        cv2.fillPoly(self.mask, [self.points], (255, 255, 255))

    def run(self):

        # Create a Tkinter window to open the file dialog
        root = Tk()
        root.withdraw()

        if self.image_path is None:
            # Open the file dialog to select the image
            self.image_path = filedialog.askopenfilename()

        # Call the function to create the polygon and remove everything outside
        self.create_polygon(self.image_path)


if __name__ == "__main__":
    img_cropper = ImageCropper()
    img_cropper.run()
    selected_area = img_cropper.mask
