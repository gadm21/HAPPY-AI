import cv2
import numpy as np
from yu4u.model import get_model
import tensorflow as tf
from yu4u.model import get_model
global graph
from pathlib import Path
from keras.utils.data_utils import get_file

pretrained_model = "https://github.com/yu4u/age-gender-estimation/releases/download/v0.5/age_only_resnet50_weights.061-3.300-4.410.hdf5"
modhash = "306e44200d3f632a5dccac153c2966f2"
weight_file = get_file("age_only_resnet50_weights.061-3.300-4.410.hdf5", pretrained_model,
                               cache_subdir="pretrained_models",
                               file_hash=modhash, cache_dir=Path(__file__).resolve().parent)
model_age = get_model(model_name="ResNet50")
model_age.load_weights(weight_file)
img_size_age = 224
graph = tf.get_default_graph()

def predict_age(cropface):

    img = cv2.resize(cropface, (img_size_age, img_size_age))
    img = np.array(img, dtype=np.float32)
    img = np.reshape(img, (-1, img_size_age, img_size_age, 3))

    # predict ages and genders of the detected faces
    with graph.as_default():
        results_age = model_age.predict(img)
    ages = np.arange(0, 101).reshape(101, 1)
    predicted_age = results_age.dot(ages).flatten()
    
    return predicted_age