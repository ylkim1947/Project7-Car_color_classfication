## 한글 경로 이미지 읽기 쓰기, 이미지 crop (margin주기 가능) 등의 함수 제공 

import os
import numpy as np
import cv2



def resize(image, w, h):
    resized_image = cv2.resize(image, dsize=(w, h), interpolation=cv2.INTER_AREA)
    return resized_image


# box 정보에 대해 margin 값만큼 확장함
def expand_box(box, margin, img_width = None, img_height = None):
    x = box["x"]
    y = box["y"]
    w = box["w"]
    h = box["h"]

    x = x - margin
    x = max(x, 0)
    y = y - margin
    y = max(y, 0)

    w = w + 2*margin
    if img_width and x + w > img_width:
        w = img_width - x
    
    h = h + 2*margin
    if img_height and y + h > img_height:
        h = img_height - y

    new_box = {
        "x": x, 
        "y": y,
        "w": w,
        "h": h
    }

    return new_box


# 이미지 crop
def crop_image(image_np, box, margin = 0):
    if margin > 0:
        box = expand_box(box, margin, image_np.shape[1], image_np.shape[0])
       
    x1 = box["x"]
    y1 = box["y"]
    x2 = box["x"] + box["w"]
    y2 = box["y"] + box["h"]
    return image_np[y1:y2, x1:x2]


# 한글 경로 지원
def imwrite(file_path, img, params=None):
    try: 
        ext = os.path.splitext(file_path)[1]
        result, n = cv2.imencode(ext, img, params)
        if result: 
            with open(file_path, mode='w+b') as f:
                n.tofile(f)
                return True
        else: 
            return False 
    except Exception as e: 
        print(e)
        return False


# 한글 경로 지원
def imread( file_path ) :
    stream = open( file_path.encode("utf-8") , "rb")
    bytes = bytearray(stream.read())
    np_array = np.asarray(bytes, dtype=np.uint8)
    return cv2.imdecode(np_array , cv2.IMREAD_UNCHANGED)


