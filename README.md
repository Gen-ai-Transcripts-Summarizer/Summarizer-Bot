# 🎯 AI-Powered Meeting Transcript Summarizer

This project is a full-stack AI tool designed to convert audio or raw text meeting files into meaningful summaries. It transcribes audio using Whisper, summarizes the content using Azure OpenAI (GPT-4), and allows for download of the output summary — all integrated in a user-friendly React frontend and FastAPI backend.

---

## 🖥️ Frontend (React)

The React frontend provides a clean and intuitive interface to interact with the system. It offers:

- **Dual upload options:** Users can upload either audio files (e.g., `.mp3`, `.wav`) or `.txt` files containing transcripts.
- **API Integration:** The frontend sends HTTP POST requests to FastAPI endpoints using `fetch`.
- **Response Rendering:** On successful processing, it displays the original transcript and summarized content on screen.
- **Downloadable Output:** Users can download the final summary as `summary_<filename>.txt`.
- **Cross-Origin Support:** Integrated with CORS to ensure communication between different ports (e.g., React on 5173, FastAPI on 8000).

---

## 🚀 Backend (FastAPI + Whisper + Azure OpenAI)

The FastAPI backend acts as the core processing engine:

### 🔉 Audio Processing with Whisper
- Uses OpenAI’s `whisper` model to transcribe speech from uploaded audio files into text.
- The transcription is stored and later used as input to the summarization model.

### 🧠 LLM Summarization with Azure OpenAI (GPT-4)
- After obtaining the transcript (either from a `.txt` file or via Whisper), it’s sent to Azure OpenAI's GPT-4 model.
- The backend crafts a system prompt instructing the model to extract:
  - Key discussion points
  - Decisions made
  - Action items (with assignees and deadlines)

### 📁 Folder Structure
- `uploads/audio/`: Stores incoming audio files.
- `uploads/text/`: Stores incoming text transcripts.
- `output/`: Contains the generated summaries.

---

## 🧠 How the LLM (GPT-4) Works

GPT-4 is used in a **chat-completion mode** through Azure OpenAI. The backend sends the following payload:

```json
{
  "model": "gpt-4o",
  "messages": [
    {
      "role": "system",
      "content": "You are a professional meeting assistant. Given a raw meeting transcript..."
    },
    {
      "role": "user",
      "content": "Transcript: <full transcript text>"
    }
  ]
}
```

The model responds with a structured summary, making it easy for teams to:
- Review discussions without reading entire transcripts
- Identify tasks, deadlines, and responsibilities
- Improve meeting efficiency and documentation

---

## 🧩 Token Chunking for Long Transcripts

LLMs like GPT-4 have token limits (e.g., ~128k for GPT-4o). To handle transcripts longer than the model’s token limit, the backend implements **chunking**:

- The transcript is split into smaller text chunks, each under a safe token limit (e.g., 4000 tokens).
- Each chunk is summarized independently using GPT-4.
- Finally, the chunk-level summaries are merged and optionally re-summarized to produce the final condensed output.

🔧 This ensures:
- Compatibility with LLM constraints
- Reliable output even for long meetings
- Better memory usage and performance

---

## ✅ Summary

With a modern frontend, powerful FastAPI backend, Whisper transcription, and GPT-4 summarization — this tool is a production-grade solution for automating meeting documentation and boosting team productivity.

