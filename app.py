
from flask import Flask, jsonify, request, render_template
import os

from price_data import PRICE_DATA
from predict import predict_image
from live_prices import get_live_prices


app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/static"
)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it does not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/result")
def result():
    return render_template("result.html")


@app.route("/api/test")
def test_api():
    return jsonify({
        "success": True,
        "message": "Backend API is working!"
    })


@app.route("/api/prices/<category>")
def get_prices(category):

    if category not in PRICE_DATA:
        return jsonify({
            "success": False,
            "message": "Category not found"
        }), 404

    prices = PRICE_DATA[category]

    return jsonify({
        "success": True,
        "category": category,
        "prices": prices
    })


@app.route("/api/upload", methods=["POST"])
def upload_image():

    if "image" not in request.files:
        return jsonify({
            "success": False,
            "message": "No image uploaded"
        }), 400

    image = request.files["image"]

    if image.filename == "":
        return jsonify({
            "success": False,
            "message": "No image selected"
        }), 400

    # Use only the filename, not any supplied folder path
    filename = os.path.basename(image.filename)

    if not filename:
        return jsonify({
            "success": False,
            "message": "Invalid filename"
        }), 400

    image_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    image.save(image_path)

    # Predict fashion category using the AI model
    predicted_class, confidence = predict_image(image_path)

    # Fetch shopping results from SerpApi
    try:
        prices = get_live_prices(predicted_class)

    except Exception:
        app.logger.exception("Live price search failed")

        return jsonify({
            "success": False,
            "message": "Live price search failed. Please try again.",
            "predicted_category": predicted_class,
            "confidence": confidence
        }), 502

    return jsonify({
        "success": True,
        "message": "Image prediction and live price search completed",
        "filename": filename,
        "predicted_category": predicted_class,
        "confidence": confidence,
        "prices": prices
    })


if __name__ == "__main__":
    app.run(debug=True)