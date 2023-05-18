

# #######################################
#    Date  : 2023.5
#    Input : hypre_IJ format vector
#    Output: plot for 1d vector
########################################

from matplotlib import pyplot as plt
import numpy as np
from itertools import product
import re

    
def plot_vector(filename, size, save_dir, title):
    
    if (size == 1) :
        with open(filename) as fp:
            num = eval(fp.readline())
            vector1 = []
            for i in range(num):
                vector1.append(eval(fp.readline()))
    else : 
        with open(filename[0]) as fp:
            num = eval(fp.readline())
            vector1 = []
            for i in range(num):
                vector1.append(eval(fp.readline()))
    
        with open(filename[1]) as fp:
            num = eval(fp.readline())
            vector2 = []
            for i in range(num):
                vector2.append(eval(fp.readline()))

    # print(vector)
    plt.figure(figsize=(10,8),dpi=200)
    
    plt.subplot(2, 1, 1)
    plt.title(title)
    # plt.imshow([vector1], cmap='jet', aspect='auto')
    plt.plot(np.arange(num), vector1, marker='.', markersize=0.0001)
    
    if (size>1):
        plt.subplot(2, 1, 2)
        plt.plot(np.arange(num), vector2, marker='.', markersize=0.0001)
        
    # plt.show()
    plt.savefig(save_dir)
    

if __name__=="__main__":
    rhs_type = 4
    
    vector = ['/home/dyt/matrix/filter_matrix_hypre/refine_0/hypre_rhs_%d.0' % rhs_type,
              '/home/dyt/matrix/filter_matrix_hypre/refine_0/hypre_sol_rhs_%d.0' % rhs_type]
    
    # vector = ['/home/dyt/matrix/filter_matrix_hypre/refine_0/hypre_rhs_0.0',
    #           '/home/dyt/matrix/filter_matrix_hypre/refine_0/hypre_sol_rhs_0.0']
    
    if rhs_type == 5:
        title = 'rhs_const'
    elif rhs_type == 0:
        title = 'rhs_rand'
    elif rhs_type == 1:
        title = 'rhs_real_b'
    elif rhs_type == 2:
        title = 'rhs_imag_b'
    elif rhs_type == 3:
        title = 'rhs_real_r'
    elif rhs_type == 4:
        title = 'rhs_imag_r'
    
    save_dir = './rhs_%d.png' % rhs_type 
    
    
    plot_vector(vector, 2, save_dir, title)
    
    
