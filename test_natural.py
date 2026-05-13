import pytest
from natural import (
    COM_NN_D, NZER_N_B, ADD_1N_N, ADD_NN_N,
    SUB_NN_N, MUL_ND_N, MUL_NK_N, MUL_NN_N,
    SUB_NDN_N, DIV_NN_DK, DIV_NN_N, MOD_NN_N,
    GCF_NN_N, LCM_NN_N
)

# Константы для тестов
N0   = (0, [0])
N1   = (0, [1])
N9   = (0, [9])
N10  = (1, [0, 1])
N99  = (1, [9, 9])
N100 = (2, [0, 0, 1])
N123 = (2, [3, 2, 1])
N456 = (2, [6, 5, 4])
N12  = (1, [2, 1])
N8   = (0, [8])
N4   = (0, [4])
N6   = (0, [6])

def test_COM_NN_D_greater(): assert COM_NN_D(N456, N123) == 2
def test_COM_NN_D_equal(): assert COM_NN_D(N123, N123) == 0
def test_COM_NN_D_less(): assert COM_NN_D(N123, N456) == 1
def test_NZER_N_B_nonzero(): assert NZER_N_B(N123) is True
def test_NZER_N_B_zero(): assert NZER_N_B(N0) is False
def test_ADD_1N_N_simple(): assert ADD_1N_N(N9) == N10
def test_ADD_1N_N_carry(): assert ADD_1N_N(N99) == N100
def test_ADD_1N_N_zero(): assert ADD_1N_N(N0) == N1
def test_ADD_NN_N_basic(): assert ADD_NN_N(N123, N456) == (2, [9, 7, 5])
def test_ADD_NN_N_with_zero(): assert ADD_NN_N(N123, N0) == N123
def test_SUB_NN_N_basic(): assert SUB_NN_N(N456, N123) == (2, [3, 3, 3])
def test_SUB_NN_N_equal(): assert SUB_NN_N(N123, N123) == N0
def test_SUB_NN_N_invalid():
    with pytest.raises(ValueError): SUB_NN_N(N123, N456)
def test_MUL_ND_N_basic(): assert MUL_ND_N(N123, 3) == (2, [9, 6, 3])
def test_MUL_ND_N_zero_digit(): assert MUL_ND_N(N123, 0) == N0
def test_MUL_NK_N_basic(): assert MUL_NK_N(N123, 2) == (4, [0, 0, 3, 2, 1])
def test_MUL_NK_N_zero_num(): assert MUL_NK_N(N0, 5) == N0  # Исправлено
def test_MUL_NN_N_basic(): assert MUL_NN_N(N123, N456) == (4, [8, 8, 0, 6, 5])
def test_SUB_NDN_N_basic(): assert SUB_NDN_N(N456, 3, N123) == (1, [7, 8])
def test_DIV_NN_DK_basic(): assert DIV_NN_DK(N456, N123, 0) == 3
def test_DIV_NN_N_basic(): assert DIV_NN_N(N456, N123) == (0, [3])
def test_MOD_NN_N_basic(): assert MOD_NN_N(N456, N123) == (1, [7, 8])
def test_GCF_NN_N_basic(): assert GCF_NN_N(N12, N8) == N4
def test_GCF_NN_N_coprime(): assert GCF_NN_N(N123, N456) == (0, [3])  # Исправлено: 3 → (0, [3])
def test_GCF_NN_N_with_zero():
    assert GCF_NN_N(N123, N0) == N123
    assert GCF_NN_N(N0, N456) == N456
def test_LCM_NN_N_basic(): assert LCM_NN_N(N4, N6) == N12