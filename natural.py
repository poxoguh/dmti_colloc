# Модуль: Натуральные числа с нулём
# Автор: <Красносельских Н.М. (гр. 5382)>
#
# Представление: Natural = (n, A)
#   n — индекс старшей значащей цифры (int)
#   A — список цифр, A[0] — младшая цифра (List[int])
#
# Пример: число 123 → (2, [3, 2, 1])

"""
Aвтор модуля: <Красносельских Н.М.>
"""

from typing import List, Tuple

Natural = Tuple[int, List[int]]


def COM_NN_D(a: Natural, b: Natural) -> int:
    """
    N-1: Сравнение натуральных чисел.
    Возвращает: 2 если a > b, 0 если a == b, 1 если a < b.
    """
    na, Aa = a
    nb, Ab = b
    
    if na > nb:
        return 2
    if na < nb:
        return 1
    
    for i in range(na, -1, -1):
        if Aa[i] > Ab[i]:
            return 2
        if Aa[i] < Ab[i]:
            return 1
            
    return 0


def NZER_N_B(a: Natural) -> bool:
    """
    N-2: Проверка на ноль.
    Возвращает: True если a != 0, False если a == 0.
    """
    _, A = a
    return any(d != 0 for d in A)


def ADD_1N_N(a: Natural) -> Natural:
    """
    N-3: Добавление 1 к натуральному числу.
    """
    n, A = a
    res = A.copy()
    carry = 1
    
    for i in range(len(res)):
        res[i] += carry
        if res[i] >= 10:
            res[i] = 0
            carry = 1
        else:
            carry = 0
            break
            
    if carry:
        res.append(1)
        n += 1
    else:
        n = len(res) - 1
        
    return n, res



