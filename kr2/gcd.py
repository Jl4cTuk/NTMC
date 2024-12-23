# gcd.py

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
        steps = []
        step_num = 1
        while b.coeffs != [0]:
            steps.append(f"Шаг {step_num}:")
            steps.append(f"НОД({a}, {b})")
            quotient = a // b
            remainder = a % b
            steps.append(f"{a} ÷ {b} = {quotient} с остатком {remainder}")
            a, b = b, remainder
            step_num +=1
        steps.append(f"\nНОД = {a}")
        return a, "\n".join(steps)

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

def gcd_polynomials(coeffs1: List[int], coeffs2: List[int], p: int) -> str:
    """
    Вычисляет НОД двух полиномов над полем Z_p и возвращает подробный вывод.
    
    :param coeffs1: Коэффициенты первого полинома от старшей к младшей степени.
    :param coeffs2: Коэффициенты второго полинома от старшей к младшей степени.
    :param p: Модуль p для поля Z_p.
    :return: Строка с подробным описанием шагов вычисления НОД.
    """
    f = PolynomialZp(coeffs1, p)
    g = PolynomialZp(coeffs2, p)
    solve = f"Вычисление НОД двух полиномов:\n"
    solve += f"f(x) = {f}\n"
    solve += f"g(x) = {g}\n\n"
    
    _, steps = f.gcd(g)
    solve += steps
    
    return solve
