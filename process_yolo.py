import os
from pprint import pprint

def process_yolo(id, yolo_data):
    txtFilename= yolo_data.get('image').replace(yolo_data.get('image').split(id)[1].split('.')[1], "txt").split(id)[1]
    with open(f'./static/{id}/labels/{txtFilename}', 'a') as file:
        pprint(yolo_data, indent= 3)
        file.write(f"{yolo_data['label_index']} {yolo_data['middle_x']} {yolo_data['middle_y']} {yolo_data['width']} {yolo_data['height']}\n")
