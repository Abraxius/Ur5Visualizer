# ViZo
Overview
A program which visualizes movements, working areas and similar of a UR5 control. This is part of the research project at the HS Fulda.

The system provides visual and acoustic feedback by projecting information directly onto the work surface and playing audio signals when required. The information is displayed via a projector. It consists of:

- A FastAPI server that manages objects and sounds via a REST API

- A PyGame-based visualizer that displays and projects the data

Visual elements (circles, rectangles, texts, lines, images) and audio signals are managed and updated via HTTP requests. Objects can be rotated, colored, hidden and saved.

# Setup and Usage
1. Clone the repository
```
git clone https://github.com/Abraxius/Ur5Visualizer.git
cd visualizer
```
2. Install dependencies
Make sure Python 3.8+ is installed. Then install the required packages:

```
pip install -r requirements.txt
```
3. Start the FastAPI server
```
.\venv\Scripts\Activate
cd .\ViZo\
cd .\src\
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```
This will launch the REST API server on http://127.0.0.1:8000.

4. Start the PyGame visualizer
```
.\venv\Scripts\Activate
cd .\ViZo\
cd .\src\
python main.py
```
The visualizer will fetch data from the API and project it (using a projector or screen).

# API Usage
You can interact with the system via HTTP requests (e.g., from Python, curl, or any other application). The server handles object creation, updates, and sound playback.

Base URL
```
http://localhost:8000
```

Docs URL - Overview
```
http://127.0.0.1:8000/docs
```

## Object Endpoints

| Endpoint           | Method | Description                           |
|--------------------|---------|----------------------------------------|
| `/objects`         | GET     | Returns all current objects |
| `/objects/{id}`    | GET     | Returns a single object by ID       |
| `/objects`         | POST    | Creates a new object              |
| `/update/{id}`     | POST    | Updates an existing object by ID                |
| `/update/{id}`     | DELETE    | Delete an existing object by ID              |

To create a object:
Send a POST request to /objects with a JSON body like:
```
{
{
  "id": 0,
  "name": "Alex",
  "type": "rectangle",
  "x": 100,
  "y": 100,
  "color": "blue",
  "scale_x": 100,
  "scale_y": 100,
  "border_width": 5,
  "visible": true,
  "lines_points": [
    [
      0,
      0
    ],
    [
      1,
      1
    ]
  ],
  "text": "",
  "rotation": 0
}
}
```

Here is an overview of all parameters:
| Parameter       | Type     | Description                                               |
|-----------------|----------|-----------------------------------------------------------|
| `id`            | `int`    | Auto-assigned if not set manually                         |
| `name`          | `str`    | Name or filename (for images/sounds)                      |
| `type`          | `str`    | `circle`, `rectangle`, `text`, `image`, `lines`           |
| `x`, `y`        | `int`    | Position (center) of the object                           |
| `color`         | `str`    | Color name or RGB list (e.g. `[0, 128, 255]`)    |
| `scale_x/y`     | `int`    | Size or dimensions depending on type                      |
| `rotation`      | `int`    | Rotation angle in degrees                                 |
| `visible`       | `bool`   | Display status (`true` or `false`)                        |
| `border_width`  | `int`    | 0 = filled shape; >0 = border thickness                   |
| `text`          | `str`    | Text content (only for `type = "text"`)                   |
| `lines_points`  | `list[tuple[int, int]]` | List of point tuples (only for `type = "lines"`) |

Most optional fields can be omitted or set to default values.

Here is an overview of which parameters are required for which type:

| Object Type | Required Attributes                                                                 |
|-------------|--------------------------------------------------------------------------------------|
| Circle      | `id`, `name`, `type`, `x`, `y`, `color`, `scale_x`, `border_width`, `visible`       |
| Lines       | `id`, `name`, `type`, `color`, `border_width`, `visible`, `line_points`             |
| Rectangle   | `id`, `name`, `type`, `x`, `y`, `color`, `scale_x`, `scale_y`, `border_width`, `visible`, `rotation` |
| Image       | `id`, `name`, `type`, `x`, `y`, `scale_x`, `scale_y`, `visible`, `rotation`         |
| Text        | `id`, `name`, `type`, `x`, `y`, `visible`, `text`                                   |

Note for Images: The name must match the filename located in the /images folder.

## Sound Endpoints

| Endpoint     | Method | Description                          |
|--------------|--------|--------------------------------------|
| `/sounds`    | GET    | Returns the current sound queue      |
| `/sounds`    | DELETE | Deletes the current sound queue      |

To play a sound:
Send a POST request to /sounds with a JSON body like:
```
{
  "id": 0,
  "name": "Twin.mp3"
}
```
Make sure the .wav file is located in the /sounds folder.

After playback, the visualizer will automatically send a DELETE request to remove it from the queue.

# Future Improvements
Planned enhancements for usability and flexibility:

- Web interface for managing objects and sounds without editing JSON manually

- Dynamic object type support, with drawing logic for new types added automatically

- Scene control and grouping via extended API routes

- Upload function for sounds and images
