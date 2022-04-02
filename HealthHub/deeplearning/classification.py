import numpy as np
import cv2
import os
import keras
from keras.models import Sequential
from keras.layers import (
    Dense,
    Dropout,
    Activation,
    Flatten,
    Conv3D,
    Conv2D,
    MaxPooling2D,
    AveragePooling2D,
)


def prepare(picture_fn):
    img_array = cv2.resize(cv2.imread(picture_fn, cv2.IMREAD_GRAYSCALE), (100, 100))
    img_array = np.array(img_array).reshape(-1, 100, 100, 1)

    return img_array


def create_model():
    model = Sequential()

    model.add(Conv2D(256, (4, 4), input_shape=(100, 100, 1), activation="relu"))
    model.add(MaxPooling2D(pool_size=(3, 3)))
    model.add(Dropout(0.2))

    model.add(Conv2D(156, (3, 3), activation="relu"))
    model.add(AveragePooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Flatten())

    model.add(Dense(64, activation="relu"))
    model.add(Dense(32, activation="relu"))
    model.add(Dense(1, activation="sigmoid"))

    model.compile(optimizer="adam", metrics=["accuracy"], loss="binary_crossentropy")

    return model


def predict(app, img):
    array = prepare(img)
    model = create_model()
    model.load_weights(os.path.join(app.root_path, "deeplearning/model.h5"))
    return model.predict(array)[0]
