import streamlit as st
import cv2
from PIL import Image
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.auth.exceptions import RefreshError
import io
from ultralytics import YOLO
import torch
import pandas
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from collections import Counter
from google.auth.transport.requests import Request


st.title('Crop Recommendation System')


ESP32_CAMERA_STREAM_URL = 'http://192.168.22.107:81/stream'


st.title("ESP32 Camera Stream and Capture")


def capture_and_save():
    cap = cv2.VideoCapture(ESP32_CAMERA_STREAM_URL)
    live_video = st.empty()
    detect = st.button("detect")
    while(True):
        ret, frame = cap.read()
        if frame is None:
            st.warning("Received a None frame. Skipping this iteration.")
            break
        live_video.image(frame, channels="BGR", use_column_width=False)
        if detect:
            cap.release()
            model = YOLO("D:/capstone/best.pt")
            results = model.predict(source=frame)
            for r in results:
                im_array = r.plot()
                im = Image.fromarray(im_array[..., ::-1])
                st.image(im, channels="BGR", use_column_width=False)
                im.save('D:/capstone/results.jpg')
            l=set()
            for item in results:
                for box in item.boxes:
                    class_id = int(box.data[0][-1])
                    l.add(model.names[class_id])
            k=list(l)
            print(k)

            data = pd.read_csv("D:/capstone/Crop.csv")
            features = data[["N","P","K","temperature","humidity","rainfall","ph"]]
            features = features.fillna(features.mean())
            scaler = StandardScaler()
            scaler_features = scaler.fit_transform(features)
            kmeans= KMeans(n_clusters=3)
            kmeans.fit(scaler_features)
            cluster_labels = kmeans.labels_
            print(kmeans.cluster_centers_)
            print(kmeans.inertia_)

            crops_per_cluster = {}
            for i in range(kmeans.n_clusters):
                cluster_data = data[cluster_labels == i]
                crops_in_cluster = list(cluster_data["label"])

                
                crop_counts = Counter(crops_in_cluster)
                crops_with_counts = [(crop, count) for crop, count in crop_counts.items()]

                crops_per_cluster[i] = crops_with_counts

        
            print("Crops in each cluster:")
            for cluster_id, crops in crops_per_cluster.items():
                print(f"Cluster {cluster_id + 1}:")
                if isinstance(crops[0], tuple): 
                    for crop, count in crops:
                        print(f"- {crop} ({count} times)")
                else:
                    print("- " + ", ".join(crops))
            other_crops_with_higher_frequency = []
            total = []
            for user_crop in k:
                max_count = 0
                max_cluster_id = None
                for cluster_id, crops in crops_per_cluster.items():
                    for crop, count in crops:
                        if crop == user_crop and count>max_count:
                            max_count = count
                            max_cluster_id = cluster_id

                if max_cluster_id is not None:
                    print(f"For crop '{user_crop}':")
                    print(f"The cluster with the highest frequency is Cluster {max_cluster_id + 1}.")

                    other_crops_with_higher_frequency = [
                        crop for crop, count in crops_per_cluster[max_cluster_id] if count > 80
                    ]

                    if user_crop in other_crops_with_higher_frequency:
                        other_crops_with_higher_frequency.remove(user_crop)

                    if other_crops_with_higher_frequency:
                        print("Other crops in the same cluster with higher frequency:")
                        for crop in other_crops_with_higher_frequency:
                            print(f"- {crop}")
                    else:
                        print("No other crops in the same cluster have a higher frequency.")
                else:
                    print(f"The crop '{user_crop}' was not found in any cluster.")
                total+=other_crops_with_higher_frequency
            if total:
                st.write("The crops recommended are:")
                for i in total:
                    st.write(i)
            else:
                st.write("Crops are not recommended")
            

capture_and_save()

