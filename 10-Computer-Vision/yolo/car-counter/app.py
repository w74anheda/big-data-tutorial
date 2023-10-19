# import requirements
import sys

import numpy as np
sys.path.insert(0, '..')
import hyperloglog as hll
import cv2
import helper
import cvzone



# initialize ...
valid_classess = ['car', 'truck', 'bus', 'motorbike', 'bicycle', 'motorcycle']
area_1_counter = hll.HyperLogLog(0.01)
area_2_counter = hll.HyperLogLog(0.01)
capture = helper.videoCapture('../../datasets/videos/car01.mp4')
mask = cv2.imread('mask.jpg')
img_count_label = cv2.imread('graphics.png', cv2.IMREAD_UNCHANGED)

def handler(ymodel, frame, success):
    global mask,img_count_label 
    
    
    
    
    frame_shape = (1280, 720)
    frame = cv2.resize(frame, frame_shape)
    mask = cv2.resize(mask, frame_shape)
    masked_frame = cv2.bitwise_and(frame, mask)
    frame = masked_frame
    frame = cvzone.overlayPNG(frame, img_count_label, (0, 0))
    result = ymodel.track(source=frame, persist=True, verbose=False)[0]
    
    
    for box in result.boxes:
        class_name = helper.box_class_name(ymodel, box)
        confidence = helper.box_confidence(box)

        if not box.is_track or confidence < 0 or class_name not in valid_classess:
            continue

        id, [w, h], [x1, y1, x2, y2] = helper.box_info(box)

        xc, yc = helper.rectangle_center_point(p1=(x1, y1), p2=(x2, y2))

        # draw object shape
        color = helper.confidence_color(confidence)
        cvzone.cornerRect(frame, (x1, y1, w, h), l=10,t=2, colorR=color, colorC=color)
        cv2.circle(
            frame, (xc, yc), radius=5,
            color=(100, 100, 255), thickness=cv2.FILLED
        )



        # draw areas
        area_1 = [(305, 504),(405, 404) , (1016, 421),  (1086, 521)]
        cv2.polylines(frame,[np.array(area_1)],True,(100,200,20),5)
       
       
        print(cv2.norm((305, 504), (405, 404))*0.05)
       
       
       
        # test point in areas
        is_touched_area = cv2.pointPolygonTest(
            np.array(area_1),
            (xc,yc),
            False
        )
        cvzone.putTextRect(
            frame,
            f'id: {id} - {"in area" if is_touched_area>=0 else "out area"}',
            pos=(max(0, x1), max(35, (y1-5))),
            scale=1.5, thickness=2, offset=3)
        
        
        if is_touched_area >=0:
            area_1_counter.add(id)
       
       
       
       
       
       
       
       
       
      

        # show object count
        cv2.putText(
            frame,
            f'{len(area_1_counter)}',
            (217, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (50, 200, 0),
            3,
        )
        cv2.putText(
            frame,
            f'{len(area_2_counter)}',
            (463, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 50, 190),
            3,
        )

    frame_ = frame
    # frame_ = result.plot()

    return frame_


helper.cmv_video_handler(
    source=capture,
    ymodel_path='../weights/yolov8l.pt',
    wait_key=1,
    handler=handler
)
