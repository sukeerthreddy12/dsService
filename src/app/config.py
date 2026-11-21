import os

KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "expense_service")
