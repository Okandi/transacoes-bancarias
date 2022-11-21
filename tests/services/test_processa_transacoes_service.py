import sys
sys.path.append("/home/f45825/Arquivos/Projetos/registro-transacoes/app")
from src.services.processa_transacoes_service import ProcessaTransacoesService
from unittest.mock import MagicMock, patch
from pytest import raises


caminho = "src.services.processa_transacoes_service."


@patch(caminho+"ConsolidadorInfo")
@patch(caminho+"AntiFraudeInfo")
@patch(caminho+"TipoChave")
@patch(caminho+"TipoTransacao")
@patch(caminho+"TransacaoPIX")
@patch(caminho+"TBSender")
@patch(caminho+"TBReceiver")
@patch(caminho+"Brazil")
@patch(caminho+"TBCSVFileWriter")
def test_processa_transacao_ted_valida(mock_csv_writer, mock_calendar, mock_tb_receiver,
                                       mock_tb_sender, mock_transacao_pix, mock_tipo_transacao,
                                       mock_tipo_chave, mock_anti_fraude_info, mock_consolidador_info):
    stub_transacao = MagicMock()
    stub_transacao.envio.hour = 15
    mock_tipo_transacao.TED = stub_transacao.tipo
    stub_chave_valor = stub_transacao.destino_agencia + "|" + stub_transacao.destino_conta
    mock_tb_receiver().get_transferencia_bancaria.side_effect = [
        stub_transacao, Exception("para loop")
    ]
    with raises(Exception) as e:
        ProcessaTransacoesService().processa_transacoes()
    assert e.value.args[0] == "para loop"
    mock_anti_fraude_info.assert_called_once_with(
        stub_transacao.tipo,
        stub_chave_valor,
        mock_tipo_chave.CONTA,
        stub_transacao.valor,
        stub_transacao.envio
    )
    mock_tb_sender().send_to_antifraude.assert_called_once_with(mock_anti_fraude_info())
    mock_consolidador_info.assert_called_once_with(
        stub_transacao.tipo,
        stub_transacao.valor,
        stub_transacao.envio
    )
    mock_csv_writer().save_transacao.assert_called_once_with(mock_consolidador_info())
    mock_tb_sender().send_to_consolidador.assert_called_once_with(mock_consolidador_info())


@patch(caminho+"timedelta")
@patch(caminho+"ConsolidadorInfo")
@patch(caminho+"AntiFraudeInfo")
@patch(caminho+"TipoChave")
@patch(caminho+"TipoTransacao")
@patch(caminho+"TransacaoPIX")
@patch(caminho+"TBSender")
@patch(caminho+"TBReceiver")
@patch(caminho+"Brazil")
@patch(caminho+"TBCSVFileWriter")
def test_processa_transacao_ted_invalida(mock_csv_writer, mock_calendar, mock_tb_receiver,
                                         mock_tb_sender, mock_transacao_pix, mock_tipo_transacao,
                                         mock_tipo_chave, mock_anti_fraude_info, mock_consolidador_info,
                                         mock_timedelta):
    stub_transacao_invalida = MagicMock()
    stub_transacao_tratada = MagicMock()
    mock_tb_receiver().get_transferencia_bancaria.side_effect = [
        stub_transacao_invalida, stub_transacao_tratada, Exception("para loop")
    ]
    stub_transacao_invalida.envio.hour = 16
    stub_transacao_invalida.envio.__iadd__().__iadd__().replace.return_value = stub_transacao_invalida.envio
    mock_calendar().is_working_day.side_effect = [
        True, False, True, True
    ]
    stub_transacao_tratada.envio.hour = 0
    mock_tipo_transacao.TED = stub_transacao_tratada.tipo
    stub_chave_valor = stub_transacao_tratada.destino_agencia + "|" + stub_transacao_tratada.destino_conta
    with raises(Exception) as e:
        ProcessaTransacoesService().processa_transacoes()
    assert e.value.args[0] == "para loop"
    stub_transacao_invalida.envio.__iadd__().__iadd__().replace.assert_called_once()
    mock_tb_sender().send_to_transferencia_bancaria.assert_called_once_with(stub_transacao_invalida)
    mock_anti_fraude_info.assert_called_once_with(
        stub_transacao_tratada.tipo,
        stub_chave_valor,
        mock_tipo_chave.CONTA,
        stub_transacao_tratada.valor,
        stub_transacao_tratada.envio
    )
    mock_tb_sender().send_to_antifraude.assert_called_once_with(mock_anti_fraude_info())
    mock_consolidador_info.assert_called_once_with(
        stub_transacao_tratada.tipo,
        stub_transacao_tratada.valor,
        stub_transacao_tratada.envio
    )
    mock_csv_writer().save_transacao.assert_called_once_with(mock_consolidador_info())
    mock_tb_sender().send_to_consolidador.assert_called_once_with(mock_consolidador_info())


