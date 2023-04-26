#!/bin/python3

import os
import sys
import re
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, coo_matrix, load_npz, save_npz
from scipy.sparse.linalg import eigs
import matplotlib.pyplot as plt
import seaborn as sns

######   Read matrix  ############
def load_IJmatrix(filename, row_first = 0, col_first = 0):

    print("\nstart read " + filename + "\n")
    i = 0
    for line in open(filename, "r" ):
        line = line.strip("\n")
        line = re.split(r"[ ]+", line)
        if (i == 0) :
            size = int(line[1]) - int(line[0]) + 1
            row = []
            col = []
            data = []
        if (i > 0):
            row.append(int(line[0]) - row_first)
            col.append(int(line[1]) - col_first)
            data.append(float(line[2]))
        i = i + 1

    if (size == len(row)):
        print("num of row: " + len(row) + "\n")

    print("\nread matrix success!\n")

    row = np.array(row)
    col = np.array(col)
    data = np.array(data, dtype=np.float64)

    matrix = coo_matrix((data, (row, col)), shape=(size, size), dtype=np.float64)

    nnz = matrix.count_nonzero()
    print("nnz of matrix: %d" % nnz)

    return matrix, nnz

def load_IJmatrix_complex(filename, row_first = 0, col_first = 0):

    print("\nstart read " + filename + "\n")
    i = 1
    for line in open(filename, "r" ):
        line = line.strip("\n")
        line = re.split(r"[ ]+", line)
        
        # print(line)
        
        if (i == 1) :
            size = int(line[1])
            print("size of matrix: " + str(size) + "\n")
            row_ptr = []
            col_idx = []
            data_real = []
            data_imag = []
        if (i == 2) :
            nnz = int(line[1])
            
        if ( i <= size + 2):
            i = i + 1
            continue
        elif (i > size + 2 and i <= 2 * size + 3):
            row_ptr.append(int(line[1]) - row_first)
        elif (i > 2 * size + 3 and i <= 2 * size + 3 + nnz):
            col_idx.append(int(line[1]) - col_first)
        else:
            # print(line)
            data_real.append(float(line[0]))
            data_imag.append(float(line[1]))
            
        i = i + 1

    if (size == len(row_ptr) - 1):
        print("num of row: " + str(size))

    print("\nread matrix success!\n")

    row_ptr = np.array(row_ptr)
    col_idx = np.array(col_idx)
    data_real = np.array(data_real, dtype=np.float64)
    data_imag = np.array(data_imag, dtype=np.float64)
    data_complex = np.array(np.sqrt(data_real ** 2 + data_imag ** 2))
    
    matrix_real = csr_matrix((data_real, col_idx, row_ptr), shape=(size, size), dtype=np.float64)
    matrix_imag = csr_matrix((data_imag, col_idx, row_ptr), shape=(size, size), dtype=np.float64)

    matrix_complex = csr_matrix((data_complex, col_idx, row_ptr), shape=(size, size), dtype=np.float64)
    
    nnz_real = matrix_real.count_nonzero()
    nnz_imag = matrix_imag.count_nonzero()
    print("nnz of matrix_real: %d" % nnz_real)
    print("nnz of matrix_imag: %d" % nnz_imag)

    return matrix_real, matrix_imag, matrix_complex, nnz_real, nnz_imag
    

######   Plot matrix  ############
def plot_matrix(matrix, refine, file = "matrix"):
    """
    Plots a matrix.
    """
    plt.figure(figsize=(20, 20))
    plt.title("refine = %d" % refine)
    plt.spy(matrix, markersize=0.02)
    # plt.show()
    file_path = "plot/" + file + "_%d.png" % refine
    plt.savefig(file_path, dpi = 500, bbox_inches='tight')
    
