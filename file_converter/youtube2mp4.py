#pip install pytube
# python youtube2mp4.py -l '<youtube_link>' -o video_mp4/

#from pytube import YouTube #if error use pytubefix
#from pytube.exceptions import VideoUnavailable, RegexMatchError

from pytubefix import YouTube
from pytubefix.cli import on_progress
from pytubefix.exceptions import VideoUnavailable, RegexMatchError
import sys
import argparse
import re

parser = argparse.ArgumentParser(description="A simple argument parser example.")
parser.add_argument("-o", "--saveTo", help="path to save the video", required=True)
parser.add_argument("-l", "--videoLink", help="link to youtube video", required=True)
args = parser.parse_args()

# ####### GENERIC PROGRESS BAR ########
def progress_callback(stream, chunk, bytes_remaining):
    # to show progress bar
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100

    # Print the progress
    sys.stdout.write(f"\rDownloading: {percentage_of_completion:5.1f}%")
    sys.stdout.flush()

def extract_video_id(url):
    """
    Extract the video ID from a YouTube URL.
    """
    # (?:...) is a non-capturing group — it groups the alternatives without capturing them
    # v= matches URLs like: https://www.youtube.com/watch?v=VIDEO_ID
    # youtu\.be/ matches shortened URLs like: https://youtu.be/VIDEO_ID
    # | means “or”
    # ([a-zA-Z0-9_-]{11}) is a capturing group — it matches and saves the actual YouTube video ID
    # [a-zA-Z0-9_-] means it matches any letter (upper/lower), digit, underscore _, or dash -
    # {11} means it matches exactly 11 characters — which is the standard length of a YouTube video ID

    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None

def download_youtube_video(url, save_path):
    video_id = extract_video_id(video_url)
    if not video_id:
        print("❌ Error: Invalid YouTube URL.")
        return
    try:
        youtube_link = f"https://www.youtube.com/watch?v={video_id}"
        yt = YouTube(youtube_link, on_progress_callback=on_progress) # or on_progress_callback = progress_callback
        print(f"Downloading: {yt.title}")
        stream = yt.streams.filter(file_extension='mp4', progressive=True).get_highest_resolution()
        print("Starting download...")
        stream.download(output_path=save_path)
        print("Download completed!")
    except VideoUnavailable:
        print("Error: The video is unavailable.")
    except RegexMatchError:
        print("Error: The URL format is invalid.")
    except Exception as e:
        print("Error:", e)

# Example usage
video_url = args.videoLink  # Desired video URL
save_path = args.saveTo
download_youtube_video(video_url, save_path)
