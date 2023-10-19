from ultralytics import YOLO
import cv2
import numpy as np
import os
import helper
from cvzone import stackImages
from random import randint
import pytesseract
from PIL import Image



class McqReader:

    CURRENT_DIR_PATH = os.path.dirname(__file__)

    def start(self):
        img = helper.imread(
            f'{self.CURRENT_DIR_PATH}/assets/1.jpg',
            (900,900)
        )
        result = self.calculate(img)
        # multi page support
        # create pdf,exel for each user with results image and final score
        # test camera
        # web panle with streamlit
        
    def preprocessing_img(self, img):
        img_gray = helper.imgray(img)
        img_blur = helper.imgblur(img_gray)
        # img_canny = imgcanny(img_blur)
        img_canny = 255 - img_blur
        preprocessed_img = img_canny

        return preprocessed_img, [img_gray, img_blur, img_canny]

    def calculate(self, img):
        
       

        # preprocessing mcq paper
        preprocessed_img, img_layers = self.preprocessing_img(img)
        # find userid, answers, pagenumber contour
        # contours, hierarchy = cv2.findContours(preprocessed_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # answer_contours = helper.rectWithMinArea(contours,min_area=4000)[0]
        # answer_points = helper.reorderPoints(helper.getCornerPoint(answer_contours))
        
        # preprocessed_img = cv2.threshold(preprocessed_img,70,255,cv2.THRESH_BINARY)[1]
        # cv2.imshow('asd',preprocessed_img)
        # cv2.waitKey(0)
        # exit()
        
        
        # answers img
        # answers_img = helper.dropImgPoints(img, answer_points)
        answers_img = preprocessed_img
        answers_img_preprocessed , _ = self.preprocessing_img(answers_img)
        answers_img_preprocessed = cv2.threshold(answers_img_preprocessed,150,255,cv2.THRESH_BINARY)[1]
        boxes = helper.imgSplit(answers_img_preprocessed)
        user_choices = helper.user_answers(boxes)
        
        imgggg = helper.show_answers(answers_img,user_choices,[randint(0,3) for i in range(len(user_choices))])
                
                
        
        # *************************************
        # return user score and true or false for each question
        # ************************************* 
 
        # draw user_id wrapper, answers wrapper corner points
        points_img = helper.drawContours(
            img=img,
            contours=[
                answer_points,
                      ],
            colors=[(255, 255, 0), (0, 255, 0)],
            thickness=15
        )

        # show stacked images
        helper.imshow(
            stackImages(
                [
                    *img_layers,
                    points_img,
                    imgggg,
                ],
                cols=4,
                scale=.5
            )
        )


if __name__ == '__main__':
    mcq_reader = McqReader()
    mcq_reader.start()

# 01:24:30
