# server.py
from flask import Flask, request, jsonify

app = Flask(__name__)
coordinates = {"x": 400, "y": 300}  # Initialkoordinaten

@app.route("/update", methods=["POST"]) #überschreibt die aktuellen koordinaten mit den neuen
def update_coordinates():
    global coordinates
    data = request.get_json()
    coordinates["x"] = data.get("x", coordinates["x"])
    coordinates["y"] = data.get("y", coordinates["y"])
    return jsonify({"status": "success"})

@app.route("/coordinates", methods=["GET"])
def get_coordinates():
    return jsonify(coordinates)

if __name__ == "__main__":
    app.run(debug=True)
