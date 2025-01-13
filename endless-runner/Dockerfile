# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install dependencies for Pygame and Xvfb
RUN apt-get update && apt-get install -y \
    xvfb \
    python3-pygame \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the Pygame script using xvfb-run
CMD ["xvfb-run", "--auto-servernum", "--server-args='-screen 0 800x600x24'", "python", "endless-runner.py"]