from lisa2v2 import Currency


class ExchangeRate:
    def __init__(self, from_currency: Currency, to_currency: Currency, rate: float):
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.rate = rate

    def change_rate(self, new_rate: float) -> None:
        self.rate = new_rate

    def get_inverse(self) -> float:
        if self.rate <= 0:
            raise ValueError("Exchange rate must be greater than 0 to calculate inverse.")
        return round(1 / self.rate, 4)

    def get_rate(self) -> float:
        return self.rate

    def __str__(self):
        return f'From currency {self.from_currency} to currency {self.to_currency} exchange rate is {self.rate}'

