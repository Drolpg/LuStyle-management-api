class AlreadyExistsException(Exception):
    def __init__(self, message="Item já existe"):
        self.message = message
