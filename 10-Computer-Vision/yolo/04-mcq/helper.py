import math
import cv2
import hashlib
import string
import random
import numpy as np


import pytesseract
import matplotlib.pyplot as plt
import re

def get_confidence(box):
    return math.ceil(box.conf[0] * 100) / 100


def get_class_name(model, box):
    return model.names[int(box.cls[0])]


def get_width_height(data):
    if isinstance(data, list):
        x1, y1, x2, y2 = data
        w, h = x2 - x1, y2 - y1
    else:
        x1, y1, x2, y2 = [int(_) for _ in box.xyxy[0]]
        w, h = x2 - x1, y2 - y1

    return w, h


def get_points(box):
    x1, y1, x2, y2 = [int(_) for _ in box.xyxy[0]]
    return x1, y1, x2, y2


def get_video_shape(cap):
    return (
        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    )


def md5(str):
    return hashlib.md5(str.encode('utf-8')).hexdigest()


def get_center_point_of_rectangle(p1: tuple, p2: tuple):
    width, height = get_width_height([*p1, *p2])
    xc = p1[0] + width // 2
    yc = p1[1] + height // 2
    return xc, yc


def is_toched_line(lineCoordinates: list, point: tuple, thickness: int = 20):
    return (lineCoordinates[0] < point[0] < lineCoordinates[2]
            and lineCoordinates[1]-thickness < point[1] < lineCoordinates[3]+thickness)


def imread(path, size: tuple = (1280, 720)):
    img = cv2.imread(path)
    return cv2.resize(img, size)


def imshow(img, wait_key: int = 0, window_name: str = None):
    if not window_name:
        window_name = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=5)
        )
    cv2.imshow(window_name, img)
    cv2.waitKey(wait_key)


def imgray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def imgblur(img):
    return cv2.GaussianBlur(img, (5, 5), 10)


def imgcanny(img):
    return cv2.Canny(img, 10, 50)


def getCornerPoint(contour):
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02*peri, True)
    return approx


def drawContours(img, contours: list = [], colors: list = [], thickness: int = 5):
    imgTemp = img.copy()
    for i, c in enumerate(contours):
        imgTemp = cv2.drawContours(
            imgTemp, c, -1, colors[i] if len(colors)>i else (0, 255, 0), thickness)
    return imgTemp


def getRectContour(contours):
    rectangles = []
    for contour in contours:
        approx = getCornerPoint(contour)
        if len(approx) == 4:
            rectangles.append(contour)
    return rectangles


def rectWithMinArea(contours, min_area: int = 0, max_area: int = 0):
    items = []
    rectangles = getRectContour(contours)
    for contour in rectangles:
        area = cv2.contourArea(contour)
        if (area >= min_area if min_area else True) and (max_area >= area if max_area else True):
            items.append(contour)
    return items


def reorderPoints(points):
    points = points.reshape((4, 2))
    new_points = np.zeros((4, 1, 2), np.int32)
    add = points.sum(1)  # sum x,y to each other for each points
    new_points[0] = points[np.argmin(add)]  # [0, 0]
    new_points[3] = points[np.argmax(add)]  # [w, h]
    diff = np.diff(points, axis=1)
    new_points[1] = points[np.argmin(diff)]  # [w, 0]
    new_points[2] = points[np.argmax(diff)]  # [0, h]
    return new_points


def dropImgPoints(img, points):
    height = img.shape[0]
    width = img.shape[1]
    pt1 = np.float32(points)
    pt2 = np.float32(
        [
            [0, 0],
            [width, 0],
            [0, height],
            [width, height]
        ]
    )
    matrix = cv2.getPerspectiveTransform(pt1, pt2)
    img_wraped = cv2.warpPerspective(img, matrix, (width, height))
    return img_wraped


