from pytubefix import YouTube
from pytubefix.cli import on_progress
from pytubefix.exceptions import VideoUnavailable, RegexMatchError
import os
from .utils import extract_video_id, sanitize_filename

def download_video(url, output_path="video_mp4"):
    """
    Downloads a YouTube video in MP4 format.
    """
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL.")

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    try:
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}", on_progress_callback=on_progress)
        print(f"Downloading Video: {yt.title}")
        
        stream = yt.streams.filter(file_extension='mp4', progressive=True).get_highest_resolution()
        if not stream:
            raise Exception("No suitable MP4 stream found.")
            
        stream.download(output_path=output_path)
        print(f"\nDownload completed: {os.path.join(output_path, stream.default_filename)}")
        return os.path.join(output_path, sanitize_filename(stream.default_filename))
        
    except (VideoUnavailable, RegexMatchError) as e:
        raise Exception(f"YouTube Error: {str(e)}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}")

def download_audio(url, output_path="video_mp3"):
    """
    Downloads matching YouTube audio and saves as MP3.
    """
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL.")

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    try:
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}", on_progress_callback=on_progress)
        print(f"Downloading Audio: {yt.title}")
        
        # Get the best audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()
        if not audio_stream:
            raise Exception("No audio stream found.")

        # Download it
        out_file = audio_stream.download(output_path=output_path)
        
        # Rename to .mp3
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        
        # If the file already exists, we might need to remove it or rename it
        if os.path.exists(new_file):
            os.remove(new_file)
            
        os.rename(out_file, new_file)
        
        print(f"\nAudio extraction completed: {new_file}")
        return new_file
        
    except (VideoUnavailable, RegexMatchError) as e:
        raise Exception(f"YouTube Error: {str(e)}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}")
