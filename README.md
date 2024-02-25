# A small service for preparing weekly meetings etc
Uses Flask sessions to store everything between endpoints

- Built in Python
- Uses [Flask](https://pypi.org/project/Flask/)
- Loads config using [PyYAML](https://pypi.org/project/PyYAML/)
- Uses [waitress](https://pypi.org/project/waitress/)


# Quickstart Guide

- Have python and pip installed
- Create a venv (virtual environment):
    - `python -m venv .venv`
    - `.venv/Scripts/Activate.ps1` (might get stopped by windows' execution policy)
    - `pip install Flask pyyaml waitress`
    - `deactivate`
- Ensure that the python path points to your venv
- Run app.py

From there, you should be able to make POST requests to the server on the assigned port (default: 0.0.0.0:5000)  
  
/add_text
- `{"guid"?: str, "text": Any}` -> `{"guid": str}`

/get_text
- `{"guid": str}` -> `{"text": List[Any]}`
