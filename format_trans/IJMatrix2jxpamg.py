#!/bin/python3

import os
import re

def trans2jxpamg_matrix(matrix, save_matrix):

    statr_line_number = 2
    row_first = 1
    col_first = 1
    row = []
    col = []
    value = []
    i = 1
 
    for line in open(matrix):
        line = line.strip("\n")
        line = re.split(r"[ ]+", line)
        # print(line)

        if i == statr_line_number:
            row_first = int(line[0])
            col_first = int(line[1])
            
            row.append(int(line[0]) - row_first)
            col.append(int(line[1]) - col_first)
            value.append(str(line[2]))
        i = i + 1

    numrow = max(row) + 1
    Z = zip(row,col,value)
    Z = sorted(Z,key=lambda s: s[0],reverse=False)    

    print("\nread matrix success!\n")

    row,col,value = zip(*Z)

    # for i in range(406312):
    #     print(row[i],col[i],value[i])
    # exit(0)

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
    matrix = '/home/dyt/code/python_script/jpsol_ams/jpsol.G_00000000'
    save_matrix = '/home/dyt/code/python_script/jpsol_ams/matrix.G'

    trans2jxpamg_matrix(matrix, save_matrix)

    # rhs_path = '/home/matrix/iter00001/b/job0'
    # save_rhs = '/home/matrix/iter00001/b/jxpamg_iter00001_job0_rhs'
    
    # trans2jxpamg_rhs(rhs_path, save_rhs)
