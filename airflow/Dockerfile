FROM apache/airflow:2.8.1-python3.11

# Cambiar a root para instalar paquetes del sistema
USER root

# Instalar dependencias del sistema (si necesitas curl u otras)
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Cambiar de nuevo a airflow
USER airflow

# Instalar dependencias Python
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Descargar recursos NLTK si es necesario
RUN python -m nltk.downloader punkt stopwords
