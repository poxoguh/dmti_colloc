# Модуль: Натуральные числа с нулём
# Автор: <Красносельских Н.М. (гр. 5382)>
#
# Представление: Natural = (n, A)
#   n — индекс старшей значащей цифры (int)
#   A — список цифр, A[0] — младшая цифра (List[int])
#
# Пример: число 123 → (2, [3, 2, 1])

"""
@file natural.py
@brief Реализация модуля N (натуральные числа с нулём).
@author Красносельских Н.М. (гр. 5382)
"""

from typing import List, Tuple

Natural = Tuple[int, List[int]]


def COM_NN_D(a: Natural, b: Natural) -> int:
    """
    @brief N-1: Сравнение натуральных чисел.
    @param a Первое натуральное число
    @param b Второе натуральное число
    @return 2 если a > b, 0 если a == b, 1 если a < b
    """
    na, Aa = a
    nb, Ab = b

    # Сравнение длины чисел, число с большим разрядом всегда больше
    if na > nb:
        return 2
    if na < nb:
        return 1

    # Если длины равны, идем поразрядно от старших к младшим индексам
    for i in range(na, -1, -1):
        if Aa[i] > Ab[i]:
            return 2
        if Aa[i] < Ab[i]:
            return 1

    return 0


def NZER_N_B(a: Natural) -> bool:
    """
    @brief N-2: Проверка на ноль.
    @param a Натуральное число
    @return True если a != 0, False если a == 0
    """
    _, A = a
    return any(d != 0 for d in A) # True если есть хоть один элемент != 0


def ADD_1N_N(a: Natural) -> Natural:
    """
    @brief N-3: Добавление 1 к натуральному числу.
    @param a Натуральное число
    @return Результат прибавления единицы
    """
    n, A = a
    res = A.copy()
    carry = 1

    for i in range(len(res)):
        res[i] += carry
        # Если разряд переполняется, сбрасываем его в 0, оставляем перенос = 1
        if res[i] >= 10:
            res[i] = 0
            carry = 1
        else:
            carry = 0
            break

    # Если перенос остался, добавляем единицу в начало числа (т.е. конец списка)
    if carry:
        res.append(1)
        n += 1
    else:
        n = len(res) - 1

    return n, res



def ADD_NN_N(a: Natural, b: Natural) -> Natural:
    """
    @brief N-4: Сложение натуральных чисел.
    @param a Первое натуральное число
    @param b Второе натуральное число
    @return Сумма натуральных чисел
    @note Использует: COM_NN_D
    """
    na, Aa = a
    nb, Ab = b
    max_n = max(na, nb)
    res = [0] * (max_n + 2)  # +2 на случай переноса
    carry = 0  # Перенос для сложения

    # Сложение столбиком - идём от младших разрядов к старшим
    for i in range(max_n + 1):
        # Если разряды кончились, подставляем 0
        va = Aa[i] if i <= na else 0
        vb = Ab[i] if i <= nb else 0
        s = va + vb + carry
        res[i] = s % 10 # Текущий разряд
        carry = s // 10 # Перенос

    if carry:
        res[max_n + 1] = carry
        final_n = max_n + 1
    else:
        final_n = max_n

    # Убираем ведущие нули
    while final_n > 0 and res[final_n] == 0:
        final_n -= 1

    return final_n, res[:final_n + 1]


