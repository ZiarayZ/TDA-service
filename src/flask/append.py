from flask import session, request
from uuid import uuid4


def handle_text():
    if request.method == "POST":
        text = request.json.get("text", None)
        guid = request.json.get("guid", None)
        if text is None:
            raise TypeError(f"invalid type, text: {text}")
        if guid is None:
            guid = uuid4().hex
        # add text to memory
        if guid in session:
            sessionText = session[guid]
            if isinstance(sessionText, list):
                sessionText.append(text)
            session[guid] = sessionText
        else:
            session[guid] = [text]
        return {"guid": guid}
    else:
        raise ConnectionRefusedError(f"invalid request method")


def handle_return():
    if request.method == "POST":
        guid = request.json.get("guid", None)
        if guid is None:
            raise TypeError(f"invalid type, guid: {guid}")
        # return all text pulled from memory/end session
        if guid in session:
            text = session[guid]
            session.clear()
            return {"text": text}
        else:
            raise IndexError("missing text")
    else:
        raise ConnectionRefusedError("invalid request method")
