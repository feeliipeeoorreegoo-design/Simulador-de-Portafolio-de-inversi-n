class Portfolio:
    def __init__(self, initial_cash: float):
        self.cash = initial_cash
        self.positions = {}
        self.history = [initial_cash]

    def add_position(self, asset, shares):
        self.positions[asset] = self.positions.get(asset, 0) + shares

    def remove_position(self, asset, shares):
        if asset in self.positions:
            self.positions[asset] -= shares
            if self.positions[asset] <= 0:
                del self.positions[asset]

    def update_cash(self, amount):
        self.cash += amount