def imgSplit(img):
    wrappers = []
    cols = np.hsplit(img,6)
    cols.reverse()
    for col in cols:
        col = np.vstack( [ col, np.zeros((20,150))] ) # 6 = 6 *150 = 900 pix
        # cv2.imshow('asdasd',col)
        # cv2.waitKey(0)
        # exit()
        rows = np.vsplit(col,23)
        for row in rows:
            # cv2.imshow('asdasd',row)
            # cv2.waitKey(0)
            wrappers.append(row)

    # find selected
    boxes = []
    for wrapper in wrappers:
        cols = np.hsplit(wrapper[:,:108],4)
        cols.reverse()
        checks = []
        for i,col in enumerate(cols):
            # if i ==0:
            #     continue
            # cv2.imshow(f'asdasd {i}',col)
            # col = col[9:81, 9:81]
            # cv2.imshow('asdasd',col)
            # cv2.waitKey(0)
            checks.append(col)
        # exit()
        boxes.append(checks)
    return boxes


def user_answers(boxes:list):
    choices = []
    for i,box in enumerate(boxes):
            _ = []
            for col in box:
                _.append(cv2.countNonZero(col))
            checked_value = max(_)
            checked_index = _.index(checked_value)
            if checked_value > 20:
                choices.append(checked_index)
            else:
                choices.append(-1)
    return choices


def choice_point(answer_width,answer_height,question,choice_index):
    cw = answer_width // 5
    cols = [
        [*range(0,23)],
        [*range(23,46)],
        [*range(46,69)],
        [*range(69,92)],
        [*range(92,115)],
        [*range(115,138)],
    ]
    cols.reverse()
    for i,col in enumerate(cols):
        if question in col:
            start = col[0]
            end = col[-1]
            # x = abs((answer_width *i) + (cw*choice_index+1 + 12))
            # print(question,i)
            x = (answer_width * (i+1 if i != 0 else 1) ) - (cw*(choice_index+1) + 12)
            y = (answer_height*col.index(question)) + 23
            
            if start+0<=question<=start+8 and choice_index == 0:
                x = x-8
                y = y+6
            elif start+8<question<=start+15 and choice_index == 0:
                x = x-8
                y = y-2
            elif start+15<question<=end and choice_index == 0:
                x = x-8
                y = y-5
            if start+0<=question<=start+9 and choice_index == 1:
                x = x-2
                y = y+6
            elif start+9<question<=end and choice_index == 1:
                x = x-4
                y = y-2
                if start+18<=question<=end:
                    y = y-4 
            elif start+0<=question<=start+9 and choice_index == 2:
                y = y+4
            elif start+16<=question<=end and choice_index == 2:
                y = y-6
            elif start+0<=question<=start+8 and choice_index == 3:
                x = x+6
                y = y+6
            elif start+8<question<=start+14 and choice_index == 3:
                x = x+6
                y = y+1
            elif start+15<=question<=end and choice_index == 3:
                x = x+6
                y = y-4
    return x,y


def show_answers(img,user_choices, questions):
    secWidth = img.shape[0] // 6
    secHeight = img.shape[1] // 23
    
    for i,q in enumerate(questions):
        
        # if user_choices[i] == -1 :
        #     continue
        
        if user_choices[i] == questions[i]:
            # print(i,user_choices[i], questions[i])
            x,y = choice_point(secWidth,secHeight,i,questions[i])
            cv2.circle(img,(x,y),5,(0,255,0),cv2.FILLED)
        else:
            x,y = choice_point(secWidth,secHeight,i,questions[i])
            cv2.circle(img,(x,y),5,(0,0,255),cv2.FILLED)
        # x,y = choice_point(secWidth,secHeight,i,0)
        # cv2.circle(img,(x,y),5,(0,0,255),cv2.FILLED)  
        # x,y = choice_point(secWidth,secHeight,i,1)
        # cv2.circle(img,(x,y),5,(0,0,255),cv2.FILLED)  
        # x,y = choice_point(secWidth,secHeight,i,2)
        # cv2.circle(img,(x,y),5,(0,0,255),cv2.FILLED)  
        # x,y = choice_point(secWidth,secHeight,i,3)
        # cv2.circle(img,(x,y),5,(0,0,255),cv2.FILLED)   
    return img


