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

    extraer_reddit = BashOperator(
        task_id="extraer_desde_reddit",
        bash_command="python /app/producer.py"
    )

    procesar_palabras = BashOperator(
        task_id="procesar_y_guardar_palabras",
        bash_command="python /app/consumer.py"
    )

    extraer_reddit >> procesar_palabras
