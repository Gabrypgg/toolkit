# pip install youtube-transcript-api
# python youtubeTranscriber.py -l "<youtube_link>" -lang "en" -o youtube_transcriptions

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
#from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptAvailable
from pytubefix import YouTube
import argparse
import re

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

def fetch_transcript(video_url, language, save_path):
    video_id = extract_video_id(video_url)
    if not video_id:
        print("❌ Error: Invalid YouTube URL.")
        return

    try:
        #OPTION 1: print in command line
        #transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        #for entry in transcript:
        #    print(f"{entry['start']:.2f}s: {entry['text']}")

        #OPTION 2: save json file
        transcript = YouTubeTranscriptApi().fetch(video_id, languages=[language])
        #print(transcript)
        formatter = JSONFormatter()
        # .format_transcript(transcript) turns the transcript into a JSON string.
        json_formatted = formatter.format_transcript(transcript)
        # Now we can write it out to a file.
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        #save file as tile - language .json
        title = yt.title
        with open(f'{save_path}/{title} - {transcript.language}.json', 'w', encoding='utf-8') as json_file:
            json_file.write(json_formatted)

    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch YouTube video transcription.")
    parser.add_argument("-l", "--link", help="YouTube video URL", required=True)
    parser.add_argument("-lang", "--language", help="Language code, possible values: it, en, fr, es,.....", required=True)
    parser.add_argument("-o", "--saveTo", help="path to save the video", required=True)
    args = parser.parse_args()

    fetch_transcript(args.link, args.language, args.saveTo)