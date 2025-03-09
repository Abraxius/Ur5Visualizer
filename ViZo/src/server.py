from fastapi import FastAPI, Request, Form, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Union
from typing import List, Tuple, Optional
import asyncio
import random
import json

app = FastAPI()
print("Server läuft...")

# Datenmodell für Objekte
class VisualObject(BaseModel):
    id: int
    name: str = "Alex"
    type: str = "rectangle" # z.B. "circle" oder "rectangle"
    x: int = 100
    y: int = 100
    color: str = "blue"
    scale_x: int = "100"
    scale_y: int = "100"
    border_width: int = "5"
    visible: bool
    lines_points: List[Tuple[int, int]] = [[0, 0], [1, 1]]
    text: Optional[str] = ""
    rotation: int = 0

class Sounds(BaseModel):
    id: int
    name: str = "Twin.mp3"
    
#Formen-Speicher (vorerst in-memory)
#objects = [
#    VisualObject(id="1-blue", type="circle", x=200, y=200, color="blue", scale_x=20, scale_y=20, visible=True),
#    VisualObject(id="2-red", type="circle", x=100, y=100, color="red", scale_x=20, scale_y=20, visible=True),
#    VisualObject(id="3-green", type="circle", x=300, y=300, color="green", scale_x=20, scale_y=20, visible=True)
#]

#VisualObject(
#    id="1", 
#    name="Text",
#    type="text",
#    x=50,
#    y=100,
#    scale_x=50,
#    scale_y=40,
#    border_width=5,
#    visible=True,
#    line_points=[[0,0], [1,1], [2,2]],
#    text="Hello world",
#    rotation=45,
#)

#Sound-Speicher
sounds = []

# Lade die Objekte aus einer JSON-Datei
def dict(self):
    """Umwandlung der VisualObject-Instanz in ein Dictionary für JSON."""
    return {
        "id": self.id,
        "name": self.name,
        "type": self.type,
        "x": self.x,
        "y": self.y,
        "color": self.color,
        "scale_x": self.scale_x,
        "scale_y": self.scale_y,
        "border_width": self.border_width,
        "visible": self.visible,
        "lines_points": self.lines_points,
        "text": self.text,
        "rotation": self.rotation
    }

@classmethod
def from_dict(cls, data):
    """Erstelle ein VisualObject aus einem Dictionary."""
    try:
        return cls(
            id=data["id"],
            name=data["name"],
            type=data["type"],
            x=data["x"],
            y=data["y"],
            color=data["color"],
            scale_x=data["scale_x"],
            scale_y=data["scale_y"],
            border_width=data["border_width"],
            visible=data["visible"],
            lines_points=data["lines_points"],
            text=data["text"],
            rotation=data["rotation"]
        )
    except KeyError as e:
        print(f"Fehlender Key: {e}")
        raise
    except TypeError as e:
        print(f"Typfehler: {e}")
        raise

# Lade die Objekte aus einer JSON-Datei
def load_objects():
    try:
        with open('objects.json', 'r') as f:
            data = json.load(f)
            print(f"Geladene Daten: {data}")  # Debug-Ausgabe
            # Umwandlung der gespeicherten Dictionaries zurück in VisualObject-Instanzen
            return [VisualObject.parse_obj(obj) for obj in data]
    except (FileNotFoundError, json.JSONDecodeError):
        print("Die Speicherdatei existiert nicht oder ist leer.")
        return []

# Speichere die Objekte in eine JSON-Datei
def save_objects(objects: List[VisualObject]):
    with open('objects.json', 'w') as f:
        # Umwandlung der VisualObject-Instanzen in Dictionaries für die Speicherung
        json.dump([obj.dict() for obj in objects], f, indent=4)

# Die in-memory-Liste von Objekten, wird von der JSON-Datei geladen
objects = load_objects()
    
if not objects:
    print("Es werden standard Objekte erzeugt.")
    
    #objects = [
    #    VisualObject(id="1", name="leander", type="circle", x=200, y=200, color="blue", scale_x=20, scale_y=20, border_width=5, visible=True),
    #    VisualObject(id="2", name="hannah", type="circle", x=100, y=100, color="red", scale_x=20, scale_y=20, border_width=5, visible=True),
    #    VisualObject(id="3", name="alex", type="rectangle", x=300, y=300, color="green", scale_x=100, scale_y=50, border_width=5, visible=True)
    #]

    save_objects(objects)

@app.post("/update/{object_id}")
def update_object(object_id: int, coords: VisualObject):
    for obj in objects:
        if obj.id == object_id:
            print(f"Updating object {obj.id}: {coords}")
            obj.type = coords.type
            obj.name = coords.name
            obj.x = coords.x
            obj.y = coords.y
            obj.scale_x = coords.scale_x
            obj.scale_y = coords.scale_y
            obj.border_width = coords.border_width
            obj.color = coords.color
            obj.visible = coords.visible
            obj.lines_points = coords.lines_points
            obj.text = coords.text
            obj.rotation = coords.rotation
            print(f"Updated object {obj.id}: {obj}")

    save_objects(objects)
    return {"message": "Objekt aktualisiert"}

@app.post("/update_coordinate/{object_id}")
def update_coordinates(object_id: int, coords: VisualObject):
    for obj in objects:
        if obj.id == object_id:
            obj.x = coords.x
            obj.y = coords.y
            print(f"Updated object {obj.id}: {obj}")

    save_objects(objects)
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

#crud interface

@app.post("/objects")
def create_object(obj: VisualObject):
    """Ein neues Objekt erstellen."""
    new_id = len(objects) + 1  # Automatische ID-Zuweisung
    new_object = VisualObject(id=new_id, name=obj.name, type=obj.type, x=obj.x, y=obj.y, color=obj.color, scale_x=obj.scale_x, scale_y=obj.scale_y, border_width=obj.border_width, visible=obj.visible, lines_points=obj.lines_points, text=obj.text, rotation=obj.rotation)
    objects.append(new_object)
    save_objects(objects)
    return {"message": "Objekt hinzugefügt", "object": new_object}

@app.post("/sounds")
def create_sound(sound: Sounds):
    """Einen im Ordner abgelegten Sound abspielen. Dafür wird der Sound hinzugefügt."""
    new_id = len(sounds) + 1  # Automatische ID-Zuweisung
    new_sound = Sounds(id=new_id, name=sound.name)
    sounds.append(new_sound)
    return {"message": "Spiele Sound ab", "object": new_sound}

@app.get("/sounds", response_model=List[Sounds])
def get_sound():
    """Einen im Ordner abgelegten Sound abspielen. Dafür werden die Sounds geladen."""
    return sounds

@app.delete("/sounds")
def delete_sound():
    sounds.clear()
    return {"message": "Alle Sounds gelöscht"}

# ToDo: Funktioniert noch nicht richtig, ist aktuell allerdings auch unnötig, deshalb auskommentiert
#@app.delete("/sounds/{sound_name}")
#def delete_sound(sound_name: str):
#    """Hier werden die Sounds aus der Liste gelöscht, damit sie nicht endlos abspielen."""
#    for snd in sounds:
#        if snd.name == sound_name:
#            sounds.remove(sound_name)
#            return {"message": "Der Sound wurde gelöscht"}
#    return {"message": "Der Sound wurde nicht gefunden"}