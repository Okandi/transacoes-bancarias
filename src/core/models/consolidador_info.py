from src.core.enum.tipo_transacao_enum import TipoTransacao
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ConsolidadorInfo:
    tipo: TipoTransacao
    valor: float
    envio: datetime
