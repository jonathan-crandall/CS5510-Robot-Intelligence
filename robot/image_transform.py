# %%
import cv2
from matplotlib import pyplot as plt
import numpy as np


class ImgTransform:
    def __init__(self, image):
        fig, self.axs = plt.subplots(3, 2)

        self.axs[0, 0].imshow(image)
        self.axs[0, 0].set_title("Unfiltered Image")

        filtered_image = self.apply_filter(image)
        threshold_image = self.apply_threshold(filtered_image)

        cnv, largest_contour = self.detect_contour(threshold_image, image.shape)
        self.corners = self.detect_corners_from_contour(cnv, largest_contour)

        self.destination_points, self.h, self.w = self.get_destination_points(
            self.corners
        )
        self.cropped = cv2.cvtColor(self.transform(image), cv2.COLOR_BGR2RGB)

        self.axs[2, 1].imshow(self.cropped)
        self.axs[2, 1].set_title("Filtered Image")
        fig.tight_layout(pad=0.5)
        plt.show()

        # f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
        # # f.subplots_adjust(hspace=.2, wspace=.05)
        # ax1.imshow(un_warped)
        # ax2.imshow(cropped)
        # plt.show()

    def apply_filter(self, image):

        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        kernel = np.ones((5, 5), np.float32) / 15
        filtered = cv2.filter2D(gray, -1, kernel)
        self.axs[0, 1].imshow(cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB))
        self.axs[0, 1].set_title("Filtered Image")
        return filtered

    def apply_threshold(self, filtered):

        ret, thresh = cv2.threshold(filtered, 250, 255, cv2.THRESH_OTSU)
        self.axs[1, 0].imshow(cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB))
        self.axs[1, 0].set_title("After applying OTSU threshold")
        return thresh

    def detect_contour(self, img, image_shape):

        canvas = np.zeros(image_shape, np.uint8)
        contours, hierarchy = cv2.findContours(
            img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
        )
        cnt = sorted(contours, key=cv2.contourArea, reverse=True)[0]
        cv2.drawContours(canvas, cnt, -1, (0, 255, 255), 3)
        self.axs[1, 1].set_title("Largest Contour")
        self.axs[1, 1].imshow(canvas)
        return canvas, cnt

    def detect_corners_from_contour(self, canvas, cnt):

        epsilon = 0.02 * cv2.arcLength(cnt, True)
        approx_corners = cv2.approxPolyDP(cnt, epsilon, True)
        cv2.drawContours(canvas, approx_corners, -1, (255, 255, 0), 10)
        approx_corners = sorted(np.concatenate(approx_corners).tolist())
        # print('\nThe corner points are ...\n')
        for index, c in enumerate(approx_corners):
            character = chr(65 + index)
            # print(character, ':', c)
            cv2.putText(
                canvas,
                character,
                tuple(c),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                2,
                cv2.LINE_AA,
            )

        # Rearranging the order of the corner points
        # print(approx_corners)
        approx_corners = [approx_corners[i] for i in [1, 2, 0, 3]]
        self.axs[2, 0].imshow(canvas)
        self.axs[2, 0].set_title("Corner Points: Douglas-Peucker")
        return approx_corners

    def get_destination_points(self, corners):

        w1 = np.sqrt(
            (corners[0][0] - corners[1][0]) ** 2 + (corners[0][1] - corners[1][1]) ** 2
        )
        w2 = np.sqrt(
            (corners[2][0] - corners[3][0]) ** 2 + (corners[2][1] - corners[3][1]) ** 2
        )
        w = min(int(w1), int(w2))

        h1 = np.sqrt(
            (corners[0][0] - corners[2][0]) ** 2 + (corners[0][1] - corners[2][1]) ** 2
        )
        h2 = np.sqrt(
            (corners[1][0] - corners[3][0]) ** 2 + (corners[1][1] - corners[3][1]) ** 2
        )
        h = max(int(h1), int(h2))

        destination_corners = np.float32(
            [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
        )

        # print('\nThe destination points are: \n')
        for index, c in enumerate(destination_corners):
            character = chr(65 + index) + "'"
            # print(character, ':', c)

        # print('\nThe approximated height and width of the original image is: \n', (h, w))
        return destination_corners, h, w

    def unwarp(self, img, src, dst):

        h, w = img.shape[:2]
        H, _ = cv2.findHomography(
            src, dst, method=cv2.RANSAC, ransacReprojThreshold=3.0
        )
        # print('\nThe homography matrix is: \n', H)
        un_warped = cv2.warpPerspective(img, H, (w, h), flags=cv2.INTER_LINEAR)

        return un_warped

    def transform(self, image):
        un_warped = self.unwarp(
            image, np.float32(self.corners), self.destination_points
        )

        cropped = un_warped[0 : self.h, 0 : self.w]
        # cv2.imwrite("images/cropped.jpg", cropped)
        return cropped


# %%
# Example usage

if __name__ == "__main__":
    image = cv2.imread("images/workspace.jpg")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    transform = ImgTransform(image)
    transform.transform(image)
# %%
