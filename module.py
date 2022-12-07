import numpy as np
import pandas as pd
import tensorflow as tf
from keras.models import load_model
from PIL import Image


model = load_model('model/model.h5')
labels = pd.read_csv("label/labels.csv")
class_names = []
for i in labels['Nama']:
    class_names.append(i)


def predict_image(image):
    image = tf.keras.utils.load_img(image, target_size=(32, 32))
    image = tf.image.rgb_to_grayscale(image)
    image = tf.keras.utils.img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = np.vstack([image])
    prediction = model.predict(image, batch_size=32)
    print(prediction)
    predicted_class = class_names[np.argmax(prediction[0])]
    confidence = round(100 * (np.max(prediction[0])), 2)
    return predicted_class, confidence
