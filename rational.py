# Модуль: Рациональные числа (дроби)
# Автор: Лунёва Е.П. (гр. 5382)
#
# Представление: Rational = (numerator, denominator)
#   numerator   — целое число (Integer)
#   denominator — натуральное число (Natural), всегда > 0
#
# Пример: дробь -3/4 → ((1, 0, [3]), (0, [4]))

"""
Aвтор модуля: Лунёва Е.П.
"""
from typing import List, Tuple
from natural import GCF_NN_N, LCM_NN_N
from integer import ABS_Z_N, DIV_ZZ_Z, MUL_ZZ_Z, ADD_ZZ_Z, SUB_ZZ_Z, TRANS_N_Z, TRANS_Z_N
Natural = Tuple[int, List[int]]
Integer = Tuple[int, int, List[int]]
Rational = Tuple[Integer, Natural]


def RED_Q_Q(a: Rational) -> Rational:
    """
    Q-1: Сокращение дроби.
    Использует: ABS_Z_N, GCF_NN_N, DIV_ZZ_Z
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
    Q-2: Проверка сокращённой дроби на целое.
    Возвращает: True если знаменатель == 1, иначе False.
    """
    _, denominator = a
    n, A = denominator
    # Знаменатель равен 1, если n=0 и A[0]=1
    return n == 0 and len(A) == 1 and A[0] == 1


def TRANS_Z_Q(a: Integer) -> Rational:
    """
    Q-3: Преобразование целого в дробное.
    """
    # Целое число a представляется как дробь a/1
    return a, (0, [1])


def TRANS_Q_Z(a: Rational) -> Integer:
    """
    Q-4: Преобразование сокращённой дроби в целое (знаменатель == 1).
    """
    numerator, denominator = a
    if not INT_Q_B(a):
        raise ValueError("Дробь не является целым числом (знаменатель != 1)")
    return numerator


def ADD_QQ_Q(a: Rational, b: Rational) -> Rational:
    """
    Q-5: Сложение дробей.
    Использует: LCM_NN_N, MUL_ZZ_Z, ADD_ZZ_Z
    """
    num_a, den_a = a
    num_b, den_b = b

    lcm_den = LCM_NN_N(den_a, den_b)

    mul_a = DIV_ZZ_Z(TRANS_N_Z(lcm_den), TRANS_N_Z(den_a))
    mul_b = DIV_ZZ_Z(TRANS_N_Z(lcm_den), TRANS_N_Z(den_b))

    term1 = MUL_ZZ_Z(num_a, mul_a)
    term2 = MUL_ZZ_Z(num_b, mul_b)
    res_num = ADD_ZZ_Z(term1, term2)

    return RED_Q_Q((res_num, lcm_den))


def SUB_QQ_Q(a: Rational, b: Rational) -> Rational:
    """
    Q-6: Вычитание дробей.
    Использует: LCM_NN_N, MUL_ZZ_Z, SUB_ZZ_Z
    """
    num_a, den_a = a
    num_b, den_b = b

    lcm_den = LCM_NN_N(den_a, den_b)

    mul_a = DIV_ZZ_Z(TRANS_N_Z(lcm_den), TRANS_N_Z(den_a))
    mul_b = DIV_ZZ_Z(TRANS_N_Z(lcm_den), TRANS_N_Z(den_b))

    term1 = MUL_ZZ_Z(num_a, mul_a)
    term2 = MUL_ZZ_Z(num_b, mul_b)
    res_num = SUB_ZZ_Z(term1, term2)

    return RED_Q_Q((res_num, lcm_den))


def MUL_QQ_Q(a: Rational, b: Rational) -> Rational:
    """
    Q-7: Умножение дробей.
    Использует: MUL_ZZ_Z
    """
    num_a, den_a = a
    num_b, den_b = b

    res_num = MUL_ZZ_Z(num_a, num_b)
    res_den = ABS_Z_N(MUL_ZZ_Z(TRANS_N_Z(den_a), TRANS_N_Z(den_b)))

    return RED_Q_Q((res_num, res_den))


def DIV_QQ_Q(a: Rational, b: Rational) -> Rational:
    """
    Q-8: Деление дробей (делитель != 0).
    Использует: MUL_ZZ_Z
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
