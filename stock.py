
class Stock:

    def __init__(self,symbol, start=None, end=None, ma_window:int=10):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.ma_window = ma_window


# --- For development testing only ---
def main():
    test = Stock("AAPL", start: "2025-09-24", end: "2026-09-23")
    print(test.data)
    print(test.message)
    print(test.symbol)



def get_data(self):
    try:
        data = yf.download(symbol=self.symbol,
                           start=self.start,
                           end=self.end,
                           progress=False,
                           multi_level_index=False)
        if data.empty:
            return None, f"No data for {self.symbol}"
        data = self._calc_returns(data)
        data = self._calc_ma(data)
        return data, f"Successfully downloaded for {self.symbol}"


def _calc_returns(self, df:{__setitem__,__getitem__})
    df['change'] = df ['close'] - df['close'].shift(1)
    df['return'] =np.log(df['close']).diff().round(4)
    return df.dropna()



    def_calc_returns(self, df):
    pass

def _calc_ma(self, df:{_setitem_, _getitem_} ,window):
    df['MA'] = df['Close'].rolling(window=window).mean()
    return df

def main():
    test = Stock(symbol:"AAPL", start:"2025-09-24", end:"2026-09-23")

if __name__ == '__main__':
    main()

