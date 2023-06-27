#!/usr/bin/python3
# -*- coding: UTF-8 -*- 

########################################
#    Date  : 2023.5
#    Input : JPSOL_jaumin logfile
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
        my_obj = re.compile(r'.*?Number of processes = (?P<rank>\d+)'
                            ,re.S)
        
    elif(type_num == 10):
        my_obj = re.compile(r'.*?Size of A : [(?P<num_rows_A>\d+), (?P<num_cols_A>\d+)]'
                            ,re.S)
    elif(type_num == 11):
        my_obj = re.compile(r'.*?Norm of residual \t(?P<Final_res>\d+.\d+e[+-]?\d+)'
                            ,re.S)
    elif(type_num == 12):
        my_obj = re.compile(r'.*?Norm of init res \t(?P<Init_res>\d+.\d+e[+-]?\d+)'
                            ,re.S)
    elif(type_num == 13):
        my_obj = re.compile(r'.*?Relative Residual norm \t(?P<Rel_res>\d+.\d+e[+-]?\d+)'
                            ,re.S)
    
    
    elif(type_num == 14):
        my_obj = re.compile(r'.*?Number of iterations = (?P<iter>\d+)'
                            ,re.S)
        
    elif(type_num == 20):
        my_obj = re.compile(r'.*?total_time = (?P<solve_time>\d+.\d+)'
                            ,re.S)
    elif(type_num == 21):
        my_obj = re.compile(r'.*?KSPSetUp  (?P<KSPSetUp>\d+.\d+)'
                            ,re.S)
    elif(type_num == 22):
        my_obj = re.compile(r'.*?KSPSolve  (?P<KSPSolve>\d+.\d+)'
                            ,re.S)
    elif(type_num == 27):
        my_obj = re.compile(r'.*?KSPConvergedReason: (?P<reason>.*?)\n'
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
    for i in range(0, len(list), 1):
        if list[i] == 'rhs':
            dict["rhs"] = int(list[i+1].split(".")[0])
        elif list[i] == 'ASM':
            dict["ASM"] = 1
            dict["method"] = list[i+1].split(".")[0]
        elif list[i] == 'GMRES':
            dict["asm_type"] = list[i+1].split(".")[0]
        elif list[i] == 'CG':
            dict["asm_type"] = list[i+1].split(".")[0]
        elif list[i] == 'Cho':
            dict["asm_type"] = list[i+1].split(".")[0]
        elif list[i] == 'refine':
            dict["refine"] = int(list[i+1])
        elif list[i] == 'np':
            dict["np"] = int(list[i+1].split(".")[0])
        elif list[i] == 'tol.log':
            dict["tol"] = 1

    
    # dict["AMG_SM"] = int(list[-1].split(".")[0])
    return dict


#提取每次运行的mpip文件的信息
# 1.找到对应的文件名
# 2.打开文件，用正则表达式提取信息
# 3.最后处理数据，写入到结果字典中


#TODO:同一进程数下，同一l下m排序，再s
if __name__=="__main__":
    #待读取文件的文件夹绝对地址
    file_path = '/home/dyt/test_filter/petsc_thmaxwell/sipB_log/0622_asm_test'
    dataframe_dir = "/home/dyt/test_filter/petsc_thmaxwell/table/SipB_asm_parallel_0622.xls"
    files = os.listdir(file_path) # 获得文件夹中所有文件的名称列表
    result_list= []
    for file in files:
        with open(file_path+"/"+file, "r" ) as fo:
            dict_tmp = init_my_dict()
            dict_tmp = get_par_from_filename(file,dict_tmp)
            result_content = fo.read()
            print("\nread" + " " + file + " success\n")
            
            dict_tmp = get_iter_info(result_content,get_re_obj(14),dict_tmp)
            dict_tmp = get_iter_info(result_content,get_re_obj(10),dict_tmp)
            
            dict_tmp = get_residual_info(result_content,get_re_obj(11),dict_tmp)    # Init res
            dict_tmp = get_residual_info(result_content,get_re_obj(12),dict_tmp)    # Final res
            dict_tmp = get_residual_info(result_content,get_re_obj(13),dict_tmp)    # Rel res
            
            dict_tmp = get_time_info(result_content,get_re_obj(21),dict_tmp)   # setup
            dict_tmp = get_time_info(result_content,get_re_obj(22),dict_tmp)  # solve
            
            result_list.append(dict_tmp)
            print(dict_tmp)

    data = pd.DataFrame(result_list)
    #data = data.sort_index(axis=1)
    #data = data.sort_values(by=['num_rows_A', 'rank'], ascending=True)
    #data = data.sort_values(by=['theta','rank'], ascending=True)    
    data.to_excel(dataframe_dir)