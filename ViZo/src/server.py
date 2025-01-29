from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Union

app = FastAPI()
print("Server läuft...")

# Statische Dateien und Templates konfigurieren
app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

class Coordinates(BaseModel):
    shape: str
    x: int
    y: int

#Formen-Speicher (vorerst in-memory)
shapes = []

# Initiale Koordinaten
current_coordinates = {"x": 200, "y": 200}

@app.post("/update")
def update_coordinates(coords: Coordinates):
    global current_coordinates
    current_coordinates["x"] = coords.x
    current_coordinates["y"] = coords.y
    return {"message": "Koordinaten aktualisiert"}

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/add_shape")
async def add_shape(shape: Shape):
    shapes.append(shape.dict())
    return {"message": "Shape added", "shapes": shapes}

@app.get("/status")
def get_coordinates():
    return current_coordinates
