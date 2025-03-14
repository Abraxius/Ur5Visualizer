# Ur5Visualizer
A program which visualizes movements, working areas and similar of a UR5 control. This is part of the research project at the HS Fulda.

# Requirements.txt

This file contains the required packages

# Server.py

The server is started with this command
```
.\venv\Scripts\Activate
cd .\ViZo\
cd .\src\
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```


# Visualizer.py

The visualizer is started with this command
```
.\venv\Scripts\Activate
cd .\ViZo\
cd .\src\
python main.py
```

# These are the attributes that are expected from the individual objects

![image](https://github.com/user-attachments/assets/810bb1c2-77ce-4c1d-be99-5c454924a7b8)
