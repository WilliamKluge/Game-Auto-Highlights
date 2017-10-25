# Main file for Overwatch-Auto-Hilights
# Author: William Kluge
# Date: 2017-10-25
import cv2
import numpy
import time
from moviepy.video.io.VideoFileClip import VideoFileClip
from matplotlib import pyplot as plt

from src.grip import GripPipeline


def main():
    name_image = cv2.imread("name.png")
    pipline = GripPipeline(name_image)
    input_path = input("Enter the path of the video to edit: ")

    input_video = VideoFileClip(input_path)

    start = time.time()
    processed_frames = 0

    for frame in input_video.iter_frames():

        pipline.process(frame)

        if pipline.find_contours_output:
            # If the array is not none (there are contours
            plt.subplot(111), plt.imshow(frame, cmap='gray')
            plt.title("Contours found on image"), plt.xticks([]), plt.yticks([])
            plt.suptitle("Scanned image")
            plt.show()

        processed_frames += 1
        if processed_frames % 100 == 0:
            print(processed_frames / (time.time() - start), "fps")

    print("Done.")


if __name__ == "__main__":
    main()