def plot_matrix_data(val, refine, bins_lower, bins_upper, title="", file="matrix"):
    """
    Plots matrix data.
    """
    plt.figure(figsize=(20, 20))
    sns.histplot(data = val, kde=False, discrete=False, binwidth=1, binrange=[bins_lower, bins_upper], stat="percent")
    plt.xlabel("nnz per row")
    plt.title(title + " (refine = %d)" % refine)
    file_path = "plot/" + file + "_%d.png" % refine
    plt.savefig(file_path, dpi = 500, bbox_inches='tight')
    
def plot_matrix_data_log(val, refine, bins_lower, bins_upper, save_flag = 0, title="", file="matrix"):
    """
    Plots matrix data by log10.
    """
    val_range = np.log10(val)

    plt.figure(figsize=(20, 20))
    plt.xlabel("data range")
    sns.histplot(data = val_range, kde=False, discrete=False, binwidth=1, binrange=[bins_lower, bins_upper], stat="percent")
    plt.title(title + " (refine = %d)" % refine)
    
    if (save_flag == 1):
        file_path = "plot/" + file + "_%d.png" % refine
        plt.savefig(file_path, dpi = 500, bbox_inches='tight')
    else :
        plt.show()
        
######   Analyze matrix  ############
def matrix_property(matrix, file, output_file, plot_data_flag = 0):
    size = matrix.shape[0]
    num_nonzeros = matrix.count_nonzero()
    print("size of matrix %s: %d" % (file, size))
    print("nnz of matrix %s : %d\n" % (file, num_nonzeros))
    
    max_eigenvalue = eigs(matrix, k=2, return_eigenvectors=False, which='LM')
    # min_eigenvalue = eigs(matrix, k=2, return_eigenvectors=False, which='SM')
    
    diag = matrix.diagonal()
    diag_max = max(diag)
    diag_min = min(diag)
    num_diag_pos = np.array([diag > 0]).sum()
    num_diag_neg = np.array([diag < 0]).sum()

    nnz_per_row = matrix.getnnz(axis=1)
    nnz_per_row_max = max(nnz_per_row)
    nnz_per_row_min = min(nnz_per_row)
    
    bins_lower = int(np.floor(nnz_per_row_min))
    bins_upper = int(np.ceil(nnz_per_row_max))
    bins_nnz = [i for i in range(bins_lower, bins_upper+2, 1)]
    nnz_per_row_range = pd.cut(nnz_per_row, bins_nnz, right=False)
    nnz_per_row_range_count = pd.value_counts(nnz_per_row_range, sort=False)
    if (nnz_per_row_range_count.sum() == size):
        print("nnz per row range count success!")
    else:
        print("nnz per row range count = %d, nnz = %d" % (nnz_per_row_range_count.sum(), size))


    ## histogram of nnz per row 
    if (plot_data_flag == 1):
        plot_matrix_data(nnz_per_row, refine, bins_lower, bins_upper, "nnz per row", "%s_nnz" % file)
    
    ## Off diagonal
    zero_diag_matrix = matrix - coo_matrix((diag, (range(size), range(size))), shape=(size, size))

    offdiag_max = max(abs(zero_diag_matrix.data))
    offdiag_min = min(abs(zero_diag_matrix.data))
    offdiag_min_act = min(zero_diag_matrix.data)

    row_ptr = zero_diag_matrix.indptr
    # off-diag values
    num_offdiag_pos = 0
    num_offdiag_neg = 0
    # diagonal dominant
    num_diag_dominant = 0
    num_diag_non_dominant = 0
    num_equal_diag_dominant = 0
    num_equal_diag_non_dominant = 0

    # offd all negative -- Z property
    num_Z_row = 0
    num_dd_Z_row = 0
    max_bandwidth = 0
    
    for i in range(len(row_ptr)-1):
        sum = 0
        Z_flag = 0
        tmp = max(zero_diag_matrix.indices[row_ptr[i]:row_ptr[i+1]]) - min(zero_diag_matrix.indices[row_ptr[i]:row_ptr[i+1]])
        if (tmp > max_bandwidth):
            max_bandwidth = tmp
        
        for j in range(row_ptr[i], row_ptr[i+1]):
            if (zero_diag_matrix.data[j] > 0):
                Z_flag = 1
                num_offdiag_pos = num_offdiag_pos + 1
            else:
                num_offdiag_neg = num_offdiag_neg + 1
                
            sum = sum + abs(zero_diag_matrix.data[j])
            
        if diag[i] > sum :
            num_diag_dominant = num_diag_dominant + 1
        else :
            num_diag_non_dominant = num_diag_non_dominant + 1
        
        if diag[i] >= sum :
            num_equal_diag_dominant = num_equal_diag_dominant + 1
        else :
            num_equal_diag_non_dominant = num_equal_diag_non_dominant + 1
            
        if Z_flag == 0:
            num_Z_row = num_Z_row + 1
            if diag[i] > sum :
                num_dd_Z_row = num_dd_Z_row + 1

    ## Multiscale
    ratio_max = 0
    ratio_min = 0xFFFFFFF
    ratio_row = []
    for i in range(len(row_ptr)-1):
        row_data = matrix.data[row_ptr[i]:row_ptr[i+1]]
        row_data = row_data[row_data != 0]
        max_row_data = max(abs(row_data))
        min_row_data = min(abs(row_data))
        if (min_row_data) :
            ratio = max_row_data / min_row_data
            ratio_row.append(ratio)
            if (ratio > ratio_max):
                ratio_max = ratio
            if (ratio < ratio_min):
                ratio_min = ratio

    bins_lower = int(np.floor(np.log10(ratio_min)))
    bins_upper = int(np.ceil(np.log10(ratio_max)))
    bins_ratio = [i for i in range(bins_lower, bins_upper+1, 1)]
    ratio_row_range = pd.cut(np.log10(ratio_row), bins_ratio, right=False)
    ratio_row_range_count = pd.value_counts(ratio_row_range, sort=False)
    if (ratio_row_range_count.sum() == size):
        print("ratio row range count success!\n")
    else :
        print("ratio row range count = %d, size = %d" % (ratio_row_range_count.sum(), size))
    
    ##  histogram of ratio per row
    if (plot_data_flag == 1):
        plot_matrix_data_log(ratio_row, refine, bins_lower, bins_upper, 1, "ratio of value per row", "%s_ratio" % file)
    
    ## Multiscale row 
    row = np.where(np.log10(ratio_row)>(bins_upper-1))[0][0]
    data_row = matrix.data[row_ptr[row]:row_ptr[row+1]]
    max_data_row = max(abs(data_row))
    min_data_row = min(abs(data_row))

    ## print
    temp = sys.stdout
    file_ptr = open(output_file, 'w')
    sys.stdout = file_ptr
    print("==============================================")
    print("size of matrix:".ljust(30) + "\t %d" % size)
    print("num of nonzeors:".ljust(30) + "\t %d" % num_nonzeros)
    print("max nnz per row:".ljust(30) + "\t %d" % nnz_per_row_max)
    print("min nnz per row:".ljust(30) + "\t %d" % nnz_per_row_min)
    print("max bandwidth:".ljust(30) + "\t %d" % max_bandwidth)
    print("----------------------------------------------")
    print("num of positive diag:".ljust(30) + "\t %d" % num_diag_pos)
    print("num of negative diag:".ljust(30) + "\t %d" % num_diag_neg)
    print("max diag value:".ljust(30) + "\t %.4e" % diag_max)
    print("min diag value:".ljust(30) + "\t %.4e" % diag_min)
    print("----------------------------------------------")
    print("num of positive off-diag:".ljust(30) + "\t %d" % num_offdiag_pos)
    print("num of negative off-diag:".ljust(30) + "\t %d" % num_offdiag_neg)
    print("max off-diag value(abs):".ljust(30) + "\t %.4e" % offdiag_max)
    print("min off-diag value(abs):".ljust(30) + "\t %.4e" % offdiag_min)
    print("min off-diag value:".ljust(30) + "\t %.4e" % offdiag_min_act)
    print("----------------------------------------------")
    print("num of rows(diag dominant):".ljust(30) + "\t %d (%.2f%%)" % (num_equal_diag_dominant , num_equal_diag_dominant/size*100))
    print("num of rows(strictly dd):".ljust(30) + "\t %d (%.2f%%)" % (num_diag_dominant , num_diag_dominant/size*100))
    print("num of rows(strictly non-dd):".ljust(30) + "\t %d" % num_diag_non_dominant)
    print("num of rows(Z-property):".ljust(30) + "\t %d " % (num_Z_row))
    print("num of rows(dd && Z-property):".ljust(30) + "\t %d" % (num_dd_Z_row))       
    print("----------------------------------------------")
    print("max ratio of row value:".ljust(30) + "\t %.4e" % ratio_max)
    print("    ------------------------------------------")
    print("    max value of the row (abs):".ljust(25) + "\t %.4e" % max_data_row)
    print("    min value of the row (abs):".ljust(25) + "\t %.4e" % min_data_row)
    print("    ------------------------------------------")
    print("min ratio of row value:".ljust(30) + "\t %.4e" % ratio_min)
    print("----------------------------------------------")
    print("max eigenvalue:".ljust(30) + "\t %.2e + %.2e i" % (max_eigenvalue[-1].real, max_eigenvalue[-1].imag))
    # print("min eigenvalue:".ljust(30) + "\t %.2e + %.2e i" % (min_eigenvalue[0].real, min_eigenvalue[0].imag))
    # print("min eigenvalue:".ljust(30) + "\t %.2e + %.2e i" % (min_eigenvalue[1].real, min_eigenvalue[1].imag))
    print("==============================================")
    
    ## Ratio of value per row
    print("\n=====================================================")
    print("range of ratio".ljust(20) + "|\tcount \t percentage  ")
    print("-----------------------------------------------------")
    for i in range(len(ratio_row_range_count)):
        range_str = "[1.0E+%2d , 1.0E+%2d)" % (bins_ratio[i], bins_ratio[i+1])
        print(range_str.ljust(20) + "|\t%6d \t" % (ratio_row_range_count[i]) + ("%2.2f%%" % (ratio_row_range_count[i]/size*100)).rjust(8))
    print("-----------------------------------------------------")
    range_str = "[1.0E+%2d , 1.0E+%2d)" % (bins_ratio[0], bins_ratio[-1])
    print(range_str.ljust(15) + "|\t%6d \t" % (ratio_row_range_count.sum()) + ("%2.2f%%" % (ratio_row_range_count.sum()/size*100)).rjust(8))
    print("=====================================================\n")

    
    ## nnz per row
    print("\n=====================================================")
    print("nnz per row".ljust(15) + "|\tcount \t percentage  ")
    print("-----------------------------------------------------")
    for i in range(len(nnz_per_row_range_count)):
        range_str = "[%2d , %2d)" % (bins_nnz[i], bins_nnz[i+1])
        print(range_str.ljust(15) + "|\t%6d \t" % (nnz_per_row_range_count[i]) + ("%2.2f%%" % (nnz_per_row_range_count[i]/size*100)).rjust(8))
    print("-----------------------------------------------------")
    range_str = "[%2d , %2d)" % (bins_nnz[0], bins_nnz[-1])
    print(range_str.ljust(15) + "|\t%6d \t" % (nnz_per_row_range_count.sum()) + ("%2.2f%%" % (nnz_per_row_range_count.sum()/size*100)).rjust(8))
    print("=====================================================\n")
    
    sys.stdout = temp

