# A small service for preparing weekly meetings etc
Uses Flask sessions to store everything between endpoints

- Built in Python
- Uses [Flask](https://pypi.org/project/Flask/)
- Loads config using [PyYAML](https://pypi.org/project/PyYAML/)
- Uses [waitress](https://pypi.org/project/waitress/)


# Windows Quickstart Guide

- Have python and pip installed
- Create a venv (virtual environment):
    - `python -m venv .venv`
    - `.venv/Scripts/Activate.ps1` (might get stopped by windows' execution policy)
    - `pip install Flask pyyaml waitress`
    - `deactivate`
- Ensure that the python path points to your venv
- Run app.py

From there, you should be able to make POST requests to the server on the assigned port (default: 0.0.0.0:5000)  
  
`/add_text`
- `{"text": Any}` -> `{"guid": str, "new_session": bool}` (creates a guid to use in future requests)
- `{"guid": str, "text": Any}` -> `{"guid": str, "new_session": bool}` (returns guid you sent)

`/get_text`
- `{"guid": str}` -> `{"text": List[Any]}`
