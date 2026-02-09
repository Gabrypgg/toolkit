from moviepy import VideoFileClip
import os

def convert_video_to_mp3(video_path, output_ext="mp3"):
    """Converts video file to MP3 audio file"""
    try: 
        filename, ext = os.path.splitext(video_path)

        # Load the video clip and extract its audio
        video_clip = VideoFileClip(video_path) #mp4 file
        audio_clip = video_clip.audio

        # Write the audio to a separate file
        audio_clip.write_audiofile(f"{filename}.{output_ext}")
        
        # Close audio and video clips
        video_clip.close()
        audio_clip.close()

        print("Audio extraction successful!")

    except Exception as e:
        print(f"Error: {e}")

# usage
video_file = "video.mov" #"your_video.mp4"  
convert_video_to_mp3(video_file)