import pandas as pd
from functions.bollinger import get_bollinger_bands
from functions.ema import get_ema
from functions.support_resistance import get_support_resistance
from functions.rsi import get_rsi, rsi_signals

def handler(event, context):
    allCoins = parseSymbols(event)

    for i in allCoins:
        i['bollinger_up'], i['bollinger_down'] = get_bollinger_bands(i['close'])
        i['exponential_moving_avg'] = get_ema(i['close'])
        i['support'], i['resistance'] = get_support_resistance(i['close'])
        rsi = get_rsi(i['close'])
        i['rsi'] = rsi
        buy, sell, _sigs = rsi_signals(i['close'], rsi)
        
        i['buy_signal'] = buy
        i['sell_signal'] = sell
    
    return pd.concat(allCoins).to_json()


def parseSymbols(data):
    eth = data[data['symbol'] == 'ETHBTC']
    eth.reset_index(drop=True, inplace=True) # reset the index to use datetime
    matic = data[data['symbol'] == 'MATICBTC']
    matic.reset_index(drop=True, inplace=True)
    xrp = data[data['symbol'] == 'XRPBTC']
    xrp.reset_index(drop=True, inplace=True)
    ltc = data[data['symbol'] == 'LTCBTC']
    ltc.reset_index(drop=True, inplace=True)
    neo = data[data['symbol'] == 'NEOBTC']
    neo.reset_index(drop=True, inplace=True)
    algo = data[data['symbol'] == 'ALGOBTC']
    algo.reset_index(drop=True, inplace=True)
    bnb = data[data['symbol'] == 'BNBBTC']
    bnb.reset_index(drop=True, inplace=True)

    return eth, matic, xrp, ltc, neo, algo, bnb
