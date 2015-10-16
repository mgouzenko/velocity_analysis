#!/usr/local/bin/python
import sys
import os
import json

import cv2
import cv
import numpy as np
from PIL import Image, ImageDraw

CONFIG = "config.json"
START = "start.png"
END = "end.png"
OVERLAY = "overlayed.png"
ANNOTATED = "annotated.png"
FPS = 30.0

TYPE_TO_DIAMETER = {"3m": 3.04,
		    "2m": 2.04,
		    "1.5m": 1.54}

ESCAPE_VELOCITIES = {}
for key in TYPE_TO_DIAMETER:
	ESCAPE_VELOCITIES[key] = []

def main():
	if len(sys.argv) < 2:
		print "Point overlay at root of points"
		return
	test_root = sys.argv[1]
        for point_dir in [directory for directory in os.listdir(test_root) if not directory.startswith('.')]:
            try:
		make_images(os.path.join(test_root, point_dir))
            except Exception as e:
                print e
	print ESCAPE_VELOCITIES

def make_images(point_directory):
	config = json.load(open(os.path.join(point_directory, CONFIG)))
	start_image = Image.open(os.path.join(point_directory, START))
	end_image = Image.open(os.path.join(point_directory, END))

	mask=Image.new('L', start_image.size, color=122)
	end_image.paste(start_image, (config["x_delta"],
            config["y_delta"]), mask)
	end_image.save(os.path.join(point_directory, OVERLAY))

	draw = ImageDraw.Draw(start_image)
	total_lengths = 0
	total_pixels = 0
	for (xpos, ypos, rad) in config["spheres"]:
		draw.ellipse((xpos-rad, ypos-rad, xpos+rad, ypos+rad))
		total_pixels += rad * 2
		total_lengths += TYPE_TO_DIAMETER[config["sphere_type"]]
	length_per_pixel = total_lengths/total_pixels
	pixel_delta = (config["x_delta"] ** 2 + config["y_delta"] ** 2) ** 0.5
	length_traveled = pixel_delta * length_per_pixel
	seconds_elapsed = config["t_delta"]/FPS
	speed = length_traveled/seconds_elapsed
	ESCAPE_VELOCITIES[config["sphere_type"]].append(speed)

	# circles = find_circles(os.path.join(point_directory, START))
	# for (xpos, ypos, rad) in circles:
	# 	draw.ellipse((xpos-rad, ypos-rad, xpos+rad, ypos+rad))
	start_image.save(os.path.join(point_directory, ANNOTATED))

# def find_circles(img):
# 	image = cv2.imread(img)
# 	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# 	circles = cv2.HoughCircles(gray, cv.CV_HOUGH_GRADIENT, 13, minDist=50, param1=40, param2=150, minRadius=2,maxRadius=28)
# 	circles = np.round(circles[0, :]).astype("int")
# 	return circles


if __name__ == "__main__":
	main()
