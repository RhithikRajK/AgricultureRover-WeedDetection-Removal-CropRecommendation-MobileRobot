import cv2
import io
from ultralytics import YOLO
import torch
import pandas
import matplotlib.pyplot as plt
import numpy as np
from firebase import firebase
import streamlit as st
from PIL import Image
import serial
import json

st.title('Weed Detection')
ESP32_CAMERA_STREAM_URL = 'http://192.168.22.107:81/stream'
st.title("ESP32 Camera Stream and Capture")

def postprocess_yolo(image, yolo_output):
    confidence_threshold = 0.2
    height, width, _ = image.shape
    class_ids = []
    confidences = []
    boxes = []
    class_id = yolo_output.cls[0]
    confidence = float(yolo_output.conf[0])
    print(confidence)
    if confidence > confidence_threshold:
      x_min, y_min, x_max, y_max = map(int, yolo_output.xyxy[0][0:4])
      print(x_min)
      x, y = int((x_min + x_max) / 2), int((y_min + y_max) / 2)
      class_ids.append(class_id)
      confidences.append(float(confidence))
      boxes.append(x_min)
      boxes.append(y_min)
      boxes.append(x_max)
      boxes.append(y_max)
      final_coordinates = [x,y]
    st.write("Detected Coordinates!!")
    return final_coordinates

def show():
    live_video = st.empty()
    capture_button = st.button("Capture")
    cap = cv2.VideoCapture(ESP32_CAMERA_STREAM_URL)
    while(True):
        ret, frame = cap.read()
        live_video.image(frame, channels="BGR", use_column_width=False)
        if capture_button:
            cap.release()
            return frame
    
model = YOLO("D:/capstone1/bestweed.pt")
image = show()
st.image(image,channels="BGR")
results = model.predict(source=image)

for r in results:
    im_array = r.plot()
    im = Image.fromarray(im_array[..., ::-1])
    im.show()
    st.image(im,channels="BGR")
    im.save('D:/capstone/results.jpg')

c=0
for i in range(1):
    yolo_output = results[0].boxes[i]
    print(yolo_output.xyxy[0][0])
    # Post-process to get final coordinates
    coordinates = postprocess_yolo(image, yolo_output)

    if coordinates:
        # Assuming coordinates is a tuple (x, y) of the detected object
        x, y = coordinates[0], coordinates[1]

        data = {"x":x,
                "y":y}

        print("Detected Coordinates:", str(data))
        st.write(str(data))
        break
    else:
        st.write("No coordinates")
        break