def SUB_NN_N(a: Natural, b: Natural) -> Natural:
    """
    @brief N-5: Вычитание из первого большего натурального числа второго меньшего или равного.
    @param a Первое натуральное число (должно быть >= b)
    @param b Второе натуральное число
    @return Разность натуральных чисел
    @note Использует: COM_NN_D
    """
    if COM_NN_D(a, b) == 1:
        raise ValueError("Первое число должно быть >= второго")

    na, Aa = a
    nb, Ab = b
    res = Aa.copy()
    borrow = 0

    # Вычитание столбиком
    for i in range(nb + 1):
        res[i] -= (Ab[i] + borrow)
        # Если отрицательный, занимаем 10 из следующего старшего разряда
        if res[i] < 0:
            res[i] += 10
            borrow = 1
        else:
            borrow = 0

    # Если остался borrow = 1, продолжаем идти по числу a, вычитая borrow
    for i in range(nb + 1, na + 1):
        res[i] -= borrow
        if res[i] < 0: # Занимаем 10
            res[i] += 10
            borrow = 1
        else:
            borrow = 0

    # Уменьшаем длину, пока в начале числа (конце res) есть ведущие нули
    final_n = na
    while final_n > 0 and res[final_n] == 0:
        final_n -= 1

    # Нормализуем число с учетом новой длины
    return final_n, res[:final_n + 1]


def MUL_ND_N(a: Natural, d: int) -> Natural:
    """
    @brief N-6: Умножение натурального числа на цифру d (0 <= d <= 9).
    @param a Натуральное число
    @param d Цифра (0-9)
    @return Произведение числа на цифру
    """
    if d == 0: # Умножение на 0
        return 0, [0]

    n, A = a
    res = [0] * (n + 2) # +2 на случай переноса
    carry = 0

    # Проходим по всем разрядам, умножая на d
    for i in range(n + 1):
        prod = A[i] * d + carry
        res[i] = prod % 10 # Текущий разряд
        carry = prod // 10 # Перенос

    if carry:
        res[n + 1] = carry
        final_n = n + 1
    else:
        final_n = n

    # Нормализуем
    while final_n > 0 and res[final_n] == 0:
        final_n -= 1

    return final_n, res[:final_n + 1]


def MUL_NK_N(a: Natural, k: int) -> Natural:
    """
    @brief N-7: Умножение натурального числа на 10^k.
    @param a Натуральное число
    @param k Показатель степени (натуральное или 0)
    @return Результат умножения на 10^k
    """
    if k == 0:
        return a
    n, A = a
    # Явная обработка нуля: 0 * 10^k всегда остаётся 0 в канонической форме
    if n == 0 and A == [0]:
        return (0, [0])
    return n + k, [0] * k + A # Добавляем k нулей в конец числа


def MUL_NN_N(a: Natural, b: Natural) -> Natural:
    """
    @brief N-8: Умножение натуральных чисел.
    @param a Первое натуральное число
    @param b Второе натуральное число
    @return Произведение натуральных чисел
    @note Использует: MUL_ND_N, MUL_Nk_N, ADD_NN_N
    """
    nb, Ab = b
    res = 0, [0]

    # Умножение столбиком
    for i in range(nb + 1):
        if Ab[i] != 0:
            term = MUL_ND_N(a, Ab[i]) # Умножаем
            term_shifted = MUL_NK_N(term, i) # Смещаем
            res = ADD_NN_N(res, term_shifted) # Суммируем в res

    return res


def SUB_NDN_N(a: Natural, d: int, b: Natural) -> Natural:
    """
    @brief N-9: Вычитание из натурального другого натурального, умноженного на цифру.
    @param a Натуральное число (уменьшаемое)
    @param d Цифра (множитель)
    @param b Натуральное число (вычитаемое)
    @return Результат вычитания: a - d * b (неотрицательный)
    @note Использует: SUB_NN_N, MUL_ND_N, COM_NN_D
    """
    prod = MUL_ND_N(b, d)
    if COM_NN_D(a, prod) == 1:
        raise ValueError("Результат вычитания должен быть неотрицательным")
    return SUB_NN_N(a, prod)


