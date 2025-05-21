# 📊 Bitcoin Reddit Pipeline with Kafka, MongoDB & Airflow

This project builds a complete data pipeline for collecting Reddit posts about **Bitcoin**,
streaming them through **Kafka**, processing word frequency with **Python**, and storing results in **MongoDB**,
all orchestrated via **Apache Airflow**, and deployed in **Docker** containers.

## 📁 Project Structure
```
reddit_bitcoin_data_pipeline/
├── README.md
├── docker-compose.yml
├── .env
├── airflow/
│   ├── dags/
│   │   └── reddit_dag.py
│   ├── logs/...
│   ├── Dockerfile
│   └── requirements.txt
├── app/
│   ├── producer.py
│   ├── consumer.py
│   ├── .env
│   ├── Dockerfile
│   └── requirements.txt
```

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/ArianMG/reddit_bitcoin_data_pipeline.git
cd reddit_bitcoin_data_pipeline
```

### 2. Create `.env` file in root directory for docker compose
This file will be used to configure PostgreSQL, MongoDB, and Airflow.
```env
# .env
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgres_password
POSTGRES_DB=postgres_db

MONGO_INITDB_ROOT_USERNAME=mongo_user
MONGO_INITDB_ROOT_PASSWORD=mongo_password

AIRFLOW_USER=airflow_user
AIRFLOW_PASSWORD=airflow_password
AIRFLOW_EMAIL=airflow_email
```

### 3. Create Reddit API Credentials in `.env`
Create a file named `.env` inside the `app/` folder with the following content:
```env
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USER_AGENT=your_user_agent
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password
```
These will be automatically loaded into the producer.

### 3. Run the stack
```bash
docker compose up -d --build
```

### 4. Access Airflow
Open [http://localhost:8080](http://localhost:8080) in your browser.
- User: from `.env` → `AIRFLOW_USER`
- Password: from `.env` → `AIRFLOW_PASSWORD`

### 5. Access Mongo Express
Open [http://localhost:8081](http://localhost:8081) to explore MongoDB collections.
- User: from `.env` → `MONGO_INITDB_ROOT_USERNAME`
- Password: from `.env` → `MONGO_INITDB_ROOT_PASSWORD`

## 📦 Components Overview

- **Producer (`producer.py`)**: Collects Reddit posts from multiple subreddits related to Bitcoin, including: r/Bitcoin, r/bitcoin, r/BTC, r/btc, and r/Btc and sends them to Kafka.
- **Kafka**: Receives and buffers messages.
- **Consumer (`consumer.py`)**: Reads from Kafka, filters text, counts word frequency, and stores results in MongoDB.
- **MongoDB**: Stores top 10 most used words by date.
- **Airflow DAG (`reddit_dag.py`)**: Automates the producer and consumer tasks.

## ⚙️ Permissions & Setup Notes
- Ensure `airflow/logs` and `app/` directories exist and are mounted correctly.
- Give proper write permissions to logs:
```bash
sudo chown -R 50000:0 airflow/logs
```

## 🧰 Common Docker Commands
- Start services: `docker compose up -d --build`
- View logs: `docker compose logs -f airflow`
- Access Airflow container: `docker compose exec airflow bash`
- Test producer manually: `docker compose exec app python producer.py`
- Test consumer manually: `docker compose exec app python consumer_batch.py`
- List Kafka topics:
  ```bash
  docker compose exec kafka /usr/bin/kafka-topics --list --bootstrap-server kafka:9092
  ```
- Read messages from topic:
  ```bash
  docker compose exec kafka /usr/bin/kafka-console-consumer --topic reddit-bitcoin-topic --from-beginning --bootstrap-server kafka:9092
  ```

## 🧪 Testing DAG Execution
1. Open Airflow UI and unpause `reddit_bitcoin_pipeline` DAG.
2. Click ▶️ to trigger manually.
3. Verify task success and MongoDB data via Mongo Express or Compass.

## 📈 Example Output in MongoDB
```json
{
  "fecha": "2025-05-20T15:42:00",
  "palabras": [["bitcoin", 21], ["btc", 14], ["price", 9]]
}
```

---
© 2025 — Built for Bitcoin sentiment analysis using open tools.