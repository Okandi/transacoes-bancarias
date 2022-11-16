from kafka import KafkaConsumer
from pprint import pprint
import json

antifraude_consumer = KafkaConsumer("antifraude",
                                    bootstrap_servers="server",
                                    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
                                    )

for msg in antifraude_consumer:
    pprint(msg.value)
