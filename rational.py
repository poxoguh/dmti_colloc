# Модуль: Рациональные числа (дроби)
# Автор: Лунёва Е.П. (гр. 5382)
#
# Представление: Rational = (numerator, denominator)
#   numerator   — целое число (Integer)
#   denominator — натуральное число (Natural), всегда > 0
#
# Пример: дробь -3/4 → ((1, 0, [3]), (0, [4]))

"""
@file rational.py
@brief Реализация модуля Q (рациональные числа).
@author Лунёва Е.П. (гр. 5382)
"""

from typing import List, Tuple
from natural import GCF_NN_N, LCM_NN_N
from integer import ABS_Z_N, DIV_ZZ_Z, MUL_ZZ_Z, ADD_ZZ_Z, SUB_ZZ_Z, TRANS_N_Z, TRANS_Z_N

Natural = Tuple[int, List[int]]
Integer = Tuple[int, int, List[int]]
Rational = Tuple[Integer, Natural]


def RED_Q_Q(a: Rational) -> Rational:
    """
    @brief Q-1: Сокращение дроби.
    @param a Дробь
    @return Сокращённая дробь
    @note Использует: ABS_Z_N, GCF_NN_N, DIV_ZZ_Z
    """
    numerator, denominator = a

    #  1. Защита от краха при нулевом числителе или знаменателе
    if numerator == (0, 0, [0]) or denominator == (0, [0]):
        return ((0, 0, [0]), (0, [1]))

    # 2. Находим НОД модуля числителя и знаменателя
    abs_numerator = ABS_Z_N(numerator)
    gcd = GCF_NN_N(abs_numerator, denominator)

    # 3. Сокращаем дробь
    new_numerator = DIV_ZZ_Z(numerator, TRANS_N_Z(gcd))
    new_denominator = TRANS_Z_N(DIV_ZZ_Z(TRANS_N_Z(denominator), TRANS_N_Z(gcd)))
    return new_numerator, new_denominator


def INT_Q_B(a: Rational) -> bool:
    """
    @brief Q-2: Проверка сокращённой дроби на целое.
    @param a Дробь
    @return True если знаменатель == 1, иначе False
    """
    _, denominator = a
    n, A = denominator
    # Знаменатель равен 1, если n=0 и A[0]=1
    return n == 0 and len(A) == 1 and A[0] == 1


def TRANS_Z_Q(a: Integer) -> Rational:
    """
    @brief Q-3: Преобразование целого в дробное.
    @param a Целое число
    @return Рациональное число
    """
    # Целое число a представляется как дробь a/1
    return a, (0, [1])


def TRANS_Q_Z(a: Rational) -> Integer:
    """
    @brief Q-4: Преобразование сокращённой дроби в целое.
    @param a Дробь
    @return Целое число
    @note Знаменатель должен быть равен 1
    """
    numerator, denominator = a
    if not INT_Q_B(a):
        raise ValueError("Дробь не является целым числом (знаменатель != 1)")
    return numerator


def ADD_QQ_Q(a: Rational, b: Rational) -> Rational:
    """
    @brief Q-5: Сложение дробей.
    @param a Первая дробь
    @param b Вторая дробь
    @return Сумма дробей
    @note Использует: LCM_NN_N, MUL_ZZ_Z, ADD_ZZ_Z
    """
    num_a, den_a = a
    num_b, den_b = b

    # Находим НОК
    lcm_den = LCM_NN_N(den_a, den_b)

    # Дополнительные множители для числителей
    mul_a = DIV_ZZ_Z(TRANS_N_Z(lcm_den), TRANS_N_Z(den_a))
    mul_b = DIV_ZZ_Z(TRANS_N_Z(lcm_den), TRANS_N_Z(den_b))

    # Домножаем числители на дополнительные множители и складываем их
    term1 = MUL_ZZ_Z(num_a, mul_a)
    term2 = MUL_ZZ_Z(num_b, mul_b)
    res_num = ADD_ZZ_Z(term1, term2)

    return RED_Q_Q((res_num, lcm_den))


def SUB_QQ_Q(a: Rational, b: Rational) -> Rational:
    """
    @brief Q-6: Вычитание дробей.
    @param a Первая дробь
    @param b Вторая дробь
    @return Разность дробей
    @note Использует: LCM_NN_N, MUL_ZZ_Z, SUB_ZZ_Z
    """
    num_a, den_a = a
    num_b, den_b = b

    # Находим НОК
    lcm_den = LCM_NN_N(den_a, den_b)

    # Дополнительные множители для числителей
    mul_a = DIV_ZZ_Z(TRANS_N_Z(lcm_den), TRANS_N_Z(den_a))
    mul_b = DIV_ZZ_Z(TRANS_N_Z(lcm_den), TRANS_N_Z(den_b))

    # Домножаем числители на дополнительные множители и вычитаем их
    term1 = MUL_ZZ_Z(num_a, mul_a)
    term2 = MUL_ZZ_Z(num_b, mul_b)
    res_num = SUB_ZZ_Z(term1, term2)

    return RED_Q_Q((res_num, lcm_den))


def MUL_QQ_Q(a: Rational, b: Rational) -> Rational:
    """
    @brief Q-7: Умножение дробей.
    @param a Первая дробь
    @param b Вторая дробь
    @return Произведение дробей
    @note Использует: MUL_ZZ_Z
    """
    num_a, den_a = a
    num_b, den_b = b

    res_num = MUL_ZZ_Z(num_a, num_b)
    res_den = ABS_Z_N(MUL_ZZ_Z(TRANS_N_Z(den_a), TRANS_N_Z(den_b)))

    return RED_Q_Q((res_num, res_den))


def DIV_QQ_Q(a: Rational, b: Rational) -> Rational:
    """
    @brief Q-8: Деление дробей.
    @param a Делимое (дробь)
    @param b Делитель (дробь, != 0)
    @return Частное от деления
    @note Использует: MUL_ZZ_Z
    """
    num_a, den_a = a
    num_b, den_b = b

    # Проверка делителя на ноль
    if num_b[1] == 0 and num_b[2] == [0]:
        raise ZeroDivisionError("Деление на ноль запрещено")

    res_num = MUL_ZZ_Z(num_a, TRANS_N_Z(den_b))
    res_den = ABS_Z_N(MUL_ZZ_Z(TRANS_N_Z(den_a), num_b))

    if num_b[0] == 1:  # sign == 1 означает отрицательное число
        # Если результат не ноль, меняем знак (0 ↔ 1)
        if not (res_num[1] == 0 and res_num[2] == [0]):
            res_num = (1 - res_num[0], res_num[1], res_num[2])

    return RED_Q_Q((res_num, res_den))
