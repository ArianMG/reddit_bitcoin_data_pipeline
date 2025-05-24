FROM apache/airflow:2.8.1-python3.11

# Switch to root user to install system packages
USER root

# Install system dependencies
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch back to the Airflow user, which is the default for Airflow
USER airflow

# Copy the .env file from the project root to /app inside the container
COPY ../.env /app/.env

# Install Python dependencies
COPY airflow/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Download the required NLTK data packages using a Python command.
RUN python -c "import nltk; nltk.download('punkt')"
RUN python -c "import nltk; nltk.download('stopwords')"
RUN python -c "import nltk; nltk.download('punkt_tab')"