# Analyse Crop Image
Based on an input satellite image check what percentage is green surface.
The user can select which area to analyse, and based on the colors in the picture analyse where there are crops and where there is an empyt patch.


Here we can see an example of a satellite picture where the green surface area is of  70.4%

![Initial & Final Images](Images/Outputs/first_and_final_images.png)


The code works by:
* Selecting HSV color threshold (you can canalise the most adequate threshold in [HSV Boundaries Helper](color_hsv_boundaries_helper.py))
* Converting the image to HSV colors
* Filter the colors beyond the thresholds
![Color Mask](Images/Outputs/green_color_mask.png)
* Select the desired area of the picture
![Lot Crop](Images/Outputs/desired_lot_crop.png)
* Calculate green percentage and create an output picture
![Color Mask](Images/Outputs/final_image.png)