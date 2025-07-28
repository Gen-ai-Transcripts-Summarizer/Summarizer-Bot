from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from openai import AzureOpenAI
import whisper
import os
import tiktoken

# ------------------------------
# CONFIGURATION
# ------------------------------
AZURE_API_KEY = ""
AZURE_ENDPOINT = ""
DEPLOYMENT_NAME = ""
API_VERSION = ""

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create folders if they don't exist
os.makedirs("uploads/audio", exist_ok=True)
os.makedirs("uploads/text", exist_ok=True)

# Load Whisper model
whisper_model = whisper.load_model("base") 

# Azure client setup
client = AzureOpenAI(
    api_key=AZURE_API_KEY,
    azure_endpoint=AZURE_ENDPOINT,
    api_version=API_VERSION,
)

# ------------------------------
# Tokenization Function
# ------------------------------
def tokenize_transcript(transcript: str, model: str = "gpt-4", max_tokens_per_chunk: int = 1000):
    tokenizer = tiktoken.encoding_for_model(model)
    token_ids = tokenizer.encode(transcript)
    total_tokens = len(token_ids)
    print(f"Total tokens: {total_tokens}")

    # Create chunks of 1000 tokens
    chunks = [
        token_ids[i:i + max_tokens_per_chunk]
        for i in range(0, total_tokens, max_tokens_per_chunk)
    ]

    # Decode chunks to strings
    text_chunks = [tokenizer.decode(chunk) for chunk in chunks]
    return text_chunks

# ------------------------------
# Function to summarize transcript
# ------------------------------
def summarize_transcript(transcript: str) -> str:
    try:
        chunks = tokenize_transcript(transcript)
        summaries = []

        for chunk in chunks:
            response = client.chat.completions.create(
                model=DEPLOYMENT_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a professional meeting assistant. Given a raw meeting transcript, generate a structured summary that includes:\n"
                            "- Key discussion points\n"
                            "- Decisions made\n"
                            "- Action items (with assignees and deadlines if mentioned)"
                        )
                    },
                    {
                        "role": "user",
                        "content": f"Transcript:\n{chunk}\n\nPlease provide the summary."
                    }
                ],
                temperature=0.7,
                max_tokens=1024,
                top_p=1.0
            )
            summaries.append(response.choices[0].message.content.strip())

        return "\n".join(summaries)
    except Exception as e:
        return f"❌ Error during summarization: {e}"

# ------------------------------
# AUDIO UPLOAD ENDPOINT
# ------------------------------
@app.post("/upload/audio")
async def upload_audio(file: UploadFile = File(...)):
    try:
        audio_path = os.path.join("uploads/audio", file.filename)
        with open(audio_path, "wb") as f:
            f.write(await file.read())

        result = whisper_model.transcribe(audio_path)
        transcript = result["text"]
        summary = summarize_transcript(transcript)

        # Save summary
        output_path = os.path.join("uploads/text", "output.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(summary)

        return {
            "filename": file.filename,
            "transcript": transcript,
            "summary": summary
        }
    except Exception as e:
        return {"error": str(e)}

# ------------------------------
# TEXT UPLOAD ENDPOINT
# ------------------------------
@app.post("/upload/text")
async def upload_text(file: UploadFile = File(...)):
    try:
        text_path = os.path.join("uploads/text", file.filename)
        with open(text_path, "wb") as f:
            f.write(await file.read())

        with open(text_path, "r", encoding="utf-8") as f:
            transcript = f.read()

        summary = summarize_transcript(transcript)

        # Save summary
        output_path = os.path.join("uploads/text", "output.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(summary)

        return {
            "filename": file.filename,
            "transcript": transcript,
            "summary": summary
        }
    except Exception as e:
        return {"error": str(e)}
