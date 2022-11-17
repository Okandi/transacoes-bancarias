from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers="localhost:9092", value_serializer=lambda m: json.dumps(m).encode("utf-8"))


info = {
    "tipo": "TED",
    "origem": {
        "banco": "260",
        "agencia": "0001",
        "conta": "9123"
    },
    "destino": {
        "banco": "380",
        "agencia": "0021",
        "conta": "123"
    },
    "valor": 1000.0,
    "envio": "2022-10-02T15:30:01"
}

producer.send("transferencia_bancaria", info).get()
