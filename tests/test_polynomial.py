"""
Тесты модуля Polynomial (P-1 .. P-13)
Запуск: pytest tests/test_polynomial.py -v
"""
import pytest
from polynomial import (
    ADD_PP_P, SUB_PP_P, MUL_PQ_P, MUL_PXK_P,
    LED_P_Q, DEG_P_N, FAC_P_Q, MUL_PP_P,
    DIV_PP_P, MOD_PP_P, GCF_PP_P, DER_P_P, NMR_P_P
)
from rational import Q0, Q1, Q2_1, Qm1, Q1_2, Q3_2

# ──────────────────────────────────────────────
# ВСПОМОГАТЕЛЬНЫЕ КОНСТАНТЫ
# ──────────────────────────────────────────────
# Polynomial = (m, C), где C[i] — коэффициент при x^i
# Ноль: (-1, [])
P0 = (-1, [])

# 1: (0, [1])
P1 = (0, [Q1])

# x: (1, [Q0, Q1])
Px = (1, [Q0, Q1])

# x+1: (1, [Q1, Q1])
Px1 = (1, [Q1, Q1])

# x-1: (1, [Qm1, Q1])
Pxm1 = (1, [Qm1, Q1])

# x^2: (2, [Q0, Q0, Q1])
Px2 = (2, [Q0, Q0, Q1])

# x^2-1: (2, [Qm1, Q0, Q1])
Px2m1 = (2, [Qm1, Q0, Q1])

# 2x: (1, [Q0, Q2_1])
P2x = (1, [Q0, Q2_1])

# 2*x^2 + 3*x + 1: (2, [Q1, Q3_1, Q2_1])
P2x2_3x_1 = (2, [Q1, ( (0,0,[3]), N1 ), Q2_1])


# ──────────────────────────────────────────────
# P-1: ADD_PP_P — Сложение
# ──────────────────────────────────────────────
def test_ADD_PP_P_basic():
    # (x+1) + (x-1) = 2x
    result = ADD_PP_P(Px1, Pxm1)
    assert DEG_P_N(result) == 1
    assert result[1][1] == Q2_1  # коэффициент при x

def test_ADD_PP_P_different_deg():
    # (x^2) + (x+1) = x^2 + x + 1
    result = ADD_PP_P(Px2, Px1)
    assert DEG_P_N(result) == 2

def test_ADD_PP_P_with_zero():
    assert ADD_PP_P(Px1, P0) == Px1


# ──────────────────────────────────────────────
# P-2: SUB_PP_P — Вычитание
# ──────────────────────────────────────────────
def test_SUB_PP_P_basic():
    # (x+1) - (x-1) = 2
    result = SUB_PP_P(Px1, Pxm1)
    assert DEG_P_N(result) == 0
    assert result[1][0] == Q2_1  # свободный член = 2


# ──────────────────────────────────────────────
# P-3: MUL_PQ_P — Умножение на число
# ──────────────────────────────────────────────
def test_MUL_PQ_P_basic():
    # 2 * (x+1) = 2x + 2
    result = MUL_PQ_P(Px1, Q2_1)
    assert DEG_P_N(result) == 1
    assert result[1][0] == Q2_1  # свободный член = 2

def test_MUL_PQ_P_by_zero():
    assert MUL_PQ_P(Px1, Q0) == P0


# ──────────────────────────────────────────────
# P-4: MUL_PXK_P — Умножение на x^k
# ──────────────────────────────────────────────
def test_MUL_PXK_P_basic():
    # (x+1) * x^2 = x^3 + x^2
    result = MUL_PXK_P(Px1, 2)
    assert DEG_P_N(result) == 3

def test_MUL_PXK_P_zero():
    assert MUL_PXK_P(Px1, 0) == Px1


# ──────────────────────────────────────────────
# P-5: LED_P_Q — Старший коэффициент
# ──────────────────────────────────────────────
def test_LED_P_Q_basic():
    assert LED_P_Q(Px2m1) == Q1  # старший коэффициент = 1

def test_LED_P_Q_zero():
    assert LED_P_Q(P0) == Q0


# ──────────────────────────────────────────────
# P-6: DEG_P_N — Степень
# ──────────────────────────────────────────────
def test_DEG_P_N_basic():
    assert DEG_P_N(Px2m1) == 2

def test_DEG_P_N_zero():
    assert DEG_P_N(P0) == -1


# ──────────────────────────────────────────────
# P-7: FAC_P_Q — Контент
# ──────────────────────────────────────────────
def test_FAC_P_Q_basic():
    # content(2x + 4) = 2
    P2x_4 = (1, [ ( (0,0,[4]), N1 ), Q2_1 ])
    result = FAC_P_Q(P2x_4)
    assert result == Q2_1


# ──────────────────────────────────────────────
# P-8: MUL_PP_P — Умножение многочленов
# ──────────────────────────────────────────────
def test_MUL_PP_P_basic():
    # (x+1)*(x-1) = x^2 - 1
    result = MUL_PP_P(Px1, Pxm1)
    assert result == Px2m1

def test_MUL_PP_P_by_zero():
    assert MUL_PP_P(Px1, P0) == P0


# ──────────────────────────────────────────────
# P-9: DIV_PP_P — Частное
# ──────────────────────────────────────────────
def test_DIV_PP_P_basic():
    # (x^2-1) / (x+1) = x-1
    result = DIV_PP_P(Px2m1, Px1)
    assert result == Pxm1

def test_DIV_PP_P_less():
    # x / x^2 = 0
    result = DIV_PP_P(Px, Px2)
    assert result == P0


# ──────────────────────────────────────────────
# P-10: MOD_PP_P — Остаток
# ──────────────────────────────────────────────
def test_MOD_PP_P_basic():
    # (x^2-1) % (x+1) = 0
    result = MOD_PP_P(Px2m1, Px1)
    assert result == P0

def test_MOD_PP_P_less():
    # x % x^2 = x
    result = MOD_PP_P(Px, Px2)
    assert result == Px


# ──────────────────────────────────────────────
# P-11: GCF_PP_P — НОД многочленов
# ──────────────────────────────────────────────
def test_GCF_PP_P_basic():
    # gcd(x^2-1, x-1) = x-1
    result = GCF_PP_P(Px2m1, Pxm1)
    assert result == Pxm1


# ──────────────────────────────────────────────
# P-12: DER_P_P — Производная
# ──────────────────────────────────────────────
def test_DER_P_P_basic():
    # d/dx (x^2) = 2x
    result = DER_P_P(Px2)
    assert result == P2x

def test_DER_P_P_constant():
    # d/dx (5) = 0
    P5 = (0, [ ( (0,0,[5]), N1 ) ])
    assert DER_P_P(P5) == P0


# ──────────────────────────────────────────────
# P-13: NMR_P_P — Удаление кратных корней
# ──────────────────────────────────────────────
def test_NMR_P_P_basic():
    # (x-1)^2 = x^2 - 2x + 1 → x-1
    P_x2_2x_1 = (2, [Q1, ( (1,0,[2]), N1 ), Q1])  # x^2 - 2x + 1
    result = NMR_P_P(P_x2_2x_1)
    assert DEG_P_N(result) == 1  # степень стала 1
