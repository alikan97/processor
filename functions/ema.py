def get_ema(data, days=2, smoothing_value=2):
    """
    Get the exponential moving average, similar to SMA, however uses the previous
    data which performs better for exponential movement
    :param data list: List of closing prices
    :param days int: Rate of day
    :param smoothing_value int: smoothing value
    :return : List of ema values
    """
    first_ema = sum(data[:days])/days # SMA
    ema = [first_ema]
    
    for price in data[days:]:
        ema.append((price * (smoothing_value / (1 + days))) + ema[-1] * (1 - (smoothing_value / (1 + days))))
        
    return ema