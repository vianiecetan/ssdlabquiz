#!/usr/bin/env sh

set -x

# Run the Docker container with the Python image
docker run -d -p 8000:8000 --name my-python-app -v c:\\Users\\Vianiece\\Desktop\\SSD\\labquiz\\src:/app python:3.9-slim python /app/app.py

sleep 1
set +x

echo 'Now...'
echo 'Visit http://localhost:8000 to see your Python application in action.'
