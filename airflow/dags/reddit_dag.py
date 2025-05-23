from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "start_date": datetime(2024, 1, 1),
}

with DAG(
    dag_id="reddit_bitcoin_pipeline",
    schedule="@hourly",
    default_args=default_args,
    catchup=False
) as dag:

    extract = BashOperator(
        task_id="extract_from_reddit",
        bash_command="python /app/producer.py"
    )

    process = BashOperator(
        task_id="process_and_store_words",
        bash_command="python /app/consumer.py"
    )

    extract >> process
