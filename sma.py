def get_sma(data, rate=2):
    """
    Get simple moving average
    :param list data: List of close prices for instrument
    :param list data: Window sampling rate
    :return: mean value
    """
    return data.rolling(rate).mean()