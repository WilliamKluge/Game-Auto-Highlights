# Main file for Overwatch-Auto-Hilights
# Author: William Kluge
# Date: 2017-10-25
import cv2
import numpy
import time
from moviepy.video.io.VideoFileClip import VideoFileClip
from matplotlib import pyplot as plt

from src.grip import GripPipeline


def print_stats(fps, frame_count):
    print_string = str(round(fps, 2)) + "fps : Time Remaining: "
    time_remaining = frame_count / fps

    if time_remaining > 60:
        print_string += str(time_remaining / 60) + " minutes"
    else:
        print_string += str(time_remaining) + " seconds"


def main():
    name_image = cv2.imread("name.png")
    pipline = GripPipeline(name_image)
    input_path = input("Enter the path of the video to edit: ")
    input_path = input_path.replace("\"", "")  # Removes the "" around the path so that file paths can be copied as path

    input_video = VideoFileClip(input_path)

    start = time.time()
    processed_frames = 0
    # Amount of frames in the video
    frame_count = int(input_video.fps * input_video.duration)

    for frame in input_video.iter_frames():

        pipline.process(frame)

        if len(pipline.find_contours_output) > 0:
            # If the array is not none (there are contours)
            plt.subplot(121), plt.imshow(frame, cmap='gray')
            plt.title("Scanned Image"), plt.xticks([]), plt.yticks([])
            plt.subplot(122), plt.imshow(pipline.rgb_threshold_output, cmap='gray')
            plt.title("RGB Filter Output"), plt.xticks([]), plt.yticks([])
            plt.suptitle("Frame Analysis")
            plt.show()

        processed_frames += 1
        print("Processed frame #" + str(processed_frames))
        if processed_frames % 10 == 0:
            fps = processed_frames / (time.time() - start)
            print_stats(fps, frame_count)

    print("Done.")


if __name__ == "__main__":
    main()
