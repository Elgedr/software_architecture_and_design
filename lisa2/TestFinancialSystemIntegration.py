

import unittest


from lisa2v2.FinancialSystem import FinancialSystem
from lisa2v2.Money import Money


class TestFinancialSystemIntegration(unittest.TestCase):

    def setUp(self):
        """Set up the financial system and add currencies and exchange rates."""
        self.fin_system = FinancialSystem(base_currency_code="USD")

        # Add currencies
        self.eur = self.fin_system.add_currency("EUR", "Euro")
        self.jpy = self.fin_system.add_currency("JPY", "Japanese Yen")
        self.gbp = self.fin_system.add_currency("GBP", "British Pound")
        self.usd = self.fin_system.add_currency("USD", "US Dollar")

        # Set exchange rates
        self.fin_system.set_exchange_rate(self.eur, 1.2)  # 1 EUR = 1.2 USD
        self.fin_system.set_exchange_rate(self.jpy, 0.0091)  # 1 JPY = 0.0091 USD
        self.fin_system.set_exchange_rate(self.gbp, 0.85)  # 1 GBP = 0.85 EUR

    def test_full_system_conversion(self):
        """Test the complete conversion flow through the financial system."""
        # Initialize Money instances
        money_in_eur = Money(100, self.eur)  # 100 EUR
        money_in_jpy = Money(1000, self.jpy)  # 1000 JPY
        money_in_gbp = Money(50, self.gbp)  # 50 GBP

        # Convert EUR to USD
        base_currency = self.fin_system.base_currency

        print(base_currency)
        converted_usd_from_eur = money_in_eur.convert(base_currency,
                                                      self.fin_system.exchange_rates.values())
        self.assertEqual(converted_usd_from_eur.amount, 120)  # 100 EUR * 1.2

        # Convert JPY to USD
        converted_usd_from_jpy = money_in_jpy.convert(base_currency,
                                                      self.fin_system.exchange_rates.values())
        self.assertEqual(converted_usd_from_jpy.amount, 9.1)  # 1000 JPY * 0.0091

        # Convert GBP to USD through EUR
        converted_usd_from_gbp = money_in_gbp.convert(base_currency,
                                                      self.fin_system.exchange_rates.values())
        converted_eur = money_in_gbp.convert(self.eur, self.fin_system.exchange_rates.values())
        converted_usd_via_eur = converted_eur.convert(base_currency,
                                                      self.fin_system.exchange_rates.values())
        self.assertAlmostEqual(converted_usd_from_gbp.amount, converted_usd_via_eur.amount)

        # Transitivity check: Convert JPY to GBP through USD and EUR
        converted_to_usd_from_jpy = money_in_jpy.convert(base_currency,
                                                         self.fin_system.exchange_rates.values())
        converted_to_eur_from_usd = converted_to_usd_from_jpy.convert(self.eur, self.fin_system.exchange_rates.values())
        converted_to_gbp_via_usd_eur = converted_to_eur_from_usd.convert(self.gbp,
                                                                         self.fin_system.exchange_rates.values())

        # Directly convert JPY to GBP
        converted_to_gbp_directly = money_in_jpy.convert(self.gbp, self.fin_system.exchange_rates.values())

        self.assertAlmostEqual(converted_to_gbp_via_usd_eur.amount, converted_to_gbp_directly.amount, delta=0.1)


if __name__ == '__main__':
    unittest.main()
