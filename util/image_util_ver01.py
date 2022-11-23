## 한글 경로 이미지 읽기 쓰기, 이미지 crop (margin주기 가능) 등의 함수 제공 

import os
import numpy as np
import cv2
import common_util


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

# Adding by Younglae (AI_14)
def listdirs(rootdir,path_list=[]):
    
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            #print(d)
            if d.count('\\') ==10:
                path_list.append(d)
            listdirs(d,path_list)
    return path_list


if __name__ == "__main__":
    
    #base_folders = r"D:\codestates\Section6\cp2\091\01.데이터\1.Training\라벨링데이터"
    #base_folders = r"D:\codestates\Section6\cp2\091\01.데이터\2.Validation\라벨링데이터"
    
    #base_folders_list = common_util.listdirs(base_folders,path_list=[])
    # ##01. Crop된 파일 옮길 폴더 만들기 (if true)
    # source_path = r"D:\codestates\Section6\cp2\091"
    # target_path = r"D:\codestates\Section6\cp2\092"
    # # for file in os.listdir(target_path):
    #     # d = os.path.join(target_path, file)
    #     # if os.path.isdir(d) is not:
    # if os.listdir(target_path) ==[]:
    #     common_util.create_folders(source_path,target_path)

    ##02. Crop 될 파일 폴더 
    base_output_folders = r"D:\codestates\Section6\cp2\091\01.데이터\1.Training\원천데이터"
    #base_output_folders = r"D:\codestates\Section6\cp2\091\01.데이터\2.Validation\원천데이터"
    base_output_folders_list = listdirs(base_output_folders,path_list=[])
    image_sz = 224
    margin =20
    for i in range(len(base_output_folders_list)):
        print(i)
        BASE_FOLDER=base_output_folders_list[i]
        target_path = BASE_FOLDER.replace('\\091\\','\\092\\') # target path 만들기 
        if os.listdir(target_path) ==False:
            common_util.create_folders(BASE_FOLDER,target_path)       
        #BASE_OUTPUT_FOLDER=base_output_folders_list[i]


        for folder in os.listdir(BASE_FOLDER):
            last_path = os.path.join(BASE_FOLDER, folder)
            output_folder = os.path.join(target_path, folder)
            common_util.check_folder(BASE_FOLDER)

            JPG_ex = r'.jpg'
            jpg_list = [file for file in os.listdir(last_path) if file.endswith(JPG_ex)]
            JSON_ex = r'.json'
            json_list = [file for file in os.listdir(last_path) if file.endswith(JSON_ex)]
             
            for N_file in range(len(jpg_list)):
                jpg_file= os.path.join(last_path,jpg_list[N_file])
                json_file= os.path.join(last_path,json_list[N_file])
                print(jpg_file)

                #jpg_file = os.path.join(last_path, file)
                #json_file = os.path.splitext(file)[0] + ".json"

                label_dict = common_util.load_json(json_file)
                ## 차량 전체 이미지 찾기 
                Whole_car = 0 
                for ii in range(len(label_dict["shapes"])):
                    if label_dict["shapes"][ii]['label'] =='P00.차량전체':
                        Whole_car = 1 
                        x,y =  label_dict["shapes"][ii]['points'][0]
                        x2,y2  = label_dict["shapes"][ii]['points'][1]
                        box={"x" : x ,"y" : y ,"w" : x2-x , "h": y2-y}
                ## 이미지 resize  
                img_file = imread( jpg_file )
                if Whole_car == 0: 
                    jpg_resized = resize(img_file, image_sz, image_sz)
                else: 
                    ##차량 전체 이미지 크롭 (1. margin box 2. )
                    #new_box = expand_box(box, margin, img_width = None, img_height = None)
                    img_file_croped = crop_image(img_file, box, margin)
                    jpg_resized = resize(img_file_croped, image_sz, image_sz)
                jpg_save = jpg_file.replace('\\091','\\092')
                imwrite(jpg_save, jpg_resized, params=None)
            

                # object_list = label_dict["learningDataInfo"]["objects"]
                # print(len(object_list))
