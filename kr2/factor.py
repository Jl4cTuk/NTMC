# factor.py

import numpy as np
from typing import List

class PolynomialZp:
    def __init__(self, coeffs: List[int], p: int):
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

def factor(coeffs: List[int], p: int) -> str:
    """
    Факторизует полином над полем Z_p и возвращает подробный вывод.

    :param coeffs: Список коэффициентов полинома от старшей к младшей степени.
    :param p: Модуль p для поля Z_p.
    :return: Строка с подробным описанием шагов факторизации.
    """
    f = PolynomialZp(coeffs, p)
    solve = f"Факторизовать многочлен:\n{f} c Z_{p}[x]\n\n"

    n = f.deg()
    solve += f"n = deg(f)\n"
    solve += f"n = {f.deg()}\n\n"
    
    # 1) Построить матрицу Q
    Q = []
    for j in range(n):  # Для каждого j от 0 до n-1
        power_coeffs = [1] + [0] * (p * j)
        x_pj = PolynomialZp(power_coeffs, p)
        tmp = x_pj % f
        solve += f"{j}: {x_pj} mod f(x) = {tmp} -> "

        row = [0] * n
        for i, c in enumerate(tmp.coeffs):
            row[n - len(tmp.coeffs) + i] = c
        solve += f'{row[::-1]}\n'
        Q.append(row[::-1])

    # Итоговая матрица Q
    Q = np.array(Q, dtype=int)
    solve += f"\nМатрица Q:\n{Q}\n"

    # # 2) Найти ранг r = rang(Q - E), k = n - r
    # E = np.eye(n, dtype=int)
    # Q_mod = (Q - E) % p  # Вычитаем единичную матрицу
    # solve += f"\nМатрица Q - E mod {p}:\n{Q_mod}\n"
    
    # Q_transposed = Q_mod.T
    # solve += f"\nМатрица (Q - E)^T:\n{Q_transposed}\n"

    # # Убираем нулевые строки и линейно зависимые строки
    # Q_reduced = Q_transposed[~np.all(Q_transposed == 0, axis=1)]
    # Q_unique = np.unique(Q_reduced, axis=0)
    # solve += f"\nМатрица (Q - E)^T без нулевых и линейно зависимых строк:\n{Q_unique}\n"

    # Вычисляем ранг
    # r = np.linalg.matrix_rank(Q_unique)
    # k = n - r
    # solve += f"\nРанг полученной матрицы: {r}\n"
    # solve += f"r = {r} => k = n - r\n"
    # solve += f"    => k = {n} - {r}\n"
    # solve += f"    => k = {k}\n"

    # Если k = 1 – выход, многочлен неразложим
    # if k == 1:
    #     solve += f"k = 1 - выход, многочлен неразложимый."
    #     return solve
    
    solve += "\nРешение системы не реализовано.\n"

    # Здесь можно добавить реальное решение системы или дальнейшие шаги факторизации

    return solve
