# Kraken price checker

If you enable two-factor authentication with Kraken, logging in is time-consuming. 

With this program, even if two-factor authentication is enabled, you can check the balance of  [Kraken](https://www.kraken.com/) more quickly. 

Moreover, you can check the balance in your favorite currency with the shell as follows:

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

## Setup
1. install [veox/python3-krakenex](https://github.com/veox/python3-krakenex).

1. Clone this repository.

1. Get **API key** and **API secret** from the [Kraken](https://www.kraken.com/). Only premission of **'Query Funds'** is required.

1. Set your OS enviroment variable as follows.
    ```
    KRAKEN_KEY = *Your API key*
    KRAKEN_SECRET = *Your API secret*
    ```

1. Edit `TARGET_CURRENCY` variable in the `src/kraken.py` as you like. (e.g. `'USD'` or `'JPY'`)

1. Run the `run.bat` or `run.sh` and you'll get the balance.

## License
MIT
