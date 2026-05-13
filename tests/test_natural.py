"""
Тесты модуля Natural (N-1 .. N-14)
Запуск: pytest tests/test_natural.py -v
"""
import pytest
from natural import (
    COM_NN_D, NZER_N_B, ADD_1N_N, ADD_NN_N,
    SUB_NN_N, MUL_ND_N, MUL_NK_N, MUL_NN_N,
    SUB_NDN_N, DIV_NN_DK, DIV_NN_N, MOD_NN_N,
    GCF_NN_N, LCM_NN_N
)

# ──────────────────────────────────────────────
# ВСПОМОГАТЕЛЬНЫЕ КОНСТАНТЫ
# ──────────────────────────────────────────────
N0   = (0, [0])           # 0
N1   = (0, [1])           # 1
N9   = (0, [9])           # 9
N10  = (1, [0, 1])        # 10
N99  = (1, [9, 9])        # 99
N100 = (2, [0, 0, 1])     # 100
N123 = (2, [3, 2, 1])     # 123
N456 = (2, [6, 5, 4])     # 456
N579 = (2, [9, 7, 5])     # 579
N12  = (1, [2, 1])        # 12
N8   = (0, [8])           # 8
N4   = (0, [4])           # 4
N6   = (0, [6])           # 6


# ──────────────────────────────────────────────
# N-1: COM_NN_D — Сравнение
# ──────────────────────────────────────────────
def test_COM_NN_D_greater():
    assert COM_NN_D(N456, N123) == 2

def test_COM_NN_D_equal():
    assert COM_NN_D(N123, N123) == 0

def test_COM_NN_D_less():
    assert COM_NN_D(N123, N456) == 1

def test_COM_NN_D_zero():
    assert COM_NN_D(N0, N0) == 0
    assert COM_NN_D(N1, N0) == 2
    assert COM_NN_D(N0, N1) == 1


# ──────────────────────────────────────────────
# N-2: NZER_N_B — Проверка на ноль
# ──────────────────────────────────────────────
def test_NZER_N_B_nonzero():
    assert NZER_N_B(N123) is True
    assert NZER_N_B(N1) is True

def test_NZER_N_B_zero():
    assert NZER_N_B(N0) is False


# ──────────────────────────────────────────────
# N-3: ADD_1N_N — Прибавление 1
# ──────────────────────────────────────────────
def test_ADD_1N_N_simple():
    assert ADD_1N_N(N9) == N10

def test_ADD_1N_N_carry():
    assert ADD_1N_N(N99) == N100

def test_ADD_1N_N_zero():
    assert ADD_1N_N(N0) == N1


# ──────────────────────────────────────────────
# N-4: ADD_NN_N — Сложение
# ──────────────────────────────────────────────
def test_ADD_NN_N_basic():
    assert ADD_NN_N(N123, N456) == N579

def test_ADD_NN_N_with_carry():
    assert ADD_NN_N(N99, N1) == N100

def test_ADD_NN_N_with_zero():
    assert ADD_NN_N(N123, N0) == N123
    assert ADD_NN_N(N0, N456) == N456


# ──────────────────────────────────────────────
# N-5: SUB_NN_N — Вычитание
# ──────────────────────────────────────────────
def test_SUB_NN_N_basic():
    assert SUB_NN_N(N456, N123) == (2, [3, 3, 3])  # 333

def test_SUB_NN_N_equal():
    assert SUB_NN_N(N123, N123) == N0

def test_SUB_NN_N_result_zero():
    assert SUB_NN_N(N10, N10) == N0

def test_SUB_NN_N_invalid():
    with pytest.raises(ValueError):
        SUB_NN_N(N123, N456)  # a < b


# ──────────────────────────────────────────────
# N-6: MUL_ND_N — Умножение на цифру
# ──────────────────────────────────────────────
def test_MUL_ND_N_basic():
    assert MUL_ND_N(N123, 3) == (2, [9, 6, 3])  # 369

def test_MUL_ND_N_zero_digit():
    assert MUL_ND_N(N123, 0) == N0

def test_MUL_ND_N_by_one():
    assert MUL_ND_N(N123, 1) == N123

def test_MUL_ND_N_carry():
    assert MUL_ND_N(N99, 2) == (2, [8, 9, 1])  # 198


