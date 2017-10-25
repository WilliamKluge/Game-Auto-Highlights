# Main file for Overwatch-Auto-Hilights
# Author: William Kluge
# Date: 2017-10-25
import cv2
import numpy
from moviepy.video.io.VideoFileClip import VideoFileClip
from matplotlib import pyplot as plt


def convert_image(img):
    # img[:, :, 0] = numpy.ones([1080, 1920]) * 255
    # img[:, :, 1] = numpy.ones([1080, 1920]) * 255
    # img[:, :, 2] = numpy.ones([1080, 1920]) * 0
    # 
    # r, g, b = cv2.split(img)
    # return cv2.merge([b, g, r])
    return img[0, :, 0].max()


def main():
    name_image = cv2.imread("name.png")
    method = cv2.TM_SQDIFF
    input_path = input("Enter the path of the video to edit:")

    input_video = VideoFileClip(input_path)

    for frame in input_video.iter_frames():
        w, h = 133, 50
        start_x, start_y = 1530, 40
        image = frame[start_y:start_y+h, start_x:start_x+w]
        frame_copy = frame

        # Apply template Matching
        res = cv2.matchTemplate(image, name_image, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc

        bottom_right = (top_left[0] + w + start_x, top_left[1] + h + start_y)
        # cv2.rectangle(frame_copy, (top_left[0] + 1528, top_left[1] + 65), bottom_right, 255, 2)
        cv2.rectangle(frame_copy, (start_x, start_y), (start_x + w, start_y + h), 255, 5)

        if min_val > 0.5:
            plt.subplot(131), plt.imshow(image, cmap='gray')
            plt.title("Scanned Image Area"), plt.xticks([]), plt.yticks([])
            plt.subplot(132), plt.imshow(res, cmap='gray')
            plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
            plt.subplot(133), plt.imshow(frame_copy, cmap='gray')
            plt.title('Detected Point in Image'), plt.xticks([]), plt.yticks([])
            plt.suptitle("cv2.TM_SQDIFF")
            plt.show()

    print("Done.")


if __name__ == "__main__":
    main()
