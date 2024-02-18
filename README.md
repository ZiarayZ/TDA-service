# A small service for preparing weekly meetings etc

- Built in Python
- Uses [Flask](https://pypi.org/project/Flask/)
- Loads config using [PyYAML](https://pypi.org/project/PyYAML/)
- Uses [waitress](https://pypi.org/project/waitress/)


# Quickstart Guide

- Have python installed
- Create a venv (virtual environment)
- `.venv/Scripts/Activate.ps1` (might need to mess with permissions to allow this)
- `pip install Flask pyyaml waitress`
- `deactivate`
- Ensure that the python path points to your venv
- Run app.py