# Kraken price checker

A tool to check the balance of [Kraken](https://www.kraken.com/) **more quickly** in your **favorite currency**.

You can also **record the history** of balance into the database if you want.


```
               Balance      Rate(JPY)  Total(JPY)
-------------------------------------------------
   XBT:        0.11916     444,875.00      53,013
   XRP:    4,315.45550          20.96      90,463
   ETH:        3.05850      32,350.00      98,942
   BCH:        0.11916      52,495.25       6,256
-------------------------------------------------
 Total:                                   248,674
```

## Dependencies
- [Python 3](https://www.python.org/downloads/)
- [veox/python3-krakenex](https://github.com/veox/python3-krakenex)
- [peewee](https://github.com/coleifer/peewee) (if you want to use database)

## Setup
1. install [veox/python3-krakenex](https://github.com/veox/python3-krakenex).

1. Clone this repository.

1. Get **API key** and **API secret** from the [Kraken](https://www.kraken.com/). Only premission of **'Query Funds'** is required.

1. Set your OS enviroment variable as follows.
    ```
    KRAKEN_KEY = *Your API key*
    KRAKEN_SECRET = *Your API secret*
    ```

1. Edit `TARGET_CURRENCY` variable in the `src/config.ini` as you like. (e.g. `'USD'` or `'JPY'`)

1. Run the `run.bat` or `run.sh` and you'll get the balance.

**To record the history in the database, additional settings are required as follows**

1. Install [peewee](https://github.com/coleifer/peewee).

1. Edit `RECORD_TO_DB` variable in the `src/config.ini` to `True`

1. Set your OS enviroment variable as follows. You can choice any databases like sqlite, postgres, mysql and mariadb. Check [this page](http://docs.peewee-orm.com/en/latest/peewee/database.html#connecting-using-a-database-url) for more details.
    ```
    DB_FOR_KRAKEN = mysql://user:passwd@ip:port/my_db
    ```
1. Run the `run.bat` or `run.sh`.

## License
MIT
