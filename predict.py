import tensorflow as tf
from tensorflow import keras

from model_config import CLASS_NAMES


import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "fashion_model.keras")
IMAGE_SIZE = (224, 224)


# Load trained model
model = keras.models.load_model(MODEL_PATH)

print("Model loaded successfully!")
def predict_image(image_path):

    # Load image
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
    predicted_index = tf.argmax(predictions[0]).numpy()

    predicted_class = CLASS_NAMES[predicted_index]

    # Get confidence
    confidence = float(predictions[0][predicted_index]) * 100
    print("Predicted Category:", predicted_class)
    print("Confidence:", round(confidence, 2), "%")
    return predicted_class, confidence


if __name__ == "__main__":

    image_path = input("Enter image path: ")

    predict_image(image_path)