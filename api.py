from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import subprocess
import os
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

class TTSRequest(BaseModel):
    text: str

PYTHON_EXE = r"C:\Users\Nicky\Documents\tetosp\kokoro_env\Scripts\python.exe"
VOICE = "ff_siwis"

@app.post("/tts")
async def generate_tts(request: TTSRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Le texte ne peut pas être vide.")

    # Créer un fichier unique dans outputs/
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    output_file = f"output_{uuid.uuid4().hex}.wav"
    output_path = os.path.join(output_dir, output_file)

    cmd = [
        PYTHON_EXE,
        "-m", "kokoro",
        "--voice", VOICE,
        "--text", request.text,
        "--output-file", output_path,
        "--speed", "1.0"
    ]

    try:
        subprocess.run(cmd, check=True)
        if not os.path.exists(output_path):
            raise HTTPException(status_code=500, detail="Le fichier audio n'a pas été généré.")

        # FastAPI va servir ce fichier à partir de /outputs/...
        return {"audio_file": f"outputs/{output_file}"}

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=str(e))
