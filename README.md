# Kraken price checker
You can check your balance of the [Kraken](https://www.kraken.com/) faster, even if you activate the two-factor authentication.

## What for
If you enable two-factor authentication with Kraken, logging in is time-consuming. With this program you can quickly check your balance in the shell as follows:

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

1. Get **API key** and **API secret** from the [Kraken](https://www.kraken.com/). Only premission of **'Query Funds'** is required.

1. Set enviroment variable as follows.
    ```
    KRAKEN_KEY = *Your API key*
    KRAKEN_SECRET = *Your API secret*
    ```

1. Edit `TARGET_CURRENCY` variable in the `src/kraken.py` as you like.

1. run the program like `python src/kraken.py` and you'll get the balance.

## License
MIT
