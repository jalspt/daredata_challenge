from flask import Flask, request, jsonify
import pandas as pd
import os
import sys

# Add the modules directory to the path so we can import the data_science package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from modules.ds.ds_package.src.data_science.modelling import SimpleModel

# Initialize the model
MODEL = SimpleModel()

# Path to models folder - relative path from this file to the models folder in ds module
MODELS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ds/models'))
MODEL.load(MODELS_FOLDER)

# Create Flask app
app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    # Validate input data
    if not data or "idx" not in data or "features" not in data:
        return jsonify({"error": "Invalid input data. Required fields: idx, features"}), 400

    try:
        # Make prediction
        label = MODEL.predict_with_logging(
            data["idx"],
            pd.DataFrame([data["features"]])
        )
        
        return jsonify({"label": int(label)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)