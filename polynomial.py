# Модуль: Многочлены с рациональными коэффициентами
# Авторы: <Смирнов А.Н. (гр. 5382)>
#
# Представление: Polynomial = (m, C)
#   m — степень многочлена (int)
#   C — список коэффициентов типа Rational, C[0] — коэффициент при x^0
#
# Пример: 3/2 * x^2 + 0 * x + 1/4 → (2, [Q(1,4), Q(0,1), Q(3,2)])

"""
Aвтор модуля: <Смирнов А.Н.>
"""

from typing import List, Tuple
from natural import LCM_NN_N, GCF_NN_N
from integer import ABS_Z_N, TRANS_N_Z, TRANS_Z_N, DIV_ZZ_Z, MUL_ZZ_Z, MUL_ZM_Z
from rational import ADD_QQ_Q, SUB_QQ_Q, MUL_QQ_Q, DIV_QQ_Q, RED_Q_Q

Natural = Tuple[int, List[int]]
Integer = Tuple[int, int, List[int]]
Rational = Tuple[Integer, Natural]
Polynomial = Tuple[int, List[Rational]]

# Канонический ноль: 0/1. Используем его везде вместо ручных кортежей.
ZERO_RAT = ((0, 0, [0]), (0, [1]))

def _is_zero_rat(q: Rational) -> bool:
    return q == ZERO_RAT

def _normalize(m: int, C: List[Rational]) -> Polynomial:
    while m >= 0 and _is_zero_rat(C[m]):
        m -= 1
    return (m, C[:m + 1]) if m >= 0 else (-1, [])

def _int_to_rat(k: int) -> Rational:
    if k == 0: return ZERO_RAT
    digits = [int(d) for d in reversed(str(k))]
    n = len(digits) - 1
    while n > 0 and digits[n] == 0: n -= 1
    return (TRANS_N_Z((n, digits[:n+1])), (0, [1]))

# ──────────────────────────────────────────────
# РЕАЛИЗАЦИЯ ФУНКЦИЙ
# ──────────────────────────────────────────────
def ADD_PP_P(a: Polynomial, b: Polynomial) -> Polynomial:
    m1, C1 = a; m2, C2 = b
    m = max(m1, m2)
    C1_ext = C1 + [ZERO_RAT] * (m - m1)
    C2_ext = C2 + [ZERO_RAT] * (m - m2)
    return _normalize(m, [ADD_QQ_Q(C1_ext[i], C2_ext[i]) for i in range(m + 1)])

def SUB_PP_P(a: Polynomial, b: Polynomial) -> Polynomial:
    m1, C1 = a; m2, C2 = b
    m = max(m1, m2)
    C1_ext = C1 + [ZERO_RAT] * (m - m1)
    C2_ext = C2 + [ZERO_RAT] * (m - m2)
    return _normalize(m, [SUB_QQ_Q(C1_ext[i], C2_ext[i]) for i in range(m + 1)])

def MUL_PQ_P(a: Polynomial, q: Rational) -> Polynomial:
    m, C = a
    return (-1, []) if m < 0 or _is_zero_rat(q) else _normalize(m, [MUL_QQ_Q(c, q) for c in C])

def MUL_PXK_P(a: Polynomial, k: int) -> Polynomial:
    m, C = a
    if m < 0 or k < 0: return (-1, [])
    if k == 0: return a
    return (m + k, [ZERO_RAT] * k + C)

def LED_P_Q(a: Polynomial) -> Rational:
    m, C = a
    return ZERO_RAT if m < 0 else C[m]

def DEG_P_N(a: Polynomial) -> int:
    return a[0]

def FAC_P_Q(a: Polynomial) -> Rational:
    m, C = a
    if m < 0: return ZERO_RAT
    nonzero = [(num, den) for num, den in C if not _is_zero_rat((num, den))]
    if not nonzero: return ZERO_RAT

    lcm_den = nonzero[0][1]
    for _, den in nonzero[1:]: lcm_den = LCM_NN_N(lcm_den, den)

    first_num, first_den = nonzero[0]
    mult = TRANS_Z_N(DIV_ZZ_Z(TRANS_N_Z(lcm_den), TRANS_N_Z(first_den)))
    gcd_val = ABS_Z_N(MUL_ZZ_Z(first_num, TRANS_N_Z(mult)))

    for num, den in nonzero[1:]:
        mult = TRANS_Z_N(DIV_ZZ_Z(TRANS_N_Z(lcm_den), TRANS_N_Z(den)))
        scaled = MUL_ZZ_Z(num, TRANS_N_Z(mult))
        gcd_val = GCF_NN_N(gcd_val, ABS_Z_N(scaled))

    lead_num, _ = nonzero[-1]
    res_num = TRANS_N_Z(gcd_val)
    if lead_num[0] == 1: res_num = MUL_ZM_Z(res_num)
    return RED_Q_Q((res_num, lcm_den))

def MUL_PP_P(a: Polynomial, b: Polynomial) -> Polynomial:
    m1, C1 = a; m2, C2 = b
    if m1 < 0 or m2 < 0: return (-1, [])
    res = (-1, [])
    for i in range(m1 + 1):
        if _is_zero_rat(C1[i]): continue
        res = ADD_PP_P(res, MUL_PXK_P(MUL_PQ_P(b, C1[i]), i))
    return res

def DIV_PP_P(a: Polynomial, b: Polynomial) -> Polynomial:
    if DEG_P_N(b) < 0: raise ValueError("Деление на нулевой многочлен")
    if DEG_P_N(a) < DEG_P_N(b): return (-1, [])
    
    R = list(a[1]); m_a, m_b = a[0], b[0]; C_b = b[1]; lead_b = C_b[m_b]
    q_m = m_a - m_b; Q_C = [ZERO_RAT] * (q_m + 1)
    for i in range(q_m, -1, -1):
        if _is_zero_rat(R[i + m_b]): continue
        q_i = DIV_QQ_Q(R[i + m_b], lead_b); Q_C[i] = q_i
        for j in range(m_b + 1):
            R[i + j] = SUB_QQ_Q(R[i + j], MUL_QQ_Q(q_i, C_b[j]))
    return _normalize(q_m, Q_C)

def MOD_PP_P(a: Polynomial, b: Polynomial) -> Polynomial:
    if DEG_P_N(b) < 0: raise ValueError("Деление на нулевой многочлен")
    return SUB_PP_P(a, MUL_PP_P(b, DIV_PP_P(a, b)))

def GCF_PP_P(a: Polynomial, b: Polynomial) -> Polynomial:
    while DEG_P_N(b) >= 0: a, b = b, MOD_PP_P(a, b)
    return a

def DER_P_P(a: Polynomial) -> Polynomial:
    m, C = a
    if m <= 0: return (-1, [])
    res_C = [MUL_QQ_Q(_int_to_rat(i+1), C[i+1]) for i in range(m)]
    return _normalize(m - 1, res_C)

def NMR_P_P(a: Polynomial) -> Polynomial:
    if DEG_P_N(a) < 0: return a
    d = DER_P_P(a)
    if DEG_P_N(d) < 0: return a
    return DIV_PP_P(a, GCF_PP_P(a, d))
