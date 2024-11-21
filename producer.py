# producer.py

import time
import psutil
from kafka import KafkaProducer
from prometheus_client import start_http_server, Counter, Gauge
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Prometheus metrics
MESSAGES_SENT = Counter('kafka_producer_messages_sent_total', 'Total number of messages sent by the producer')
MEMORY_USAGE = Gauge('app_memory_usage', 'Current memory usage in MB')

def get_memory_usage():
    process = psutil.Process()
    mem = process.memory_info().rss / (1024 * 1024)  # Convert bytes to MB
    MEMORY_USAGE.set(mem)

def main():
    # Start Prometheus metrics server
    start_http_server(8000)
    logging.info("Producer metrics server started on port 8000")

    # Initialize Kafka producer with updated bootstrap_servers
    producer = KafkaProducer(bootstrap_servers='kafka_b:9092')
    logging.info("Kafka Producer initialized")

    total_messages = 10
    try:
        for message_number in range(total_messages):
            message = f"Message {message_number}".encode('utf-8')
            producer.send('test-topic', message)
            producer.flush()
            MESSAGES_SENT.inc()
            get_memory_usage()
            logging.info(f"Produced: {message.decode('utf-8')}")
            time.sleep(1)  # Optional: Pause for a second between messages

        logging.info(f"Produced {total_messages} messages. Stopping message production.")

        # Keep the script running to allow Prometheus to scrape metrics
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        logging.info("Producer stopped by user.")
    finally:
        producer.close()
        logging.info("Kafka Producer closed.")

if __name__ == "__main__":
    main()
