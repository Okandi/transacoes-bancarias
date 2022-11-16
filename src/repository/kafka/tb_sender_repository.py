from src.infrastructure.kafka.tb_kafka_infrastructure import TBKafkaInfrastructure
from src.core.models.consolidador_info import ConsolidadorInfo
from src.core.models.anti_fraude_info import AntiFraudeInfo
from src.core.interfaces.tb_repositories_interfaces.itb_sender import ITBSender
from src.core.models.transacao import TransacaoTED
from datetime import datetime


class TBSender(ITBSender):

    def __init__(self):
        self._kafka_producer = TBKafkaInfrastructure().get_kafka_producer()
    
    def send_to_transferencia_bancaria(self, info: TransacaoTED) -> None:
        transacao = {
            "tipo": info.tipo.name,
            "origem": {
                "banco": info.origem_banco,
                "agencia": info.origem_agencia,
                "conta": info.origem_conta
            },
            "destino": {
                "banco": info.destino_banco,
                "agencia": info.destino_agencia,
                "conta": info.destino_conta
            },
            "valor": info.valor,
            "envio": self._transforma_data_em_string(info.envio)
        }
        self._kafka_producer.send("transferencia_bancaria", transacao).get()
    
    def send_to_antifraude(self, info: AntiFraudeInfo) -> None:
        transacao = {
            "tipo": info.tipo.name,
            "chave": {
                "valor": info.chave_valor,
                "tipo_chave": info.chave_tipo_chave.name.lower()
            },
            "valor": info.valor,
            "envio": self._transforma_data_em_string(info.envio)
        }
        self._kafka_producer.send("antifraude", transacao).get()
    
    def send_to_consolidador(self, info: ConsolidadorInfo) -> None:
        transacao = {
            "tipo": info.tipo.name,
            "valor": info.valor,
            "envio": self._transforma_data_em_string(info.envio)
        }
        self._kafka_producer.send("consolidador", transacao).get()

    @staticmethod
    def _transforma_data_em_string(data: datetime) -> str:
        return str(data).replace(" ", "T")
