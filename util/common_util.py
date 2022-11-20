import os
import json
from datetime import datetime
import logging

def get_timestamp():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return timestamp

def get_now_timestring():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return timestamp

# 텍스트 읽기
def read_text(file_path, encoding="utf-8"):
    text = None
    with open(file_path, 'r', encoding=encoding) as f:
        text = f.read()

    return text

# 텍스트를 읽어서 list 리턴
def read_lines(file_path, encoding="utf-8"):
    return read_text(file_path, encoding).split("\n")

# 텍스트 쓰기
def save_text(file_path, text, encoding="utf-8"):
    with open(file_path, 'w', encoding=encoding) as f:
        f.write(text)

def save_lines(file_path, lines, encoding="utf-8"):
    text = "\n".join(lines)
    save_text(file_path, text, encoding)

def save_json(json_path, data, encoding="utf-8"):
    save_text(json_path, json.dumps(data, ensure_ascii=False, indent=4), encoding)

def load_json(json_path, encoding="utf-8"):
    return json.loads(read_text(json_path, encoding))

def check_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# source 폴더 아래의 폴더들을 target 폴더에 빈폴더로 생성함
def create_folders(source_folder, target_folder):
    folders = os.listdir(source_folder)
    for folder in folders:
        folder_path = os.path.join(source_folder, folder)
        if os.path.isdir(folder_path):
            target_path = os.path.join(target_folder, folder)
            if not os.path.exists(target_path):
                os.makedirs(target_path)



def get_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)s) %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger

if __name__ == "__main__":
    pass
