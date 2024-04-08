from ultralytics import YOLO
import pyrebase
import cv2
import numpy as np
import math


config ={ 
    "apiKey": "AIzaSyAKxtVvABDyKusllWFQIQqRbKqkvkp063s",
    "authDomain": "cctv-security-system.firebaseapp.com",
    "projectId": "cctv-security-system",
    "storageBucket": "cctv-security-system.appspot.com",
    "messagingSenderId": "606255301184",
    "appId": "1:606255301184:web:118b926d197b58feea95a5",
    "measurementId": "G-9HH0NJY7N0",
    "serviceAccount": "cctv-security-system-firebase-adminsdk-h91tv-8bdd8dece7.json",
    "databaseURL": "https://cctv-security-system-default-rtdb.asia-southeast1.firebasedatabase.app/"
}

results = ["person", "bicyle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "girrafe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee","skis", "snowboard","sports ball", "kite", "baseball bat", "baseball gloves", "stakeboard", "surfboard", "tennis rackets", "bottles", "wine glass", "cup", "fork ", "knife", "spoon", "bowl", "banana", "apple","sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa","pottedplant", "bed","dining table", "toilet", "tv remote", "laptop", "mouse", "remote", "keyboard", "cell phone", "micro wave", "oven", "toaster", "sink", "refrigirator", "book", "clock", "vase", "scissor", "teddy bear", "hair drier", "tooth brush"]

model = YOLO('yolov8n.pt')

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

# storage.child("images/pic.jpg").put("images/pic.jpg")
def filter_detections(results, labels_to_detect):
    filtered_detections = np.empty((0, 5))

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])

            currentClass = labels_to_detect[cls]

            # Check if the current class is a car, truck, bus, or motorbike with confidence > 0.3
            if currentClass in ["car", "truck", "bus", "motorbike"] and conf > 0.3:
                currentArray = np.array([x1, y1, x2, y2, conf])
                filtered_detections = np.vstack((filtered_detections, currentArray))

    return filtered_detections



def upload_frame(frame):
    labels_to_detect = ["person", "car", "truck"]  # Adjust this list as needed
    results = model(frame)
    detected_objects = filter_detections(results, labels_to_detect)  # Pass labels_to_detect argument
    if detected_objects:
        _, img_encoded = cv2.imencode('.jpg', frame)
        storage.child("images/frame.jpg").put(img_encoded.tobytes())
        print("Frame uploaded successfully.")
    else:
        print("No people or vehicles detected.")


# Capture video from camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Resize frame to fit YOLOv5 input size
    resized_frame = cv2.resize(frame, (640, 480))

    # Convert frame from BGR to RGB
    rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

    upload_frame(rgb_frame)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()