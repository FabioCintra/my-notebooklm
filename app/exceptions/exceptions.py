class NotFound(Exception):
    def __init__(self, message, erros):
        super().__init__(message)
        self.erros = erros
