import cv2
import numpy as np
from PIL import Image


def has_face(photo_file):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Конвертируем BytesIO в массив numpy
    image = Image.open(photo_file)
    image_np = np.array(image)
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    return len(faces) > 0

