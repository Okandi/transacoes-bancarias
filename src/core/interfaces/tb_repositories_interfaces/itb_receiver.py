from src.core.models.transacao import TransacaoTED, TransacaoPIX
from abc import ABC, abstractmethod


class ITBReceiver(ABC):
    
    @abstractmethod
    def get_transferencia_bancaria(self) -> TransacaoTED | TransacaoPIX:
        ...
