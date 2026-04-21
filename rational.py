# Модуль: Рациональные числа (дроби)
# Авторы: <Фамилия И.О. (гр. XXXX)>, <Фамилия И.О. (гр. XXXX)>
#
# Представление: Rational = (numerator, denominator)
#   numerator   — целое число (Integer)
#   denominator — натуральное число (Natural), всегда > 0
#
# Пример: дробь -3/4 → ((1, 0, [3]), (0, [4]))

from typing import List, Tuple
from natural import ABS_Z_N, GCF_NN_N, LCM_NN_N
from integer import DIV_ZZ_Z, MUL_ZZ_Z, ADD_ZZ_Z, SUB_ZZ_Z, TRANS_N_Z, TRANS_Z_N

Natural = Tuple[int, List[int]]
Integer = Tuple[int, int, List[int]]
Rational = Tuple[Integer, Natural]


def RED_Q_Q(a: Rational) -> Rational:
    """
    Q-1: Сокращение дроби.
    Использует: ABS_Z_N, GCF_NN_N, DIV_ZZ_Z
    Автор: <Фамилия И.О.>
    """
    pass


def INT_Q_B(a: Rational) -> bool:
    """
    Q-2: Проверка сокращённой дроби на целое.
    Возвращает: True если знаменатель == 1, иначе False.
    Автор: <Фамилия И.О.>
    """
    pass


def TRANS_Z_Q(a: Integer) -> Rational:
    """
    Q-3: Преобразование целого в дробное.
    Автор: <Фамилия И.О.>
    """
    pass


def TRANS_Q_Z(a: Rational) -> Integer:
    """
    Q-4: Преобразование сокращённой дроби в целое (знаменатель == 1).
    Автор: <Фамилия И.О.>
    """
    pass


def ADD_QQ_Q(a: Rational, b: Rational) -> Rational:
    """
    Q-5: Сложение дробей.
    Использует: LCM_NN_N, MUL_ZZ_Z, ADD_ZZ_Z
    Автор: <Фамилия И.О.>
    """
    pass


def SUB_QQ_Q(a: Rational, b: Rational) -> Rational:
    """
    Q-6: Вычитание дробей.
    Использует: LCM_NN_N, MUL_ZZ_Z, SUB_ZZ_Z
    Автор: <Фамилия И.О.>
    """
    pass


def MUL_QQ_Q(a: Rational, b: Rational) -> Rational:
    """
    Q-7: Умножение дробей.
    Использует: MUL_ZZ_Z
    Автор: <Фамилия И.О.>
    """
    pass


def DIV_QQ_Q(a: Rational, b: Rational) -> Rational:
    """
    Q-8: Деление дробей (делитель != 0).
    Использует: MUL_ZZ_Z
    Автор: <Фамилия И.О.>
    """
    pass
