## AIHUB 데이터를 labelme json으로 변경 
# 차량 외관 데이터 


import os
import json
import shutil

import cv2
import numpy as np

import common_util



def create_labelme_file(labelme_path, object_list):

    # 이미지 크기는 1920x1080이라고 간주 (AIHUB 데이터 확인)
    width = 1920
    height = 1080

    labelme_dict = common_util.load_json("labelme_template.json")    

    shape_list = []
    for item in object_list:

        class_name = item["classId"]
        # coords = item["coords"]
        x1 = int(item["left"])
        y1 = int(item["top"])
        w = int(item["width"])
        h = int(item["height"])
        x2 = x1 + w
        y2 = y1 + h
    
        shape_dict = {
            "label": class_name,
            "points": [[x1, y1], [x2, y2]],
            "group_id": None,
            "shape_type": "rectangle",
            "flags": {}
        }
        shape_list.append(shape_dict)

    if len(shape_list) == 0:
        # 유효한 객체가 없으면 처리 중단

        return

    labelme_dict["shapes"] = shape_list
    labelme_dict["imagePath"] = os.path.splitext(os.path.basename(labelme_path))[0] + ".jpg"
    labelme_dict["imageWidth"] = width
    labelme_dict["imageHeight"] = height

    common_util.save_json(labelme_path, labelme_dict)
    print("save labelme:", labelme_path)




if __name__ == "__main__":
    
    # BASE_FOLDER = r"I:\DATA\AIHUB_차량외관\091.차량 외관 영상 데이터\01.데이터\1.Training\라벨링데이터\TL2\HY_현대\041_그랜저"
    # BASE_FOLDER = r"I:\DATA\AIHUB_차량외관\091.차량 외관 영상 데이터\01.데이터\1.Training\라벨링데이터\TL2\HY_현대\063_싼타페"
    BASE_FOLDER = r"I:\DATA\AIHUB_차량외관\091.차량 외관 영상 데이터\01.데이터\1.Training\라벨링데이터\TL2\HY_현대\098_팰리세이드"
    
    # BASE_OUTPUT_FOLDER = r"I:\DATA\AIHUB_차량외관\091.차량 외관 영상 데이터\01.데이터\1.Training\원천데이터\TS2\HY_현대\041_그랜저"
    # BASE_OUTPUT_FOLDER = r"I:\DATA\AIHUB_차량외관\091.차량 외관 영상 데이터\01.데이터\1.Training\원천데이터\TS2\HY_현대\063_싼타페"
    BASE_OUTPUT_FOLDER = r"I:\DATA\AIHUB_차량외관\091.차량 외관 영상 데이터\01.데이터\1.Training\원천데이터\TS2\HY_현대\098_팰리세이드"

    for folder in os.listdir(BASE_FOLDER):
        folder_path = os.path.join(BASE_FOLDER, folder)
        output_folder = os.path.join(BASE_OUTPUT_FOLDER, folder)
        common_util.check_folder(output_folder)
        for file in os.listdir(folder_path):
            print(file)
            json_path = os.path.join(folder_path, file)
            
            labelme_file = os.path.splitext(file)[0] + ".json"
            
            labelme_path = os.path.join(output_folder, labelme_file)
            
            label_dict = common_util.load_json(json_path)
            object_list = label_dict["learningDataInfo"]["objects"]
            print(len(object_list))
            create_labelme_file(labelme_path, object_list)
