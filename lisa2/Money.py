from lisa2v2.Currency import Currency


class Money:
    def __init__(self, amount: float, currency: Currency):
        self.amount = amount
        self.currency = currency

    def convert(self, to_currency: Currency, exchange_rates: list) -> 'Money':
        # If converting to the same currency, return itself
        if self.currency == to_currency:
            return self

        # Check if the current currency is the base currency (USD)
        if "base" in self.currency.name.lower():

            # Convert from the base currency to the target currency
            to_currency_rate = next(
                (rate for rate in exchange_rates if
                 "base" in rate.from_currency.name.lower() and rate.to_currency == to_currency),
                None
            )
            if to_currency_rate:
                target_amount = self.amount * to_currency_rate.rate
                return Money(round(target_amount, 2), to_currency)

            raise ValueError(f"No conversion rate available from {self.currency.code} to {to_currency.code}.")

        # Check if the target currency is the base currency
        if "base" in to_currency.name.lower():
            # Convert directly to the base currency
            base_currency_rate = next(
                (rate for rate in exchange_rates if
                 rate.from_currency == self.currency),
                None
            )

            if base_currency_rate:
                target_amount = self.amount * base_currency_rate.rate
                return Money(round(target_amount, 2), to_currency)

            raise ValueError(f"No conversion rate available from {self.currency.code} to base currency.")

        # Convert to the base currency first
        base_currency_rate = next(
            (rate for rate in exchange_rates if
             rate.from_currency == self.currency and "base" in rate.to_currency.name.lower()),
            None
        )

        # Convert from base currency to target currency
        to_currency_rate = next(
            (rate for rate in exchange_rates if
             "base" in rate.from_currency.name.lower() and rate.to_currency == to_currency),
            None
        )

        if base_currency_rate and to_currency_rate:
            # Convert to USD first, then to the target currency
            usd_amount = self.amount * base_currency_rate.rate
            target_amount = usd_amount * to_currency_rate.rate
            return Money(round(target_amount, 2), to_currency)

        raise ValueError(f"No conversion rate available from {self.currency.code} to {to_currency.code}.")

    def increase(self, amount: float) -> None:
        self.amount = (self.amount + amount)

    def decrease(self, amount: float) -> None:
        if self.amount >= amount:
            self.amount = (self.amount - amount)
        else:
            raise ValueError("Insufficient funds to decrease by this amount")
