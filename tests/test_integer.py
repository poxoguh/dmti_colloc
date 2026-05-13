"""
Тесты модуля Integer (Z-1 .. Z-10)
Запуск: pytest tests/test_integer.py -v
"""
import pytest
from integer import (
    ABS_Z_N, POZ_Z_D, MUL_ZM_Z, TRANS_N_Z, TRANS_Z_N,
    ADD_ZZ_Z, SUB_ZZ_Z, MUL_ZZ_Z, DIV_ZZ_Z, MOD_ZZ_Z
)
from natural import (
    N0, N1, N9, N10, N99, N100, N123, N456, N579, N12, N8, N4, N6
)

# ──────────────────────────────────────────────
# ВСПОМОГАТЕЛЬНЫЕ КОНСТАНТЫ
# ──────────────────────────────────────────────
# Integer = (sign, n, A), sign: 0=+/0, 1=-
Z0   = (0, 0, [0])          # 0
Z1   = (0, 0, [1])          # 1
Z9   = (0, 0, [9])          # 9
Z10  = (0, 1, [0, 1])       # 10
Z99  = (0, 1, [9, 9])       # 99
Z123 = (0, 2, [3, 2, 1])    # 123
Z456 = (0, 2, [6, 5, 4])    # 456
Zm1  = (1, 0, [1])          # -1
Zm9  = (1, 0, [9])          # -9
Zm123= (1, 2, [3, 2, 1])    # -123


# ──────────────────────────────────────────────
# Z-1: ABS_Z_N — Модуль
# ──────────────────────────────────────────────
def test_ABS_Z_N_positive():
    assert ABS_Z_N(Z123) == N123

def test_ABS_Z_N_negative():
    assert ABS_Z_N(Zm123) == N123

def test_ABS_Z_N_zero():
    assert ABS_Z_N(Z0) == N0


# ──────────────────────────────────────────────
# Z-2: POZ_Z_D — Знак числа
# ──────────────────────────────────────────────
def test_POZ_Z_D_positive():
    assert POZ_Z_D(Z123) == 2
    assert POZ_Z_D(Z1) == 2

def test_POZ_Z_D_negative():
    assert POZ_Z_D(Zm123) == 1
    assert POZ_Z_D(Zm1) == 1

def test_POZ_Z_D_zero():
    assert POZ_Z_D(Z0) == 0


# ──────────────────────────────────────────────
# Z-3: MUL_ZM_Z — Умножение на -1
# ──────────────────────────────────────────────
def test_MUL_ZM_Z_positive():
    assert MUL_ZM_Z(Z123) == Zm123

def test_MUL_ZM_Z_negative():
    assert MUL_ZM_Z(Zm123) == Z123

def test_MUL_ZM_Z_zero():
    assert MUL_ZM_Z(Z0) == Z0


# ──────────────────────────────────────────────
# Z-4: TRANS_N_Z — Натуральное → Целое
# ──────────────────────────────────────────────
def test_TRANS_N_Z_basic():
    assert TRANS_N_Z(N123) == Z123

def test_TRANS_N_Z_zero():
    assert TRANS_N_Z(N0) == Z0


# ──────────────────────────────────────────────
# Z-5: TRANS_Z_N — Целое неотрицательное → Натуральное
# ──────────────────────────────────────────────
def test_TRANS_Z_N_basic():
    assert TRANS_Z_N(Z123) == N123

def test_TRANS_Z_N_zero():
    assert TRANS_Z_N(Z0) == N0


# ──────────────────────────────────────────────
# Z-6: ADD_ZZ_Z — Сложение
# ──────────────────────────────────────────────
def test_ADD_ZZ_Z_both_positive():
    assert ADD_ZZ_Z(Z123, Z456) == (0, 2, [9, 7, 5])  # 579

def test_ADD_ZZ_Z_both_negative():
    assert ADD_ZZ_Z(Zm123, Zm456) == (1, 2, [9, 7, 5])  # -579

def test_ADD_ZZ_Z_different_signs():
    assert ADD_ZZ_Z(Z456, Zm123) == (0, 2, [3, 3, 3])  # 333
    assert ADD_ZZ_Z(Z123, Zm456) == (1, 2, [3, 3, 3])  # -333

def test_ADD_ZZ_Z_with_zero():
    assert ADD_ZZ_Z(Z123, Z0) == Z123
    assert ADD_ZZ_Z(Z0, Zm456) == Zm456

def test_ADD_ZZ_Z_opposite():
    assert ADD_ZZ_Z(Z123, Zm123) == Z0


# ──────────────────────────────────────────────
# Z-7: SUB_ZZ_Z — Вычитание
# ──────────────────────────────────────────────
def test_SUB_ZZ_Z_basic():
    assert SUB_ZZ_Z(Z456, Z123) == (0, 2, [3, 3, 3])  # 333

def test_SUB_ZZ_Z_negative_result():
    assert SUB_ZZ_Z(Z123, Z456) == (1, 2, [3, 3, 3])  # -333

def test_SUB_ZZ_Z_with_zero():
    assert SUB_ZZ_Z(Z123, Z0) == Z123
    assert SUB_ZZ_Z(Z0, Z123) == Zm123


# ──────────────────────────────────────────────
# Z-8: MUL_ZZ_Z — Умножение
# ──────────────────────────────────────────────
def test_MUL_ZZ_Z_both_positive():
    assert MUL_ZZ_Z(Z123, Z456) == (0, 4, [8, 8, 0, 6, 5])  # 56088

def test_MUL_ZZ_Z_different_signs():
    assert MUL_ZZ_Z(Z123, Zm456) == (1, 4, [8, 8, 0, 6, 5])  # -56088

def test_MUL_ZZ_Z_both_negative():
    assert MUL_ZZ_Z(Zm123, Zm456) == (0, 4, [8, 8, 0, 6, 5])  # 56088

def test_MUL_ZZ_Z_with_zero():
    assert MUL_ZZ_Z(Z123, Z0) == Z0


# ──────────────────────────────────────────────
# Z-9: DIV_ZZ_Z — Частное
# ──────────────────────────────────────────────
def test_DIV_ZZ_Z_both_positive():
    assert DIV_ZZ_Z(Z456, Z123) == (0, 0, [3])  # 3

def test_DIV_ZZ_Z_different_signs():
    assert DIV_ZZ_Z(Z456, Zm123) == (1, 0, [3])  # -3

def test_DIV_ZZ_Z_both_negative():
    assert DIV_ZZ_Z(Zm456, Zm123) == (0, 0, [3])  # 3

def test_DIV_ZZ_Z_less():
    assert DIV_ZZ_Z(Z123, Z456) == Z0  # 123 < 456


# ──────────────────────────────────────────────
# Z-10: MOD_ZZ_Z — Остаток
# ──────────────────────────────────────────────
def test_MOD_ZZ_Z_basic():
    # 456 = 123*3 + 87
    assert MOD_ZZ_Z(Z456, Z123) == (0, 1, [7, 8])  # 87

def test_MOD_ZZ_Z_exact():
    assert MOD_ZZ_Z(Z99, Z9) == Z0
