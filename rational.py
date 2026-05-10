# Модуль: Рациональные числа (дроби)
# Автор: <Лунёва Е.П. (гр. 5382)>
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
    Автор: <Лунёва Е.П.>
    """
    numerator, denominator = a
    
    # Находим НОД модуля числителя и знаменателя
    abs_numerator = ABS_Z_N(numerator)
    gcd = GCF_NN_N(abs_numerator, denominator)
    
    # Сокращаем дробь, деля числитель и знаменатель на НОД
    new_numerator = DIV_ZZ_Z(numerator, TRANS_N_Z(gcd))
    new_denominator = DIV_ZZ_Z(TRANS_N_Z(denominator), TRANS_N_Z(gcd))[1]  # берём только натуральную часть
    
    return new_numerator, new_denominator


def INT_Q_B(a: Rational) -> bool:
    """
    Q-2: Проверка сокращённой дроби на целое.
    Возвращает: True если знаменатель == 1, иначе False.
    Автор: <Лунёва Е.П.>
    """
    _, denominator = a
    n, A = denominator
    # Знаменатель равен 1, если n=0 и A[0]=1
    return n == 0 and len(A) == 1 and A[0] == 1


def TRANS_Z_Q(a: Integer) -> Rational:
    """
    Q-3: Преобразование целого в дробное.
    Автор: <Лунёва Е.П.>
    """
    # Целое число a представляется как дробь a/1
    return a, (0, [1])


def TRANS_Q_Z(a: Rational) -> Integer:
    """
    Q-4: Преобразование сокращённой дроби в целое (знаменатель == 1).
    Автор: <Лунёва Е.П.>
    """
    numerator, denominator = a
    if not INT_Q_B(a):
        raise ValueError("Дробь не является целым числом (знаменатель != 1)")
    return numerator


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
