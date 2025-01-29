from fastapi import FastAPI, Request, Form, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Union
from typing import List
import asyncio
import random

app = FastAPI()
print("Server läuft...")

# Datenmodell für Objekte
class VisualObject(BaseModel):
    id: int
    type: str  # z.B. "circle" oder "rectangle"
    x: int
    y: int
    color: str
    visible: bool
    
#Formen-Speicher (vorerst in-memory)
objects = [
    VisualObject(id=1, type="circle", x=200, y=200, color="blue", visible=True),
    VisualObject(id=2, type="circle", x=100, y=100, color="red", visible=True),
    VisualObject(id=3, type="circle", x=300, y=300, color="green", visible=True)
]

@app.post("/update/{object_id}")
def update_coordinates(object_id: int, coords: VisualObject):
    for obj in objects:
        if obj.id == object_id:
            print(f"Updating object {obj.id}: {coords}")
            obj.type = coords.type
            obj.x = coords.x
            obj.y = coords.y
            obj.color = coords.color
            obj.visible = coords.visible
            print(f"Updated object {obj.id}: {obj}")
    return {"message": "Koordinaten aktualisiert"}

@app.get("/objects/{object_id}", response_model=VisualObject)
def get_object(object_id: int):
    """Ein bestimmtes Objekt anhand der ID abrufen."""
    for obj in objects:
        if obj.id == object_id:
            return obj
    return {"error": "Objekt nicht gefunden"}

@app.get("/objects/{object_id}", response_model=VisualObject)
def get_object(object_id: int):
    """Ein bestimmtes Objekt anhand der ID abrufen."""
    for obj in objects:
        if obj.id == object_id:
            return obj
    return {"error": "Objekt nicht gefunden"}

@app.get("/objects", response_model=List[VisualObject])
def get_objects():
    """Alle gespeicherten Objekte abrufen."""
    return objects

@app.post("/objects")
def create_object(obj: VisualObject):
    """Ein neues Objekt erstellen."""
    new_id = len(objects) + 1  # Automatische ID-Zuweisung
    new_object = VisualObject(id=new_id, type=obj.type, x=obj.x, y=obj.y, color=obj.color, visible=obj.visible)
    objects.append(new_object)
    return {"message": "Objekt hinzugefügt", "object": new_object}