# Модуль: Многочлены с рациональными коэффициентами
# Авторы: <Фамилия И.О. (гр. XXXX)>, <Фамилия И.О. (гр. XXXX)>
#
# Представление: Polynomial = (m, C)
#   m — степень многочлена (int)
#   C — список коэффициентов типа Rational, C[0] — коэффициент при x^0
#
# Пример: 3/2 * x^2 + 0 * x + 1/4 → (2, [Q(1,4), Q(0,1), Q(3,2)])

"""
Aвтор модуля: <>
"""

from typing import List, Tuple
from natural import LCM_NN_N, GCF_NN_N, TRANS_Z_N
from integer import ABS_Z_N, TRANS_N_Z, DIV_ZZ_Z
from rational import (
    ADD_QQ_Q, SUB_QQ_Q, MUL_QQ_Q, DIV_QQ_Q, RED_Q_Q
)

Natural = Tuple[int, List[int]]
Integer = Tuple[int, int, List[int]]
Rational = Tuple[Integer, Natural]
Polynomial = Tuple[int, List[Rational]]


def ADD_PP_P(a: Polynomial, b: Polynomial) -> Polynomial:
    """
    P-1: Сложение многочленов.
    Использует: ADD_QQ_Q
    """
    pass


def SUB_PP_P(a: Polynomial, b: Polynomial) -> Polynomial:
    """
    P-2: Вычитание многочленов.
    Использует: SUB_QQ_Q
    """
    pass


def MUL_PQ_P(a: Polynomial, q: Rational) -> Polynomial:
    """
    P-3: Умножение многочлена на рациональное число.
    Использует: MUL_QQ_Q
    """
    pass


def MUL_Pxk_P(a: Polynomial, k: int) -> Polynomial:
    """
    P-4: Умножение многочлена на x^k, k — натуральное или 0.
    """
    pass


def LED_P_Q(a: Polynomial) -> Rational:
    """
    P-5: Старший коэффициент многочлена.
    """
    pass


def DEG_P_N(a: Polynomial) -> int:
    """
    P-6: Степень многочлена.
    """
    pass


def FAC_P_Q(a: Polynomial) -> Rational:
    """
    P-7: Вынесение из многочлена НОК знаменателей коэффициентов и НОД числителей.
    Использует: ABS_Z_N, TRANS_Z_N, LCM_NN_N, GCF_NN_N, TRANS_N_Z, DIV_ZZ_Z
    """
    pass


def MUL_PP_P(a: Polynomial, b: Polynomial) -> Polynomial:
    """
    P-8: Умножение многочленов.
    Использует: MUL_PQ_P, MUL_Pxk_P, ADD_PP_P
    """
    pass


def DIV_PP_P(a: Polynomial, b: Polynomial) -> Polynomial:
    """
    P-9: Частное от деления многочлена на многочлен с остатком.
    Использует: DIV_QQ_Q, DEG_P_N, MUL_Pxk_P, SUB_PP_P, ADD_PP_P
    """
    pass


def MOD_PP_P(a: Polynomial, b: Polynomial) -> Polynomial:
    """
    P-10: Остаток от деления многочлена на многочлен с остатком.
    Использует: DIV_PP_P, MUL_PP_P, SUB_PP_P
    """
    pass


def GCF_PP_P(a: Polynomial, b: Polynomial) -> Polynomial:
    """
    P-11: НОД многочленов.
    Использует: DEG_P_N, MOD_PP_P
    """
    pass


def DER_P_P(a: Polynomial) -> Polynomial:
    """
    P-12: Производная многочлена.
    """
    pass


def NMR_P_P(a: Polynomial) -> Polynomial:
    """
    P-13: Преобразование многочлена — кратные корни в простые.
    Использует: GCF_PP_P, DER_P_P, DIV_PP_P
    """
    pass
