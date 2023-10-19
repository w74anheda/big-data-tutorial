import math
import cv2
from ultralytics import YOLO
import numpy as np


def videoCapture(src):
    capture = cv2.VideoCapture(src)
    if not capture.isOpened():
        raise ValueError(f'{src} not found!')
    return capture


def box_class_name(model, box):
    return model.names[int(box.cls[0])]


def box_confidence(box):
    return math.ceil(box.conf[0] * 100) / 100


def cmv_video_handler(source, ymodel_path: str, handler, wait_key=1):
    capture = source
    ymodel = YOLO(ymodel_path)
    count = 0

    while capture.isOpened():
        # read frame of video
        success, frame = capture.read()
        
        if not success or cv2.waitKey(wait_key) & 0xFF == ord('q'):
            break
        
        count+=1
        if count % 3 != 0:
            continue
        
        frame_ = handler(ymodel, frame, success)
        cv2.imshow('main', frame_)

    capture.release()
    cv2.destroyAllWindows()


def box_info(box):
    x1, y1, x2, y2 = [int(_) for _ in box.xyxy[0]]
    _, _, w, h = [int(_) for _ in box.xywh[0]]
    id = int(box.id)
    return id, [w, h], [x1, y1, x2, y2]


def confidence_color(confidence: float):
    if confidence >= .8:
        color = (11, 234, 93)
    elif confidence >= .5:
        color = (11, 134, 234)
    else:
        color = (56, 11, 234)
    return color


def video_shape(cap):
    return (
        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    )


def rectangle_center_point(p1: tuple, p2: tuple):
    width, height = p2[0]-p1[0], p2[1]-p1[1]
    xc = p1[0] + (width // 2)
    yc = p1[1] + (height // 2)
    return xc, yc


def is_toched_line(p1: tuple, p2: tuple, target_point: tuple, thickness: int = 20):
    return (
        (p1[0] < target_point[0] < p2[0]) and
        (p1[1]-thickness < target_point[1] < p2[1]+thickness)
    )


def is_toched_line_hdown(p1: tuple, p2: tuple, target_point: tuple, threshold: float = .5, thickness: int = 15):

    yc = (p1[1]+p2[1]) // 2
    xp1 = (p1[0] - int(p1[0]*threshold), yc-thickness)
    xp2 = (p2[0] + int(p2[0]*threshold), yc+thickness)
    return (
        (xp1[0] <= target_point[0] and target_point[1] >= xp1[1]) and
        (xp2[0] >= target_point[0] and target_point[1] <= xp2[1])
    ), [xp1, xp2]


def is_toched_line_hup(p1: tuple, p2: tuple, target_point: tuple, threshold: float = .5, thickness: int = 15):

    yc = (p1[1]+p2[1]) // 2
    xp1 = (p1[0] - int(p1[0]*threshold), yc-thickness)
    xp2 = (p2[0] + int(p2[0]*threshold), yc+thickness)
    return (
        (xp1[0] <= target_point[0] and target_point[1] <= xp1[1]) and
        (xp2[0] <= target_point[0] and target_point[1] >= xp2[1])
    ), [xp1, xp2]
