import cv2
import numpy as np
import firebase_admin
from firebase_admin import credentials, storage

# Initialize Firebase
cred = credentials.Certificate("....path/to/your/jsonfile")
firebase_admin.initialize_app(cred, {'storageBucket': 'your-bucket-id'})

# Load pre-trained object detection model
net = cv2.dnn.readNetFromTensorflow('frozen_inference_graph.pb', 'ssd_mobilenet_v2_coco.pbtxt')

# Function to detect pedestrians and vehicles
def detect_objects(frame):
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()
    return detections

# Function to upload image to Firebase storage
def upload_to_firebase(image):
    bucket = storage.bucket()
    blob = bucket.blob("images/screenshot.jpg")
    blob.upload_from_string(cv2.imencode('.jpg', image)[1].tostring(), content_type='image/jpeg')

# Main function
def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect objects in the frame
        detections = detect_objects(frame)

        # Process detections
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:  # Adjust confidence threshold as needed
                class_id = int(detections[0, 0, i, 1])
                if class_id in [1, 2]:  # Pedestrian or Vehicle class IDs
                    # Capture screenshot
                    screenshot = frame.copy()

                    # Upload screenshot to Firebase
                    upload_to_firebase(screenshot)
                    print("Screenshot uploaded to Firebase")

                    # You may want to add additional logic here, such as saving the image locally

                    break  # Break loop after first detection to avoid uploading multiple screenshots

        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
