from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import speech_recognition as sr
import io
from src.config import config
from src.domain.question import handle_user_input


app = FastAPI()

class TextRequest(BaseModel):
    user_id: str
    message: str

@app.post("/ask-text/")
async def ask_text(request: TextRequest):
    user_input = request.message
    user_id = request.user_id
    result = handle_user_input(user_input, user_id)
    return JSONResponse(content=result)

@app.post("/ask-audio/")
async def ask_audio(user_id: str = Form(...), audio_file: UploadFile = File(...)):
    recognizer = sr.Recognizer()
    audio_bytes = await audio_file.read()
    with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="es-ES")
        except sr.UnknownValueError:
            return JSONResponse(content={"error": "No se pudo entender el audio"}, status_code=400)
        except sr.RequestError as e:
            return JSONResponse(content={"error": f"Error del servicio de reconocimiento: {e}"}, status_code=500)
    result = handle_user_input(text, user_id)
    return JSONResponse(content=result)
