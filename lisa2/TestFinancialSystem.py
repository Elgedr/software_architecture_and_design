import os
import unittest

from lisa2v2.Currency import Currency
from lisa2v2.ExchangeRate import ExchangeRate
from lisa2v2.FinancialSystem import FinancialSystem
from lisa2v2.Money import Money


class TestCurrency(unittest.TestCase):

    def setUp(self):
        self.eur = Currency("EUR", "Euro")
        self.usd = Currency("USD", "US Dollar")

    def test_currency_initialization(self):
        self.assertEqual(self.eur.code, "EUR")
        self.assertEqual(self.eur.name, "Euro")

    def test_currency_string_representation(self):
        self.assertEqual(str(self.eur), "Currency code is EUR, name is Euro")


class TestExchangeRate(unittest.TestCase):

    def setUp(self):
        self.eur = Currency("EUR", "Euro")
        self.usd = Currency("USD", "US Dollar")
        self.rate = ExchangeRate(self.eur, self.usd, 1.2)

    def test_exchange_rate_initialization(self):
        self.assertEqual(self.rate.from_currency, self.eur)
        self.assertEqual(self.rate.to_currency, self.usd)
        self.assertEqual(self.rate.rate, 1.2)

    def test_change_rate(self):
        self.rate.change_rate(1.3)
        self.assertEqual(self.rate.rate, 1.3)

    def test_string_representation(self):
        self.assertEqual(str(self.rate),
                         "From currency Currency code is EUR, name is Euro to currency Currency code is USD, "
                         "name is US Dollar exchange rate is 1.2")


class TestMoney(unittest.TestCase):

    def setUp(self):
        # Initialize currencies
        self.eur = Currency("EUR", "Euro")
        self.usd = Currency("USD", "US Dollar. Base currency")
        self.jpy = Currency("JPY", "Japanese Yen")

        # Initialize exchange rates with USD as the base currency
        self.eur_to_usd_rate = ExchangeRate(self.eur, self.usd, 1.2)  # 1 EUR = 1.2 USD
        self.usd_to_eur_rate = ExchangeRate(self.usd, self.eur, round(1 / 1.2, 4))  # USD to EUR

        self.jpy_to_usd_rate = ExchangeRate(self.jpy, self.usd, 0.0091)  # 1 JPY = 0.0091 USD
        self.usd_to_jpy_rate = ExchangeRate(self.usd, self.jpy, round(1 / 0.0091, 4))  # USD to JPY

        # Initialize Money instances
        self.money_in_eur = Money(100, self.eur)  # 100 EUR
        self.money_in_usd = Money(100, self.usd)  # 100 USD
        self.money_in_jpy = Money(1000, self.jpy)  # 1000 JPY

        # Initialize Money instances
        self.money_in_eur = Money(100, self.eur)  # 100 EUR
        self.money_in_usd = Money(100, self.usd)  # 100 USD
        self.money_in_jpy = Money(1000, self.jpy)  # 1000 JPY

    def test_money_initialization(self):
        self.assertEqual(self.money_in_eur.amount, 100)
        self.assertEqual(self.money_in_eur.currency, self.eur)

    def test_convert_same_currency(self):
        converted_money = self.money_in_usd.convert(self.usd, [self.eur_to_usd_rate, self.usd_to_jpy_rate])
        self.assertEqual(converted_money.amount, 100)
        self.assertEqual(converted_money.currency, self.usd)

    def test_convert_to_usd_from_eur(self):
        converted_money = self.money_in_eur.convert(self.usd, [self.eur_to_usd_rate])
        self.assertEqual(converted_money.amount, 120)  # 100 EUR * 1.2
        self.assertEqual(converted_money.currency, self.usd)

    def test_convert_to_jpy_from_usd(self):
        converted_money = self.money_in_usd.convert(self.jpy, [self.usd_to_jpy_rate])
        self.assertEqual(converted_money.amount, 10989.01)  # 100 USD * 110
        self.assertEqual(converted_money.currency, self.jpy)

    def test_convert_from_jpy_to_usd(self):
        # You can use both rates here for conversion via USD
        converted_money = self.money_in_jpy.convert(self.usd, [self.jpy_to_usd_rate, self.usd_to_jpy_rate])
        self.assertEqual(converted_money.amount, 9.1)  # 1000 JPY * 0.0091
        self.assertEqual(converted_money.currency, self.usd)

    def test_convert_from_eur_to_usd(self):
        converted_money = self.money_in_eur.convert(self.usd, [self.eur_to_usd_rate])
        self.assertEqual(converted_money.amount, 120)  # 100 EUR * 1.2
        self.assertEqual(converted_money.currency, self.usd)

    def test_convert_to_invalid_currency(self):
        invalid_currency = Currency("GBP", "British Pound")
        with self.assertRaises(ValueError):
            self.money_in_eur.convert(invalid_currency, [self.eur_to_usd_rate])  # GBP not in provided exchange rates

    def test_increase_amount(self):
        self.money_in_usd.increase(50)
        self.assertEqual(self.money_in_usd.amount, 150)

    def test_decrease_amount(self):
        self.money_in_usd.decrease(30)
        self.assertEqual(self.money_in_usd.amount, 70)

    def test_decrease_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.money_in_usd.decrease(200)

    def test_transitivity(self):
        # Convert EUR to JPY directly via USD
        converted_to_usd = self.money_in_eur.convert(self.usd, [self.eur_to_usd_rate])
        converted_to_jpy_via_usd = converted_to_usd.convert(self.jpy, [self.usd_to_jpy_rate])

        # Convert EUR directly to JPY
        converted_to_jpy_directly = self.money_in_eur.convert(self.jpy, [self.eur_to_usd_rate, self.usd_to_jpy_rate])

        # Check if the two conversion methods yield the same result
        self.assertEqual(converted_to_jpy_via_usd.amount, converted_to_jpy_directly.amount)

    def test_transitivity_jpy_to_gbp(self):

        # Initialize GBP and additional exchange rates
        self.gbp = Currency("GBP", "British Pound")
        self.jpy_to_gbp_rate = ExchangeRate(self.jpy, self.gbp, 0.0068)  # Example: 1 JPY = 0.0068 GBP
        self.eur_to_gbp_rate = ExchangeRate(self.eur, self.gbp, 0.85)  # Example: 1 EUR = 0.85 GBP
        self.usd_to_GBP_rate = ExchangeRate(self.usd, self.gbp, 0.77)  # Example: 1 USD = 0.77 GBP

        # Convert JPY to USD, then USD to EUR, then EUR to GBP (indirect path)
        converted_to_usd = self.money_in_jpy.convert(self.usd, [self.jpy_to_usd_rate])
        converted_to_eur = converted_to_usd.convert(self.eur, [self.usd_to_eur_rate])
        converted_to_gbp_via_usd_eur = converted_to_eur.convert(self.gbp, [self.eur_to_gbp_rate, self.eur_to_usd_rate,
                                                                           self.usd_to_GBP_rate])

        # Directly convert JPY to GBP
        converted_to_gbp_directly = self.money_in_jpy.convert(self.gbp, [
            self.jpy_to_usd_rate, self.usd_to_eur_rate, self.eur_to_gbp_rate, self.jpy_to_gbp_rate, self.usd_to_GBP_rate
        ])

        # Verify if the transitive conversion yields the same result as the direct conversion
        self.assertAlmostEqual(converted_to_gbp_via_usd_eur.amount, converted_to_gbp_directly.amount, delta=0.01)


