import numpy as np
from services.market_data import get_price
from config.settings import COMISIONES

def buy(portfolio, asset, amount):
    price = get_price(asset)
    if price is None:
        return "No price available"

    rate = COMISIONES.get(asset, 0.002)
    commission = amount * rate

    if amount + commission > portfolio.cash:
        return "Insufficient funds"

    shares = amount / price

    portfolio.update_cash(-(amount + commission))
    portfolio.add_position(asset, shares)

    return f"Bought {shares:.2f} shares of {asset}"


def sell(portfolio, asset, shares):
    if asset not in portfolio.positions or portfolio.positions[asset] < shares:
        return "Not enough shares"

    price = get_price(asset)
    if price is None:
        return "No price available"

    value = shares * price

    commission = value * np.random.uniform(0.001, 0.002)

    portfolio.update_cash(value - commission)
    portfolio.remove_position(asset, shares)

    return f"Sold {shares:.2f} shares of {asset}"