#!/bin/python3

########################################
#    Date  : 2023.3
#    Input : jpsol_IJ format vector (complex)
#    Output: hypre_IJ format vector (complex)
########################################

import re


statr_line_number = 1

def trans2hypre_vector(vector, save_vector):
    i = 1
    print("\nstart read " + vector + "\n")
    for line in open(vector): 
        line = line.strip("\n")
        line = re.split(r"[ ]+", line)
        # print(i)
        if i == statr_line_number:
            numrow = int(line[1]) + 1
            with open(save_vector, "w+" ) as fo:
                fo.write(str(numrow)+"\n")
        elif i > statr_line_number:
            with open(save_vector, "a+" ) as fo:
                fo.write(str(line[1])+"\n")

        i = i + 1

if __name__=="__main__":

    filter = 0
    
    if filter == 0:
        
        refine = 2

        vector = ['/home/dyt/matrix/SPD_ams/refine_%d/hypre_x.00000' % refine,
                  '/home/dyt/matrix/SPD_ams/refine_%d/hypre_y.00000' % refine,
                  '/home/dyt/matrix/SPD_ams/refine_%d/hypre_z.00000' % refine,
                  '/home/dyt/matrix/SPD_ams/refine_%d/hypre_b.00000' % refine,]

        save_vector = ['/home/dyt/matrix/SPD_matrix_hypre/refine_%d/seq_x' % refine,
                       '/home/dyt/matrix/SPD_matrix_hypre/refine_%d/seq_y' % refine,
                       '/home/dyt/matrix/SPD_matrix_hypre/refine_%d/seq_z' % refine,
                       '/home/dyt/matrix/SPD_matrix_hypre/refine_%d/seq_b' % refine]

    else :
        refine = 1

        vector = [
                '/home/dyt/matrix/filter_ams/refine_%d/hypre_x.00000' % refine,
                '/home/dyt/matrix/filter_ams/refine_%d/hypre_y.00000' % refine,
                '/home/dyt/matrix/filter_ams/refine_%d/hypre_z.00000' % refine]

        save_vector = [
                    '/home/dyt/matrix/filter_matrix_hypre/refine_%d/seq_x' % refine, 
                    '/home/dyt/matrix/filter_matrix_hypre/refine_%d/seq_y' % refine,
                    '/home/dyt/matrix/filter_matrix_hypre/refine_%d/seq_z' % refine]

    for num in range(len(vector)):
        trans2hypre_vector(vector[num], save_vector[num])

