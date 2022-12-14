from kafka import KafkaConsumer
from pprint import pprint
import json

transferencia_bancaria_consumer = KafkaConsumer("transferencia_bancaria",
                                                bootstrap_servers="localhost:9092",
                                                auto_offset_reset="earliest",
                                                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                                                )

for msg in transferencia_bancaria_consumer:
    pprint(msg.value)
