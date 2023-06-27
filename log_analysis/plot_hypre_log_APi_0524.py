#!/usr/bin/python3
# -*- coding: UTF-8 -*- 

########################################
#    Date  : 2023.5
#    Input : hypre logfile
#    Output: Time, Iterations, Rel res
########################################

import os
import re
import pandas as pd
import csv
import numpy as np 
import matplotlib.pyplot as plt

def get_re_obj(type_num):
        
    if(type_num == 0):
        my_obj = re.compile(r'.*?Number of processes = (?P<np>\d+)'
                            ,re.S)
        
    elif(type_num == 10):
        my_obj = re.compile(r'.*?Problem size of matrix A: (?P<Size>\d+) x'
                            ,re.S)
    
    elif(type_num == 11):
        my_obj = re.compile(r'.*?L2 norm of b: (?P<Init_res>\d+.\d+e[+-]?\d+)\n'
                            ,re.S)
    elif(type_num == 12):
        my_obj = re.compile(r'.*?Iterations = (?P<Iter>\d+)'
                            ,re.S)
    
    elif(type_num == 13):
        my_obj = re.compile(r'.*?Final L2 norm of residual: (?P<Final_res>\d+.\d+e[+-]?\d+)\n'
                            ,re.S)
        
    elif(type_num == 14):
        my_obj = re.compile(r'.*?Final Relative Residual Norm = (?P<Rel_res>\d+.\d+e[+-]?\d+)\n'
                            ,re.S)
    
    elif(type_num == 15):
        my_obj = re.compile(r'.*? Solve:\n  wall clock time = (?P<Solve_Time>\d+.\d+) seconds\n'
                            ,re.S)
    elif(type_num == 16):
        my_obj = re.compile(r'.*? Setup:\n  wall clock time = (?P<Setup_Time>\d+.\d+) seconds\n'
                            ,re.S)
        
    return my_obj


def init_my_dict():
    dict_tmp = {}
    return dict_tmp

def get_dimA_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = int(value)
        break
    return dict_tmp

def get_rank_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = int(value)
        break
    return dict_tmp

def get_solvetime_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = float(value)
        break
    return dict_tmp

def get_setuptime_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = float(value)
        break
    return dict_tmp

def get_iter_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = int(value)
        break
    return dict_tmp

def get_residual_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = value
        break
    return dict_tmp

def get_time_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = float(value)
        break
    return dict_tmp



def get_iters_info(result_content,my_obj,dict_tmp,erro_index):
    result = my_obj.finditer(result_content)
    for k in result:     
        dict = k.groupdict()
        
        for key,value in dict.items():
            value = float(value)
            if(key == "Iter"):
                dict_tmp[key] = int(value)
            elif(key == "Rel Res"):
                dict_tmp[key] = float(value)
        break   
    #print(my_dict)
    return dict_tmp

# 从文件名提取参数
def get_par_from_filename(filename,dict):
    list = filename.split("_")
    print(list)
    for i in range(0, len(list), 2):
        if list[i] == 'rhs':
            dict["rhs"] = int(list[i+1])
        elif list[i] == 'AMG':
            dict["method"] = list[i+1]
        
    dict["rlxn"] = int(list[-1].split(".")[0])
    
    dict["brln"] = int(list[-2])
    
    return dict

#提取每次运行的mpip文件的信息
# 1.找到对应的文件名
# 2.打开文件，用正则表达式提取信息
# 3.最后处理数据，写入到结果字典中


#TODO:同一进程数下，同一l下m排序，再s
if __name__=="__main__":
    #待读取文件的文件夹绝对地址
    file_path = '/home/dyt/test_filter/hypre_thmaxwell/filter_log/refine_1/APi'
    dataframe_dir = "/home/dyt/test_filter/hypre_thmaxwell/table/filter_APi_1.xls"
    
    files = os.listdir(file_path) # 获得文件夹中所有文件的名称列表
    result_list= []
    
    for file in files:
        with open(file_path+"/"+file, "r" ) as fo:
            dict_tmp = init_my_dict()
            dict_tmp = get_par_from_filename(file,dict_tmp)
            result_content = fo.read()
            print("\nread" + " " + file + " success\n")
            
            dict_tmp = get_iter_info(result_content,get_re_obj(10),dict_tmp)        # size 
            dict_tmp = get_iter_info(result_content,get_re_obj(12),dict_tmp)        # Iters 
            
            dict_tmp = get_residual_info(result_content,get_re_obj(11),dict_tmp)    # Init res
            dict_tmp = get_residual_info(result_content,get_re_obj(13),dict_tmp)    # Final res
            dict_tmp = get_residual_info(result_content,get_re_obj(14),dict_tmp)    # Rel res
            
            
            
            dict_tmp = get_time_info(result_content,get_re_obj(15),dict_tmp)   # setup
            dict_tmp = get_time_info(result_content,get_re_obj(16),dict_tmp)  # solve
            
            result_list.append(dict_tmp)
            print(dict_tmp)

    data = pd.DataFrame(result_list)
    #data = data.sort_index(axis=1)
    #data = data.sort_values(by=['num_rows_A', 'rank'], ascending=True)
    #data = data.sort_values(by=['theta','rank'], ascending=True)    
    data.to_excel(dataframe_dir)
    
    
    