def DIV_NN_DK(a: Natural, b: Natural, k: int) -> int:
    """
    @brief N-10: Вычисление первой цифры деления большего натурального на меньшее, домноженное на 10^k.
    @param a Делимое (натуральное число)
    @param b Делитель (натуральное число)
    @param k Позиция цифры в результате (степень сдвига)
    @return Первая цифра частного (0-9)
    @note Использует: MUL_Nk_N, COM_NN_D
    """
    # Смещаем b на k так, чтобы у них было одно количество разрядов. k определяется в DIV_NN_N
    b_shifted = MUL_NK_N(b, k)
    # Подбираем цифру от 9 до 0, при умножении на которую делитель не превысит делимого
    for q in range(9, -1, -1):
        prod = MUL_ND_N(b_shifted, q)
        if COM_NN_D(a, prod) != 1:
            return q
    return 0  # На случай, если ничего не подошло


def DIV_NN_N(a: Natural, b: Natural) -> Natural:
    """
    @brief N-11: Неполное частное от деления.
    @param a Делимое (натуральное число)
    @param b Делитель (натуральное число, != 0)
    @return Целая часть от деления a / b
    """
    if not NZER_N_B(b):
        raise ValueError("Делитель не может быть равен нулю")
    if COM_NN_D(a, b) == 1:
        return 0, [0]

    na, _ = a
    nb, _ = b
    max_k = na - nb # Максимальная степень сдвига, разница длины чисел
    quotient = [0] * (max_k + 1)
    remainder = a

    # Основной цикл, деление уголком. Двигаемся от старших разрядов к младшим
    for k in range(max_k, -1, -1):
        b_shifted = MUL_NK_N(b, k)
        # Если текущий остаток меньше сдвинутого делителя, значит цифра частного = 0
        if COM_NN_D(remainder, b_shifted) == 1:
            quotient[k] = 0
        # Иначе ищем цифру перебором (т.е. функцией DIV_NN_DK)
        else:
            q = DIV_NN_DK(remainder, b, k)
            quotient[k] = q
            if q > 0:
                remainder = SUB_NDN_N(remainder, q, b_shifted)

    # Нормализуем
    final_n = len(quotient) - 1
    while final_n > 0 and quotient[final_n] == 0:
        final_n -= 1

    return final_n, quotient[:final_n + 1]


def MOD_NN_N(a: Natural, b: Natural) -> Natural:
    """
    @brief N-12: Остаток от деления первого натурального на второе.
    @param a Делимое (натуральное число)
    @param b Делитель (натуральное число, != 0)
    @return Остаток от деления: a mod b
    @note Использует: DIV_NN_N, SUB_NDN_N
    """
    if not NZER_N_B(b):
        raise ValueError("Делитель не может быть равен нулю")

    # остаток = a - (b * Неполное частное)
    q = DIV_NN_N(a, b) # Неполное частное
    prod = MUL_NN_N(b, q)
    return SUB_NN_N(a, prod)

def GCF_NN_N(a: Natural, b: Natural) -> Natural:
    """
    @brief N-13: НОД натуральных чисел.
    @param a Первое натуральное число
    @param b Второе натуральное число
    @return Наибольший общий делитель
    """
    # Защита от нуля: НОД(0, x) = x, НОД(x, 0) = x
    if not NZER_N_B(a): return b
    if not NZER_N_B(b): return a

    x, y = a, b
    # Алгоритм Евклида - большее число меняем на остаток от деления большего на меньшее, пока остаток не будет = 0
    while NZER_N_B(y):
        x, y = y, MOD_NN_N(x, y)
    return x


def LCM_NN_N(a: Natural, b: Natural) -> Natural:
    """
    @brief N-14: НОК натуральных чисел.
    @param a Первое натуральное число
    @param b Второе натуральное число
    @return Наименьшее общее кратное
    @note Использует: GCF_NN_N, MUL_NN_N
    """
    if not NZER_N_B(a) or not NZER_N_B(b):
        return 0, [0]

    # Связь НОД и НОК: НОК(a, b) = (a * b) / НОД(a, b)
    prod = MUL_NN_N(a, b)
    gcd = GCF_NN_N(a, b)
    return DIV_NN_N(prod, gcd)
