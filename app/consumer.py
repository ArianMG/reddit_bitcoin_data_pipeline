from kafka import KafkaConsumer
from pymongo import MongoClient
from collections import Counter, defaultdict
import json
import nltk
import datetime
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

stopwords_es = set(stopwords.words('spanish'))
stopwords_en = set(stopwords.words('english'))
stopwords_total = stopwords_es.union(stopwords_en)

# --- Configuración general ---
TOPIC = 'reddit-bitcoin-topic'
MAX_MENSAJES = 1000
KAFKA_SERVERS = 'kafka:9092'
MONGO_URI = 'mongodb://mongo:27017/'

# Kafka consumer config
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    consumer_timeout_ms=5000
)

# MongoDB config
mongo_client = MongoClient(MONGO_URI)
db = mongo_client['reddit_bitcoin']
coleccion = db['palabras_mas_mencionadas_por_hora']

# Procesamiento
conteo_por_hora = defaultdict(Counter)

print("📥 Procesando mensajes de Kafka...")

contador_mensajes = 0

for mensaje in consumer:
    data = mensaje.value
    texto = f"{data.get('titulo', '')} {data.get('texto', '')}"

    fecha_hora = datetime.datetime.utcfromtimestamp(data['fecha']).strftime('%Y-%m-%d %H:00')

    tokens = word_tokenize(texto.lower())
    palabras = [token for token in tokens if token.isalpha() and token not in stopwords_total]

    if fecha_hora not in conteo_por_hora:
        conteo_por_hora[fecha_hora] = Counter()

    conteo_por_hora[fecha_hora].update(palabras)
    contador_mensajes += 1

    if contador_mensajes >= MAX_MENSAJES:
        print("📦 Límite alcanzado, deteniendo...")
        break

# --- Guardar resultados en MongoDB ---
print("💾 Guardando resultados en MongoDB...")

for fecha_hora, contador in conteo_por_hora.items():
    top_palabras = contador.most_common(10)
    coleccion.update_one(
        {"fecha": fecha_hora},
        {"$set": {"palabras": top_palabras}},
        upsert=True
    )
    print(f"✅ {fecha_hora} -> {top_palabras}")

print("🏁 Proceso completado.")