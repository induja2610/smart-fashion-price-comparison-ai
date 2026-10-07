from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "success": True,
        "message": "Smart Fashion Price Comparison AI Backend is working!"
    })


@app.route("/api/test")
def test_api():
    return jsonify({
        "success": True,
        "message": "Backend API is working!"
    })


if __name__ == "__main__":
    app.run(debug=True)