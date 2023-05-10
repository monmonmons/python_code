#!/bin/python3

import re

matrix = '/home/matrix/solverchanllenge2021/solverchallenge21_07/solverchallenge21_07_A.mtx'
save_matrix = '/home/matrix/solverchanllenge2021/solverchallenge21_07/jxpamg_matrix07'
matrix_type = 'mtx'
statr_line_number = 4
row_first = 1
col_first = 1

i = 1
row = []
col = []
value = []
for line in open(matrix): 
    line = line.strip("\n")
    line = re.split(r"[ ]+", line)
    if i == statr_line_number:
        if matrix_type == "mtx":
            numrow = int(line[0])
            numcol = int(line[1])
        elif matrix_type == "data":
            numrow = int(line[1]) - int(line[0]) + 1
            numcol = int(line[3]) - int(line[2]) + 1
    elif i > statr_line_number:
        if i == statr_line_number + 1:
            row_first = int(line[0])
            col_first = int(line[1])
        row.append(int(line[0]) - row_first)
        col.append(int(line[1]) - col_first)
        value.append(str(line[2]))
    i = i + 1

print("\nread matrix success!\n")

row_count = [0]*(numrow)
for i in range(0, len(row)):
    j = row[i]
    row_count[j] = row_count[j] + 1

row_ptr = [0]*(numrow + 1)
for i in range(0, numrow):
    row_ptr[i+1] = row_count[i] + row_ptr[i]

print("\ntrans to csr success!\n")

with open(save_matrix, "w+" ) as fo:
    fo.write(str(numrow)+"\n")
    for i in range(0, numrow + 1):
        fo.write(str(row_ptr[i])+"\n")
    for i in range(0, len(col)):
        fo.write(str(col[i])+"\n")
    for i in range(0, len(value)):
        fo.write(str(value[i])+"\n")
