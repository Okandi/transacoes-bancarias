import sys
sys.path.append("/home/f45825/Arquivos/Projetos/registro-transacoes/app")
from src.repository.kafka.tb_sender_repository import TBSender
from unittest.mock import MagicMock, patch


caminho = "src.repository.kafka.tb_sender_repository."
stub_info = MagicMock()


@patch(caminho+"TBKafkaInfrastructure")
def test_send_to_transferencia_bancaria(mock_kafka_infrastructure):
    mock_kafka_producer = mock_kafka_infrastructure().get_kafka_producer()
    stub_transacao = {
        "tipo": stub_info.tipo.name,
        "origem": {
            "banco": stub_info.origem_banco,
            "agencia": stub_info.origem_agencia,
            "conta": stub_info.origem_conta
        },
        "destino": {
            "banco": stub_info.destino_banco,
            "agencia": stub_info.destino_agencia,
            "conta": stub_info.destino_conta
        },
        "valor": stub_info.valor,
        "envio": str(stub_info.envio).replace(" ", "T")
    }
    TBSender().send_to_transferencia_bancaria(stub_info)
    mock_kafka_producer.send.assert_called_once_with(
        "transferencia_bancaria", stub_transacao
    )
    mock_kafka_producer.send().get.assert_called_once_with()


@patch(caminho+"TBKafkaInfrastructure")
def test_send_to_antifraude(mock_kafka_infrastructure):
    mock_kafka_producer = mock_kafka_infrastructure().get_kafka_producer()
    stub_transacao = {
        "tipo": stub_info.tipo.name,
        "chave": {
            "valor": stub_info.chave_valor,
            "tipo_chave": stub_info.chave_tipo_chave.name.lower()
        },
        "valor": stub_info.valor,
        "envio": str(stub_info.envio).replace(" ", "T")
    }
    TBSender().send_to_antifraude(stub_info)
    mock_kafka_producer.send.assert_called_once_with(
        "antifraude", stub_transacao
    )
    mock_kafka_producer.send().get.assert_called_once_with()


@patch(caminho+"TBKafkaInfrastructure")
def test_send_to_consolidador(mock_kafka_infrastructure):
    mock_kafka_producer = mock_kafka_infrastructure().get_kafka_producer()
    stub_transacao = {
        "tipo": stub_info.tipo.name,
        "valor": stub_info.valor,
        "envio": str(stub_info.envio).replace(" ", "T")
    }
    TBSender().send_to_consolidador(stub_info)
    mock_kafka_producer.send.assert_called_once_with(
        "consolidador", stub_transacao
    )
    mock_kafka_producer.send().get.assert_called_once_with()
