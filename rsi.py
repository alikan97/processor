import pandas as pd
import numpy as np

def get_rsi(close, lookback = 10):
    """
    Determine the relative strength index
    :param list close: List of closing prices
    :param int lookback: Lookback period for exponential weight avg
    :return list rsi: relative strength index 
    """
    return_prices = close.diff()

    # Create empty array to store differences (i.e losses vs gains)
    change_up = []
    change_down = []

    # Loop through the return prices, and determine losses vs gains
    for i in range(len(return_prices)):
        if return_prices[i] < 0:
            change_up.append(0)
            change_down.append(return_prices[i])
        else:
            change_up.append(return_prices[i])
            change_down.append(0)
    
    up_series = pd.Series(change_up)
    down_series = pd.Series(change_down).abs()

    # Find the exponentially weight moving average to give more weight to the recent values (e.g lookback period)
    up_ewm = up_series.ewm(com=lookback-1, adjust=False).mean()
    down_ewm = down_series.ewm(com=lookback-1, adjust=False).mean()

    # Following the rsi formula
    rs = up_ewm/down_ewm
    rsi = 100 - (100/(1+rs))
    rsi_df = pd.DataFrame(rsi).rename(columns={0: 'rsi'}).set_index(close.index)

    # rsi_df = rsi_df.dropna()
    return rsi_df[3:]

def rsi_signals(prices, rsi):
    """
    Determines buy and sell signals
    :param prices list: list of closing prices
    :param rsi list: Relative strength index
    :return list buy_price, sell_price, rsi_signal
    """
    buy_price = []
    sell_price = []
    rsi_signal = []
    signal = 0

    for i in range(len(rsi)):
        # If Condition for buy signal
        if (rsi[i-1] > 30 and rsi[i] < 30):
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                rsi_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                rsi_signal.append(0)
                
        # If condition for sell signal
        elif (rsi[i-1] < 70 and rsi[i] > 70):
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                rsi_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                rsi_signal.append(0)

        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            rsi_signal.append(0)
    
    return buy_price, sell_price