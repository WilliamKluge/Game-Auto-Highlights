# Main file for Overwatch-Auto-Hilights
# Author: William Kluge
# Date: 2017-10-25
import cv2
import numpy
import time
import os

import pygame
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.editor import VideoFileClip
from matplotlib import pyplot as plt
from moviepy.video.io.preview import imdisplay

from src.GUI.MainGUI import MainGUI
from src.grip import GripPipeline


def interactive_adjust(pipeline, frame):
    """
    Allows for the user to dynamically adjust the RGB selection values for GRIP processing.
    :param pipeline: GRIP Pipeline being used
    :param frame: Frame to be processed
    :return: None
    """
    # show the associated images
    plt.subplot(121), plt.imshow(frame, cmap='gray')
    plt.title("Scanned Image"), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(pipeline.rgb_threshold_output, cmap='gray')
    plt.title("RGB Filter Output"), plt.xticks([]), plt.yticks([])
    plt.suptitle("Frame Analysis")
    plt.show()

    choice = input("Adjust RGB (y/n): ")

    if choice == "y":
        r1 = float(input("r1 adjust"))
        r2 = float(input("r2 adjust"))
        g1 = float(input("g1 adjust"))
        g2 = float(input("g2 adjust"))
        b1 = float(input("b1 adjust"))
        b2 = float(input("b2 adjust"))

        pipeline.adjust_rgb(r1, r2, g1, g2, b1, b2)

        pipeline.process(frame)

        interactive_adjust(pipeline, frame)





def print_stats(fps, frame_count):
    """
    Prints the stats for the program
    :param fps: Frames per second of the video
    :param frame_count: Number of the frame that was just processed (the most recent frame)
    :return:
    """
    print_string = str(round(fps, 2)) + "fps : Time Remaining: "
    time_remaining = frame_count / fps

    if time_remaining > 60:
        print_string += str(time_remaining / 60) + " minutes"
    else:
        print_string += str(time_remaining) + " seconds"


def main():
    gui = MainGUI()

    print("Done.")


if __name__ == "__main__":
    main()
