import sys
sys.path.append("/home/f45825/Arquivos/Projetos/registro-transacoes/app")
from src.repository.csv_file.tb_csv_file_writer import TBCSVFileWriter
from unittest.mock import MagicMock, patch, call


caminho = "src.repository.csv_file.tb_csv_file_writer."


@patch(caminho+"TBCSVFileInfrastructure")
def test_save_transacao(mock_file_connection):
    mock_file = mock_file_connection().get_file_access()
    stub_info = MagicMock()
    TBCSVFileWriter().save_transacao(stub_info)
    stub_transacao = f"{stub_info.tipo.name},{stub_info.valor},{str(stub_info.envio)}"
    assert mock_file.__enter__().write.call_args_list == [call("\n"), call(stub_transacao)]
