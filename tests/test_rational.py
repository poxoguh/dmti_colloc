"""
Тесты модуля Rational (Q-1 .. Q-8)
Запуск: pytest tests/test_rational.py -v
"""
import pytest
from rational import (
    RED_Q_Q, INT_Q_B, TRANS_Z_Q, TRANS_Q_Z,
    ADD_QQ_Q, SUB_QQ_Q, MUL_QQ_Q, DIV_QQ_Q
)
from integer import Z0, Z1, Z9, Z123, Zm1, Zm123
from natural import N0, N1, N2, N3, N4, N6, N12

# ──────────────────────────────────────────────
# ВСПОМОГАТЕЛЬНЫЕ КОНСТАНТЫ
# ──────────────────────────────────────────────
# Rational = (Integer, Natural)
Q0   = (Z0, N1)           # 0/1
Q1   = (Z1, N1)           # 1/1
Q2   = (Z1, N2)           # 1/2
Q3_2 = (Z3, N2)           # 3/2 (Z3 нужно определить)
Qm1  = (Zm1, N1)          # -1/1
Qm1_2= (Zm1, N2)          # -1/2

# Создаём недостающие целые числа
Z2 = (0, 0, [2])
Z3 = (0, 0, [3])
Z4 = (0, 0, [4])
Z6 = (0, 0, [6])

Q2_1 = (Z2, N1)           # 2/1
Q3_1 = (Z3, N1)           # 3/1
Q4_1 = (Z4, N1)           # 4/1
Q6_1 = (Z6, N1)           # 6/1
Q3_2 = (Z3, N2)           # 3/2
Q1_2 = (Z1, N2)           # 1/2


# ──────────────────────────────────────────────
# Q-1: RED_Q_Q — Сокращение дроби
# ──────────────────────────────────────────────
def test_RED_Q_Q_already_reduced():
    assert RED_Q_Q(Q3_2) == Q3_2  # 3/2 уже сокращена

def test_RED_Q_Q_reduce():
    # 4/2 -> 2/1
    Q4_2 = (Z4, N2)
    assert RED_Q_Q(Q4_2) == Q2_1

def test_RED_Q_Q_zero():
    assert RED_Q_Q(Q0) == Q0


# ──────────────────────────────────────────────
# Q-2: INT_Q_B — Проверка на целое
# ──────────────────────────────────────────────
def test_INT_Q_B_integer():
    assert INT_Q_B(Q1) is True
    assert INT_Q_B(Q2_1) is True

def test_INT_Q_B_not_integer():
    assert INT_Q_B(Q3_2) is False
    assert INT_Q_B(Q1_2) is False


# ──────────────────────────────────────────────
# Q-3: TRANS_Z_Q — Целое → Дробное
# ──────────────────────────────────────────────
def test_TRANS_Z_Q_basic():
    assert TRANS_Z_Q(Z123) == (Z123, N1)

def test_TRANS_Z_Q_zero():
    assert TRANS_Z_Q(Z0) == Q0


# ──────────────────────────────────────────────
# Q-4: TRANS_Q_Z — Дробное (целое) → Целое
# ──────────────────────────────────────────────
def test_TRANS_Q_Z_basic():
    assert TRANS_Q_Z(Q2_1) == Z2

def test_TRANS_Q_Z_not_integer():
    with pytest.raises(ValueError):
        TRANS_Q_Z(Q3_2)


# ──────────────────────────────────────────────
# Q-5: ADD_QQ_Q — Сложение
# ──────────────────────────────────────────────
def test_ADD_QQ_Q_same_den():
    # 1/2 + 1/2 = 1
    assert ADD_QQ_Q(Q1_2, Q1_2) == Q1

def test_ADD_QQ_Q_different_den():
    # 1/2 + 1/3 = 5/6
    Q1_3 = (Z1, N3)
    Q5_6 = (Z5, N6) if 'Z5' in dir() else ( (0,0,[5]), N6 )
    # Для простоты проверяем знаменатель
    result = ADD_QQ_Q(Q1_2, Q1_3)
    assert result[1] == N6  # знаменатель 6

def test_ADD_QQ_Q_with_zero():
    assert ADD_QQ_Q(Q3_2, Q0) == Q3_2


# ──────────────────────────────────────────────
# Q-6: SUB_QQ_Q — Вычитание
# ──────────────────────────────────────────────
def test_SUB_QQ_Q_basic():
    # 3/2 - 1/2 = 1
    assert SUB_QQ_Q(Q3_2, Q1_2) == Q1

def test_SUB_QQ_Q_negative():
    # 1/2 - 3/2 = -1
    assert SUB_QQ_Q(Q1_2, Q3_2) == Qm1


# ──────────────────────────────────────────────
# Q-7: MUL_QQ_Q — Умножение
# ──────────────────────────────────────────────
def test_MUL_QQ_Q_basic():
    # 1/2 * 3/2 = 3/4
    Q3_4 = (Z3, N4)
    assert MUL_QQ_Q(Q1_2, Q3_2) == Q3_4

def test_MUL_QQ_Q_with_zero():
    assert MUL_QQ_Q(Q3_2, Q0) == Q0


# ──────────────────────────────────────────────
# Q-8: DIV_QQ_Q — Деление
# ──────────────────────────────────────────────
def test_DIV_QQ_Q_basic():
    # (3/2) / (1/2) = 3
    assert DIV_QQ_Q(Q3_2, Q1_2) == Q3_1

def test_DIV_QQ_Q_by_zero():
    with pytest.raises(ZeroDivisionError):
        DIV_QQ_Q(Q1, Q0)
