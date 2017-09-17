import unittest
import kraken

class MyTest(unittest.TestCase):

    def test__get_pair_name(self):
        self.assertEqual(kraken.get_pair_name('BCH', 'EUR'), 'BCHEUR')
        self.assertEqual(kraken.get_pair_name('XBT', 'JPY'), 'XXBTZJPY')
        self.assertEqual(kraken.get_pair_name('ETH', 'USD'), 'XETHZUSD')
        self.assertEqual(kraken.get_pair_name('XRP', 'XBT'), 'XXRPXXBT')

    def test__is_right_pair_name(self):
        self.assertEqual(kraken.is_right_pair_name('XXBTZJPY'), True)
        self.assertEqual(kraken.is_right_pair_name('XXBTXXBT'), False)
        self.assertEqual(kraken.is_right_pair_name('XXRPZJPY'), False)

if __name__ == "__main__":
    unittest.main()
