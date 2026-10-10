
import os
import numpy as np
import gdown
from PIL import Image
from ai_edge_litert.interpreter import Interpreter

from model_config import CLASS_NAMES


# Project folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Smaller TensorFlow Lite model
MODEL_PATH = os.path.join(BASE_DIR, "fashion_model.tflite")

IMAGE_SIZE = (224, 224)

# Google Drive model link
MODEL_URL = (
    "https://drive.google.com/uc?"
    "id=1o7-soGYKokvLxYpILKlGDZQae1A2BnPr"
)


# Download model if it does not exist
if not os.path.exists(MODEL_PATH):
    print("AI model not found. Downloading...")

    result = gdown.download(
        MODEL_URL,
        output=MODEL_PATH,
        quiet=False
    )

    if not result or not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            "Model download failed. Check Google Drive access."
        )

if os.path.getsize(MODEL_PATH) == 0:
    raise ValueError("Downloaded model file is empty.")

print("Loading LiteRT model...")

# Load the smaller model
interpreter = Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("LiteRT model loaded successfully!")


def predict_image(image_path):

    # Open and resize image
    with Image.open(image_path) as image:
        image = image.convert("RGB")
        image = image.resize(IMAGE_SIZE)

        image_array = np.asarray(
            image,
            dtype=np.float32
        )

    # Add batch dimension
    image_array = np.expand_dims(image_array, axis=0)

    input_info = input_details[0]
    input_dtype = input_info["dtype"]

    # Handle quantized input if required
    scale, zero_point = input_info["quantization"]

    if input_dtype in (np.uint8, np.int8) and scale > 0:
        image_array = np.round(
            image_array / scale + zero_point
        )

        limits = np.iinfo(input_dtype)
        image_array = np.clip(
            image_array,
            limits.min,
            limits.max
        )

    image_array = image_array.astype(input_dtype)

    # Run prediction
    interpreter.set_tensor(
        input_info["index"],
        image_array
    )
    interpreter.invoke()

    predictions = interpreter.get_tensor(
        output_details[0]["index"]
    )[0]

    # Convert quantized output if necessary
    output_info = output_details[0]
    output_scale, output_zero_point = output_info["quantization"]

    if output_info["dtype"] in (np.uint8, np.int8) and output_scale > 0:
        predictions = (
            predictions.astype(np.float32) - output_zero_point
        ) * output_scale

    # Get predicted class
    predicted_index = int(np.argmax(predictions))
    predicted_class = CLASS_NAMES[predicted_index]

    # Confidence percentage
    confidence = float(predictions[predicted_index]) * 100

    print("Predicted Category:", predicted_class)
    print("Confidence:", round(confidence, 2), "%")

    return predicted_class, confidence
