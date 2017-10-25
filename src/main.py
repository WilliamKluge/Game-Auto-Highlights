# Main file for Overwatch-Auto-Hilights
# Author: William Kluge
# Date: 2017-10-25
import cv2
import numpy
from moviepy.video.io.VideoFileClip import VideoFileClip
from matplotlib import pyplot as plt

from src.grip import GripPipeline


def convert_image(img):
    # img[:, :, 0] = numpy.ones([1080, 1920]) * 255
    # img[:, :, 1] = numpy.ones([1080, 1920]) * 255
    # img[:, :, 2] = numpy.ones([1080, 1920]) * 0
    # 
    # r, g, b = cv2.split(img)
    # return cv2.merge([b, g, r])
    return img[0, :, 0].max()


def main():
    pipline = GripPipeline
    input_path = input("Enter the path of the video to edit: ")

    input_video = VideoFileClip(input_path)

    for frame in input_video.iter_frames():

        pipline.process(frame)

        if pipline.find_contours_output:
            # If the array is not none


    print("Done.")


if __name__ == "__main__":
    main()
