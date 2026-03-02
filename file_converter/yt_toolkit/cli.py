import argparse
import sys
from .downloader import download_video, download_audio
from .transcriber import get_transcript

def interactive_menu():
    """
    Launch an interactive menu for the user.
    """
    print("\n--- YouTube Toolkit ---")
    print("1. Download Video (MP4)")
    print("2. Download Audio (MP3)")
    print("3. Get Transcription (JSON)")
    print("4. Exit")
    
    choice = input("\nSelect an option (1-4): ")
    
    if choice == '4' or not choice:
        print("Exiting...")
        return

    url = input("Enter YouTube URL: ")
    if not url:
        print("URL is required.")
        return

    try:
        if choice == '1':
            download_video(url, output_path="video_mp4")
        elif choice == '2':
            download_audio(url, output_path="video_mp3")
        elif choice == '3':
            lang = input("Enter language code (default 'en'): ") or 'en'
            only_text = input("Text only? (y/n, default n): ").lower() == 'y'
            get_transcript(url, language=lang, text_only=only_text, output_path="transcriptions")
        else:
            print("Invalid choice.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="YouTube Toolkit CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Video command
    video_parser = subparsers.add_parser("video", help="Download a video as MP4")
    video_parser.add_argument("-l", "--link", required=True, help="YouTube video URL")
    video_parser.add_argument("-o", "--output", default="video_mp4", help="Output directory")

    # Audio command
    audio_parser = subparsers.add_parser("audio", help="Download audio as MP3")
    audio_parser.add_argument("-l", "--link", required=True, help="YouTube video URL")
    audio_parser.add_argument("-o", "--output", default="video_mp3", help="Output directory")

    # Transcribe command
    transcribe_parser = subparsers.add_parser("transcribe", help="Fetch video transcription")
    transcribe_parser.add_argument("-l", "--link", required=True, help="YouTube video URL")
    transcribe_parser.add_argument("-lang", "--language", default="en", help="Language code (e.g., en, it)")
    transcribe_parser.add_argument("-o", "--output", default="transcriptions", help="Output directory")
    transcribe_parser.add_argument("--full", default=False, help="Save full JSON with timestamps or text only")
    args = parser.parse_args()

    if args.command is None:
        interactive_menu()
    else:
        try:
            if args.command == "video":
                download_video(args.link, args.output)
            elif args.command == "audio":
                download_audio(args.link, args.output)
            elif args.command == "transcribe":
                get_transcript(args.link, args.language, args.full, args.output)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
