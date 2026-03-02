from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from pytubefix import YouTube
import os
import re
import json
from .utils import extract_video_id, sanitize_filename


def get_transcript(video_url, language='en', text_only=False, output_path='transcriptions'):
    """
    Downloads a YouTube video transcription in txt/JSON format.
    """
    video_id = extract_video_id(video_url)
    if not video_id:
        raise ValueError("Invalid YouTube URL.")

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    try:
        transcript = YouTubeTranscriptApi().fetch(video_id, languages=[language])
        formatter = JSONFormatter()
        # .format_transcript(transcript) turns the transcript into a JSON string.
        json_formatted = formatter.format_transcript(transcript)
        if text_only:
            # considering only text without minutes
            data = json.loads(json_formatted)
            text_list = [item['text'] for item in data]
            json_text_only = " ".join(text_list)
            # Now we can write it out to a file.
            yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
            #save file as tile - language .txt
            title = sanitize_filename(yt.title)
            with open(f'{output_path}/{title} - {transcript.language}.txt', 'w', encoding='utf-8') as json_file:
                json_file.write(json_text_only)
        else:
            # Now we can write it out to a file.
            yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
            #save file as tile - language .json
            title = sanitize_filename(yt.title)
            with open(f'{output_path}/{title} - {transcript.language}.json', 'w', encoding='utf-8') as json_file:
                json_file.write(json_formatted)

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