if __name__ == "__main__":
    trans_matrix = 1
    complex_matrix = 0
    subspace_matrix = 9
    
    refine = 0
    
    plot_data = 0

    matrix_path = ['/home/dyt/matrix/filter_ams/refine_%d/hypre_IJ.M.00000' % refine, 
                '/home/dyt/matrix/filter_ams/refine_%d/jpsol_CSR.A_00000000' % refine,
                '/home/dyt/matrix/filter_matrix_hypre/subspace/matrix_A_G.00000',
                '/home/dyt/matrix/filter_matrix_hypre/subspace/matrix_A_Pix.00000',
                '/home/dyt/matrix/filter_matrix_hypre/subspace/matrix_A_Piy.00000',
                '/home/dyt/matrix/filter_matrix_hypre/subspace/matrix_A_Piz.00000',
                '/home/dyt/matrix/SPD_matrix_hypre/subspace/matrix_A_G.00000',
                '/home/dyt/matrix/SPD_matrix_hypre/subspace/matrix_A_Pix.00000',
                '/home/dyt/matrix/SPD_matrix_hypre/subspace/matrix_A_Piy.00000',
                '/home/dyt/matrix/SPD_matrix_hypre/subspace/matrix_A_Piz.00000']

    save_matrix_path = ['/home/dyt/matrix/filter_matrix_python/refine_%d/M.npz' % refine, 
                        '/home/dyt/matrix/filter_matrix_python/refine_%d/A_real.npz' % refine,
                        '/home/dyt/matrix/filter_matrix_python/refine_%d/A_imag.npz' % refine,
                        '/home/dyt/matrix/filter_matrix_python/refine_%d/A_norm.npz' % refine,
                        '/home/dyt/matrix/filter_matrix_python/refine_%d/A_G.npz' % refine,
                        '/home/dyt/matrix/filter_matrix_python/refine_%d/A_Pix.npz' % refine,
                        '/home/dyt/matrix/filter_matrix_python/refine_%d/A_Piy.npz' % refine,
                        '/home/dyt/matrix/filter_matrix_python/refine_%d/A_Piz.npz' % refine,
                        '/home/dyt/matrix/SPD_matrix_python/refine_%d/A_G.npz' % refine,
                        '/home/dyt/matrix/SPD_matrix_python/refine_%d/A_Pix.npz' % refine,
                        '/home/dyt/matrix/SPD_matrix_python/refine_%d/A_Piy.npz' % refine,
                        '/home/dyt/matrix/SPD_matrix_python/refine_%d/A_Piz.npz' % refine]
    
    output_file = ["./matrix_property/M_property_%d.txt" % refine,
                   "./matrix_property/A_real_property_%d.txt" % refine,
                   "./matrix_property/A_imag_property_%d.txt" % refine,
                   "./matrix_property/A_norm_property_%d.txt" % refine,
                   "./matrix_property/A_G_property_%d.txt" % refine,
                   "./matrix_property/A_Pix_property_%d.txt" % refine,
                   "./matrix_property/A_Piy_property_%d.txt" % refine,
                   "./matrix_property/A_Piz_property_%d.txt" % refine,
                   "./matrix_property/SPD/A_G_property_%d.txt" % refine,
                   "./matrix_property/SPD/A_Pix_property_%d.txt" % refine,
                   "./matrix_property/SPD/A_Piy_property_%d.txt" % refine,
                   "./matrix_property/SPD/A_Piz_property_%d.txt" % refine]
    
    if (trans_matrix == 1):
        if (complex_matrix == 0):
            if (subspace_matrix == 0):
                matrix, nnz = load_IJmatrix(matrix_path[0])
                save_npz(save_matrix_path[0], matrix)
            elif (subspace_matrix == 1):
                matrix, nnz = load_IJmatrix(matrix_path[2])
                save_npz(save_matrix_path[4], matrix)
            elif (subspace_matrix == 3):
                matrix, nnz = load_IJmatrix(matrix_path[3])
                save_npz(save_matrix_path[5], matrix)
            elif (subspace_matrix == 4):
                matrix, nnz = load_IJmatrix(matrix_path[4])
                save_npz(save_matrix_path[6], matrix)
            elif (subspace_matrix == 5):
                matrix, nnz = load_IJmatrix(matrix_path[5])
                save_npz(save_matrix_path[7], matrix)
            elif (subspace_matrix == 6):
                matrix, nnz = load_IJmatrix(matrix_path[6])
                save_npz(save_matrix_path[8], matrix)
            elif (subspace_matrix == 7):
                matrix, nnz = load_IJmatrix(matrix_path[7])
                save_npz(save_matrix_path[9], matrix)
            elif (subspace_matrix == 8):
                matrix, nnz = load_IJmatrix(matrix_path[8])
                save_npz(save_matrix_path[10], matrix)
            elif (subspace_matrix == 9):
                matrix, nnz = load_IJmatrix(matrix_path[9])
                save_npz(save_matrix_path[11], matrix)
        else:
            matrix_real, matrix_imag, matrix_complex, nnz_real, nnz_imag = load_IJmatrix_complex(matrix_path[1])
            save_npz(save_matrix_path[1], matrix_real)
            save_npz(save_matrix_path[2], matrix_imag)
            save_npz(save_matrix_path[3], matrix_complex)
    else :
        if (complex_matrix == 0):
            if (subspace_matrix == 0):
                matrix = load_npz(save_matrix_path[0])
            elif (subspace_matrix == 1):
                matrix = load_npz(save_matrix_path[4])
            elif (subspace_matrix == 3):
                matrix = load_npz(save_matrix_path[5])
            elif (subspace_matrix == 4):
                matrix = load_npz(save_matrix_path[6])
            elif (subspace_matrix == 5):
                matrix = load_npz(save_matrix_path[7])
            elif (subspace_matrix == 6):
                matrix = load_npz(save_matrix_path[8])
            elif (subspace_matrix == 7):
                matrix = load_npz(save_matrix_path[9])
            elif (subspace_matrix == 8):
                matrix = load_npz(save_matrix_path[10])
            elif (subspace_matrix == 9):
                matrix = load_npz(save_matrix_path[11])
        else: 
            matrix_real = load_npz(save_matrix_path[1])
            matrix_imag = load_npz(save_matrix_path[2])
            matrix_complex = load_npz(save_matrix_path[3])
    
    if (complex_matrix == 0):
        if (subspace_matrix == 0):
            # plot_matrix(matrix, refine, "M_matrix")
            matrix_property(matrix, "M_matrix", output_file[0], plot_data)
        elif (subspace_matrix == 1):
            # plot_matrix(matrix, refine, "A_G_matrix")
            matrix_property(matrix, "A_G_matrix", output_file[4], plot_data)
        elif (subspace_matrix == 3):
            # plot_matrix(matrix, refine, "A_Pix_matrix")
            matrix_property(matrix, "A_Pix_matrix", output_file[5], plot_data)
        elif (subspace_matrix == 4):
            # plot_matrix(matrix, refine, "A_Piy_matrix")
            matrix_property(matrix, "A_Piy_matrix", output_file[6], plot_data)
        elif (subspace_matrix == 5):
            # plot_matrix(matrix, refine, "A_Piz_matrix")
            matrix_property(matrix, "A_Piz_matrix", output_file[7], plot_data)
        elif (subspace_matrix == 6):
            matrix_property(matrix, "A_G_matrix", output_file[8], plot_data)
        elif (subspace_matrix == 7):
            matrix_property(matrix, "A_Pix_matrix", output_file[9], plot_data)
        elif (subspace_matrix == 8):
            matrix_property(matrix, "A_Piy_matrix", output_file[10], plot_data)
        elif (subspace_matrix == 9):
            matrix_property(matrix, "A_Piz_matrix", output_file[11], plot_data)
    else :
        # plot_matrix(matrix_real, refine, "A_matrix_real")
        matrix_property(matrix_real, "A_matrix_real", output_file[1], plot_data)
        
        # plot_matrix(matrix_imag, refine, "A_matrix_imag") 
        matrix_property(matrix_imag, "A_matrix_imag", output_file[2], plot_data)
        
        matrix_property(matrix_complex, "A_matrix_complex", output_file[3], plot_data)