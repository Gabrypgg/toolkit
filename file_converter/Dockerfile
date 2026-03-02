# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY yt_toolkit ./yt_toolkit
COPY main.py .

# Create output directories
RUN mkdir -p video_mp4 video_mp3 transcriptions

# Make main.py executable
RUN chmod +x main.py

# Command to run the application
# Use -u for unbuffered output to see logs in Docker
ENTRYPOINT ["python", "-u", "main.py"]
