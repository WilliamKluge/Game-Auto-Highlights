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


def process_video(input_path, selected_clips, name_image):
    """
    Processes a video, selecting out portions that are designated by the GRIP filters to be important
    :param input_path: Path to the video file
    :param selected_clips: Array to put clips into
    :param name_image: Image to use as a template for the GRIP pipeline to search through
    :return: None
    """
    # Show every selected frame
    FRAME_BY_FRAME = False
    # Time (in seconds) to select before each kill
    CLIP_PRE_TIME = 4
    # Time (in seconds) to select after each kill
    CLIP_POST_TIME = 4
    # Time (in seconds) to ignore after the end of each clip
    CLIP_POST_IGNORE_TIME = 0

    # Read the path into memory as a video clip
    input_video = VideoFileClip(input_path)
    # Create the GRIP Pipeline for image processing
    pipline = GripPipeline(name_image)
    # Amount of frames processed
    processed_frames = 0
    # Video FPS
    video_fps = input_video.fps

    previous_clip_end = -1

    for frame in input_video.iter_frames():
        # Iterates through the frames in a clip
        if processed_frames / video_fps <= previous_clip_end:
            # If this frame is already part of the last clip, skip it
            processed_frames += 1
            continue

        pipline.process(frame)  # Processes the frame using the GRIP filter

        if pipline.find_contours_output is not None:
            # If the array is not none (there are contours)
            if FRAME_BY_FRAME:
                interactive_adjust(pipline, frame)

            clip_start_time = processed_frames / video_fps - CLIP_PRE_TIME
            clip_end_time = processed_frames / video_fps + CLIP_POST_TIME

            if clip_start_time < 0:
                # Prevents the start time being before 0 seconds
                clip_start_time = 0

            if clip_start_time < previous_clip_end:
                # Prevents overlap from this clip and the previous
                clip_start_time = previous_clip_end

            if clip_end_time > input_video.duration:
                # Prevents this clip from trying to end after the video is over
                clip_end_time = input_video.duration

            print("Selected video between", clip_start_time, "and", clip_end_time)

            # Add the subclip of the video between the start and end times to the selected clips array
            selected_clips.append(input_video.subclip(clip_start_time, clip_end_time))
            # Specify the ending time of this clip to prevent overlap
            previous_clip_end = clip_end_time + CLIP_POST_IGNORE_TIME

        # Prints out stats
        processed_frames += 1
        # fps = processed_frames / (time.time() - start)
        # print_stats(fps, frame_count)


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


def preview_clip(clip, fps=60):
    """
    Previews the clip in a pygame window until the user presses esc
    :param clip: Clip to preview
    :param fps: Frames per second to play the video at
    :return: None
    """
    screen = pygame.display.set_mode(clip.size)

    t0 = time.time()
    loop_clip = True
    while loop_clip:
        for t in numpy.arange(1.0 / fps, clip.duration - .001, 1.0 / fps):

            img = clip.get_frame(t)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:

                        # if audio:
                        #     videoFlag.clear()
                        pygame.quit()
                        return

            t1 = time.time()
            time.sleep(max(0, t - (t1 - t0)))
            imdisplay(img, screen)


def main():
    # Image that holds the user's name
    name_image = cv2.imread("name.png")
    # If the user should be asked if each clip should be a part of the demo
    USER_CHECK_CLIP = True

    pygame.init()  # Starts pygame

    # Get the path of the video to edit
    input_path = input("Enter the path of the video to edit: ")
    input_path = input_path.replace("\"", "")  # Removes the "" around the path so that file paths can be copied as path

    # Clips that were found to fit the criteria
    selected_clips = []

    if os.path.isdir(input_path):
        # If the input path was a directory
        for video_name in os.listdir(input_path):
            # Loop through every file in that directory
            process_video(input_path + "\\" + video_name, selected_clips, name_image)
    else:
        # Otherwise just process the given path
        process_video(input_path, selected_clips, name_image)

    # Dictionary for clips that the user does not want as part of the main series, but still wants to keep
    extra_clips = dict()

    if USER_CHECK_CLIP:
        # If the user is supposed to verify every clip before the highlight reel is printed
        i = 0
        while i < len(selected_clips):
            # While there are still clips to preview
            # Preview the clip
            preview_clip(selected_clips[i])

            decision = input("'y' to include clip in main series, "
                             "enter a name to put in separate serious, or "
                             "n to not include at all: ")

            if decision != "n" and decision != "y":
                # If the user did not say 'n' to delete the clip or 'y' to keep in in the main series, it is an extra
                series_key = decision

                if series_key not in extra_clips:
                    # If the series key is not already established, create the array for it
                    extra_clips[series_key] = []

                extra_clips[series_key].append(selected_clips[i])  # Add the clip to the series

            if decision == "n" or decision != "y":
                # Should not be included or is in a separate series, just delete it
                del selected_clips[i]
            else:
                # User entered 'y', just continue on with the previews
                i += 1

    pygame.quit()  # Stop running pygame after the previews are all over (should already be quit, this is a guarantee)

    pre_string = input_path[:len(input_path) - 4] + "_output\\"  # Output directory is a modified version of the input

    if not os.path.exists(pre_string):
        # If the directory does not exist, create it
        os.makedirs(pre_string)

    for series_key, series in extra_clips.items():
        # For every series created, concatenate all the clips and write the video file
        series_clip = concatenate_videoclips(series)
        series_clip.write_videofile(pre_string + series_key + ".mp4")

    # Concatenates clips and writes the main video file
    final_clip = concatenate_videoclips(selected_clips)
    final_clip.write_videofile(pre_string + "main_highlights.mp4")

    print("Done.")


if __name__ == "__main__":
    main()
