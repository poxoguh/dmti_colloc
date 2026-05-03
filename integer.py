# Модуль: Целые числа
# Авторы: <Фамилия И.О. (гр. XXXX)>, <Фамилия И.О. (гр. XXXX)>
#
# Представление: Integer = (sign, n, A)
#   sign — знак: 0 = плюс/ноль, 1 = минус
#   n    — индекс старшей цифры (int)
#   A    — список цифр, A[0] — младшая цифра (List[int])
#
# Пример: число -123 → (1, 2, [3, 2, 1])
#          число  123 → (0, 2, [3, 2, 1])

"""
Aвтор модуля: <>
"""

from typing import List, Tuple
from natural import (
    COM_NN_D, ADD_NN_N, SUB_NN_N,
    MUL_NN_N, DIV_NN_N, ADD_1N_N
)

Natural = Tuple[int, List[int]]
Integer = Tuple[int, int, List[int]]


def ABS_Z_N(a: Integer) -> Natural:
    """
    Z-1: Абсолютная величина целого числа, результат — натуральное.
    """
    pass


def POZ_Z_D(a: Integer) -> int:
    """
    Z-2: Определение положительности числа.
    Возвращает: 2 — положительное, 0 — ноль, 1 — отрицательное.
    """
    pass


def MUL_ZM_Z(a: Integer) -> Integer:
    """
    Z-3: Умножение целого на (-1).
    """
    pass


def TRANS_N_Z(a: Natural) -> Integer:
    """
    Z-4: Преобразование натурального в целое.
    """
    pass


def TRANS_Z_N(a: Integer) -> Natural:
    """
    Z-5: Преобразование целого неотрицательного в натуральное.
    """
    pass


def ADD_ZZ_Z(a: Integer, b: Integer) -> Integer:
    """
    Z-6: Сложение целых чисел.
    Использует: POZ_Z_D, ABS_Z_N, COM_NN_D, ADD_NN_N, SUB_NN_N, MUL_ZM_Z
    """
    pass


def SUB_ZZ_Z(a: Integer, b: Integer) -> Integer:
    """
    Z-7: Вычитание целых чисел.
    Использует: POZ_Z_D, ABS_Z_N, COM_NN_D, ADD_NN_N, SUB_NN_N, MUL_ZM_Z
    """
    pass


def MUL_ZZ_Z(a: Integer, b: Integer) -> Integer:
    """
    Z-8: Умножение целых чисел.
    Использует: POZ_Z_D, ABS_Z_N, MUL_NN_N, MUL_ZM_Z
    """
    pass


def DIV_ZZ_Z(a: Integer, b: Integer) -> Integer:
    """
    Z-9: Частное от деления целого на целое (делитель != 0).
    Использует: ABS_Z_N, POZ_Z_D, DIV_NN_N, ADD_1N_N
    """
    pass


def MOD_ZZ_Z(a: Integer, b: Integer) -> Integer:
    """
    Z-10: Остаток от деления целого на целое (делитель != 0).
    Использует: DIV_ZZ_Z, MUL_ZZ_Z, SUB_ZZ_Z, MUL_ZM_Z
    """
    pass
