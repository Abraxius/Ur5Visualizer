from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union

app = FastAPI()
print("Server läuft...")

class Coordinates(BaseModel):
    x: int
    y: int

# Initiale Koordinaten
current_coordinates = {"x": 200, "y": 200}

@app.post("/update")
def update_coordinates(coords: Coordinates):
    global current_coordinates
    current_coordinates["x"] = coords.x
    current_coordinates["y"] = coords.y
    return {"message": "Koordinaten aktualisiert"}

@app.get("/")
def hello_world():
    return {'message': 'Hello World!'};

@app.get("/status")
def get_coordinates():
    return current_coordinates
