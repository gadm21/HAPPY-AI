from yu4u.wide_resnet import WideResNet
import cv2
import numpy as np
import tensorflow as tf
global graph
from pathlib import Path
from keras.utils.data_utils import get_file

pretrained_model = "https://github.com/yu4u/age-gender-estimation/releases/download/v0.5/weights.28-3.73.hdf5"
modhash = 'fbe63257a054c1c5466cfd7bf14646d6'
weight_file = get_file("weights.28-3.73.hdf5", pretrained_model, cache_subdir="pretrained_models",
                               file_hash=modhash, cache_dir=str(Path(__file__).resolve().parent))
img_size = 64
model = WideResNet(img_size, depth=16, k=8)()
model.load_weights("yu4u/pretrained_models/weights.28-3.73.hdf5")
graph = tf.get_default_graph()

def predict_age_gender(cropface):
    predicted_gender = None
    predicted_age = 0

    img = cv2.resize(cropface, (img_size, img_size))
    img = np.array(img, dtype=np.float32)
    img = np.reshape(img, (-1, img_size, img_size, 3))

    # predict ages and genders of the detected faces
    with graph.as_default():
        results = model.predict(img)
    predicted_gender = results[0]
    ages = np.arange(0, 101).reshape(101, 1)
    predicted_age = results[1].dot(ages).flatten()
    predicted_gender = 'M' if predicted_gender[0][0] < 0.5 else 'F'

    return predicted_age, predicted_gender
