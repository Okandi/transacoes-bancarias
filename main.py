from src.services.processa_transacoes_service import ProcessaTransacoesService

service = ProcessaTransacoesService()

while True:
    service.processa_transacoes()
