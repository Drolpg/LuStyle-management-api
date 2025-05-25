class NotFoundException(Exception):
    def __init__(self, message="Item não encontrado"):
        self.message = message
