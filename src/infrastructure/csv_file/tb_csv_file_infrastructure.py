

class TBCSVFileInfrastructure:

    @staticmethod    
    def get_file_access():
        return open("tb_backup/transferencias_bancarias.csv", "a")
