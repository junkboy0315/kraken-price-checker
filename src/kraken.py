import krakenex

API = krakenex.API(
    key='ylRM81xbtOMiRSV2scfP2G1aZi7k5IG4wMGYslNjZwXvFzmLqK8z2wk3',
    secret='7wcryvE8yj7ogJTB8nneQ4H3OEvszJRg1WAonaayEJTCxK10xni2Wu3368DrZvRmAPhvaCWItYCCWzXfhq42Sw=='
)
TARGET_CURRENCY = 'JPY'

kraken_balance = API.query_private('Balance')['result']
kraken_asset_pairs = API.query_public('AssetPairs')['result']

my_balance = []

class AssetClass():
    def __init__(self, name, amount):
        self.name = name
        self.amount = float(amount)
        self.amount_as_XBT = None
        self.amount_as_CURRENCY = None
        self.calc_via_XBT_needed = None

# store balance info to the array
for name, amount in kraken_balance.items():
    # get rid of unnecesarry 'X'
    # e.g. 'XXBT' => 'XBT'
    if name[0] == 'X':
        name = name[1::]
    my_balance.append(AssetClass(name, amount))

def get_pair_name(origin, target):
    '''
    get the right pair name for the ticker query.
    
    if the pair is not contained by the Kraken's pair list,
    return False, otherwise return pair string like 'XXBTZJPY'
    '''

    # pairs of these class doesn't contain 'X' and 'Z'
    #   e.g. 'BCHXBT', 'DASHXBT'
    # but other currencies like as follows
    #   e.g. 'XXBTZJPY', 'XETHZEUR'
    IRREGULAR_ASSET_CLASSES = ['BCH', 'DASH', 'EOS', 'GNO']
    CURRENCIES = ['USD', 'EUR', 'JPY', 'CAD', 'GBP']

    pair_name = ''

    if origin in IRREGULAR_ASSET_CLASSES:
        pair_name = origin + target
    elif target in CURRENCIES:
        pair_name = 'X{}Z{}'.format(origin, target)
    else:
        pair_name ='X{}X{}'.format(origin, target)

    if is_right_pair_name(pair_name) is False:
        return False
    
    return pair_name

def is_right_pair_name(pair_name):
    if pair_name not in kraken_asset_pairs.keys():
        return False
    return True

# judge calculation via XBT is needed
for asset_class in my_balance:
    if get_pair_name(asset_class.name, TARGET_CURRENCY) is False:
        asset_class.calc_via_XBT_needed = True

query = set()

for asset_class in my_balance:
    if asset_class.calc_via_XBT_needed:
        query.add(get_pair_name(asset_class.name, 'XBT'))
        query.add(get_pair_name('XBT', TARGET_CURRENCY))
    else:
        query.add(get_pair_name(asset_class.name, TARGET_CURRENCY))

query = ','.join(query)
ticker = API.query_public('Ticker', {'pair': query})['result']


for asset_class in my_balance:
    if asset_class.calc_via_XBT_needed:
        pair1 = get_pair_name(asset_class.name, 'XBT')
        pair2 = get_pair_name('XBT', TARGET_CURRENCY)
        
        result = asset_class.amount * (
            float(ticker[pair1]['c'][0])
            * float(ticker[pair2]['c'][0])
        )

        asset_class.amount_as_CURRENCY = result

    else:
        pair = get_pair_name(asset_class.name, TARGET_CURRENCY)
        asset_class.amount_as_CURRENCY = asset_class.amount * float(ticker[pair]['c'][0])

for asset in my_balance:
    print(asset.name, '{:10.0f}'.format(asset.amount_as_CURRENCY))
