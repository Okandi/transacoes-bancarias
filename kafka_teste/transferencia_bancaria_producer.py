from kafka import KafkaProducer
from datetime import datetime
import json

producer = KafkaProducer(bootstrap_servers="localhost:9092", value_serializer=lambda m: json.dumps(m).encode("utf-8"))


info = {
    "tipo": "PIX",
    "origem": {
        "banco": "260",
        "agencia": "0001",
        "conta": "9123"
    },
    "destino": {
        "banco": "380",
        "chave": "exemplo@gmail.com"
    },
    "valor": 514.0,
    "envio": (str(datetime.now()).replace(" ", "T"))[:-7]
}

producer.send("transferencia_bancaria", info).get()
