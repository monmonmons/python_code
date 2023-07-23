#!/bin/python3
save_rhs = "/home/matrix/dyt_matrix/jxpamg_560_560_rhs"

numrow = 560*560
with open(save_rhs, "w+" ) as fo:
    fo.write(str(numrow)+"\n")
    for i in range(0, numrow):
        fo.write(str(1)+"\n")