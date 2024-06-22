from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define cyclical stocks could vary; these are placeholders
        self.tickers = ["GM", "F", "CAT", "DE", "NKE"]
        self.lookback_period = 50  # 50 day SMA for trend determination

    @property
    def interval(self):
        return "1day"  # Using daily data

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        # Intentionally left blank as data required is managed internally
        return []

    def run(self, data):
        allocation_dict = {}

        for ticker in self.tickers:
            ohlcv = data["ohlcv"]
            # Confirm we have enough data to compute SMA
            if len(ohlcv) >= self.lookback_period:
                sma50 = SMA(ticker, ohlcv, self.lookback_period)
                
                if sma50 is not None:
                    current_price = ohlcv[-1][ticker]["close"]
                    if current_price > sma50[-1]:
                        # The market is on an upward trend
                        allocation_dict[ticker] = 1 / len(self.tickers)  # Equally weight stocks
                    else:
                        # Market is in a downturn, hold 50% in cash equivalent by reducing stock allocation
                        allocation_dict[ticker] = 0.5 / len(self.tickers) 
                else:
                    log(f"Unable to compute SMA for {ticker}")
            else:
                log(f"Not enough data for {ticker} to compute SMA")

        return TargetAllocation(allocation_dict)