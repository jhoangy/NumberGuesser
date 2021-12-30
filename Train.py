import cv2
import tensorflow as tf
import numpy as np

CATEGORIES = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


def prepare(filepath):
    IMG_SIZE = 28  # 50 in txt-based
    img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)


model = tf.keras.models.load_model("64x3-CNN.model")
x = [prepare('test.jpg')]
prediction = model.predict(x)
print(prediction)  # will be a list in a list.
print(np.argmax(prediction[0]))
