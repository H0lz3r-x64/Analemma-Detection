import math
import numpy as np
import cv2
import os
import sys
import xlsxwriter

sys.path.append("..")
import Util
from Util.Image import Image
from Util.Contours import Contours
from Util.Draw import Draw


def main():
    lastCenterXY = (0.0, 0.0)
    data = list[list[str]]()

    directory = r'..\InputImages\2020_14_Uhr'
    allFiles = os.listdir(directory)

    # iterate over files in that directory
    for filename in allFiles:

        # checking if suffix is of image type
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            f = os.path.join(directory, filename)

            # checking if it is a file
            if os.path.isfile(f):

                # read image
                img = cv2.imread(f)

                # run sun recognition
                centerXY = find_brightest(img, lastCenterXY, filename[:10])
                if centerXY != (0.0, 0.0):
                    lastCenterXY = centerXY

                # append result to data list
                data.append([filename[:10], str(centerXY[0]), str(centerXY[1])])

    # finally write data to excel file
    write_to_excel(data)


def find_brightest(img: np.ndarray, last_center: tuple, filename="img", radius=51) -> list:
    # reduce image size by 20px on all sides and auto converts it to gray
    img = Image.size_reduction(img, 20)

    # blur the img
    blur = cv2.GaussianBlur(img, (radius, radius), 0)

    # calculate minMax method
    minMaxMethod = img.copy()
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(blur)
    minMaxCenter = maxLoc

    # apply the minMax method
    cv2.circle(minMaxMethod, maxLoc, radius, (0, 0, 0), 1)

    # prepare the img for the robust method
    thresh = cv2.threshold(blur, 210, 225, cv2.THRESH_BINARY)[1]
    erode = cv2.erode(thresh, None, iterations=7)
    dilate = cv2.dilate(erode, None, iterations=4)
    canny = Image.get_formated_canny(dilate)

    # calculate robust method
    points = np.argwhere(canny > 0)
    robustCenter, radius = cv2.minEnclosingCircle(points)

    # apply robust method
    robustMethod = img.copy()
    x = int(robustCenter[1])
    y = int(robustCenter[0])
    rad = int(radius)
    cv2.circle(robustMethod, (x, y), rad, (0, 0, 0), 1)

    # debug print
    print("lastCenter: " + str(last_center))
    print("dist: " + str(math.dist(robustCenter, last_center)))
    print("robustCenter: " + str(robustCenter))
    print("maxLoc: " + str(robustCenter))
    print("----------------------------------")

    # determine which method to use
    result = minMaxMethod.copy()
    center = minMaxCenter

    if robustCenter == (0.0, 0.0):
        if last_center != (0.0, 0.0):
            if not(math.dist(minMaxCenter, last_center) < 50):
                result = robustMethod.copy()
                center = robustCenter
        else:
            result = img.copy()
            center = (0.0, 0.0)

    # debug output
    labels = [[filename, "thresh", "canny"], ["minMax method", "robust method", "result"]]
    stacked = Image.stackImages([[img, thresh, canny], [minMaxMethod, robustMethod, result]], 0.7, labels)
    Image.show(stacked)

    # return result of determined method
    return center


def write_to_excel(data: list[list[str]]):
    # open workbook
    workbook = xlsxwriter.Workbook(
        r'..\OutputData\analemma_13Uhr.xlsx')

    # either get the first worksheet or create one if none exists
    if len(workbook.worksheets()) == 0:
        worksheet = workbook.add_worksheet()
    else:
        worksheet = workbook.worksheets()[0]


    worksheet.write('A1', 'Date')
    worksheet.write('B1', 'X')
    worksheet.write('C1', 'Y')

    for i, value in enumerate(data):
        i = i + 2
        worksheet.write('A' + str(i), value[0])
        worksheet.write('B' + str(i), round(float(value[1]), 2))
        worksheet.write('C' + str(i), round(float(value[2]), 2))
        worksheet.autofit()
    workbook.close()


if __name__ == '__main__':
    main()
