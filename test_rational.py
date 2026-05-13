import pytest
from rational import (
    RED_Q_Q, INT_Q_B, TRANS_Z_Q, TRANS_Q_Z,
    ADD_QQ_Q, SUB_QQ_Q, MUL_QQ_Q, DIV_QQ_Q
)

# Локальные константы
N1 = (0, [1]); N2 = (0, [2]); N3 = (0, [3]); N4 = (0, [4]); N6 = (0, [6])
Z0 = (0, 0, [0]); Z1 = (0, 0, [1]); Z2 = (0, 0, [2]); Z3 = (0, 0, [3]); Zm1 = (1, 0, [1])

Q0 = (Z0, N1); Q1 = (Z1, N1); Q1_2 = (Z1, N2); Q3_2 = (Z3, N2); Qm1 = (Zm1, N1)

def test_RED_Q_Q(): assert RED_Q_Q(( (0,0,[4]), N2 )) == (Z2, N1)
def test_INT_Q_B(): assert INT_Q_B(Q1) is True and INT_Q_B(Q1_2) is False
def test_TRANS_Z_Q(): assert TRANS_Z_Q(Z3) == (Z3, N1)
def test_TRANS_Q_Z(): assert TRANS_Q_Z(Q2_1 := (Z2, N1)) == Z2
def test_ADD_QQ_Q(): assert ADD_QQ_Q(Q1_2, Q1_2) == Q1
def test_SUB_QQ_Q(): assert SUB_QQ_Q(Q3_2, Q1_2) == Q1
def test_MUL_QQ_Q(): assert MUL_QQ_Q(Q1_2, Q3_2) == (Z3, N4)
def test_DIV_QQ_Q(): assert DIV_QQ_Q(Q3_2, Q1_2) == (Z3, N1)
def test_DIV_QQ_Q_zero():
    with pytest.raises(ZeroDivisionError): DIV_QQ_Q(Q1, Q0)