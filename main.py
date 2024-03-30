import cv2
import numpy as np
import firebase_admin
from firebase_admin import credentials, storage

# Initialize Firebase
cred = credentials.Certificate("cctv-security-system-firebase-adminsdk-h91tv-8bdd8dece7.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'gs://cctv-security-system.appspot.com'})

# cctv-security-system-firebase-adminsdk-h91tv-8bdd8dece7.json
# gs://cctv-security-system.appspot.com

config ={ 
    "apiKey": "AIzaSyAKxtVvABDyKusllWFQIQqRbKqkvkp063s",
    "authDomain": "cctv-security-system.firebaseapp.com",
    "projectId": "cctv-security-system",
    "storageBucket": "cctv-security-system.appspot.com",
    "messagingSenderId": "606255301184",
    "appId": "1:606255301184:web:118b926d197b58feea95a5",
    "measurementId": "G-9HH0NJY7N0",
    "serviceAccount": "cctv-security-system-firebase-adminsdk-h91tv-8bdd8dece7.json"
}
image = cv2.imread('images\pic.jpg')
# Function to upload image to Firebase storage
def upload_to_firebase(image):
    if isinstance(image, np.ndarray):
        bucket = storage.bucket()
        _, encoded_image = cv2.imencode('.jpg', image)
        encoded_image_bytes = encoded_image.tobytes()
        blob = bucket.blob("images/screenshot.jpg")
        blob.upload_from_string(encoded_image_bytes, content_type='image/jpeg')
        print("Screenshot uploaded to Firebase")
    else:
        print("Error: Invalid image format")



if __name__ == "__main__":
    upload_to_firebase(image)
