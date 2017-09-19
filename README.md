# Kraken price checker

If you enable two-factor authentication with Kraken, logging in is time-consuming. 

With this program, even if two-factor authentication is enabled, you can check the balance of  [Kraken](https://www.kraken.com/) more quickly. 

Moreover, you can check the balance in your favorite currency with the shell as follows:

```
-----------------------
XBT   :          52,622
XRP   :          91,205
ETH   :          97,309
BCH   :           6,252
-----------------------
total :         247,388
-----------------------
                  (JPY)
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

1. run the program like `python src/kraken.py` and you'll get the balance.

## License
MIT
