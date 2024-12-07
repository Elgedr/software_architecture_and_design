class Currency:
    def __init__(self, code: str, name: str):
        self.code = code
        self.name = name

    def __str__(self):
        return f'Currency code is {self.code}, name is {self.name}'

