import os
import webbrowser

from lisa2v2.Currency import Currency

from lisa2v2.ExchangeRate import ExchangeRate


class FinancialSystem:
    def __init__(self, base_currency_code: str = "USD"):
        self.currencies = {}  # {currency_code:Currency}
        self.exchange_rates = {}  # {(currency_code, base_currency_code):ExchangeRate}
        self.base_currency = Currency(base_currency_code, "Base Currency")
        self.add_currency(base_currency_code, self.base_currency.name)

    def add_currency(self, code: str, name: str):
        if code not in self.currencies:
            new_currency = Currency(code, name)
            self.currencies[code] = new_currency
            return new_currency

    def set_exchange_rate(self, currency: Currency, rate_to_base: float):
        if rate_to_base <= 0:
            raise ValueError("Exchange rate must be greater than 0")

        if currency.code in self.currencies and self.base_currency.code in self.currencies:
            self.exchange_rates[(currency.code, self.base_currency.code)] = ExchangeRate(currency, self.base_currency,
                                                                                         round(rate_to_base, 4))
            reversed_currency = self.exchange_rates[(currency.code, self.base_currency.code)].get_inverse()
            self.exchange_rates[(self.base_currency.code, currency.code)] = ExchangeRate(self.base_currency, currency,
                                                                                         reversed_currency)
        else:
            raise ValueError("Currency not recognized in the system")

    def change_exchange_rate(self, from_code: str, to_code: str, new_rate: float):
        if new_rate <= 0:
            raise ValueError("New exchange rate must be greater than 0")

        if (from_code, to_code) in self.exchange_rates:
            pair1 = self.exchange_rates[(from_code, to_code)]
            pair1.change_rate(new_rate)
            pair2 = self.exchange_rates[(to_code, from_code)]
            pair2.change_rate(pair1.get_inverse())
            print(f"Updated exchange rate from {from_code} to {to_code}: {new_rate}")
            print(f"Updated exchange rate from {to_code} to {from_code}: {pair2.rate}")
        else:
            raise ValueError("Exchange rate for this currency pair does not exist. Use set_exchange_rate first.")

    def get_exchange_rate(self, from_code: str, to_code: str) -> float:
        if (from_code, to_code) in self.exchange_rates:
            return self.exchange_rates[(from_code, to_code)].get_rate()
        else:
            raise ValueError("The exchange rate has not been set")

    def display_exchange_rates(self, filename: str = "exchange_rates.html") -> str:
        html_table = """
        <html><head><style>
        table { font-family: Arial, sans-serif; border-collapse: collapse; width: 50%; margin: 20px; }
        th, td { border: 1px solid #dddddd; text-align: left; padding: 8px; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        </style></head><body>
        <table><tr><th>From</th><th>To</th><th>Rate</th></tr>"""

        for (from_code, to_code), rate_obj in self.exchange_rates.items():
            html_table += f"<tr><td>{from_code}</td><td>{to_code}</td><td>{rate_obj.rate}</td></tr>"

        html_table += "</table></body></html>"

        with open(filename, 'w') as file:
            file.write(html_table)

        webbrowser.open_new_tab(f'file:///{os.path.abspath(filename)}')
        return html_table
