# Модуль: Целые числа
# Автор: Гришко С.В (гр. 5385)
#
# Представление: Integer = (sign, n, A)
#   sign — знак: 0 = плюс/ноль, 1 = минус
#   n    — индекс старшей цифры (int)
#   A    — список цифр, A[0] — младшая цифра (List[int])
#
# Пример: число -123 → (1, 2, [3, 2, 1])
#          число  123 → (0, 2, [3, 2, 1])

"""
Автор модуля: Гришко С.В (гр. 5385)
"""

from typing import List, Tuple
from natural import (
    COM_NN_D, ADD_NN_N, SUB_NN_N,
    MUL_NN_N, DIV_NN_N, ADD_1N_N, NZER_N_B
)

Natural = Tuple[int, List[int]]
Integer = Tuple[int, int, List[int]]


def ABS_Z_N(a: Integer) -> Natural:
    """
    Z-1: Абсолютная величина целого числа, результат — натуральное.
    """
    _, n, A = a
    return (n, A.copy())


def POZ_Z_D(a: Integer) -> int:
    """
    Z-2: Определение положительности числа.
    Возвращает: 2 — положительное, 0 — ноль, 1 — отрицательное.
    """
    sign, n, A = a
    # Ноль: индекс 0 и единственная цифра 0
    if n == 0 and A[0] == 0:
        return 0
    return 1 if sign == 1 else 2


def MUL_ZM_Z(a: Integer) -> Integer:
    """
    Z-3: Умножение целого на (-1).
    """
    sign, n, A = a
    # Ноль всегда остаётся со знаком 0
    if n == 0 and A[0] == 0:
        return (0, 0, [0])
    new_sign = 1 - sign
    # Нормализация: убираем ведущие нули
    while n > 0 and A[n] == 0:
        n -= 1
    return (new_sign, n, A[:n + 1].copy())


def TRANS_N_Z(a: Natural) -> Integer:
    """
    Z-4: Преобразование натурального в целое.
    """
    n, A = a
    return (0, n, A.copy())


def TRANS_Z_N(a: Integer) -> Natural:
    """
    Z-5: Преобразование целого неотрицательного в натуральное.
    """
    _, n, A = a
    return (n, A.copy())


def ADD_ZZ_Z(a: Integer, b: Integer) -> Integer:
    """
    Z-6: Сложение целых чисел.
    Использует: POZ_Z_D, ABS_Z_N, COM_NN_D, ADD_NN_N, SUB_NN_N, MUL_ZM_Z
    """
    sign_a, n_a, A_a = a
    sign_b, n_b, A_b = b
    
    # Обработка нуля
    if n_a == 0 and A_a[0] == 0:
        return (sign_b, n_b, A_b.copy())
    if n_b == 0 and A_b[0] == 0:
        return (sign_a, n_a, A_a.copy())
    
    abs_a = ABS_Z_N(a)
    abs_b = ABS_Z_N(b)

    # Одинаковые знаки: складываем модули
    if sign_a == sign_b:
        res_abs = ADD_NN_N(abs_a, abs_b)
        return (sign_a, res_abs[0], list(res_abs[1]))
    
    # Разные знаки: вычитаем меньший модуль из большего
    cmp = COM_NN_D(abs_a, abs_b)
    if cmp == 2:  # |a| > |b|
        res_abs = SUB_NN_N(abs_a, abs_b)
        # Нормализация результата
        n_res = res_abs[0]
        while n_res > 0 and res_abs[1][n_res] == 0:
            n_res -= 1
        if n_res == 0 and res_abs[1][0] == 0:
            return (0, 0, [0])
        return (sign_a, n_res, res_abs[1][:n_res + 1])
    elif cmp == 1:  # |a| < |b|
        res_abs = SUB_NN_N(abs_b, abs_a)
        n_res = res_abs[0]
        while n_res > 0 and res_abs[1][n_res] == 0:
            n_res -= 1
        if n_res == 0 and res_abs[1][0] == 0:
            return (0, 0, [0])
        return (sign_b, n_res, res_abs[1][:n_res + 1])
    else:  # |a| == |b| -> результат 0
        return (0, 0, [0])


def SUB_ZZ_Z(a: Integer, b: Integer) -> Integer:
    """
    Z-7: Вычитание целых чисел.
    Использует: POZ_Z_D, ABS_Z_N, COM_NN_D, ADD_NN_N, SUB_NN_N, MUL_ZM_Z
    """
    # a - b = a + (-b)
    return ADD_ZZ_Z(a, MUL_ZM_Z(b))


def MUL_ZZ_Z(a: Integer, b: Integer) -> Integer:
    """
    Z-8: Умножение целых чисел.
    Использует: POZ_Z_D, ABS_Z_N, MUL_NN_N, MUL_ZM_Z
    """
    sign_a, _, _ = a
    sign_b, _, _ = b
    abs_a = ABS_Z_N(a)
    abs_b = ABS_Z_N(b)

    res_abs = MUL_NN_N(abs_a, abs_b)
    # Знак результата: XOR
    new_sign = sign_a ^ sign_b
    
    # Нормализация: если результат 0, знак должен быть 0
    if res_abs[0] == 0 and res_abs[1][0] == 0:
        return (0, 0, [0])
    return (new_sign, res_abs[0], list(res_abs[1]))


def DIV_ZZ_Z(a: Integer, b: Integer) -> Integer:
    """
    Z-9: Частное от деления целого на целое (делитель != 0).
    Использует: ABS_Z_N, POZ_Z_D, DIV_NN_N, ADD_1N_N
    """
    sign_a, _, _ = a
    sign_b, _, _ = b
    abs_a = ABS_Z_N(a)
    abs_b = ABS_Z_N(b)

    res_abs = DIV_NN_N(abs_a, abs_b)
    new_sign = sign_a ^ sign_b
    
    # Нормализация нуля
    if res_abs[0] == 0 and res_abs[1][0] == 0:
        return (0, 0, [0])
    return (new_sign, res_abs[0], list(res_abs[1]))


def MOD_ZZ_Z(a: Integer, b: Integer) -> Integer:
    """
    Z-10: Остаток от деления целого на целое (делитель != 0).
    Возвращает всегда НЕОТРИЦАТЕЛЬНЫЙ остаток (0 <= r < |b|).
    Использует: DIV_ZZ_Z, MUL_ZZ_Z, SUB_ZZ_Z, ADD_ZZ_Z, ABS_Z_N, TRANS_N_Z
    """
    # 1. Вычисляем остаток по стандартному делению
    q = DIV_ZZ_Z(a, b)
    r = SUB_ZZ_Z(a, MUL_ZZ_Z(b, q))
    
    # 2. Если остаток отрицательный (sign == 1), корректируем: r = r + |b|
    #    (Ноль имеет sign == 0, поэтому проверка точная)
    if r[0] == 1 and not (r[1] == 0 and r[2] == [0]):
        r = ADD_ZZ_Z(r, TRANS_N_Z(ABS_Z_N(b)))
        
    return r
