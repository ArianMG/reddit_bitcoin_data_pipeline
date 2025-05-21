import os
from dotenv import load_dotenv
import praw
from kafka import KafkaProducer
import json

load_dotenv()

SUBREDDIT_LIMIT = 100

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD")
)

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

subreddit = reddit.subreddit('Bitcoin+bitcoin+BTC+btc+Btc')
for submission in subreddit.new(limit=SUBREDDIT_LIMIT):
    mensaje = {
        "id": submission.id,
        "titulo": submission.title,
        "texto": submission.selftext,
        "fecha": submission.created_utc
    }
    producer.send('reddit-bitcoin-topic', mensaje)
    print(f"Mensaje enviado: {mensaje['id']}")

producer.flush()