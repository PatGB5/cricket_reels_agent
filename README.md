# 🏏 Cricket Reels Generator (AI + HeyGen + FastAPI)

A smart pipeline to auto-create Instagram-ready cricket reels using **AI avatars**, **Gemini**, and **HeyGen** — with auto image overlays and full frontend preview flow.

## 🚀 What It Does

- 🧠 Fetches cricket facts (based on today's date)
- ✍️ Generates a catchy script with Gemini
- 🎤 Narrates it using HeyGen avatar + voice
- 🖼️ Overlays relevant images using Whisper timestamping
- ✅ Lets you preview, edit & download the reel via frontend

---

## 🛠️ Tech Stack

- 🤖 Gemini 2.5 (Vertex AI)
- 🧑‍🚀 HeyGen API (Avatar + Voice)
- 🧵 Whisper (Transcription)
- 🎞️ moviepy (Overlay logic)
- ⚙️ FastAPI (Backend)
- 🌐 React + Tailwind (Frontend)
- ☁️ Vercel + Localhost (Deployment)

---

## 📁 Folder Structure

cricket_reels_agent/
├── app/services/ # AI, video, and image logic
├── data/ # Scripts, videos, images
├── main.py # FastAPI entrypoint
├── frontend/ # Vercel-compatible frontend

## 🧪 API Overview

| Endpoint          | Purpose                         |
|------------------|----------------------------------|
| `/generate_script/` | Generate script + facts         |
| `/create_video/`    | Generate HeyGen avatar video    |
| `/edit_video/`      | Overlay images and finalize     |

---

## ⚡ Quick Start

```bash
git clone ...
cd cricket_reels_agent
pip install -r requirements.txt
uvicorn main:app --reload

🎯 Author
Parth Tokekar
📧 parth.tokekar@students.iiit.ac.in
