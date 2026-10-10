
import os
import tensorflow as tf
from tensorflow import keras
import gdown

from model_config import CLASS_NAMES


# Project folder path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# AI model path
MODEL_PATH = os.path.join(BASE_DIR, "fashion_model.keras")

# Image size used for prediction
IMAGE_SIZE = (224, 224)


# Download the AI model if it is missing
if not os.path.exists(MODEL_PATH):
    print("AI model not found. Downloading from Google Drive...")

    MODEL_URL = "https://drive.google.com/uc?id=1xZkBkbMrxUPvxuWOgsaeKG2EgoD4RxDm"

    download_result = gdown.download(
        MODEL_URL,
        MODEL_PATH,
        quiet=False,
        fuzzy=True
    )

    if not download_result or not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            "AI model download failed. Check Google Drive sharing settings."
        )

# Load trained model
model = keras.models.load_model(MODEL_PATH)

print("Model loaded successfully!")


def predict_image(image_path):

    # Load image and resize
    image = tf.keras.utils.load_img(
        image_path,
        target_size=IMAGE_SIZE
    )

    # Convert image to array
    image_array = tf.keras.utils.img_to_array(image)

    # Add batch dimension
    image_array = tf.expand_dims(image_array, 0)

    # Make prediction
    predictions = model.predict(image_array, verbose=0)

    # Get predicted class
    predicted_index = int(tf.argmax(predictions[0]).numpy())
    predicted_class = CLASS_NAMES[predicted_index]

    # Get confidence
    confidence = float(predictions[0][predicted_index]) * 100

    print("Predicted Category:", predicted_class)
    print("Confidence:", round(confidence, 2), "%")

    return predicted_class, confidence


if __name__ == "__main__":

    image_path = input("Enter image path: ")
    predict_image(image_path)
