#!/usr/bin/python3
# -*- coding: UTF-8 -*- 

import os
import re
import pandas as pd
import csv
import numpy as np 
import matplotlib.pyplot as plt

def get_re_obj(type_num):
    
    if(type_num == 10):
        my_obj = re.compile(r'.*?the size of A : (?P<num_rows_A>\d+)'
                            ,re.S)
    elif(type_num == 11):
        my_obj = re.compile(r'.*?load system TIME = (?P<load_system_time>\d+.\d+)'
                            ,re.S)
    elif(type_num == 2):
        my_obj = re.compile(r'.*?rank[[](?P<rank>\d+)[]]: mord'
                            ,re.S)
    elif(type_num == 12):
        my_obj = re.compile(r'.*?MPI using (?P<rank>\d+) processors'
                            ,re.S)
    elif(type_num == 13):
        my_obj = re.compile(r'.*?create matrix T TIME = (?P<createT_time>\d+.\d+)'
                            ,re.S)
    elif(type_num == 14):
        my_obj = re.compile(r'.*?create condensation matrix Cs TIME = (?P<createC_time>\d+.\d+)'
                            ,re.S)  
    elif(type_num == 15):
        my_obj = re.compile(r'.*?elimation TIME = (?P<elimt_time>\d+.\d+)'
                            ,re.S)
    elif(type_num == 16):
        my_obj = re.compile(r'.*?condensation TIME = (?P<conden_time>\d+.\d+)'
                            ,re.S)
    elif(type_num == 17):
        my_obj = re.compile(r'.*?size of Ac = (?P<num_rows_Ac>\d+)'
                            ,re.S)
    elif(type_num == 18):
        my_obj = re.compile(r'.*?Number of iterations = (?P<iter>\d+)'
                            ,re.S)
    elif(type_num == 19):
        my_obj = re.compile(r'.*?Relative Residual norm (?P<rel_residual>\d+.\d+e[-+]?\d+)'
                            ,re.S)
    elif(type_num == 9):
        my_obj = re.compile(r'.*?Relative Residual norm (?P<rel_residual>.*?)\n'
                            ,re.S)
    elif(type_num == 20):
        my_obj = re.compile(r'.*?total_time = (?P<solve_time>\d+.\d+)'
                            ,re.S)
    elif(type_num == 21):
        my_obj = re.compile(r'.*?Num levels = (?P<num_levels>\d+)'
                            ,re.S)
    elif(type_num == 22):
        my_obj = re.compile(r'.*?KSPSetUp  (?P<KSPSetUp>\d+.\d+)'
                            ,re.S)
    elif(type_num == 23):
        my_obj = re.compile(r'.*?KSPSolve  (?P<KSPSolve>\d+.\d+)'
                            ,re.S)
    elif(type_num == 24):
        my_obj = re.compile(r'.*?-pc_hypre_boomeramg_coarsen_type (?P<coarsen>.*?)\n'
                            ,re.S)
    elif(type_num == 25):
        my_obj = re.compile(r'.*?-ksp_type (?P<KSPtype>.*?)\n'
                            ,re.S)
    elif(type_num == 26):
        my_obj = re.compile(r'.*?-pc_type (?P<PCtype>.*?)\n'
                            ,re.S)
    elif(type_num == 27):
        my_obj = re.compile(r'.*?KSPConvergedReason: (?P<reason>.*?)\n'
                            ,re.S)                        
    elif(type_num == 28):
        my_obj = re.compile(r'.*?Strength Threshold = (?P<theta>\d+.\d+)'
                            ,re.S)    
    elif(type_num == 29):
        my_obj = re.compile(r'.*?HYPRE_BOOMERAMGSetNodal[(][)] (?P<nodal>\d+)'
                            ,re.S)  
    elif(type_num == 30):
        my_obj = re.compile(r'.*?HYPRE_BoomerAMGSetInterpVecVariant[(][)] (?P<variant>\d+)'
                            ,re.S)  
    return my_obj


def init_my_dict():
    dict_tmp = {}
    #dict_tmp["mpiP_dir_name"] = "mpip"
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

def get_loadtime_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = float(value)
        break
    return dict_tmp

def get_Ttime_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = float(value)
        break
    return dict_tmp

def get_Ctime_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = float(value)
        break
    return dict_tmp

def get_elimationtime_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = float(value)
        break
    return dict_tmp

def get_condensationtime_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = float(value)
        break
    return dict_tmp

def get_dimAc_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = int(value)
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

def get_relresidual_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = value
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

def get_numlevels_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = int(value)
        break
    return dict_tmp

def get_kspsetuptime_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = float(value)
        break
    return dict_tmp

def get_kspsolvetime_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = float(value)
        break
    return dict_tmp

def get_coarsetype_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = value
        break
    return dict_tmp

def get_ksptype_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = value
        break
    return dict_tmp

def get_pctype_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = value
        break
    return dict_tmp

def get_reason_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = value
        break
    return dict_tmp

def get_theta_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = float(value)
        break
    return dict_tmp

def get_header_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            if(key == "num_proccess"):
                dict_tmp[key] = int(value)
            else:
                dict_tmp[key] = value.strip('\'')
        break
    return dict_tmp

def get_nodal_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = int(value)
        break
    return dict_tmp

def get_variant_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = int(value)
        break
    return dict_tmp

def get_iters_info(result_content,my_obj,dict_tmp,erro_index):
    result = my_obj.finditer(result_content)
    for k in result:     
        dict = k.groupdict()
        # result_list.append(dict)
    # print(result_list[-1]) 
        for key,value in dict.items():
            value = float(value)
            if(key == "Iters"):
                dict_tmp[key] = int(value)
            elif(key == "rel_res"):
                dict_tmp[key] = float(value)
        break   
    #print(my_dict)
    return dict_tmp



#提取每次运行的mpip文件的信息
# 1.找到对应的文件名
# 2.打开文件，用正则表达式提取信息
# 3.最后处理数据，写入到结果字典中


#TODO:同一进程数下，同一l下m排序，再s
if __name__=="__main__":
    #待读取文件的文件夹绝对地址
    file_path = '/home/dyt/test_filter/hypre_thmaxwell/SPD_log'
    dataframe_dir = "/home/dyt/test_filter/hypre_thmaxwell/table/SPD_refine_1.xls"
    files = os.listdir(file_path) # 获得文件夹中所有文件的名称列表
    result_list= []
    for file in files:
        with open(file_path+"/"+file, "r" ) as fo:
            dict_tmp = init_my_dict()
            result_content = fo.read()
            print("\nread" + " " + file + " success\n")
            
            dict_tmp = get_iter_info(result_content,get_re_obj(18),dict_tmp)
            dict_tmp = get_relresidual_info(result_content,get_re_obj(9),dict_tmp)
            dict_tmp = get_solvetime_info(result_content,get_re_obj(20),dict_tmp)
            
            dict_tmp = get_kspsetuptime_info(result_content,get_re_obj(22),dict_tmp)
            dict_tmp = get_kspsolvetime_info(result_content,get_re_obj(23),dict_tmp)
            
            dict_tmp = get_nodal_info(result_content,get_re_obj(29),dict_tmp)
            dict_tmp = get_variant_info(result_content,get_re_obj(30),dict_tmp)
            
            result_list.append(dict_tmp)
            print(dict_tmp)

    data = pd.DataFrame(result_list)
    #data = data.sort_index(axis=1)
    #data = data.sort_values(by=['num_rows_A', 'rank'], ascending=True)
    #data = data.sort_values(by=['theta','rank'], ascending=True)    
    data.to_excel(dataframe_dir)