import os
import time
import numpy as np
import tensorflow as tf

from django.conf import settings
from django.shortcuts import render
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing import image


MODEL_PATH = os.path.join(settings.BASE_DIR, "malaria", "ml_model", "malaria_model.h5")


model = models.Sequential([
    layers.Input(shape=(128, 128, 3)),

    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(2, activation='softmax')
])

model.load_weights(MODEL_PATH)


def predict_label(img_path):
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    classes = ['Parasitized (مصاب)', 'Uninfected (سليم)']

    result_index = int(np.argmax(prediction))
    confidence = float(np.max(prediction)) * 100

    return classes[result_index], confidence


def malaria_home(request):
    prediction = None
    confidence = None
    img_url = None

    if request.method == "POST":
        uploaded_img = request.FILES.get("my_image")

        if uploaded_img:
            filename = f"{int(time.time())}_{uploaded_img.name}"

            upload_dir = os.path.join(settings.MEDIA_ROOT, "malaria_uploads")
            os.makedirs(upload_dir, exist_ok=True)

            img_path = os.path.join(upload_dir, filename)

            with open(img_path, "wb+") as destination:
                for chunk in uploaded_img.chunks():
                    destination.write(chunk)

            prediction, confidence = predict_label(img_path)
            img_url = settings.MEDIA_URL + "malaria_uploads/" + filename

    return render(
        request,
        "malaria/index.html",
        {
            "prediction": prediction,
            "confidence": confidence,
            "img_path": img_url,
        }
    )