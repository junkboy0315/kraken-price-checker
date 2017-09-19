"""
Testfile for kraken.py
"""

import unittest
import kraken

class MyTest(unittest.TestCase):
    def test_class_ApiHelper(self):
        # get_asset_pairs()
        pairs = kraken.ApiHelper.get_asset_pair_names()
        self.assertEqual({'XXBTZGBP', 'GNOXBT'} <= pairs, True)

        # get_ticker()
        pairs = kraken.ApiHelper.get_ticker('XXBTZJPY')
        self.assertIsNotNone(pairs['XXBTZJPY']['c'][0])

    def test_class_AssetPair(self):
        # is_valid_pair()
        self.assertEqual(kraken.AssetPair.is_valid('XBT', 'JPY'), True)
        self.assertEqual(kraken.AssetPair.is_valid('XBT', 'XBT'), False)
        self.assertEqual(kraken.AssetPair.is_valid('XRP', 'JPY'), False)

        # generate_pair_name()
        self.assertEqual(kraken.AssetPair.generate_name('BCH', 'EUR'), 'BCHEUR')
        self.assertEqual(kraken.AssetPair.generate_name('XBT', 'JPY'), 'XXBTZJPY')
        self.assertEqual(kraken.AssetPair.generate_name('ETH', 'USD'), 'XETHZUSD')
        self.assertEqual(kraken.AssetPair.generate_name('XRP', 'XBT'), 'XXRPXXBT')

if __name__ == "__main__":
    unittest.main()
