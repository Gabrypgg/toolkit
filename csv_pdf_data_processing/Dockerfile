# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python scripts
COPY pdf2csv.py .
COPY clean.py .
COPY plot.py .

# Copy your data folder into the container's /app/data/ directory
# This assumes your CSV file is in a local folder named 'data'
COPY data/ ./data/

# Run clean_csv.py when the container launches
CMD ["python", "clean_csv.py"]