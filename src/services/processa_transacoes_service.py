from src.repository.csv_file.tb_csv_file_writer import TBCSVFileWriter
from src.core.models.transacao import TransacaoTED, TransacaoPIX
from src.core.models.consolidador_info import ConsolidadorInfo
from src.repository.kafka.tb_receiver_repository import TBReceiver
from src.core.models.anti_fraude_info import AntiFraudeInfo
from src.core.enum.tipo_transacao_enum import TipoTransacao
from src.repository.kafka.tb_sender_repository import TBSender
from src.core.enum.tipo_chave_enum import TipoChave
from datetime import datetime, timedelta
from workalendar.america import Brazil


class ProcessaTransacoesService:
    
    def __init__(self) -> None:
        self._file_writer = TBCSVFileWriter()
        self._calendario = Brazil()
        self._tb_receiver = TBReceiver()
        self._tb_sender = TBSender()

    def processa_transacoes(self) -> None:
        transacao = self._tb_receiver.get_transferencia_bancaria()
        if type(transacao) == TransacaoPIX or self._verifica_horario_valido(transacao.envio):
            self._envia_para_antifraude(transacao)
            self._envia_para_consolidador(transacao)
        else:
            self._envia_para_transferencia_bancaria(transacao)
    
    def _verifica_horario_valido(self, data: datetime) -> bool:
        if self._calendario.is_working_day(data):
            if data.hour < 16:
                return True
        return False

    def _envia_para_antifraude(self, transacao: TransacaoTED | TransacaoPIX) -> None:
        match transacao.tipo:
            case TipoTransacao.TED:
                chave_valor = transacao.destino_agencia + "|" + transacao.destino_conta
                tipo_chave = TipoChave.CONTA
            case TipoTransacao.PIX:
                chave_valor = transacao.destino_chave
                tipo_chave = self._identifica_tipo_chave_pix(transacao.destino_chave)
        anti_fraude_indo = AntiFraudeInfo(
            transacao.tipo,
            chave_valor,
            tipo_chave,
            transacao.valor,
            transacao.envio
        )
        self._tb_sender.send_to_antifraude(anti_fraude_indo)

    def _identifica_tipo_chave_pix(self, chave: str) -> TipoChave:
        if "@" in chave:
            return TipoChave.EMAIL
        elif "(" in chave:
            return TipoChave.TELEFONE
        return TipoChave.CPF
    
    def _envia_para_consolidador(self, transacao: TransacaoTED | TransacaoPIX) -> None:
        consolidador_info = ConsolidadorInfo(
            transacao.tipo,
            transacao.valor,
            transacao.envio
        )
        self._cria_arquivo_backup(consolidador_info)
        self._tb_sender.send_to_consolidador(consolidador_info)
    
    def _cria_arquivo_backup(self, info: ConsolidadorInfo) -> None:
        self._file_writer.save_transacao(info)

    def _envia_para_transferencia_bancaria(self, transacao: TransacaoTED) -> None:
        transacao.envio = self._corrige_data_para_dia_util(transacao.envio)
        self._tb_sender.send_to_transferencia_bancaria(transacao)

    def _corrige_data_para_dia_util(self, data: datetime) -> datetime:
        while True:
            data += timedelta(days=1)
            if self._calendario.is_working_day(data):
                return data.replace(hour=0, minute=0, second=0)
