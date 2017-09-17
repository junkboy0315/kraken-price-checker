import sys
import krakenex

API = krakenex.API(
    key='ylRM81xbtOMiRSV2scfP2G1aZi7k5IG4wMGYslNjZwXvFzmLqK8z2wk3',
    secret='7wcryvE8yj7ogJTB8nneQ4H3OEvszJRg1WAonaayEJTCxK10xni2Wu3368DrZvRmAPhvaCWItYCCWzXfhq42Sw=='
)

BALANCE = API.query_private('Balance')['result']
TARGET_CURRENCY = 'JPY'
CURRENCIES = ['USD', 'EUR', 'JPY', 'CAD', 'GBP']

my_balance = []
query = set()

class AssetPair():
    """Handle asset pairs."""

    VALID_PAIRS = set(API.query_public('AssetPairs')['result'].keys())

    @classmethod
    def get_pair_name(cls, origin, target):

        # pairs contains following asset class don't contain first 'X' and inner 'Z'.
        #   e.g. 'BCHXBT', 'DASHXBT'
        # but others contains like as follows.
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
        if cls.get_pair_name(origin, target) in cls.VALID_PAIRS:
            return True
        return False

    @classmethod
    def is_valid_pair_name(cls, pair_name):
        if pair_name in cls.VALID_PAIRS:
            return True
        return False

class Asset():
    def __init__(self, name, amount):
        self.name = name
        self.amount = float(amount)
        self.amount_as_money = None
        self.calc_via_XBT_needed = None

# store assets info to the array
for name, amount in BALANCE.items():
    # get rid of unnecesarry 'X'
    # e.g. 'XXBT' => 'XBT'
    if name[0] == 'X':
        name = name[1::]

    my_balance.append(Asset(name, amount))

# calc asset pairs need to fetch
for asset in my_balance:
    if AssetPair.is_valid_pair(asset.name, TARGET_CURRENCY):
        # get the amount of money directly
        query.add(AssetPair.get_pair_name(asset.name, TARGET_CURRENCY))
    else:
        # get the amount money via XBT
        asset.calc_via_XBT_needed = True
        query.add(AssetPair.get_pair_name(asset.name, 'XBT'))
        query.add(AssetPair.get_pair_name('XBT', TARGET_CURRENCY))

# if the query contains asset pairs that are not valid,
# display that information and exit tht program.
if not query <= AssetPair.VALID_PAIRS:
    sys.exit('The query contains invalid AssetPair: ' + str(query - AssetPair.VALID_PAIRS))

# join the query and make a string => 'XXBTZJPY,BCHXBT'
query = ','.join(query)

# get the ticker data
ticker = API.query_public('Ticker', {'pair': query})['result']


for asset in my_balance:
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

for asset in my_balance:
    print(asset.name, '{:10.0f}'.format(asset.amount_as_money))
