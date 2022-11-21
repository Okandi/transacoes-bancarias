import sys
sys.path.append("/home/f45825/Arquivos/Projetos/registro-transacoes/app")
from src.repository.kafka.tb_receiver_repository import TBReceiver
from unittest.mock import MagicMock, patch


caminho = "src.repository.kafka.tb_receiver_repository."


@patch(caminho+"datetime")
@patch(caminho+"TransacaoTED")
@patch(caminho+"TipoTransacao")
@patch(caminho+"TBKafkaInfrastructure")
def test_cria_transacao_ted(mock_kafka_infrastructure, mock_tipo_transacao,
                            mock_transacao_ted, mock_datetime):
    stub_transacao = mock_kafka_infrastructure().get_kafka_consumer().__next__().value
    stub_tipo = MagicMock()
    stub_transacao.__getitem__.return_value = stub_tipo
    mock_tipo_transacao.TED.name = stub_tipo
    response = TBReceiver().get_transferencia_bancaria()
    assert response == mock_transacao_ted()
    mock_datetime.strptime.assert_called_once_with(
        str(stub_transacao.__getitem__()),
        "%Y-%m-%dT%H:%M:%S"
    )


@patch(caminho+"datetime")
@patch(caminho+"TransacaoPIX")
@patch(caminho+"TipoTransacao")
@patch(caminho+"TBKafkaInfrastructure")
def test_cria_transacao_pix(mock_kafka_infrastructure, mock_tipo_transacao,
                            mock_transacao_pix, mock_datetime):
    stub_transacao = mock_kafka_infrastructure().get_kafka_consumer().__next__().value
    stub_tipo = MagicMock()
    stub_transacao.__getitem__.return_value = stub_tipo
    mock_tipo_transacao.PIX.name = stub_tipo
    response = TBReceiver().get_transferencia_bancaria()
    assert response == mock_transacao_pix()
    mock_datetime.strptime.assert_called_once_with(
        str(stub_transacao.__getitem__()),
        "%Y-%m-%dT%H:%M:%S"
    )


@patch(caminho+"datetime")
@patch(caminho+"print")
@patch(caminho+"TransacaoTED")
@patch(caminho+"TipoTransacao")
@patch(caminho+"TBKafkaInfrastructure")
def test_transacao_tipo_errado(mock_kafka_infrastructure, mock_tipo_transacao,
                               mock_transacao_ted, mock_print, fake_datetime):
    stub_transacao1 = MagicMock()
    stub_transacao2 = MagicMock()
    mock_kafka_infrastructure().get_kafka_consumer().__next__.side_effect = [
        stub_transacao1, stub_transacao2
    ]
    mock_tipo_transacao.TED.name = stub_transacao2.value.__getitem__()
    response = TBReceiver().get_transferencia_bancaria()
    assert response == mock_transacao_ted()
    mock_print.assert_called_once_with(
        f"Tipo da transação inválida: {stub_transacao1.value.__getitem__()}"
    )


@patch(caminho+"datetime")
@patch(caminho+"print")
@patch(caminho+"TransacaoTED")
@patch(caminho+"TipoTransacao")
@patch(caminho+"TBKafkaInfrastructure")
def test_transacao_campo_errado(mock_kafka_infrastructure, mock_tipo_transacao,
                               mock_transacao_ted, mock_print, fake_datetime):
    stub_transacao1 = MagicMock()
    stub_transacao2 = MagicMock()
    stub_transacao1.value = {}
    mock_kafka_infrastructure().get_kafka_consumer().__next__.side_effect = [
        stub_transacao1, stub_transacao2
    ]
    mock_tipo_transacao.TED.name = stub_transacao2.value.__getitem__()
    response = TBReceiver().get_transferencia_bancaria()
    assert response == mock_transacao_ted()
    mock_print.assert_called_once_with(
        "Transação inválida: campo 'tipo' não existe"
    )
