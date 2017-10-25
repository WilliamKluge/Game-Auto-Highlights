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
    method = cv2.TM_SQDIFF_NORMED
    input_path = input("Enter the path of the video to edit:")

    input_video = VideoFileClip(input_path)

    for frame in input_video.iter_frames():
        
        #image = convert_image(frame)
        w, h = 1920, 1080
        # Apply template Matching
        res = cv2.matchTemplate(frame, name_image, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc

        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(frame, top_left, bottom_right, 255, 2)

        if max_val >= 0.5:
            plt.subplot(121), plt.imshow(res, cmap='gray')
            plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
            plt.subplot(122), plt.imshow(frame, cmap='gray')
            plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
            plt.suptitle("sqdiff_norm")
            plt.show()

    print("Done.")


if __name__ == "__main__":
    main()
