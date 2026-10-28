class Deposit:
    def __init__(self, first=0, second=0, years=0):
        self.__first = self.__second = self.__years = 0
        if first: self.first = first
        if second: self.second = second
        if years: self.years = years

    @property
    def first(self): return self.__first
    @first.setter
    def first(self, v):
        if v <= 0: raise ValueError("Сумма должна быть > 0")
        self.__first = v

    @property
    def second(self): return self.__second
    @second.setter
    def second(self, v):
        if v <= 0: raise ValueError("Ставка должна быть > 0")
        self.__second = v

    @property
    def years(self): return self.__years
    @years.setter
    def years(self, v):
        if v <= 0: raise ValueError("Срок должен быть > 0")
        self.__years = v

    def read(self):
        try:
            self.first = float(input("Сумма вклада: "))
            self.second = float(input("Годовая ставка (%): "))
            self.years = float(input("Срок (лет): "))
        except ValueError as e:
            print("Ошибка:", e)

    def display(self):
        print(f"Вклад: {self.first}, Ставка: {self.second}%, Срок: {self.years} лет")

    def final_amount(self):
        return self.first * (1 + self.second / 100) ** self.years

    def profit(self):
        return self.final_amount() - self.first


d = Deposit()
d.read()
d.display()
print(f"Итоговая сумма: {d.final_amount():.2f}")
print(f"Прибыль: {d.profit():.2f}")