import numpy as np
from sma import get_sma

def get_bollinger_bands(data, rate=2):
    """
    Get the bollinger bands for instrument 
    :param list data: List of instrument closing prices
    :return int upper: Upper bollinger band
    :return int lower: Lower bollinger band
    """
    sma = get_sma(data)
    std = data.rolling(rate).std()
    upper = sma + std * 2 # Calculate top band
    lower = sma - std * 2 # Calculate bottom band

    return upper, lower
