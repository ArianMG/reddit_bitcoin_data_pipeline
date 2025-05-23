import praw
import json
import os
from kafka import KafkaProducer
from dotenv import load_dotenv

# --- Load environment variables from the .env file located at the project root --- #
load_dotenv()

# --- Number of posts to fetch from Reddit --- #
SUBREDDIT_LIMIT = 100

# --- Initialize Reddit client using credentials from the .env file --- #
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD")
)

# --- Initialize Kafka producer --- #
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# --- Target multiple variations of the Bitcoin subreddit name --- #
subreddit = reddit.subreddit('Bitcoin+bitcoin+BTC+btc+Btc')

# --- Fetch new posts and send them to the Kafka topic --- #
for submission in subreddit.new(limit=SUBREDDIT_LIMIT):
    message = {
        "id": submission.id,
        "title": submission.title,
        "body": submission.selftext,
        "timestamp": submission.created_utc
    }
    producer.send('reddit-bitcoin-topic', message)
    print(f"Sent: {message['title']}")

# --- Ensure all messages are sent before exiting --- #
producer.flush()