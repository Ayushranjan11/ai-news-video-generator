import os
import requests
from dotenv import load_dotenv
import argparse
import google.generativeai as genai
from gtts import gTTS
# Import the loop function from moviepy effects
from moviepy.editor import *
from moviepy.video.fx.all import loop

# Load environment variables from the .env file
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Step 1: Configure APIs ---
# Configure the Google Gemini API with our key
try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    print(f"[FATAL ERROR] Could not configure Google API: {e}")
    print("Please ensure your GOOGLE_API_KEY in the .env file is correct.")
    exit()

def get_trending_news(topic):
    """Fetches a relevant news article for a given topic using NewsAPI."""
    print(f"\n[INFO] Step 1: Fetching news for topic: '{topic}'...")
    url = (f"https://newsapi.org/v2/everything?"
           f"q={topic}&"
           "sortBy=relevancy&"
           "language=en&"
           "pageSize=1&"
           f"apiKey={NEWS_API_KEY}")
    
    try:
        response = requests.get(url)
        # This will raise an error for bad responses (4xx or 5xx)
        response.raise_for_status() 
        data = response.json()
        if not data['articles']:
            print(f"[ERROR] No articles found for '{topic}'. Try a different topic.")
            return None, None
        
        article = data['articles'][0]
        title = article.get('title', 'No Title')
        # Get the description or content, whichever is available
        content = article.get('description') or article.get('content', 'No content available.')
        print(f"-> Found article: '{title}'")
        return title, content
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch news from NewsAPI: {e}")
        print("Please ensure your NEWS_API_KEY is correct and you have an internet connection.")
        return None, None

def generate_script(title, content):
    """Generates a short video script using the Google Gemini API."""
    print("[INFO] Step 2: Generating video script with Google Gemini...")
    # Use the latest recommended model from Google
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Based on the following news article, create a short, engaging video script of about 3 to 4 sentences.
    The script should be a simple, clear news summary.
    Do not use complex words or markdown like asterisks.
    Start the script directly, without any preamble like "Here is the script:".

    Article Title: {title}
    Article Content Snippet: {content}
    """
    
    try:
        response = model.generate_content(prompt)
        # Clean up the text to remove markdown and extra whitespace
        script = response.text.strip().replace('*', '').replace('`', '')
        print("-> Script generated successfully.")
        return script
    except Exception as e:
        print(f"[ERROR] Failed to generate script from Google Gemini: {e}")
        return None

def generate_audio(script, filename="audio.mp3"):
    """Generates an audio file from the script using Google Text-to-Speech."""
    print("[INFO] Step 3: Generating audio voiceover...")
    try:
        tts = gTTS(text=script, lang='en', slow=False)
        tts.save(filename)
        print(f"-> Audio saved as '{filename}'")
        return filename
    except Exception as e:
        print(f"[ERROR] Failed to generate audio file: {e}")
        return None

def create_video(script, audio_path, output_filename):
    """Creates a video by combining a background VIDEO, text overlay, and audio."""
    print("[INFO] Step 4: Creating video file using MoviePy...")
    background_video_path = "background.mp4" # Use a video file now
    
    if not os.path.exists(background_video_path):
        print(f"[FATAL ERROR] Background video not found! Make sure 'background.mp4' is in the project folder.")
        return

    try:
        # Load the audio to get its duration
        audio_clip = AudioFileClip(audio_path)
        audio_duration = audio_clip.duration + 1 # Add 1 sec padding

        # --- MODIFICATION START ---
        # Load the background video clip
        background_clip = VideoFileClip(background_video_path, audio=False) # audio=False to ignore its original sound

        # Loop the background video to match the audio duration
        looped_background_clip = background_clip.fx(loop, duration=audio_duration)
        # --- MODIFICATION END ---


        # Create the text clip that will be overlaid on the video
        text_clip = TextClip(
            script,
            fontsize=15,
            color='white',
            font='Arial-Bold', # A common font, change if needed
            method='caption', # Automatically wraps text to fit the width
            size=(looped_background_clip.w * 0.8, None), # Text width is 80% of video width
            stroke_color='white',
            stroke_width=2
        )
        
        # Set the position and duration of the text overlay
        text_clip = text_clip.set_position('center').set_duration(audio_duration)

        # Combine (composite) the video clip and text clip
        final_video = CompositeVideoClip([looped_background_clip, text_clip])
        
        # Set the audio for the final video
        final_video.audio = audio_clip
        
        # Write the final video file to disk
        final_video.write_videofile(
            output_filename,
            codec='libx264',
            audio_codec='aac',
            fps=24
        )
        print(f"\n[SUCCESS] Video saved as '{output_filename}'!")

    except Exception as e:
        if "No such file or directory" in str(e) and "convert" in str(e):
             print(f"[FATAL ERROR] MoviePy dependency 'ImageMagick' not found.")
             print("Please install it by running this command in your terminal: brew install imagemagick")
        else:
            print(f"[ERROR] Failed to create video file: {e}")


def main():
    """Main function to orchestrate the video creation pipeline."""
    parser = argparse.ArgumentParser(description="Zero-Cost AI Video Generation Tool")
    parser.add_argument("--topic", type=str, required=True, help="News topic for the video.")
    args = parser.parse_args()
    
    title, content = get_trending_news(args.topic)
    
    if title and content:
        script = generate_script(title, content)
        if script:
            audio_file = generate_audio(script)
            if audio_file:
                # Create a clean filename from the article title
                safe_filename = "".join(x for x in title if x.isalnum() or x in " _-").rstrip()
                output_video_file = f"{safe_filename}.mp4"
                create_video(script, audio_file, output_video_file)

if __name__ == "__main__":
    main()