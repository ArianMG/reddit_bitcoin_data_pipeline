import json
import datetime
from collections import Counter, defaultdict
from kafka import KafkaConsumer
from pymongo import MongoClient
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# --- Define stopwords in English and Spanish --- #
stopwords_es = set(stopwords.words('spanish'))
stopwords_en = set(stopwords.words('english'))
stopwords_total = stopwords_es.union(stopwords_en)

# --- Configuration constants --- #
TOPIC = 'reddit-bitcoin-topic'            # Kafka topic to consume from
MAX_MENSAJES = 1000                       # Max number of messages to process
KAFKA_SERVERS = 'kafka:9092'              # Kafka broker address
MONGO_URI = 'mongodb://mongo:27017/'      # MongoDB connection URI

# --- Initialize Kafka Consumer --- #
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',         # Read from the beginning of the topic
    enable_auto_commit=True,
    consumer_timeout_ms=5000              # Stop after 5 seconds of no new messages
)

# --- Connect to MongoDB --- #
mongo_client = MongoClient(MONGO_URI)
db = mongo_client['reddit_bitcoin']
collection = db['top_words_by_hour']      # Target collection for storing results

# Dictionary to count words per hour
count_by_hour = defaultdict(Counter)

print("Processing Kafka messages...")

message_counter = 0

# --- Consume and process messages from Kafka --- #
for message in consumer:
    data = message.value
    text = f"{data.get('title', '')} {data.get('body', '')}"

    # Extract UTC hour from timestamp (format: YYYY-MM-DD HH:00)
    date_hour = datetime.datetime.utcfromtimestamp(data['timestamp']).strftime('%Y-%m-%d %H:00')

    # Tokenize and clean text
    tokens = word_tokenize(text.lower())
    words = [token for token in tokens if token.isalpha() and token not in stopwords_total]

    # Update word count for the given hour
    count_by_hour[date_hour].update(words)
    message_counter += 1

    if message_counter >= MAX_MENSAJES:
        print("Limit reached, stopping...")
        break

# --- Save results into MongoDB --- #
print("Saving results to MongoDB...")

for date, count in count_by_hour.items():
    top_words = count.most_common(10)
    collection.update_one(
        {"timestamp": date},
        {"$set": {"words": top_words}},
        upsert=True
    )
    print(f"{date} -> {top_words}")

print("Process completed")