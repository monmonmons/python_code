#!/bin/python3

########################################
#    Date  : 2023.3
#    Input : hypre_IJ format matrix
#    Output: hypre_CSR format matrix
########################################

import os
import re

def trans2jxpamg_matrix(matrix, save_matrix):

    row_first = 0
    col_first = 0
    row = []
    col = []
    value = []

    # files = os.listdir(matrix_path)
    # for file in files:
    i = 0
    print("\nstart read " + matrix + "\n")
    for line in open(matrix, "r" ):
        line = line.strip("\n")
        line = re.split(r"[ ]+", line)
        #print(line)
        if(i > 0):
            row.append(int(line[0]) - row_first)
            col.append(int(line[1]) - col_first)
            value.append(str(line[2]))
        i = i + 1

    numrow = max(row) + 1
    print("num of row: " + str(numrow) + "\n")
    Z = zip(row,col,value)
    Z = sorted(Z,key=lambda s: s[0],reverse=False)    

    print("\nread matrix success!\n")

    row,col,value = zip(*Z)

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
            fo.write(str(row_ptr[i] + 1)+"\n")
        for i in range(0, len(col)):
            fo.write(str(col[i] + 1)+"\n")
        for i in range(0, len(value)):
            fo.write(str(value[i])+"\n")

def trans2jxpamg_rhs(rhs_file, save_rhs):
    index = []
    value = []
    files = os.listdir(rhs_file)
    for file in files:
        i = 0
        print("\nstart read" + " " + file + "\n")
        for line in open(rhs_file+"/"+file, "r" ):
            line = line.strip("\n")
            line = re.split(r"[ ]+", line)
            if(i > 0):
                index.append(int(line[0]))
                value.append(str(line[1]))
            i = i + 1 
    Z = zip(index,value)
    Z = sorted(Z,key=lambda s: s[0],reverse=False)

    print("\nread rhs success!\n")

    index,value = zip(*Z)

    with open(save_rhs, "w+" ) as fo:
        fo.write(str(len(value))+"\n")
        for i in range(0, len(value)):
            fo.write(str(value[i])+"\n")

if __name__=="__main__":
    
    # matrix_path = ['/home/dyt/code/python_script/IJ_matrix/job_seq_IJ_A',
    #                 '/home/dyt/code/python_script/IJ_matrix/job_seq_IJ_G']

    # save_matrix = ['/home/dyt/Software/hypre_2.27/src/thmaxwell/jpsol_ams/matrix_IJ.A',
    #                 '/home/dyt/Software/hypre_2.27/src/thmaxwell/jpsol_ams/matrix_IJ.G']
    refine = 1

    matrix = ['/home/dyt/matrix/filter_matrix_hypre/subspace/matrix_A_G.00000',
              '/home/dyt/matrix/filter_matrix_hypre/subspace/matrix_A_Pix.00000',
              '/home/dyt/matrix/filter_matrix_hypre/subspace/matrix_A_Piy.00000',
              '/home/dyt/matrix/filter_matrix_hypre/subspace/matrix_A_Piz.00000']

    save_matrix = ['/home/dyt/matrix/filter_matrix_hypre/subspace/hypre_A_G',
                   '/home/dyt/matrix/filter_matrix_hypre/subspace/hypre_A_Pix',
                   '/home/dyt/matrix/filter_matrix_hypre/subspace/hypre_A_Piy',
                   '/home/dyt/matrix/filter_matrix_hypre/subspace/hypre_A_Piz'
                   ]
    

    for num in range(len(matrix)):
        trans2jxpamg_matrix(matrix[num], save_matrix[num])

    

