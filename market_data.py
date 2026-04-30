import yfinance as yf

def get_price(asset: str):
    data = yf.download(asset, period="1d", progress=False)
    if data.empty:
        return None
    return float(data["Close"].values.flatten()[0])