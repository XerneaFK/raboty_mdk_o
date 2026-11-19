"""ПЗ №3 — Тема 2: IT Asset."""
from dataclasses import dataclass, field


class InvalidPriceError(ValueError): ...
class InvalidMonthsError(ValueError): ...
class AssetLimitExceededError(Exception): ...


@dataclass
class ITAsset:
    """Единица техники с линейной амортизацией."""
    name: str
    inventory_id: str
    initial_price: float
    months_used: int = 0
    lifetime_months: int = field(default=0, init=False, repr=False)

    def __post_init__(self):
        # dataclass сам не валидирует — проверяем здесь
        if self.initial_price <= 0:
            raise InvalidPriceError(f"Цена должна быть > 0, получено {self.initial_price}")
        if self.months_used < 0:
            raise InvalidMonthsError(f"Месяцы должны быть >= 0, получено {self.months_used}")

    def calculate_residual_value(self) -> float:
        return self.initial_price * max(0.0, 1 - self.months_used / self.lifetime_months)

    def __str__(self):
        return f"{type(self).__name__} «{self.name}»: {self.calculate_residual_value():.0f} ₽"

    def __eq__(self, other):
        return isinstance(other, ITAsset) and self.inventory_id == other.inventory_id

    def __lt__(self, other):
        return self.calculate_residual_value() < other.calculate_residual_value()

    def __add__(self, other):
        return self.calculate_residual_value() + other.calculate_residual_value()

    def __sub__(self, months: int):
        # возвращаем новый объект, не мутируем исходный
        if months < 0:
            raise InvalidMonthsError(months)
        return type(self)(self.name, self.inventory_id,
                          self.initial_price, self.months_used + months)


class Laptop(ITAsset):     lifetime_months = 36
class Monitor(ITAsset):    lifetime_months = 60
class Smartphone(ITAsset): lifetime_months = 24


class AssetWarehouse:
    LIMIT = 150_000

    def __init__(self, owner):
        self.owner = owner
        self._assets = []

    def total(self):
        return sum(a.calculate_residual_value() for a in self._assets)

    def add(self, asset):
        if self.total() + asset.calculate_residual_value() > self.LIMIT:
            raise AssetLimitExceededError(
                f"Лимит {self.LIMIT} ₽ превышен: "
                f"{self.total() + asset.calculate_residual_value():.0f} ₽"
            )
        self._assets.append(asset)

    def __len__(self):
        return len(self._assets)

    def __getitem__(self, i):
        return self._assets[i]

    def __str__(self):
        body = "\n".join(f"  • {a}" for a in self._assets)
        return f"Склад {self.owner}:\n{body}\n  ИТОГО: {self.total():.0f} ₽"


if __name__ == "__main__":
    laptop = Laptop("ThinkPad", "INV-1", 80_000, 18)
    monitor = Monitor("Dell", "INV-2", 25_000, 12)
    phone = Smartphone("iPhone", "INV-3", 40_000, 6)

    print("Полиморфизм:")
    for a in (laptop, monitor, phone):
        print(f"  {a}")

    print("\nМагические методы:")
    print("  eq:", laptop == Laptop("ThinkPad", "INV-1", 80_000, 18))
    print("  lt:", laptop < phone)
    print("  add:", f"{laptop + phone:.0f} ₽")
    print("  sub:", laptop - 6)

    wh = AssetWarehouse("Иванов")
    for a in (laptop, monitor, phone):
        wh.add(a)
    print(f"\nlen = {len(wh)}, [0] = {wh[0]}")

    print("\nСортировка:")
    for a in sorted(wh):
        print(f"  {a}")

    print("\nИсключения:")
    for fn in [
        lambda: Laptop("X", "X", -1000),
        lambda: Monitor("Y", "Y", 10_000, -3),
        lambda: wh.add(Laptop("New", "INV-4", 80_000, 0)),
    ]:
        try:
            fn()
        except (InvalidPriceError, InvalidMonthsError, AssetLimitExceededError) as e:
            print(f"  ✗ {type(e).__name__}: {e}")