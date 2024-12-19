from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic
from flask import Flask, request, jsonify
import json
import threading
from datetime import datetime

KAFKA_BROKER = 'localhost:9092'
INPUT_TOPIC = 'input-topic'
OUTPUT_TOPIC = 'output-topic'
DLQ_TOPIC = 'dead-letter-topic'
GROUP_ID = 'stream-group'

producer = Producer({'bootstrap.servers': KAFKA_BROKER})


def delivery_report(err, msg):
    """Обработка результата доставки сообщений"""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def ensure_topic_exists(topic_name):
    """Создаёт тему, если она не существует"""
    admin_client = AdminClient({'bootstrap.servers': KAFKA_BROKER})
    topics = admin_client.list_topics(timeout=10).topics

    if topic_name not in topics:
        print(f"Creating topic '{topic_name}'...")
        new_topic = NewTopic(topic_name, num_partitions=3,
                             replication_factor=1)  # 3 партиции для масштабирования
        admin_client.create_topics([new_topic])


# Убедимся, что темы существуют
ensure_topic_exists(INPUT_TOPIC)
ensure_topic_exists(OUTPUT_TOPIC)
ensure_topic_exists(DLQ_TOPIC)

app = Flask(__name__)


@app.route('/send', methods=['POST'])
def send_message():
    """Эндпоинт для отправки сообщений в Kafka"""
    try:
        message = request.json.get('message')
        if not message:
            return jsonify({'error': 'Message is required'}), 400

        producer.produce(INPUT_TOPIC, value=json.dumps(
            message), callback=delivery_report)
        producer.flush()

        return jsonify({'status': 'Message sent successfully'})
    except Exception as e:
        print(f"Producer error: {e}")
        return jsonify({'error': str(e)}), 500


def stream_processing(consumer_id):
    """Обрабатывает сообщения из одной темы и отправляет их в другую"""
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': GROUP_ID,
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe([INPUT_TOPIC])

    try:
        print(f"Starting stream processor (Consumer {consumer_id})...")
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Consumer error: {msg.error()}")
                    raise KafkaException(msg.error())

            try:
                original_message = json.loads(msg.value().decode('utf-8'))
                print(
                    f"[Consumer {consumer_id}] Received message: {original_message}")

                # Преобразование сообщения
                transformed_message = {
                    'original': '123',
                    'processed_at': datetime.utcnow().isoformat(),
                    'status': 'processed'
                }

                producer.produce(OUTPUT_TOPIC, value=json.dumps(
                    transformed_message), callback=delivery_report)
                producer.flush()

            except Exception as e:
                print(
                    f"[Consumer {consumer_id}] Error processing message: {e}")
                dlq_message = {
                    'original_message': msg.value().decode('utf-8'),
                    'error': str(e),
                    'failed_at': datetime.utcnow().isoformat()
                }
                producer.produce(DLQ_TOPIC, value=json.dumps(dlq_message))
                producer.flush()

    except Exception as e:
        print(f"Stream processing error (Consumer {consumer_id}): {e}")
    finally:
        consumer.close()


if __name__ == '__main__':
    num_consumers = 3
    for i in range(num_consumers):
        threading.Thread(target=stream_processing,
                        args=(i,), daemon=True).start()

    # Запуск Flask API
    app.run(host='0.0.0.0', port=8080)
