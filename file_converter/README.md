# YouTube Toolkit

A robust CLI tool and containerized application for downloading YouTube videos, audio, and transcriptions.

## Features

- **Download Video**: Save YouTube videos as MP4 in high resolution.
- **Download Audio**: Extract and save audio from YouTube videos as MP3.
- **Fetch Transcriptions**: Obtain video transcriptions in JSON or txt format.
- **Interactive CLI**: Easy-to-use menu-driven interface.
- **Docker Ready**: Fully containerized for isolated execution.

## Installation

### Local Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd file_converter
    ```

2.  **Install dependencies**:
    We recommend using a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    pip install -r requirements.txt
    ```

3.  **System Dependencies**:
    The toolkit requires `ffmpeg` for audio conversion. Install it using your package manager:
    - **macOS**: `brew install ffmpeg`
    - **Ubuntu/Debian**: `sudo apt install ffmpeg`

## Usage

### Interactive Mode
Simply run the main script without arguments to launch the interactive menu:
```bash
python main.py
```

### Command Line Interface
You can also use subcommands for direct actions:

- **Download Video**:
  ```bash
  python main.py video -l "<youtube-url>" -o video_mp4
  ```

- **Download Audio**:
  ```bash
  python main.py audio -l "<youtube-url>" -o video_mp3
  ```

- **Fetch Transcription**:
  ```bash
  python main.py transcribe -l "<youtube-url>" -lang "it" -o transcriptions
  ```

## Docker Usage

The easiest way to run the toolkit without installing dependencies locally is via Docker.

1.  **Build and Run**:
    ```bash
    docker-compose run --rm yt-toolkit
    ```
    This will launch the interactive menu inside the container.

2.  **Persistent Storage**:
    Downloads are automatically mapped to your local machine:
    - `./video_mp4` -> Videos
    - `./video_mp3` -> Audio
    - `./transcriptions` -> Transcriptions

## Project Structure

- `yt_toolkit/`: Core package containing modular logic.
  - `downloader.py`: Handles video and audio downloads.
  - `transcriber.py`: Handles transcription fetching.
  - `cli.py`: Command-line interface and interactive menu.
  - `utils.py`: Shared utilities.
- `main.py`: Entry point for the application.
- `Dockerfile` & `docker-compose.yml`: Containerization logic.
- `requirements.txt`: Python dependencies.
