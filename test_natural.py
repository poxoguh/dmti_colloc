"""
Тесты модуля Natural (N-1 .. N-14)
Запуск: pytest tests/test_natural.py
"""
import pytest
from natural import (
    COM_NN_D, NZER_N_B, ADD_1N_N, ADD_NN_N,
    SUB_NN_N, MUL_ND_N, MUL_Nk_N, MUL_NN_N,
    SUB_NDN_N, DIV_NN_Dk, DIV_NN_N, MOD_NN_N,
    GCF_NN_N, LCM_NN_N
)

# Вспомогательные числа для тестов
# 0   → (0, [0])
# 1   → (0, [1])
# 9   → (0, [9])
# 99  → (1, [9, 9])
# 123 → (2, [3, 2, 1])
# 456 → (2, [6, 5, 4])

N0   = (0, [0])
N1   = (0, [1])
N9   = (0, [9])
N99  = (1, [9, 9])
N123 = (2, [3, 2, 1])
N456 = (2, [6, 5, 4])


# --- N-1: COM_NN_D ---
def test_COM_NN_D_greater():
    assert COM_NN_D(N456, N123) == 2

def test_COM_NN_D_equal():
    assert COM_NN_D(N123, N123) == 0

def test_COM_NN_D_less():
    assert COM_NN_D(N123, N456) == 1


# --- N-2: NZER_N_B ---
def test_NZER_N_B_nonzero():
    assert NZER_N_B(N123) == True

def test_NZER_N_B_zero():
    assert NZER_N_B(N0) == False


# --- N-3: ADD_1N_N ---
def test_ADD_1N_N_simple():
    assert ADD_1N_N(N9) == (1, [0, 1])  # 9+1 = 10

def test_ADD_1N_N_carry():
    assert ADD_1N_N(N99) == (2, [0, 0, 1])  # 99+1 = 100


# --- N-4: ADD_NN_N ---
def test_ADD_NN_N_basic():
    # 123 + 456 = 579
    assert ADD_NN_N(N123, N456) == (2, [9, 7, 5])

def test_ADD_NN_N_with_carry():
    # 99 + 1 = 100
    assert ADD_NN_N(N99, N1) == (2, [0, 0, 1])


# --- N-5: SUB_NN_N ---
def test_SUB_NN_N_basic():
    # 456 - 123 = 333
    assert SUB_NN_N(N456, N123) == (2, [3, 3, 3])

def test_SUB_NN_N_equal():
    # 123 - 123 = 0
    assert SUB_NN_N(N123, N123) == (0, [0])


# --- N-6: MUL_ND_N ---
def test_MUL_ND_N_basic():
    # 123 * 3 = 369
    assert MUL_ND_N(N123, 3) == (2, [9, 6, 3])

def test_MUL_ND_N_zero():
    assert MUL_ND_N(N123, 0) == (0, [0])


# --- N-7: MUL_Nk_N ---
def test_MUL_Nk_N_basic():
    # 123 * 10^2 = 12300
    assert MUL_Nk_N(N123, 2) == (4, [0, 0, 3, 2, 1])

def test_MUL_Nk_N_zero_k():
    assert MUL_Nk_N(N123, 0) == N123


# --- N-8: MUL_NN_N ---
def test_MUL_NN_N_basic():
    # 123 * 456 = 56088
    assert MUL_NN_N(N123, N456) == (4, [8, 8, 0, 6, 5])

def test_MUL_NN_N_by_one():
    assert MUL_NN_N(N123, N1) == N123


# --- N-9: SUB_NDN_N ---
def test_SUB_NDN_N_basic():
    # 456 - 3*123 = 456 - 369 = 87
    assert SUB_NDN_N(N456, 3, N123) == (1, [7, 8])


# --- N-10: DIV_NN_Dk ---
def test_DIV_NN_Dk_basic():
    # первая цифра деления 456 на 123*10^0 = 3
    assert DIV_NN_Dk(N456, N123, 0) == 3


# --- N-11: DIV_NN_N ---
def test_DIV_NN_N_basic():
    # 456 // 123 = 3
    assert DIV_NN_N(N456, N123) == (0, [3])

def test_DIV_NN_N_exact():
    # 99 // 9 = 11
    assert DIV_NN_N(N99, N9) == (1, [1, 1])


# --- N-12: MOD_NN_N ---
def test_MOD_NN_N_basic():
    # 456 % 123 = 87
    assert MOD_NN_N(N456, N123) == (1, [7, 8])

def test_MOD_NN_N_exact():
    # 99 % 9 = 0
    assert MOD_NN_N(N99, N9) == N0


# --- N-13: GCF_NN_N ---
def test_GCF_NN_N_basic():
    # НОД(12, 8) = 4
    N12 = (1, [2, 1])
    N8  = (0, [8])
    N4  = (0, [4])
    assert GCF_NN_N(N12, N8) == N4


# --- N-14: LCM_NN_N ---
def test_LCM_NN_N_basic():
    # НОК(4, 6) = 12
    N4  = (0, [4])
    N6  = (0, [6])
    N12 = (1, [2, 1])
    assert LCM_NN_N(N4, N6) == N12
