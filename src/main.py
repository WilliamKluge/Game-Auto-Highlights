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


def process_video(input_path, selected_clips, name_image):
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

    start_process_time = -1

    for frame in input_video.iter_frames():
        # Iterates through the frames in a clip

        if processed_frames / video_fps <= start_process_time:
            processed_frames += 1
            continue

        pipline.process(frame)  # Processes the frame using the GRIP filter

        if len(pipline.find_contours_output) > 0:
            # If the array is not none (there are contours)
            if FRAME_BY_FRAME:
                # show the associated images
                plt.subplot(121), plt.imshow(frame, cmap='gray')
                plt.title("Scanned Image"), plt.xticks([]), plt.yticks([])
                plt.subplot(122), plt.imshow(pipline.rgb_threshold_output, cmap='gray')
                plt.title("RGB Filter Output"), plt.xticks([]), plt.yticks([])
                plt.suptitle("Frame Analysis")
                plt.show()

            clip_start_time = processed_frames / video_fps - CLIP_PRE_TIME
            clip_end_time = processed_frames / video_fps + CLIP_POST_TIME

            if clip_start_time < 0:
                clip_start_time = 0

            if clip_start_time < start_process_time:
                clip_start_time = start_process_time

            if clip_end_time > input_video.duration:
                # If the end of the clip would be past the end of the video
                clip_end_time = input_video.duration

            print("Selected video between", clip_start_time, "and", clip_end_time)

            selected_clips.append(input_video.subclip(clip_start_time, clip_end_time))
            start_process_time = clip_end_time + CLIP_POST_IGNORE_TIME

        # Prints out stats
        processed_frames += 1
        # fps = processed_frames / (time.time() - start)
        # print_stats(fps, frame_count)


def print_stats(fps, frame_count):
    print_string = str(round(fps, 2)) + "fps : Time Remaining: "
    time_remaining = frame_count / fps

    if time_remaining > 60:
        print_string += str(time_remaining / 60) + " minutes"
    else:
        print_string += str(time_remaining) + " seconds"


def preview_clip(clip, fps=60):
    screen = pygame.display.set_mode(clip.size)

    result = []

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
                        return result

            t1 = time.time()
            time.sleep(max(0, t - (t1 - t0)))
            imdisplay(img, screen)


def main():
    # Image that holds the user's name
    name_image = cv2.imread("name.png")
    # If the user should be asked if each clip should be a part of the demo
    USER_CHECK_CLIP = True

    pygame.init()

    # Get the path of the video to edit
    input_path = input("Enter the path of the video to edit: ")
    input_path = input_path.replace("\"", "")  # Removes the "" around the path so that file paths can be copied as path

    # Clips that were found to fit the criteria
    selected_clips = []

    if os.path.isdir(input_path):
        for input_path in os.listdir(input_path):
            process_video(input_path, selected_clips, name_image)
    else:
        process_video(input_path, selected_clips, name_image)

    extra_clips = dict()

    if USER_CHECK_CLIP:
        i = 0
        while i < len(selected_clips):

            preview_clip(selected_clips[i])

            decision = input("'y' to include clip in main series, "
                             "enter a name to put in separate serious, or "
                             "n to not include at all: ")

            if decision != "n" and decision != "y":
                series_key = decision

                if series_key in extra_clips:
                    extra_clips[series_key].append(selected_clips[i])
                else:
                    extra_clips[series_key] = [selected_clips[i]]

            if decision == "n" or decision != "y":
                # Should not be included or is in a separate series
                del selected_clips[i]
            else:
                # User entered 'y'
                i += 1

    pygame.quit()

    pre_string = input_path[:len(input_path) - 4] + "_output\\"

    if not os.path.exists(pre_string):
        os.makedirs(pre_string)

    for series_key, series in extra_clips.items():
        series_clip = concatenate_videoclips(series)
        series_clip.write_videofile(pre_string + series_key + ".mp4")

    # Writing video file
    final_clip = concatenate_videoclips(selected_clips)
    # Rename the video input_path (without the .mp4 extension) + _highlights.mp4
    final_clip.write_videofile(pre_string + "main_highlights.mp4")

    print("Done.")


if __name__ == "__main__":
    main()
