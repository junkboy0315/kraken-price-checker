"""
This module checks the balance of the Kraken and displays it.
"""

import os
import sys
import krakenex

from datetime import datetime
from peewee import *
from playhouse.db_url import connect

API = krakenex.API(
    key=os.environ['KRAKEN_KEY'],
    secret=os.environ['KRAKEN_SECRET'],
)
CURRENCIES = ['USD', 'EUR', 'JPY', 'CAD', 'GBP']

# Currency you want to display (EDIT THIS VALUE AS YOU LIKE)
TARGET_CURRENCY = 'JPY'

# Record result to MariaDB (EDIT THIS VALUE AS YOU LIKE)
RECORD_TO_DB = False

class ApiHelper():
    """
    Helper to get data from the API and return the results.
    """

    @classmethod
    def get_asset_pair_names(cls):
        """
        Get the official asset-pair-names of Kraken.

        Returns:
            set(str): simple set of asset-pair-name as follows.
                      {'XXBTZGBP', 'GNOXBT', 'DASHUSD',,,,,}

        """

        q = API.query_public('AssetPairs')

        if q['error']:
            sys.exit('Failed to fetch AssetPairs: ' + q['error'])

        return set(q['result'].keys())

    @classmethod
    def get_balance(cls):
        """
        Get your balance data.

        Returns:
            dict_items: simple pair of asset and amount as follows.
                        dict_items([('XXBT', '0.1191648200'), ('XXRP', '4315.45550200'),,,,)])

        """

        q = API.query_private('Balance')

        if q['error']:
            sys.exit('Failed to fetch Balance: ' + q['error'])

        return q['result'].items()

    @classmethod
    def get_ticker(cls, _query):
        """
        Get the ticker data.

        Returns:
            dict: ticker data you asked.
                  {'BCHXBT': {....}, 'XXBTZJPY': {....},,,,,}

        """

        q = API.query_public('Ticker', {'pair': _query})

        if q['error']:
            sys.exit('Failed to fetch Ticker: ' + q['error'])

        return q['result']

class AssetPair():
    """
    handles things associated with asset pairs.
    """

    # Store the official asset-pair-names data of Kraken.
    VALID_NAMES = ApiHelper.get_asset_pair_names()

    @classmethod
    def generate_name(cls, origin, target):
        """ Generate an asset-pair-name used for the Kraken API

        Generate an asset-pair-name string like 'XXBTZJPY'
        from the pair of the asset name.
        These are used for the query string of the Kraken API.

        Args:
            origin(str): Original asset name. e.g. 'XBT'
            target(str): Target asset name. e.g. 'JPY' or 'XRP'

        Returns:
            str: asset-pair-name like 'XXBTZJPY' which is NOT checked
                 if it's valid for the Kraken API

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
        if target in CURRENCIES:
            return 'X{}Z{}'.format(origin, target)

        return 'X{}X{}'.format(origin, target)

    @classmethod
    def is_valid(cls, origin, target):
        """
        check if the asset-pair is valid for the Kraken API.

        Args:
            origin(str): Original asset name. e.g. 'XBT'
            target(str): Target asset name. e.g. 'JPY' or 'XRP'

        Returns:
            bool: True for valid, False for invalid.

        """

        if cls.generate_name(origin, target) in cls.VALID_NAMES:
            return True
        return False


class Asset():
    """
    Represents each asset of the balance.
    """

    def __init__(self, _name, _amount):
        self.name = _name
        self.amount = float(_amount)
        self.rate = None

    def getTotal(self):
        return self.amount * self.rate

def record_to_db(balance):
    "Record the balance data to the database you like"

    # you can choice any dbs like sqlite, postgres, mysql and mariadb.
    # DB_FOR_KRAKEN which is a enviroment variable
    # should be like "mysql://user:passwd@ip:port/my_db"
    #
    # for more detail, see:
    # http://docs.peewee-orm.com/en/latest/peewee/database.html#connecting-using-a-database-url
    db = connect(os.environ.get('DB_FOR_KRAKEN'))

    class Log(Model):
        asset = CharField()
        date = DateTimeField()
        amount = FloatField()
        rate = FloatField()
        total = FloatField()
        currency = CharField()

        class Meta:
            database = db

    # don't create tables if the 2nd arg is 'True'
    db.create_tables([Log], True)

    query = []

    for asset in balance:
        query.append({
            'asset': asset.name,
            'date': datetime.now(),
            'amount': asset.amount,
            'rate': asset.rate,
            'total': asset.getTotal(),
            'currency': TARGET_CURRENCY,
        })

    Log.insert_many(query).execute()

def main():
    # Your balance of Kraken
    balance = []

    # asset-pair-names that need Ticker information
    query = set()

    # store assets info to the array
    for name, amount in ApiHelper.get_balance():
        # get rid of unnecesarry 'X'
        # e.g. 'XXBT' => 'XBT'
        if name[0] == 'X':
            name = name[1::]

        balance.append(Asset(name, amount))

    # Find asset-pairs that need ticker information
    for asset in balance:
        if AssetPair.is_valid(asset.name, TARGET_CURRENCY):
            # assets that can be calculated directly
            query.add(AssetPair.generate_name(asset.name, TARGET_CURRENCY))
        else:
            # assets requiring two-step calculaion via XBT
            query.add(AssetPair.generate_name(asset.name, 'XBT'))
            query.add(AssetPair.generate_name('XBT', TARGET_CURRENCY))

    # If the query contains asset-pair-names that are not valid in the official API,
    # display that information and exit tht program.
    # This probably means that calculation via XBT is not available.
    if query - AssetPair.VALID_NAMES:
        sys.exit('The query contains invalid AssetPair: ' + str(query - AssetPair.VALID_NAMES))

    # join the query and make a string => 'XXBTZJPY,BCHXBT'
    query = ','.join(query)

    # get the ticker data
    ticker = ApiHelper.get_ticker(query)

    for asset in balance:
        if AssetPair.is_valid(asset.name, TARGET_CURRENCY):
            # assets that can be calculated directly
            pair = AssetPair.generate_name(asset.name, TARGET_CURRENCY)
            asset.rate = float(ticker[pair]['c'][0])
        else:
            # assets requiring two-step calculaion via XBT
            pair1 = AssetPair.generate_name(asset.name, 'XBT')
            pair2 = AssetPair.generate_name('XBT', TARGET_CURRENCY)

            asset.rate = (
                float(ticker[pair1]['c'][0]) *
                float(ticker[pair2]['c'][0])
            )

    print('')
    print('{:>6} {:>15}{:>15}{:>12}'.format(
        '',
        'Balance',
        'Rate(' + TARGET_CURRENCY + ')',
        'Total(' + TARGET_CURRENCY + ')'
    ))
    print('-------------------------------------------------')
    for asset in balance:
        print('{:>6}:{:>15,.5f}{:>15,.2f}{:>12,.0f}'.format(
            asset.name,
            asset.amount,
            asset.rate,
            asset.getTotal()
        ))
    print('-------------------------------------------------')
    print('{:>6}:{:>15}{:>15}{:>12,.0f}'.format(
        'Total',
        '',
        '',
        sum([asset.getTotal() for asset in balance])
    ))

    if RECORD_TO_DB:
        record_to_db(balance)

if __name__ == "__main__":
    main()
