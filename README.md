**description demo of Project**    https://drive.google.com/file/d/1mEMhDdoPkBNLO_I8AYsBm5kH2RYFZfK1/view?usp=sharing
#  AI-Powered Meeting Summarizer

An intelligent backend service built with **FastAPI**, leveraging **OpenAI Whisper** for transcription and **Azure GPT-4** for summarization. It transforms raw meeting audio or text transcripts into clean, actionable summaries.

---

##  Project Overview

> **Objective**: Automate the extraction of insights from meetings by converting spoken or written content into well-structured summaries containing:
> -  Key Discussion Points  
> -  Decisions Made  
> -  Action Items (with assignees and deadlines, if present)

This system ensures no important detail is missed — enabling teams to stay aligned and efficient, even after chaotic meetings.

---

##  Powered By

- 🎤 **[Whisper](https://github.com/openai/whisper)** (OpenAI): State-of-the-art speech recognition model for audio transcription.
- 💬 **[Azure OpenAI GPT-4](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/overview)**: Generates concise, human-like summaries from raw transcripts.
- ⚡ **FastAPI**: Modern Python web framework for building robust APIs.

---

##  Features

-  Upload `.mp3`, or `.txt` files
-  Auto-detects file type and handles accordingly:
  - Audio → Transcription → Summarization
  - Text → Direct Summarization
-  Stores outputs as downloadable `.txt` summaries
-  CORS-enabled for frontend integration
-  Clean and extensible codebase

---

##  Tech Stack

| Layer      | Tool/Library       |
|------------|--------------------|
| Backend    | FastAPI            |
| AI Models  | Whisper (base) + Azure GPT-4 |
| Language   | Python 3.10+       |
| Hosting    | Localhost / Uvicorn |
| Deployment | Ready for containerization |

---

##  Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ai-meeting-summarizer.git
cd ai-meeting-summarizer
