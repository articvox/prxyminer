class Candidate:

    def __init__(self, address: str, port: int):
        self.address = address
        self.port = port

    def __str__(self):
        return f'{self.address}:{self.port}'

    def __repr__(self):
        return self.__str__()

    def __dict__(self):
        return {
            'address': self.address,
            'port': self.port
        }
