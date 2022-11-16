from src.core.enum.tipo_transacao_enum import TipoTransacao
from src.core.enum.tipo_chave_enum import TipoChave
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AntiFraudeInfo:
    tipo: TipoTransacao
    chave_valor: str
    chave_tipo_chave: TipoChave
    valor: float
    envio: datetime