class TestFinancialSystem(unittest.TestCase):

    def setUp(self):
        self.fs = FinancialSystem()
        # Add the base currency
        # self.fs.add_currency("USD", "US Dollar")

    def test_add_currency(self):
        self.fs.add_currency("EUR", "Euro")
        self.assertIn("EUR", self.fs.currencies)
        self.assertEqual(self.fs.currencies["EUR"].name, "Euro")

    def test_set_exchange_rate(self):
        eur_currency = self.fs.add_currency("EUR", "Euro")
        self.fs.set_exchange_rate(eur_currency, 1.2)  # 1 EUR = 1.2 USD
        self.assertIn(("EUR", "USD"), self.fs.exchange_rates)
        self.assertIn(("USD", "EUR"), self.fs.exchange_rates)
        self.assertEqual(self.fs.get_exchange_rate("EUR", "USD"), 1.2)
        self.assertEqual(self.fs.get_exchange_rate("USD", "EUR"), round(1 / 1.2, 4))

    def test_change_exchange_rate(self):
        self.fs.add_currency("EUR", "Euro")
        self.fs.set_exchange_rate(self.fs.currencies["EUR"], 1.2)  # 1 EUR = 1.2 USD
        self.fs.change_exchange_rate("EUR", "USD", 1.3)  # Update rate to 1.3
        self.assertEqual(self.fs.get_exchange_rate("EUR", "USD"), 1.3)
        self.assertEqual(self.fs.get_exchange_rate("USD", "EUR"), 0.7692)

    def test_invalid_change_exchange_rate(self):
        self.fs.add_currency("EUR", "Euro")
        self.fs.set_exchange_rate(self.fs.currencies["EUR"], 1.2)
        with self.assertRaises(ValueError):
            self.fs.change_exchange_rate("EUR", "USD", -1)

    def test_display_exchange_rates(self):
        self.fs.add_currency("EUR", "Euro")
        self.fs.set_exchange_rate(self.fs.currencies["EUR"], 1.2)
        html_content = self.fs.display_exchange_rates()
        self.assertIn("<table>", html_content)
        self.assertIn("From</th><th>To</th><th>Rate</th>", html_content)

    def test_display_exchange_rates2(self):
        # Add multiple currencies
        self.fs.add_currency("EUR", "Euro")
        self.fs.add_currency("GBP", "British Pound")

        # Set exchange rates for the currencies
        self.fs.set_exchange_rate(self.fs.currencies["EUR"], 1.2)  # EUR to USD
        self.fs.set_exchange_rate(self.fs.currencies["GBP"], 1.35)  # GBP to USD

        # Generate the HTML content
        filename = "test_exchange_rates.html"
        html_content = self.fs.display_exchange_rates(filename=filename)

        # Basic HTML structure checks
        self.assertIn("<table>", html_content)
        self.assertIn("From</th><th>To</th><th>Rate</th>", html_content)
        self.assertIn("<tr><td>EUR</td><td>USD</td><td>1.2</td></tr>", html_content)
        self.assertIn("<tr><td>USD</td><td>EUR</td><td>0.8333</td></tr>", html_content)
        self.assertIn("<tr><td>GBP</td><td>USD</td><td>1.35</td></tr>", html_content)
        self.assertIn("<tr><td>USD</td><td>GBP</td><td>0.7407</td></tr>", html_content)

        # Check if the file was created
        self.assertTrue(os.path.isfile(filename))

        # Verify the content of the file matches the generated HTML
        with open(filename, 'r') as file:
            file_content = file.read()
            self.assertEqual(file_content, html_content)

    def test_get_exchange_rate_nonexistent(self):
        self.fs.add_currency("EUR", "Euro")
        with self.assertRaises(ValueError):
            self.fs.get_exchange_rate("EUR", "GBP")  # GBP hasn't been added


if __name__ == '__main__':
    unittest.main()
