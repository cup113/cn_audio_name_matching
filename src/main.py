import import_helper as _

from shutil import which
from flaskwebgui import FlaskUI  # type: ignore
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi import FastAPI
from pydantic import BaseModel
from base64 import decodebytes as base64_decode
from subprocess import Popen

from server.core import match_from_audio


class MatchAudio(BaseModel):
    audio_base64: str
    app_type: str


app = FastAPI(debug=True)

@app.get("/")
def redirect_index():
    return RedirectResponse("/index.html")

@app.post("/api/v1/match")
def match_audio(data: MatchAudio):
    audio = base64_decode(bytes(data.audio_base64, encoding="ascii"))
    input_filename = "tmp/input." + "webm"
    with open(input_filename, "wb") as f:
        f.write(audio)
    Popen(["ffmpeg", "-i", input_filename, "-ar", "16000", "tmp/output.wav", "-y"]).wait()
    return JSONResponse(match_from_audio("tmp/output.wav"))


app.mount("/", StaticFiles(directory="src/client/dist/"))

if __name__ == "__main__":
    FlaskUI(server="fastapi", app=app).run()
