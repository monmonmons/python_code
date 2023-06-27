#!/bin/python3

########################################
#    Date  : 2023.5
#    Input : jpsol_IJ format matrix (multiple files)
#    Output: hypre_CSR format matrix
########################################

import os
import re
import subprocess

def trans2hypre_matrix(matrix_path, matrix_name, save_matrix):

    row_first = 0
    col_first = 0
    row = []
    col = []
    value = []

    # files = os.listdir(matrix_path)
    # print("find "+ matrix_path + " -name \"" + matrix_name + "_*\"")
    _, files = subprocess.getstatusoutput("find "+ matrix_path + " -name \"" + matrix_name + ".*\"")
    
    files = files.split("\n")
    
    # print(files)
    
    for file in files:
        i = 0
        print("\nstart read " + file + "\n")
        for line in open(file, "r" ):
            line = line.strip("\n")
            line = re.split(r"[ ]+", line)
            #print(line)
            if(i > 0):
                row.append(int(line[0]) - row_first)
                col.append(int(line[1]) - col_first)
                value.append(str(line[2]))
            i = i + 1

    numrow = max(row) + 1
    print(numrow)
    print(max(col) + 1)
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

    print(row_ptr[-1])
    
    print("\ntrans to csr success!\n")

    with open(save_matrix, "w+" ) as fo:
        fo.write(str(numrow)+"\n")
        for i in range(0, numrow + 1):
            fo.write(str(row_ptr[i] + 1)+"\n")
        for i in range(0, len(col)):
            fo.write(str(col[i] + 1)+"\n")
        for i in range(0, len(value)):
            fo.write(str(value[i])+"\n")

def trans2hypre_vector(rhs_path, rhs_name, save_rhs):
    index = []
    value = []
    # files = os.listdir(rhs_file)
    
    _, files = subprocess.getstatusoutput("find "+ rhs_path + " -name \"" + rhs_name + ".*\"")
    
    files = files.split("\n")
    
    print(files)
    
    for file in files:
        i = 0
        print("\nstart read" + " " + file + "\n")
        for line in open(file, "r" ):
            line = line.strip("\n")
            line = re.split(r"[ ]+", line)
            if(i > 0):
                index.append(int(line[0]))
                value.append(str(line[1]))
            i = i + 1 
    Z = zip(index,value)
    Z = sorted(Z,key=lambda s: s[0],reverse=False)

    print("\nread vector success!\n")

    index,value = zip(*Z)
    
    print(len(value))

    with open(save_rhs, "w+" ) as fo:
        fo.write(str(len(value))+"\n")
        for i in range(0, len(value)):
            fo.write(str(value[i])+"\n")

    print("\nwrite vector to " + save_rhs + " success!\n")
    
def trans2hypre_vector_complex(rhs_path, rhs_name, save_rhs):
    index = []
    value_real = []
    value_imag = []
    
    # dict_real = dict()
    # dict_imag = dict()
    
    _, files = subprocess.getstatusoutput("find "+ rhs_path + " -name \"" + rhs_name + "_*\"")
    
    files = files.split("\n")
    
    print(files)
    
    for file in files:
        i = 0
        print("\nstart read " + file + "\n")
        for line in open(file, "r" ):
            line = line.strip("\n")
            line = re.split(r"[ ]+", line)
            if(i > 0):
                row = int(line[1])
                # if (row in dict_real.keys()) == False:
                #     dict_real[row] = str(line[2])
                #     dict_imag[row] = str(line[3])
                index.append(int(line[1]))
                value_real.append(str(line[2]))
                value_imag.append(str(line[3]))
            i = i + 1 
    
    ##### real part #####
    # print("dict length: " + str(len(dict_real)))
    
    print("index length before: " + str(len(index)))
    
    Z = dict(zip(index,value_real))
    
    print("Z length: " + str(len(Z)))
    
    index_new = list(Z.keys())
    value_real = list(Z.values())
    
    print("index length: " + str(len(index_new)))
    
    Z = zip(index_new,value_real)
    Z = sorted(Z,key=lambda s: s[0],reverse=False)

    print("\nread vector real part success!\n")

    index_new,value_real = zip(*Z)
    
    print(len(value_real))

    with open(save_rhs[0], "w+" ) as fo:
        fo.write(str(len(value_real))+"\n")
        for i in range(0, len(value_real)):
            fo.write(str(value_imag[i])+"\n")
            
    print("\nwrite vector real part to " + save_rhs[0] + " success!\n")
    
    ##### imag part #####
    
    print("index length before: " + str(len(index)))
    
    Z = dict(zip(index,value_imag))
    
    print("Z length: " + str(len(Z)))
    
    index_new = list(Z.keys())
    value_imag = list(Z.values())
    
    print("index length: " + str(len(index_new)))
    
    Z = zip(index_new,value_imag)
    Z = sorted(Z,key=lambda s: s[0],reverse=False)

    print("\nread vector imag part success!\n")

    index_new,value_imag = zip(*Z)
    
    print(len(value_imag))

    with open(save_rhs[1], "w+" ) as fo:
        fo.write(str(len(value_imag))+"\n")
        for i in range(0, len(value_imag)):
            fo.write(str(value_imag[i])+"\n")

    print("\nwrite vector real part to " + save_rhs[1] + " success!\n")
     
if __name__=="__main__":
    
    matrix = 0
    
    complex = 1
    
    if matrix == 1 :
        
        matrix_path = '/home/dyt/matrix/sipB_ams'
        matrix_name = ['hypre_IJ.M', 'hypre_IJ.G']
        
        save_matrix = ['/home/dyt/matrix/sipB_matrix_hypre/hypre_CSR.M',
                        '/home/dyt/matrix/sipB_matrix_hypre/hypre_CSR.G']
        
        # for num in range(0, len(matrix_name)):
        #     trans2hypre_matrix(matrix_path, matrix_name[num], save_matrix[num])
        num = 1
        trans2hypre_matrix(matrix_path, matrix_name[num], save_matrix[num])
    
    else :
        if complex == 0 :
            vector_path = '/home/dyt/matrix/sipB_ams'
            vector_name = [ 'hypre_x',
                            'hypre_y',
                            'hypre_z']
            save_vector = ['/home/dyt/matrix/sipB_matrix_hypre/seq_x',
                            '/home/dyt/matrix/sipB_matrix_hypre/seq_y',
                            '/home/dyt/matrix/sipB_matrix_hypre/seq_z']
            
            for num in range(0, len(vector_name)):
                trans2hypre_vector(vector_path, vector_name[num], save_vector[num])
                
        else :
            vector_path = '/home/dyt/matrix/sipB_ams'
            vector_name = ['jpsol_b', 'jpsol_rhs_iter']
            save_vector = ['/home/dyt/matrix/sipB_matrix_hypre/seq_b0_real',
                            '/home/dyt/matrix/sipB_matrix_hypre/seq_b0_imag',
                            '/home/dyt/matrix/sipB_matrix_hypre/seq_b1_real',
                            '/home/dyt/matrix/sipB_matrix_hypre/seq_b1_imag']
            
            for num in range(0, len(vector_name)):
                trans2hypre_vector_complex(vector_path, vector_name[num], save_vector[2*num:2*num+2])
            
            
        
    
    
