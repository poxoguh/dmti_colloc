import pytest
from integer import (
    ABS_Z_N, POZ_Z_D, MUL_ZM_Z, TRANS_N_Z, TRANS_Z_N,
    ADD_ZZ_Z, SUB_ZZ_Z, MUL_ZZ_Z, DIV_ZZ_Z, MOD_ZZ_Z
)

# Локальные константы
N0 = (0, [0]); N1 = (0, [1]); N123 = (2, [3, 2, 1])
Z0 = (0, 0, [0]); Z1 = (0, 0, [1]); Z123 = (0, 2, [3, 2, 1])
Z456 = (0, 2, [6, 5, 4]); Zm123 = (1, 2, [3, 2, 1]); Zm456 = (1, 2, [6, 5, 4])

def test_ABS_Z_N(): assert ABS_Z_N(Zm123) == N123
def test_POZ_Z_D(): assert POZ_Z_D(Z123) == 2 and POZ_Z_D(Zm123) == 1 and POZ_Z_D(Z0) == 0
def test_MUL_ZM_Z(): assert MUL_ZM_Z(Z123) == Zm123 and MUL_ZM_Z(Z0) == Z0
def test_TRANS_N_Z(): assert TRANS_N_Z(N123) == Z123
def test_TRANS_Z_N(): assert TRANS_Z_N(Z123) == N123
def test_ADD_ZZ_Z_same_sign(): assert ADD_ZZ_Z(Z123, Z456) == (0, 2, [9, 7, 5])
def test_ADD_ZZ_Z_diff_sign(): assert ADD_ZZ_Z(Z456, Zm123) == (0, 2, [3, 3, 3])
def test_SUB_ZZ_Z(): assert SUB_ZZ_Z(Z456, Z123) == (0, 2, [3, 3, 3])
def test_MUL_ZZ_Z(): assert MUL_ZZ_Z(Z123, Zm456) == (1, 4, [8, 8, 0, 6, 5])
def test_DIV_ZZ_Z(): assert DIV_ZZ_Z(Z456, Z123) == (0, 0, [3])
def test_MOD_ZZ_Z(): assert MOD_ZZ_Z(Z456, Z123) == (0, 1, [7, 8])