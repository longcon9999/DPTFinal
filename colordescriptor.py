import numpy as np
import cv2


def process2d(arr, x, y):
    count = 0
    for a in arr:
        if x <= a < y:
            count = count + 1
    return count


def normalized(hist):
    d = np.sum([a ** 2 for a in hist]) ** 0.5
    temp = []
    for i in hist:
        temp.append(i / d)
    return temp


class ColorDescriptor:
    def __init__(self, _bins):
        self.bins = _bins

    def describe2d(self, image):
        features = []
        (h, w) = image.shape[:2]
        (cX, cY) = (int(w / 2), int(h / 2))
        segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h), (0, cX, cY, h)]
        for (startX, endX, startY, endY) in segments:
            cornerMask = image[startX:endX, startY:endY]
            hist = self.hist2d(cornerMask)
            features.extend(hist)
        return features

    def hist2d(self, img):
        hist = []
        histB = np.histogram(img[0:, 0:, 0], bins=self.bins[0], range=[0, 256])
        histG = np.histogram(img[0:, 0:, 1], bins=self.bins[1], range=[0, 256])
        histR = np.histogram(img[0:, 0:, 2], bins=self.bins[2], range=[0, 256])
        # print("Hist B: ")
        # print(histB)
        # print("Hist G: ")
        # print(histB)
        # print("Hist R: ")
        # print(histB)
        hist.extend(histB[0])
        hist.extend(histG[0])
        hist.extend(histR[0])
        print(hist)
        return normalized(hist)

    def hist2dv2(self, image):
        hist = []
        # name = ['Hist B', 'Hist G', 'Hist R']
        for i in range(3):
            # print(name[i])
            n = 0.0
            n = 256 / self.bins[i]
            list_range = [0]
            for x in range(self.bins[i]):
                list_range.append(n * (x + 1))
            temp = []
            for x in range(len(list_range) - 1):
                count = process2d(image[0:, 0:, i].flatten(), list_range[x], list_range[x + 1])
                temp.append(count)
                # print("{}..{} : {}".format(list_range[x], list_range[x+1], count))
            hist.extend(temp)
        return normalized(hist)
