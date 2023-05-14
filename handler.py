import pandas as pd
from functions.bollinger import get_bollinger_bands
from functions.ema import get_ema
from functions.support_resistance import get_support_resistance
from functions.rsi import get_rsi, rsi_signals
from splunk import send_log, send_data, Log_Level

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

def handler(event, context):
    allCoins = parseSymbols(event)

    try:
        for i in allCoins:  
            up, down = get_bollinger_bands(i['close'])
            i.loc['bollinger_up'] = up
            i.loc['bollinger_down'] = down 
            i.loc['exponential_moving_avg'] = get_ema(i['close'])
            support, resistance = get_support_resistance(i['close'])
            i.loc['support'] = support
            i.loc['resistance'] = resistance
            rsi = get_rsi(i['close'])
            i.loc['rsi'] = rsi
            buy, sell, _sigs = rsi_signals(i['close'], rsi)
            
            i.loc['buy_signal'] = buy
            i.loc['sell_signal'] = sell
        for coin in allCoins:
            send_data(coin.to_json())
            

    except Exception as e:
        send_log(Log_Level.ERROR, f'Error occured: {e}')

if __name__ == "__main__":
    df = pd.read_json('./data/example_input.json')

    handler(df, None)