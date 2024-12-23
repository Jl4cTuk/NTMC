class PolynomialZp:
    def __init__(self, coeffs, p):
        # Храним коэффициенты от старшей степени к младшей
        self.coeffs = [c % p for c in coeffs]
        self.p = p
        # Удаляем ведущие нули
        while len(self.coeffs) > 1 and self.coeffs[0] == 0:
            self.coeffs.pop(0)

    def __str__(self):
        terms = []
        degree = len(self.coeffs) - 1
        for i, c in enumerate(self.coeffs):
            if c == 0:
                continue
            power = degree - i
            if power == 0:
                terms.append(str(c))
            elif power == 1:
                terms.append(f"{'' if c == 1 else c}x")
            else:
                terms.append(f"{'' if c == 1 else c}x^{power}")
        return " + ".join(terms) or "0"

    def deg(self):
        return len(self.coeffs) - 1

    def derivative(self):
        """Вычисление производной полинома."""
        degree = len(self.coeffs) - 1
        derived_coeffs = [((degree - i) * c) % self.p for i, c in enumerate(self.coeffs[:-1])]
        return PolynomialZp(derived_coeffs, self.p)

    def gcd(self, other):
        """Вычисление НОД двух полиномов."""
        a, b = self, other
        while b.coeffs != [0]:
            a, b = b, a % b
        return a

    def __mod__(self, other):
        """Операция деления по модулю полинома."""
        divisor_degree = len(other.coeffs) - 1
        result = self.coeffs[:]
        while len(result) >= len(other.coeffs) and result:
            scale = result[0] * pow(other.coeffs[0], -1, self.p) % self.p
            for i in range(len(other.coeffs)):
                result[i] = (result[i] - scale * other.coeffs[i]) % self.p
            result.pop(0)  # Удаляем старший коэффициент
        return PolynomialZp(result, self.p) if result else PolynomialZp([0], self.p)

    def __floordiv__(self, other):
        """Целочисленное деление полиномов."""
        quotient = []
        remainder = self.coeffs[:]
        while len(remainder) >= len(other.coeffs):
            scale = remainder[0] * pow(other.coeffs[0], -1, self.p) % self.p
            quotient.append(scale)
            for i in range(len(other.coeffs)):
                remainder[i] = (remainder[i] - scale * other.coeffs[i]) % self.p
            remainder.pop(0)
        return PolynomialZp(quotient, self.p)


def square_free_decomposition(f):
    solve = f"\nСчитаем для f(x) = {f}\n"
    factors = []  # Список для хранения множителей

    # 1) Если deg f(x) < 2 – выход. Ответ: f(x)
    if f.deg() < 2:
        solve += f"deg f(x) = {f.deg()} < 2\n"
        solve += f"Ответ: f(x) = {f}\n"
        factors.append(f)
        return factors, solve

    solve += f"deg f(x) = {f.deg()} ≥ 2\n"

    # 2) Вычислить g(x) = f'(x)
    g = f.derivative()
    solve += f"g(x) = f'(x) = {g}\n"

    # 3) Если g(x) = 0, то f(x) = (v(x))^p
    if g.coeffs == [0]:
        if all((len(f.coeffs) - 1 - i) % f.p == 0 for i, c in enumerate(f.coeffs) if c != 0):
            v_coeffs = [f.coeffs[i] for i in range(0, len(f.coeffs), f.p)]
            v = PolynomialZp(v_coeffs, f.p)
            solve += f"g(x) = 0, значит f(x) = (v(x))^{f.p}\n"
            solve += f"v(x) = {v}\n"
            sub_factors, sub_solve = square_free_decomposition(v)
            solve += sub_solve
            factors.extend(sub_factors * f.p)  # Учитываем кратность p
            return factors, solve
        else:
            raise ValueError("Степени не делятся на p — невозможно корректно извлечь корень.")

    solve += f"g(x) ≠ 0\n"

    # 4) Вычислить d(x) = НОД(g(x), f(x))
    d = f.gcd(g)
    solve += f"d(x) = НОД(f(x), g(x)) = {d}\n"

    # Если d(x) = 1 – добавить только f(x) как множитель
    if d.coeffs == [1]:
        solve += "d(x) = 1, значит f(x) свободен от квадратов.\n"
        factors.append(f)
        return factors, solve

    solve += f"d(x) ≠ 1\n"

    # 5) Иначе получить разложение f(x) = d(x) * h(x)
    h = f // d
    solve += f"f(x) = d(x) * h(x), где d(x) = {d}, h(x) = {h}\n"

    # Рекурсивно разложить d(x), h(x) не анализируется
    d_factors, d_solve = square_free_decomposition(d)
    solve += d_solve

    factors.extend(d_factors)
    factors.append(h)
    return factors, solve


def solve_polynomial(coeffs, p):
    """
    Разлагает полином на свободные квадраты над полем Z_p и возвращает подробный вывод.

    :param coeffs: Список коэффициентов полинома от старшей к младшей степени.
    :param p: Модуль p для поля Z_p.
    :return: Строка с подробным описанием шагов разложения.
    """
    f = PolynomialZp(coeffs, p)
    _, solve_steps = square_free_decomposition(f)
    return solve_steps


# Пример использования функции:
if __name__ == "__main__":
    # Пример полинома: x^5 + 2x^3 + x + 1 ∈ Z_3[x]
    p = 3
    coef = [1, 0, 2, 0, 1, 1]  # Соответствует 1*x^5 + 0*x^4 + 2*x^3 + 0*x^2 + 1*x + 1

    # Получаем подробное разложение
    detailed_steps = solve_polynomial(coef, p)

    # Выводим результат
    print("Шаги вычисления:")
    print(detailed_steps)
