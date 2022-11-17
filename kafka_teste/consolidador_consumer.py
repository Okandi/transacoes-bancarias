from kafka import KafkaConsumer
from pprint import pprint
import json

consolidador_consumer = KafkaConsumer("consolidador",
                                      bootstrap_servers="localhost:9092",
                                      value_deserializer=lambda m: json.loads(m.decode("utf-8"))
                                      )

for msg in consolidador_consumer:
    pprint(msg.value)