# ──────────────────────────────────────────────
# N-7: MUL_NK_N — Умножение на 10^k
# ──────────────────────────────────────────────
def test_MUL_NK_N_basic():
    assert MUL_NK_N(N123, 2) == (4, [0, 0, 3, 2, 1])  # 12300

def test_MUL_NK_N_zero_k():
    assert MUL_NK_N(N123, 0) == N123

def test_MUL_NK_N_zero_num():
    assert MUL_NK_N(N0, 5) == N0


# ──────────────────────────────────────────────
# N-8: MUL_NN_N — Умножение
# ──────────────────────────────────────────────
def test_MUL_NN_N_basic():
    assert MUL_NN_N(N123, N456) == (4, [8, 8, 0, 6, 5])  # 56088

def test_MUL_NN_N_by_one():
    assert MUL_NN_N(N123, N1) == N123

def test_MUL_NN_N_by_zero():
    assert MUL_NN_N(N123, N0) == N0


# ──────────────────────────────────────────────
# N-9: SUB_NDN_N — Вычитание d*b
# ──────────────────────────────────────────────
def test_SUB_NDN_N_basic():
    # 456 - 3*123 = 456 - 369 = 87
    assert SUB_NDN_N(N456, 3, N123) == (1, [7, 8])

def test_SUB_NDN_N_exact():
    # 123 - 1*123 = 0
    assert SUB_NDN_N(N123, 1, N123) == N0

def test_SUB_NDN_N_invalid():
    with pytest.raises(ValueError):
        SUB_NDN_N(N100, 5, N123)  # 100 - 5*123 < 0


# ──────────────────────────────────────────────
# N-10: DIV_NN_DK — Первая цифра деления
# ──────────────────────────────────────────────
def test_DIV_NN_DK_basic():
    assert DIV_NN_DK(N456, N123, 0) == 3  # 456 // 123 = 3

def test_DIV_NN_DK_with_shift():
    # 4560 // (123 * 10^1) = 4560 // 1230 = 3
    N4560 = (3, [0, 6, 5, 4])
    assert DIV_NN_DK(N4560, N123, 1) == 3


# ──────────────────────────────────────────────
# N-11: DIV_NN_N — Целая часть деления
# ──────────────────────────────────────────────
def test_DIV_NN_N_basic():
    assert DIV_NN_N(N456, N123) == (0, [3])  # 456 // 123 = 3

def test_DIV_NN_N_exact():
    assert DIV_NN_N(N99, N9) == (1, [1, 1])  # 99 // 9 = 11

def test_DIV_NN_N_less():
    assert DIV_NN_N(N123, N456) == N0  # 123 < 456

def test_DIV_NN_N_by_one():
    assert DIV_NN_N(N123, N1) == N123


# ──────────────────────────────────────────────
# N-12: MOD_NN_N — Остаток от деления
# ──────────────────────────────────────────────
def test_MOD_NN_N_basic():
    assert MOD_NN_N(N456, N123) == (1, [7, 8])  # 456 % 123 = 87

def test_MOD_NN_N_exact():
    assert MOD_NN_N(N99, N9) == N0

def test_MOD_NN_N_less():
    assert MOD_NN_N(N123, N456) == N123


# ──────────────────────────────────────────────
# N-13: GCF_NN_N — НОД
# ──────────────────────────────────────────────
def test_GCF_NN_N_basic():
    assert GCF_NN_N(N12, N8) == N4  # НОД(12, 8) = 4

def test_GCF_NN_N_coprime():
    assert GCF_NN_N(N123, N456) == (1, [3])  # НОД(123, 456) = 3

def test_GCF_NN_N_with_zero():
    assert GCF_NN_N(N123, N0) == N123
    assert GCF_NN_N(N0, N456) == N456


# ──────────────────────────────────────────────
# N-14: LCM_NN_N — НОК
# ──────────────────────────────────────────────
def test_LCM_NN_N_basic():
    assert LCM_NN_N(N4, N6) == N12  # НОК(4, 6) = 12

def test_LCM_NN_N_coprime():
    # НОК(3, 5) = 15
    N3 = (0, [3]); N5 = (0, [5]); N15 = (1, [5, 1])
    assert LCM_NN_N(N3, N5) == N15

def test_LCM_NN_N_with_zero():
    assert LCM_NN_N(N0, N123) == N0
    assert LCM_NN_N(N456, N0) == N0
