from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Vastu AI Server Running"

@app.route("/analyze", methods=["POST"])
def analyze():
    if 'file' not in request.files:
        return jsonify({"result": "No image received"})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"result": "No file selected"})
    
    # Save uploaded image
    filepath = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(filepath)

    # Example response
    return jsonify({
        "result": "Image received and analyzed successfully"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
