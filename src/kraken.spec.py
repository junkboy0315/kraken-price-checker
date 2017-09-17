import unittest
import kraken

class MyTest(unittest.TestCase):

    def test_class_AssetPair(self):
        self.assertEqual(kraken.AssetPair.is_valid_pair('XBT', 'JPY'), True)
        self.assertEqual(kraken.AssetPair.is_valid_pair('XBT', 'XBT'), False)
        self.assertEqual(kraken.AssetPair.is_valid_pair('XRP', 'JPY'), False)
        
        self.assertEqual(kraken.AssetPair.is_valid_pair_name('XXBTZJPY'), True)
        self.assertEqual(kraken.AssetPair.is_valid_pair_name('XXBTXXBT'), False)
        self.assertEqual(kraken.AssetPair.is_valid_pair_name('XXRPZJPY'), False)

        self.assertEqual(kraken.AssetPair.generate_pair_name('BCH', 'EUR'), 'BCHEUR')
        self.assertEqual(kraken.AssetPair.generate_pair_name('XBT', 'JPY'), 'XXBTZJPY')
        self.assertEqual(kraken.AssetPair.generate_pair_name('ETH', 'USD'), 'XETHZUSD')
        self.assertEqual(kraken.AssetPair.generate_pair_name('XRP', 'XBT'), 'XXRPXXBT')

if __name__ == "__main__":
    unittest.main()
