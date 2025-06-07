# AI News Video Generator

A Python tool that automatically fetches trending news articles, generates a summary script using the Google Gemini API, and creates a short video with a voiceover and text overlays using MoviePy.


---

## Features

-   **Content Sourcing:** Fetches the latest news on any topic via the NewsAPI.
-   **AI Scripting:** Uses Google's Gemini API (`gemini-1.5-flash`) to generate a concise summary script.
-   **Text-to-Speech:** Creates an English voiceover from the script using gTTS.
-   **Automated Video Creation:** Programmatically combines a background video, the voiceover, and text overlays using MoviePy.

## Tech Stack

-   **Language:** Python 3
-   **Core Libraries:** MoviePy, gTTS, Requests
-   **APIs:** NewsAPI, Google Gemini API
-   **Dependencies:** FFmpeg, ImageMagick, Git LFS

---

## Setup and Installation

Follow these steps to set up and run the project locally.

#### 1. Install Prerequisites (macOS)
This project requires Git LFS, FFmpeg, and ImageMagick.
```bash
brew install git-lfs ffmpeg imagemagick
git lfs install
