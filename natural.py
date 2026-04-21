# Модуль: Натуральные числа с нулём
# Авторы: <Фамилия И.О. (гр. XXXX)>, <Фамилия И.О. (гр. XXXX)>
#
# Представление: Natural = (n, A)
#   n — индекс старшей значащей цифры (int)
#   A — список цифр, A[0] — младшая цифра (List[int])
#
# Пример: число 123 → (2, [3, 2, 1])

from typing import List, Tuple

Natural = Tuple[int, List[int]]


def COM_NN_D(a: Natural, b: Natural) -> int:
    """
    N-1: Сравнение натуральных чисел.
    Возвращает: 2 если a > b, 0 если a == b, 1 если a < b.
    Автор: <Фамилия И.О.>
    """
    pass


def NZER_N_B(a: Natural) -> bool:
    """
    N-2: Проверка на ноль.
    Возвращает: True если a != 0, False если a == 0.
    Автор: <Фамилия И.О.>
    """
    pass


def ADD_1N_N(a: Natural) -> Natural:
    """
    N-3: Добавление 1 к натуральному числу.
    Автор: <Фамилия И.О.>
    """
    pass


def ADD_NN_N(a: Natural, b: Natural) -> Natural:
    """
    N-4: Сложение натуральных чисел.
    Использует: COM_NN_D
    Автор: <Фамилия И.О.>
    """
    pass


def SUB_NN_N(a: Natural, b: Natural) -> Natural:
    """
    N-5: Вычитание из первого большего натурального числа второго меньшего или равного.
    Использует: COM_NN_D
    Автор: <Фамилия И.О.>
    """
    pass


def MUL_ND_N(a: Natural, d: int) -> Natural:
    """
    N-6: Умножение натурального числа на цифру d (0 <= d <= 9).
    Автор: <Фамилия И.О.>
    """
    pass


def MUL_Nk_N(a: Natural, k: int) -> Natural:
    """
    N-7: Умножение натурального числа на 10^k, k — натуральное.
    Автор: <Фамилия И.О.>
    """
    pass


def MUL_NN_N(a: Natural, b: Natural) -> Natural:
    """
    N-8: Умножение натуральных чисел.
    Использует: MUL_ND_N, MUL_Nk_N, ADD_NN_N
    Автор: <Фамилия И.О.>
    """
    pass


def SUB_NDN_N(a: Natural, d: int, b: Natural) -> Natural:
    """
    N-9: Вычитание из натурального другого натурального, умноженного на цифру.
    Результат неотрицателен.
    Использует: SUB_NN_N, MUL_ND_N, COM_NN_D
    Автор: <Фамилия И.О.>
    """
    pass


def DIV_NN_Dk(a: Natural, b: Natural, k: int) -> int:
    """
    N-10: Вычисление первой цифры деления большего натурального на меньшее,
    домноженное на 10^k, где k — номер позиции этой цифры.
    Использует: MUL_Nk_N, COM_NN_D
    Автор: <Фамилия И.О.>
    """
    pass


def DIV_NN_N(a: Natural, b: Natural) -> Natural:
    """
    N-11: Неполное частное от деления первого натурального на второе (делитель != 0).
    Использует: DIV_NN_Dk, SUB_NDN_N
    Автор: <Фамилия И.О.>
    """
    pass


def MOD_NN_N(a: Natural, b: Natural) -> Natural:
    """
    N-12: Остаток от деления первого натурального на второе (делитель != 0).
    Использует: DIV_NN_N, SUB_NDN_N
    Автор: <Фамилия И.О.>
    """
    pass


def GCF_NN_N(a: Natural, b: Natural) -> Natural:
    """
    N-13: НОД натуральных чисел.
    Использует: MOD_NN_N, COM_NN_D, NZER_N_B
    Автор: <Фамилия И.О.>
    """
    pass


def LCM_NN_N(a: Natural, b: Natural) -> Natural:
    """
    N-14: НОК натуральных чисел.
    Использует: GCF_NN_N, MUL_NN_N
    Автор: <Фамилия И.О.>
    """
    pass
