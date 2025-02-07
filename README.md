# CapGen: Video Transcription and Captioning System

## Overview
CapGen is a full-stack web application that allows users to upload videos, transcribe audio from them, generate subtitles, and overlay those subtitles onto the video. The backend is built with Django, and the frontend is powered by React. Users can preview the generated video with captions and download it.

## Features
- Video Upload: Upload videos to the system for processing.
- Audio Transcription: Uses the Whisper model to transcribe audio from the uploaded video.
- Subtitles Generation: Generates SRT subtitle files from the transcription.
- Overlay Subtitles: Overlays the generated subtitles onto the video.
- Preview and Download: Users can preview the captioned video and download it.

## Technologies Used
- Backend: Django, Whisper, MoviePy
- Frontend: React
- Libraries:
  - Whisper for audio transcription
  - MoviePy for video manipulation (overlaying subtitles)
  - SRT for subtitle generation
  - Django Rest Framework for handling API requests

## Getting Started
- Clone Repository
- git clone https://github.com/ByronSophin/CapGen.git

- Set Up a virtual environment.
- pip install django whisper moviepy srt
- System must have ffmpeg installed as well
