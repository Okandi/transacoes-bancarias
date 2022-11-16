from src.core.enum.tipo_transacao_enum import TipoTransacao
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transacao:
    tipo = None
    origem_banco: str
    origem_agencia: str
    origem_conta: str
    valor: float
    envio: datetime


@dataclass
class TransacaoTED(Transacao):
    tipo = TipoTransacao.TED
    destino_banco: str
    destino_agencia: str
    destino_conta: str


@dataclass
class TransacaoPIX(Transacao):
    tipo = TipoTransacao.PIX
    destino_banco: str
    destino_chave: str
