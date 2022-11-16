from src.core.models.transacao import TransacaoTED, TransacaoPIX
from src.core.models.consolidador_info import ConsolidadorInfo
from src.core.models.anti_fraude_info import AntiFraudeInfo
from abc import ABC, abstractmethod


class ITBSender(ABC):
    
    @abstractmethod
    def send_to_transferencia_bancaria(self, info: TransacaoTED | TransacaoPIX) -> None:
        ...

    @abstractmethod
    def send_to_antifraude(self, info: AntiFraudeInfo) -> None:
        ...

    @abstractmethod
    def send_to_consolidador(self, info: ConsolidadorInfo) -> None:
        ...
