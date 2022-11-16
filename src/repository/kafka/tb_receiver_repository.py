from src.infrastructure.kafka.tb_kafka_infrastructure import TBKafkaInfrastructure
from src.core.models.transacao import TransacaoTED, TransacaoPIX
from src.core.enum.tipo_transacao_enum import TipoTransacao
from src.core.interfaces.tb_repositories_interfaces.itb_receiver import ITBReceiver
from datetime import datetime


class TBReceiver(ITBReceiver):
    
    def __init__(self) -> None:
        self._kafka_consumer = TBKafkaInfrastructure().get_kafka_consumer()
    
    def _trata_erros(function):
        def function_wrapper(*args):
            try:
                return function(*args)
            except KeyError as e:
                print(f"Transação inválida: campo {e} não existe")
            except ValueError as e:
                print(e)
            except Exception as e:
                print(f"Ocorreu um erro inesperado: \n{e}")
            return args[0].get_transferencia_bancaria()
        return function_wrapper
    
    @_trata_erros
    def get_transferencia_bancaria(self) -> TransacaoTED | TransacaoPIX:
        transacao = next(self._kafka_consumer).value
        match transacao["tipo"]:
            case TipoTransacao.TED.name:
                return self._cria_transacao_ted(transacao)
            case TipoTransacao.PIX.name:
                return self._cria_transacao_pix(transacao)
        raise ValueError(f"Tipo da transação inválida: {transacao['tipo']}")
    
    def _cria_transacao_ted(self, transacao: dict) -> TransacaoTED:
        return TransacaoTED(
            str(transacao["origem"]["banco"]),
            str(transacao["origem"]["agencia"]),
            str(transacao["origem"]["conta"]),
            float(transacao["valor"]),
            self._transforma_string_em_data(str(transacao["envio"])),
            str(transacao["destino"]["banco"]),
            str(transacao["destino"]["agencia"]),
            str(transacao["destino"]["conta"])
        )

    def _cria_transacao_pix(self, transacao: dict) -> TransacaoPIX:
        return TransacaoPIX(
            str(transacao["origem"]["banco"]),
            str(transacao["origem"]["agencia"]),
            str(transacao["origem"]["conta"]),
            float(transacao["valor"]),
            self._transforma_string_em_data(str(transacao["envio"])),
            str(transacao["destino"]["banco"]),
            str(transacao["destino"]["chave"])
        )

    @staticmethod
    def _transforma_string_em_data(string: str) -> datetime:
        return datetime.strptime(string, "%Y-%m-%dT%H:%M:%S")
