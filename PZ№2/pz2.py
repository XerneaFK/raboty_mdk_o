class AverageCalculator:
    def __init__(self):
        self.numbers = []

    def get_average(self, *args):
        return sum(args) / len(args) if args else None


calc = AverageCalculator()
print("Введите числа (пустая строка — выход):")

while (s := input("Число: ").strip()):
    try:
        calc.numbers.append(float(s))
    except ValueError:
        print("Это не число!")

avg = calc.get_average(*calc.numbers)
print(f"Среднее: {avg}" if avg is not None else "Числа не введены.")