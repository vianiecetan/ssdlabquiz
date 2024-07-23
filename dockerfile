FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install Git
RUN apt-get update && apt-get install -y git

# Configure Git user and email
RUN git config --global user.name "vianiece_tan_yingqi" \
    && git config --global user.email "2202045@sit.singaporetech.edu.sg"

# Copy requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest

# Copy the rest of the application code
COPY . .

# Expose the application port
EXPOSE 8000

# Set the default command to run the application
CMD ["python", "app.py"]
