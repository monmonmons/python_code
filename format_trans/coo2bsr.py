#!/bin/python3

# run note:
# spack load python@3.9.13
# python coo2bsr.py
import re
import numpy as np
from scipy.sparse import bsr_array

matrix = '/home/matrix/solverchanllenge2021/solverchallenge21_07/solverchallenge21_07_A.mtx'
matrix_type = 'mtx'
statr_line_number = 4
block_size = 4
row_first = 1
col_first = 1

save_matrix = '/home/matrix/solverchanllenge2021/fasp_bsr/fasp_matrix07_bs4'

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
            print(line[2])
            precision = len(line[2].split('.')[1])
        row.append(int(line[0]) - row_first)
        col.append(int(line[1]) - col_first)
        value.append(float(line[2]))
    i = i + 1

# print(format(value[0], '.'+str(precision)+'f'))

print("\nread matrix success!\n")

bsr = bsr_array((value, (row, col)), blocksize=(block_size,block_size), shape=(numrow, numrow))

numblock = bsr.indptr[-1]
storage_manner = 0
numblock_row = len(bsr.indptr) - 1

# for i in range(numblock_row):
#     for j in range(bsr.indptr[i],bsr.indptr[i+1],1):
#         if(i==2):
#             print(bsr.indices[j])
# print(bsr.nnz)
# print(len(bsr.indices))


with open(save_matrix, "w+" ) as fo:
    fo.write(str(numblock_row) + " " + str(numblock_row) + " " + str(numblock) + "\n")
    fo.write(str(block_size) + "\n")
    fo.write(str(storage_manner) + "\n")
    fo.write(str(numblock_row + 1) + "\n")

    for i in bsr.indptr:
        fo.write(str(i)+"\n")

    fo.write(str(numblock) + "\n")
    for i in bsr.indices:
        fo.write(str(i)+"\n")

    fo.write(str(bsr.nnz) + "\n")    
    for i in bsr.data.flatten():
        fo.write(str(format(i, '.'+str(precision)+'f'))+"\n")
