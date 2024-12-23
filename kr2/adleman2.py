from sympy import factorint
from sympy.core.numbers import igcd
from copy import deepcopy

def adleman(g, a, n):
    """
    Function to calculate log(a) mod (n-1) using the Adleman algorithm.

    Args:
        a (int): The number for which to find the logarithm.
        n (int): The modulo base.
        g (int): The generator.

    Returns:
        tuple: The value of log(a) mod (n-1) and the detailed log output.
    """
    S = [2, 3, 5]  # Factor base
    output = []

    def log(msg):
        output.append(msg)

    system = []  # To store independent equations
    exponent_matrix = []  # List of exponent vectors
    equations = []  # To store equations for solving

    log(f"1)\nФакторная база: {S}\n\n2)")

    # Helper function to compute modular inverse
    def mod_inverse(a, m):
        """Compute the modular inverse of a modulo m, if it exists."""
        g_val, x, y = extended_gcd(a, m)
        if g_val != 1:
            return None
        else:
            return x % m

    def extended_gcd(a, b):
        """Extended Euclidean Algorithm that returns gcd, x, y such that ax + by = gcd(a, b)"""
        if a == 0:
            return (b, 0, 1)
        else:
            g_val, y, x = extended_gcd(b % a, a)
            return (g_val, x - (b // a) * y, y)

    # Helper function to solve linear system modulo m using Gaussian Elimination
    def solve_modular_linear_system(A, b, m):
        """
        Solves the system of linear equations A * x = b mod m.
        Returns a solution vector x if one exists, otherwise None.
        """
        A = deepcopy(A)
        b = deepcopy(b)
        n_eq = len(A)
        if n_eq == 0:
            return None
        n_vars = len(A[0])

        for i in range(min(n_eq, n_vars)):
            # Find pivot
            pivot_row = -1
            for r in range(i, n_eq):
                if A[r][i] % m != 0 and igcd(A[r][i], m) == 1:
                    pivot_row = r
                    break
            if pivot_row == -1:
                # No pivot in this column, move to next column
                continue
            # Swap pivot row with current row
            A[i], A[pivot_row] = A[pivot_row], A[i]
            b[i], b[pivot_row] = b[pivot_row], b[i]
            # Normalize pivot row
            inv = mod_inverse(A[i][i], m)
            if inv is None:
                # Cannot invert, skip
                continue
            A[i] = [(aij * inv) % m for aij in A[i]]
            b[i] = (b[i] * inv) % m
            # Eliminate pivot column in other rows
            for r in range(n_eq):
                if r != i and A[r][i] != 0:
                    factor = A[r][i]
                    A[r] = [(aij - factor * aik) % m for aij, aik in zip(A[r], A[i])]
                    b[r] = (b[r] - factor * b[i]) % m

        # Check for consistency
        for r in range(n_eq):
            if all(aij == 0 for aij in A[r]) and b[r] != 0:
                return None  # No solution

        # Now, extract solutions
        x = [0] * n_vars
        for i in range(n_vars):
            # Find the row with pivot in column i
            pivot = -1
            for r in range(n_eq):
                if A[r][i] == 1:
                    pivot = r
                    break
            if pivot == -1:
                # Free variable, set to 0
                x[i] = 0
            else:
                x[i] = b[pivot]

        # Verify the solution
        for r in range(n_eq):
            lhs = sum(A[r][c] * x[c] for c in range(n_vars)) % m
            if lhs != b[r]:
                return None  # Invalid solution

        return x

    # Function to calculate the rank of the exponent matrix modulo m
    def calculate_rank(A, m):
        """Calculate the rank of matrix A modulo m."""
        A = deepcopy(A)
        n_eq = len(A)
        if n_eq == 0:
            return 0
        n_vars = len(A[0])

        rank = 0
        for col in range(n_vars):
            pivot = -1
            for row in range(rank, n_eq):
                if A[row][col] % m != 0 and igcd(A[row][col], m) == 1:
                    pivot = row
                    break
            if pivot == -1:
                continue
            # Swap rows
            A[rank], A[pivot] = A[pivot], A[rank]
            # Normalize pivot row
            inv = mod_inverse(A[rank][col], m)
            A[rank] = [(val * inv) % m for val in A[rank]]
            # Eliminate below and above
            for r in range(n_eq):
                if r != rank and A[r][col] != 0:
                    factor = A[r][col]
                    A[r] = [(aij - factor * aik) % m for aij, aik in zip(A[r], A[rank])]
            rank += 1
            if rank == n_vars:
                break
        return rank

    # Step 1: Form the initial system by finding k's that factor over S
    max_k = n  # To prevent infinite loops
    for k in range(1, max_k):
        val = pow(g, k, n)
        factors = factorint(val)

        # Check if all factors are in the factor base and value is unique
        if all(prime in S for prime in factors.keys()) and val not in [eq[0] for eq in system] and factors:
            # Create the exponent vector
            exponents = [factors.get(p, 0) for p in S]

            # Tentatively add the new equation
            temp_system = deepcopy(system) + [(val, k, factors)]
            temp_A = [[eq[2].get(p, 0) for p in S] for eq in temp_system]
            temp_b = [eq[1] for eq in temp_system]

            # Check the rank before adding
            current_rank = calculate_rank(temp_A, n-1)
            previous_rank = calculate_rank(exponent_matrix, n-1)
            if current_rank > previous_rank:
                # Independent equation
                system.append((val, k, factors))
                exponent_matrix.append(exponents)
                factor_terms = " + ".join([f"{power}*log{prime}" for prime, power in factors.items()])
                log(f"Возьмём случайное k = {k}: b = {g}^{k} = {val} mod {n} => log{val} = {factor_terms} = {k}")
                equations.append((exponents, k))

                log(f"Добавлено уравнение: log({val}) = {factor_terms} = {k}")

                # Check if the system has full rank
                if calculate_rank(exponent_matrix, n-1) == len(S):
                    log(f"\nДостигнут полный ранг системы уравнений (ранг = {len(S)}).")
                    break
            else:
                log(f"Уравнение для k = {k} линейно зависимо и не добавлено.")

    # Step 2: Log the formed system
    log(f"\nПолучили систему уравнений:")
    for val, k, factors in system:
        factor_breakdown = " + ".join(
            [f"{power}*log{prime}" for prime, power in factors.items()]
        )
        log(f"log({val}) = {k} ({factor_breakdown})")

    # Step 3: Solve the system and log the process
    log(f"\n3)\nРешаем систему уравнений для нахождения логарифмов:")
    A = []
    b_vector = []
    for exponents, k in equations:
        A.append(exponents)
        b_vector.append(k)

    mat_A = A
    vec_b = b_vector
    m = n - 1

    log("Составлена матрица коэффициентов (A) и вектор правых частей (b):")
    log(f"A =")
    for row in mat_A:
        log(f"    {row}")
    log(f"b =")
    for val in vec_b:
        log(f"    {val}")

    # Solve the system using the helper function
    solution = solve_modular_linear_system(mat_A, vec_b, m)

    if solution is None:
        log("Не удалось решить систему уравнений.")
        return None, "\n".join(output)

    # Assign log2, log3, log5 based on the factor base order
    logs = {}
    for i, prime in enumerate(S):
        logs[prime] = solution[i]
        log(f"log({prime}) = {solution[i]}")

    # Compute log(g) using its factorization over S
    factors_g = factorint(g)
    if all(p in S for p in factors_g):
        log_g = sum(logs[p] * power for p, power in factors_g.items()) % m
        factor_terms_g = " + ".join([f"{power}*log{p}" for p, power in factors_g.items()])
        # log(f"log({g}) = {factor_terms_g} = {log_g} mod {m}")
    else:
        log(f"Генератор g = {g} не раскладывается по факторной базе S = {S}.")
        return None, "\n".join(output)

    # Step 4: Compute log(a)
    log("\n4) Вычисляем log(a):")

    log_a = None

    # Увеличим диапазон поиска k, чтобы найти раскладывающиеся значения
    for k in range(1, n):
        product = (a * pow(g, k, n)) % n  # a * g^k 
        factors = factorint(product)

        all_in_S = all(prime in S for prime in factors.keys())
        if all_in_S:
            log(f"k = {k}: {a} * {g}^{k} = {product} mod {n}, раскладывается в S")
        else:
            log(f"k = {k}: {a} * {g}^{k} = {product} mod {n}, не раскладывается в S")

        if all_in_S:
            # Выражаем log(a) через log(product) и log(g)
            # log(a * g^k) = log(a) + k*log(g) = sum(power * log(prime)) 
            # Отсюда log(a) = sum(power * log(prime)) - k*log(g) mod m

            log_a_expr = 0
            str1 = ""
            str2 = ""

            for prime, power in factors.items():
                str1 += f"{power}*log{prime} + "
                if prime in logs:
                    log_a_expr += logs[prime] * power
                    str2 += f"{power}*{logs[prime]} + "

            log_a_expr -= k * log_g
            log_a = log_a_expr % m

            log(f"log({a}) + {k}*log({g}) = {str1[:-3]} mod {m}")
            log(f"Переходим к значениям логарифмов:")
            log(f"log({a}) + {k}*{log_g} = {str2[:-3]} mod {m}")
            log(f"Сокращаем и переносим")
            log(f"log({a}) = ({str2[:-3]}) - {k}*{log_g} mod {m} = {log_a} mod {m}")
            log(f"Ответ: {log_a}")

            return log_a, "\n".join(output)

    log("Не найдено подходящее значение k для вычисления log(a).")
    return None, "\n".join(output)

# Пример использования
# g = 6
# a = 14
# n = 109

# g = 2
# a = 13
# n = 37

g = 2
a = 7
n = 61

result, log_output = adleman(g, a, n)
print(log_output)
