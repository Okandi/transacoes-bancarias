from kafka import KafkaConsumer, KafkaProducer
import json


class TBKafkaInfrastructure:
    
    def get_kafka_consumer(self) -> KafkaConsumer:
        return KafkaConsumer("transferencia_bancaria", bootstrap_servers="server", auto_offset_reset="earliest", value_deserializer=lambda m: json.loads(m.decode("utf-8")))

    def get_kafka_producer(self) -> KafkaProducer:
        return KafkaProducer(bootstrap_servers="server", value_serializer=lambda m: json.dumps(m).encode("utf-8"))
