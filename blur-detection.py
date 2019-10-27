# import the necessary packages
from imutils import paths
import argparse
import cv2
import sys
import shutil
import os

def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv2.Laplacian(image, cv2.CV_64F).var()
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
	help="path to input directory of images")
ap.add_argument("-t", "--threshold", type=float, default=100.0,
	help="focus measures that fall below this value will be considered 'blurry'")
ap.add_argument("-b", "--blurryPath", type=str, default="blurry",
	help="Sets a path to move blurry images to")	
args = vars(ap.parse_args())

blurryPath = args["blurryPath"]

# loop over the input images
for imagePath in paths.list_images(args["images"]):
	# load the image, convert it to grayscale, and compute the
	# focus measure of the image using the Variance of Laplacian
	# method
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	fm = variance_of_laplacian(gray)

	head, tail = os.path.split(imagePath)
	# print(head + " " + tail)

	# if fm > args["threshold"]:
	# 	text = imagePath+" - Not Blurry: "+str(fm)
	# 	print(imagePath+" - Not Blurry: "+str(fm))
 
	# if the focus measure is less than the supplied threshold,
	# then the image should be considered "blurry"
	if fm < args["threshold"]:
		text = imagePath+" - Blurry: "+str(fm)
		newImagePath = os.path.join(blurryPath, tail)
		print("Moving from " + imagePath + " to " + newImagePath + " because " + str(fm))
		shutil.move(imagePath, blurryPath + "/")