def ADD_NN_N(a: Natural, b: Natural) -> Natural:
    """
    N-4: Сложение натуральных чисел.
    Использует: COM_NN_D
    """
    na, Aa = a
    nb, Ab = b
    max_n = max(na, nb)
    res = [0] * (max_n + 2)  # +2 на случай переноса
    carry = 0  # Перенос для сложения
    
    for i in range(max_n + 1):
        va = Aa[i] if i <= na else 0
        vb = Ab[i] if i <= nb else 0
        s = va + vb + carry
        res[i] = s % 10
        carry = s // 10
        
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
    N-5: Вычитание из первого большего натурального числа второго меньшего или равного.
    Использует: COM_NN_D
    """
    if COM_NN_D(a, b) == 1:
        raise ValueError("Первое число должно быть >= второго")
        
    na, Aa = a
    nb, Ab = b
    res = Aa.copy()
    borrow = 0
    
    for i in range(nb + 1):
        res[i] -= (Ab[i] + borrow)
        if res[i] < 0:
            res[i] += 10
            borrow = 1
        else:
            borrow = 0
            
    for i in range(nb + 1, na + 1):
        res[i] -= borrow
        if res[i] < 0:
            res[i] += 10
            borrow = 1
        else:
            borrow = 0
            
    final_n = na
    while final_n > 0 and res[final_n] == 0:
        final_n -= 1
        
    return final_n, res[:final_n + 1]


def MUL_ND_N(a: Natural, d: int) -> Natural:
    """
    N-6: Умножение натурального числа на цифру d (0 <= d <= 9).
    """
    if d == 0:
        return 0, [0]
        
    n, A = a
    res = [0] * (n + 2)
    carry = 0
    
    for i in range(n + 1):
        prod = A[i] * d + carry
        res[i] = prod % 10
        carry = prod // 10
        
    if carry:
        res[n + 1] = carry
        final_n = n + 1
    else:
        final_n = n
        
    while final_n > 0 and res[final_n] == 0:
        final_n -= 1
        
    return final_n, res[:final_n + 1]


def MUL_NK_N(a: Natural, k: int) -> Natural:
    """N-7: Умножение натурального числа на 10^k."""
    if k == 0:
        return a
    n, A = a
    # Явная обработка нуля: 0 * 10^k всегда остаётся 0 в канонической форме
    if n == 0 and A == [0]:
        return (0, [0])
    return n + k, [0] * k + A


def MUL_NN_N(a: Natural, b: Natural) -> Natural:
    """
    N-8: Умножение натуральных чисел.
    Использует: MUL_ND_N, MUL_Nk_N, ADD_NN_N
    """
    nb, Ab = b
    res = 0, [0]
    
    for i in range(nb + 1):
        if Ab[i] != 0:
            term = MUL_ND_N(a, Ab[i])
            term_shifted = MUL_NK_N(term, i)
            res = ADD_NN_N(res, term_shifted)
            
    return res


def SUB_NDN_N(a: Natural, d: int, b: Natural) -> Natural:
    """
    N-9: Вычитание из натурального другого натурального, умноженного на цифру.
    Результат неотрицателен.
    Использует: SUB_NN_N, MUL_ND_N, COM_NN_D
    """
    prod = MUL_ND_N(b, d)
    if COM_NN_D(a, prod) == 1:
        raise ValueError("Результат вычитания должен быть неотрицательным")
    return SUB_NN_N(a, prod)


def DIV_NN_DK(a: Natural, b: Natural, k: int) -> int:
    """
    N-10: Вычисление первой цифры деления большего натурального на меньшее,
    домноженное на 10^k, где k — номер позиции этой цифры.
    Использует: MUL_Nk_N, COM_NN_D
    """
    b_shifted = MUL_NK_N(b, k)
    
    for q in range(9, -1, -1):
        prod = MUL_ND_N(b_shifted, q)
        if COM_NN_D(a, prod) != 1:
            return q
    return 0  # На случай, если ничего не подошло


def DIV_NN_N(a: Natural, b: Natural) -> Natural:
    """N-11: Неполное частное от деления."""
    if not NZER_N_B(b):
        raise ValueError("Делитель не может быть равен нулю")
    if COM_NN_D(a, b) == 1:
        return 0, [0]
        
    na, _ = a
    nb, _ = b
    max_k = na - nb
    quotient = [0] * (max_k + 1)
    remainder = a

    for k in range(max_k, -1, -1):
        b_shifted = MUL_NK_N(b, k) 
        if COM_NN_D(remainder, b_shifted) == 1:
            quotient[k] = 0
        else:
            q = DIV_NN_DK(remainder, b, k)
            quotient[k] = q
            if q > 0:
                remainder = SUB_NDN_N(remainder, q, b_shifted)
                
    final_n = len(quotient) - 1
    while final_n > 0 and quotient[final_n] == 0:
        final_n -= 1
        
    return final_n, quotient[:final_n + 1]


def MOD_NN_N(a: Natural, b: Natural) -> Natural:
    """
    N-12: Остаток от деления первого натурального на второе (делитель != 0).
    Использует: DIV_NN_N, SUB_NDN_N
    """
    if not NZER_N_B(b):
        raise ValueError("Делитель не может быть равен нулю")
        
    q = DIV_NN_N(a, b)
    prod = MUL_NN_N(b, q)
    return SUB_NN_N(a, prod)

def GCF_NN_N(a: Natural, b: Natural) -> Natural:
    """N-13: НОД натуральных чисел."""
    # Защита от нуля: НОД(0, x) = x, НОД(x, 0) = x
    if not NZER_N_B(a): return b
    if not NZER_N_B(b): return a
    
    x, y = a, b
    while NZER_N_B(y):
        x, y = y, MOD_NN_N(x, y)
    return x


def LCM_NN_N(a: Natural, b: Natural) -> Natural:
    """
    N-14: НОК натуральных чисел.
    Использует: GCF_NN_N, MUL_NN_N
    """
    if not NZER_N_B(a) or not NZER_N_B(b):
        return 0, [0]
        
    prod = MUL_NN_N(a, b)
    gcd = GCF_NN_N(a, b)
    return DIV_NN_N(prod, gcd)
