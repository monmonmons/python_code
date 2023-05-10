#!/bin/python3

########################################
#    Date  : 2023.3
#    Input : jpsol_IJ format vector
#    Output: hypre_IJ format vector
########################################

import re

def trans2hypre_vector(vector, save_vector, pos):
    i = 1
    print("\nstart read " + vector + "\n")
    for line in open(vector): 
        line = line.strip("\n")
        line = re.split(r"[ ]+", line)
        # print(line)
        if i == statr_line_number:
            numrow = int(line[1])
            with open(save_vector, "w+" ) as fo:
                fo.write(str(numrow)+"\n")
        elif i > statr_line_number:
            if (pos == 0):
                with open(save_vector, "a+" ) as fo:
                    fo.write(str(line[2])+"\n")
            else :
                with open(save_vector, "a+" ) as fo:
                    fo.write(str(line[3])+"\n")
        i = i + 1

if __name__=="__main__":

    refine = 0

    vector = [
            '/home/dyt/matrix/filter_ams/refine_%d/jpsol_rhs_0_00000000' % refine,
            '/home/dyt/matrix/filter_ams/refine_%d/jpsol_rhs_iter_00000000' % refine]

    save_vector = [
                '/home/dyt/matrix/filter_matrix_hypre/refine_%d/seq_b0_real' % refine,
                '/home/dyt/matrix/filter_matrix_hypre/refine_%d/seq_b0_imag' % refine, 
                '/home/dyt/matrix/filter_matrix_hypre/refine_%d/seq_b1_real' % refine, 
                '/home/dyt/matrix/filter_matrix_hypre/refine_%d/seq_b1_imag' % refine]

    statr_line_number = 1

    for num in range(len(vector)):
        trans2hypre_vector(vector[num], save_vector[2*num], 0)
        trans2hypre_vector(vector[num], save_vector[2*num+1], 1)
        
    # trans2hypre_vector(vector[0], save_vector[0], 0)
    # trans2hypre_vector(vector[0], save_vector[1], 1)
