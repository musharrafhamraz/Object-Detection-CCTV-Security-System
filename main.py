import cv2
import numpy as np
import firebase_admin
from firebase_admin import credentials, storage

# Initialize Firebase
cred = credentials.Certificate("cctv-security-system-firebase-adminsdk-h91tv-8bdd8dece7.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'gs://cctv-security-system.appspot.com'})

image = cv2.imread('pic.jpg')
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
