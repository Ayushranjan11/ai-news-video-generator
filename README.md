# 🤖 AI News Video Generator

<p align="center">
  <img src="https://img.shields.io/badge/python-3.12-blue.svg" alt="Python version">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome">
</p>

A command-line tool that automatically fetches trending news articles, generates a summary script using the Google Gemini API, and creates a short, shareable video with a voiceover and text overlays using MoviePy.

---

### ✨ Features

-   **Dynamic Content:** Fetches the latest news on any user-provided topic via the NewsAPI.
-   **AI-Powered Scripting:** Uses Google's `gemini-1.5-flash` model to generate a concise and engaging summary script.
-   **Automated Voiceover:** Creates a clear English voiceover from the script using Google Text-to-Speech (gTTS).
-   **Custom Video Creation:** Programmatically combines a background video, the voiceover, and animated text overlays using the MoviePy library.
-   **Git LFS Integration:** Properly handles large video and audio file assets for version control.

---

### 🛠️ Tech Stack & Dependencies

-   **Language:** Python 3
-   **Core Libraries:**
    -   `moviepy` for video editing
    -   `gTTS` for text-to-speech
    -   `requests` for API calls
    -   `google-generativeai` for the AI model
-   **APIs:**
    -   [NewsAPI](https://newsapi.org)
    -   [Google Gemini API](https://aistudio.google.com/)
-   **System Dependencies:**
    -   `ffmpeg`
    -   `imagemagick`
    -   `git-lfs`

---

### 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine. This guide is tailored for macOS.

#### Prerequisites

Make sure you have [Homebrew](https://brew.sh/) installed on your Mac.

1.  **Install System Dependencies:**
    Open your terminal and run the following command to install Git LFS, FFmpeg, and ImageMagick.
    ```bash
    brew install git-lfs ffmpeg imagemagick
    ```
2.  **Set up Git LFS:**
    Run this one-time setup command.
    ```bash
    git lfs install
    ```

#### Installation

1.  **Clone the Repository:**
    This command will clone the project and start downloading the LFS files (like example videos).
    ```bash
    git clone [https://github.com/Ayushranjan11/ai-news-video-generator.git](https://github.com/Ayushranjan11/ai-news-video-generator.git)
    cd ai-news-video-generator
    ```

2.  **Set Up Python Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Python Packages:**
    Install all required libraries from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure API Keys:**
    -   Copy the example environment file:
        ```bash
        cp env.example .env
        ```
    -   Open the newly created `.env` file with a text editor and add your secret API keys.

5.  **Add Background Video:**
    -   Place a short video file (e.g., a looping abstract background) in the project's root directory.
    -   Make sure the file is named `background.mp4`.

---

### ▶️ Usage

To run the script, use the following command from the root of the project folder. Make sure your virtual environment is active.

```bash
python AI_video.py --topic "your topic here"
