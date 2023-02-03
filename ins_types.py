import time

class Guarantee:
    tax_ratio = 0.10

    def __init__(self, name: str, net_price: float) -> None:
        self.name = name
        self.net_price = net_price

    @property
    def price(self):
        return self.net_price * (1 + self.tax_ratio)

    def __str__(self) -> str:
        return f"Guarantee: {self.name}\tPrice: {self.price:.2f}"

    def __repr__(self) -> str:
        return f"Guarantee: {self.name}"

    @classmethod
    def disable_taxes(cls):
        cls.tax_ratio = 0


class Client:
    def __init__(self, name: str, birth_year: int) -> None:
        self.name = name
        self.birth_year = birth_year
        self.ins_products = []

    @property
    def age(self):
        current_year = int(time.strftime('%Y'))
        return current_year - self.birth_year

    def eval_premium(self) -> float:
        premium_2_pay = sum([
            guarantee.price for guarantee in self.ins_products
        ])
        assert premium_2_pay > 0, f'The premium {self.name} has to pay must be positive'
        return premium_2_pay