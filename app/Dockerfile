FROM python:3.11-slim

# Set /app as the default working directory inside the container
WORKDIR /app

# Copy all contents from the local `app` directory to the `/app` directory in the container
COPY /app /app

# Copy the .env file from the project root to /app inside the container
COPY ../.env /app/.env

# Install system dependencies
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Download the required NLTK data packages using a Python command.
RUN python -c "import nltk; nltk.download('punkt')"
RUN python -c "import nltk; nltk.download('stopwords')"
RUN python -c "import nltk; nltk.download('punkt_tab')"

# This command keeps the application container running indefinitely
CMD ["sleep", "infinity"]