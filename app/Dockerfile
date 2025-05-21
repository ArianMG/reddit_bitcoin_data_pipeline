FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y curl && \
    pip install --upgrade pip && pip install -r requirements.txt && \
    python -m nltk.downloader punkt

CMD ["sleep", "infinity"]
