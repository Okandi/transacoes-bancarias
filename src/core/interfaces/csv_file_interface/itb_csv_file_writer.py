from src.core.models.consolidador_info import ConsolidadorInfo
from abc import ABC, abstractmethod


class ITBCSVFileWriter(ABC):

    @abstractmethod
    def save_transacao(self, info: ConsolidadorInfo) -> None:
        ...