@patch(caminho+"type")
@patch(caminho+"ConsolidadorInfo")
@patch(caminho+"AntiFraudeInfo")
@patch(caminho+"TipoChave")
@patch(caminho+"TipoTransacao")
@patch(caminho+"TransacaoPIX")
@patch(caminho+"TBSender")
@patch(caminho+"TBReceiver")
@patch(caminho+"Brazil")
@patch(caminho+"TBCSVFileWriter")
def test_processa_transacao_pix_cpf(mock_csv_writer, mock_calendar, mock_tb_receiver,
                                    mock_tb_sender, mock_transacao_pix, mock_tipo_transacao,
                                    mock_tipo_chave, mock_anti_fraude_info, mock_consolidador_info,
                                    mock_type):
    stub_transacao_pix = MagicMock()
    stub_transacao_pix.tipo = mock_tipo_transacao.PIX
    mock_tb_receiver().get_transferencia_bancaria.side_effect = [
        stub_transacao_pix, Exception("para loop")
    ]
    mock_type.return_value = mock_transacao_pix
    mock_calendar().is_working_day.return_value = False
    with raises(Exception) as e:
        ProcessaTransacoesService().processa_transacoes()
    assert e.value.args[0] == "para loop"
    mock_anti_fraude_info.assert_called_once_with(
        stub_transacao_pix.tipo,
        stub_transacao_pix.destino_chave,
        mock_tipo_chave.CPF,
        stub_transacao_pix.valor,
        stub_transacao_pix.envio
    )
    mock_tb_sender().send_to_antifraude.assert_called_once_with(mock_anti_fraude_info())
    mock_consolidador_info.assert_called_once_with(
        stub_transacao_pix.tipo,
        stub_transacao_pix.valor,
        stub_transacao_pix.envio
    )
    mock_csv_writer().save_transacao.assert_called_once_with(mock_consolidador_info())
    mock_tb_sender().send_to_consolidador.assert_called_once_with(mock_consolidador_info())
    mock_tb_sender().send_to_transferencia_bancaria.assert_not_called()


@patch(caminho+"type")
@patch(caminho+"ConsolidadorInfo")
@patch(caminho+"AntiFraudeInfo")
@patch(caminho+"TipoChave")
@patch(caminho+"TipoTransacao")
@patch(caminho+"TransacaoPIX")
@patch(caminho+"TBSender")
@patch(caminho+"TBReceiver")
@patch(caminho+"Brazil")
@patch(caminho+"TBCSVFileWriter")
def test_processa_transacao_pix_telefone(mock_csv_writer, mock_calendar, mock_tb_receiver,
                                         mock_tb_sender, mock_transacao_pix, mock_tipo_transacao,
                                         mock_tipo_chave, mock_anti_fraude_info, mock_consolidador_info,
                                         mock_type):
    stub_transacao_pix = MagicMock()
    stub_transacao_pix.tipo = mock_tipo_transacao.PIX
    mock_tb_receiver().get_transferencia_bancaria.side_effect = [
        stub_transacao_pix, Exception("para loop")
    ]
    mock_type.return_value = mock_transacao_pix
    mock_calendar().is_working_day.return_value = False
    stub_transacao_pix.destino_chave = "()"
    with raises(Exception) as e:
        ProcessaTransacoesService().processa_transacoes()
    assert e.value.args[0] == "para loop"
    mock_anti_fraude_info.assert_called_once_with(
        stub_transacao_pix.tipo,
        stub_transacao_pix.destino_chave,
        mock_tipo_chave.TELEFONE,
        stub_transacao_pix.valor,
        stub_transacao_pix.envio
    )
    mock_tb_sender().send_to_antifraude.assert_called_once_with(mock_anti_fraude_info())
    mock_consolidador_info.assert_called_once_with(
        stub_transacao_pix.tipo,
        stub_transacao_pix.valor,
        stub_transacao_pix.envio
    )
    mock_csv_writer().save_transacao.assert_called_once_with(mock_consolidador_info())
    mock_tb_sender().send_to_consolidador.assert_called_once_with(mock_consolidador_info())
    mock_tb_sender().send_to_transferencia_bancaria.assert_not_called()


@patch(caminho+"type")
@patch(caminho+"ConsolidadorInfo")
@patch(caminho+"AntiFraudeInfo")
@patch(caminho+"TipoChave")
@patch(caminho+"TipoTransacao")
@patch(caminho+"TransacaoPIX")
@patch(caminho+"TBSender")
@patch(caminho+"TBReceiver")
@patch(caminho+"Brazil")
@patch(caminho+"TBCSVFileWriter")
def test_processa_transacao_pix_email(mock_csv_writer, mock_calendar, mock_tb_receiver,
                                         mock_tb_sender, mock_transacao_pix, mock_tipo_transacao,
                                         mock_tipo_chave, mock_anti_fraude_info, mock_consolidador_info,
                                         mock_type):
    stub_transacao_pix = MagicMock()
    stub_transacao_pix.tipo = mock_tipo_transacao.PIX
    mock_tb_receiver().get_transferencia_bancaria.side_effect = [
        stub_transacao_pix, Exception("para loop")
    ]
    mock_type.return_value = mock_transacao_pix
    mock_calendar().is_working_day.return_value = False
    stub_transacao_pix.destino_chave = "@"
    with raises(Exception) as e:
        ProcessaTransacoesService().processa_transacoes()
    assert e.value.args[0] == "para loop"
    mock_anti_fraude_info.assert_called_once_with(
        stub_transacao_pix.tipo,
        stub_transacao_pix.destino_chave,
        mock_tipo_chave.EMAIL,
        stub_transacao_pix.valor,
        stub_transacao_pix.envio
    )
    mock_tb_sender().send_to_antifraude.assert_called_once_with(mock_anti_fraude_info())
    mock_consolidador_info.assert_called_once_with(
        stub_transacao_pix.tipo,
        stub_transacao_pix.valor,
        stub_transacao_pix.envio
    )
    mock_csv_writer().save_transacao.assert_called_once_with(mock_consolidador_info())
    mock_tb_sender().send_to_consolidador.assert_called_once_with(mock_consolidador_info())
    mock_tb_sender().send_to_transferencia_bancaria.assert_not_called()
