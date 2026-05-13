import pytest
from polynomial import (
    ADD_PP_P, SUB_PP_P, MUL_PQ_P, MUL_PXK_P,
    LED_P_Q, DEG_P_N, FAC_P_Q, MUL_PP_P,
    DIV_PP_P, MOD_PP_P, GCF_PP_P, DER_P_P, NMR_P_P
)

# Локальные константы
N1 = (0, [1]); N0 = (0, [0])
Z0 = (0, 0, [0]); Z1 = (0, 0, [1]); Zm1 = (1, 0, [1]); Z2 = (0, 0, [2])
Q0 = (Z0, N1); Q1 = (Z1, N1); Qm1 = (Zm1, N1); Q2_1 = (Z2, N1)

P0 = (-1, [])
P1 = (0, [Q1])
Px = (1, [Q0, Q1])
Px1 = (1, [Q1, Q1])
Pxm1 = (1, [Qm1, Q1])
Px2 = (2, [Q0, Q0, Q1])
Px2m1 = (2, [Qm1, Q0, Q1])
P2x = (1, [Q0, Q2_1])

def test_ADD_PP_P(): assert ADD_PP_P(Px1, Pxm1) == P2x
def test_SUB_PP_P(): assert SUB_PP_P(Px1, Pxm1) == (0, [ ( (0,0,[2]), N1 ) ])
def test_MUL_PQ_P(): assert MUL_PQ_P(Px1, Q2_1) == (1, [ ( (0,0,[2]), N1 ), Q2_1 ])
def test_MUL_PXK_P(): assert DEG_P_N(MUL_PXK_P(Px1, 2)) == 3
def test_LED_P_Q(): assert LED_P_Q(Px2m1) == Q1
def test_DEG_P_N(): assert DEG_P_N(Px2m1) == 2 and DEG_P_N(P0) == -1
def test_MUL_PP_P(): assert MUL_PP_P(Px1, Pxm1) == Px2m1
def test_DIV_PP_P(): assert DIV_PP_P(Px2m1, Px1) == Pxm1
def test_MOD_PP_P(): assert MOD_PP_P(Px2m1, Px1) == P0
def test_GCF_PP_P(): assert GCF_PP_P(Px2m1, Pxm1) == Pxm1
def test_DER_P_P(): assert DER_P_P(Px2) == P2x
def test_NMR_P_P():
    # (x-1)^2 = x^2 - 2x + 1
    P_sq = (2, [Q1, ( (1,0,[2]), N1 ), Q1])
    assert DEG_P_N(NMR_P_P(P_sq)) == 1