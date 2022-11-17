from kafka import KafkaConsumer, KafkaProducer
import json


class TBKafkaInfrastructure:
    
    _kafka_consumer = None
    _kafka_producer = None
    
    @classmethod
    def get_kafka_consumer(cls) -> KafkaConsumer:
        if cls._kafka_consumer is None:
            cls._kafka_consumer = KafkaConsumer("transferencia_bancaria", bootstrap_servers="localhost:9092", auto_offset_reset="earliest", value_deserializer=lambda m: json.loads(m.decode("utf-8")))
        return cls._kafka_consumer

    @classmethod
    def get_kafka_producer(cls) -> KafkaProducer:
        if cls._kafka_producer is None:
            cls._kafka_producer = KafkaProducer(bootstrap_servers="localhost:9092", value_serializer=lambda m: json.dumps(m).encode("utf-8"))
        return cls._kafka_producer
