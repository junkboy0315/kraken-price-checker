import sys
import krakenex

API = krakenex.API(
    key='ylRM81xbtOMiRSV2scfP2G1aZi7k5IG4wMGYslNjZwXvFzmLqK8z2wk3',
    secret='7wcryvE8yj7ogJTB8nneQ4H3OEvszJRg1WAonaayEJTCxK10xni2Wu3368DrZvRmAPhvaCWItYCCWzXfhq42Sw=='
)
CURRENCIES = ['USD', 'EUR', 'JPY', 'CAD', 'GBP']
TARGET_CURRENCY = 'JPY'

balance = []
query = set()

class AssetPair():
    """
    handles things associated with asset pairs.
    """

    VALID_PAIR_NAMES = set(API.query_public('AssetPairs')['result'].keys())

    @classmethod
    def get_pair_name(cls, origin, target):
        """ Get an asset-pair-name used for Kraken API

        Acquire the asset-pair-name string like 'XXBTZJPY'
        from the pair of the asset name.
        These are used for the query string of the Kraken API.

        Args:
            origin(str): Original asset name. e.g. 'XRP'
            target(str): Target asset name. e.g. 'JPY' or 'XRP'

        Returns:
            str: string like 'XXBTZJPY' which is NOT checked if valid for Kraken API

        """

        # asset-pair-string which contains the following assets is irregular.
        # ['BCH', 'DASH', 'EOS', 'GNO']
        #
        # which means that
        # - the first 'X' character for crypto-currency
        # - the first 'Z' character for normal-currency
        # DOES NOT exist in the asset-pair-string.
        #   e.g. 'BCHXBT', 'DASHXBT'
        #
        # but others contains these character like as follows.
        #   e.g. 'XXBTZJPY', 'XETHZEUR'
        IRREGULAR_ASSET_CLASSES = ['BCH', 'DASH', 'EOS', 'GNO']

        if origin in IRREGULAR_ASSET_CLASSES:
            return origin + target
        elif target in CURRENCIES:
            return 'X{}Z{}'.format(origin, target)
        else:
            return 'X{}X{}'.format(origin, target)

    @classmethod
    def is_valid_pair(cls, origin, target):
        """
        check if the *pair of criptocurrency* is valid pair for the Kraken API.
        """

        if cls.get_pair_name(origin, target) in cls.VALID_PAIR_NAMES:
            return True
        return False

    @classmethod
    def is_valid_pair_name(cls, pair_name):
        """
        check if the *string* is valid asset-pair-string for Kraken API
        """

        if pair_name in cls.VALID_PAIR_NAMES:
            return True
        return False

class Asset():
    def __init__(self, name, amount):
        self.name = name
        self.amount = float(amount)
        self.amount_as_money = None
        self.calc_via_XBT_needed = None

# store assets info to the array
for name, amount in API.query_private('Balance')['result'].items():
    # get rid of unnecesarry 'X'
    # e.g. 'XXBT' => 'XBT'
    if name[0] == 'X':
        name = name[1::]

    balance.append(Asset(name, amount))

# calc asset pairs need to fetch
for asset in balance:
    if AssetPair.is_valid_pair(asset.name, TARGET_CURRENCY):
        # asset which can be exchanged directly
        query.add(AssetPair.get_pair_name(asset.name, TARGET_CURRENCY))
    else:
        # asset which can be exchanged via XBT
        asset.calc_via_XBT_needed = True
        query.add(AssetPair.get_pair_name(asset.name, 'XBT'))
        query.add(AssetPair.get_pair_name('XBT', TARGET_CURRENCY))

# if the query contains asset pairs that are not valid,
# display that information and exit tht program.
if not query <= AssetPair.VALID_PAIR_NAMES:
    sys.exit('The query contains invalid AssetPair: ' + str(query - AssetPair.VALID_PAIR_NAMES))

# join the query and make a string => 'XXBTZJPY,BCHXBT'
query = ','.join(query)

# get the ticker data
ticker = API.query_public('Ticker', {'pair': query})['result']

for asset in balance:
    if asset.calc_via_XBT_needed:
        pair1 = AssetPair.get_pair_name(asset.name, 'XBT')
        pair2 = AssetPair.get_pair_name('XBT', TARGET_CURRENCY)

        result = asset.amount * (
            float(ticker[pair1]['c'][0]) *
            float(ticker[pair2]['c'][0])
        )

        asset.amount_as_money = result

    else:
        pair = AssetPair.get_pair_name(asset.name, TARGET_CURRENCY)
        asset.amount_as_money = asset.amount * float(ticker[pair]['c'][0])

print('-----------------------')
for asset in balance:
    print('{:6}: {:15,.0f}'.format(asset.name, asset.amount_as_money))
print('-----------------------')
print('total : {:15,.0f}'.format(sum([i.amount_as_money for i in balance])))
print('-----------------------')
