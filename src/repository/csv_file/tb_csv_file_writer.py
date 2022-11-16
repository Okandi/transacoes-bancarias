from src.infrastructure.csv_file.tb_csv_file_infrastructure import TBCSVFileInfrastructure
from src.core.interfaces.csv_file_interface.itb_csv_file_writer import ITBCSVFileWriter
from src.core.models.consolidador_info import ConsolidadorInfo
import json


class TBCSVFileWriter(ITBCSVFileWriter):
    
    def __init__(self) -> None:
        self._csv_file = TBCSVFileInfrastructure()

    def save_transacao(self, info: ConsolidadorInfo) -> None:
        transacao = {
            "tipo": info.tipo.name,
            "valor": info.valor,
            "envio": str(info.envio)
        }
        with self._csv_file.get_file_access() as file:
            file.write(json.dumps(transacao))
            file.write("\n")
