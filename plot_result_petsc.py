#!/usr/bin/python3
# -*- coding: UTF-8 -*- 

import os
import re
import pandas as pd
import csv
import numpy as np 
import matplotlib.pyplot as plt

def get_re_obj(type_num):
    if(type_num == 2):
        my_obj = re.compile(r'Warning: iteration has terminated because the\n'
                            ,re.S)
    # relative residual
    elif(type_num == 3):
        my_obj = re.compile(r'.*?Norm of relative resid (?P<rel_res>\d+.\d+e[-+]?\d+)'
                            ,re.S)
    # Solve time
    elif(type_num == 4):
        my_obj = re.compile(r'.*?total_time = (?P<Total_Solve_Time>\d+\.\d+) sec'
                            ,re.S)
    # Iters
    elif(type_num == 5):
        my_obj = re.compile(r'.*?Iterations (?P<Iters>\d+),'
                            ,re.S)
    # 找到mpiP的文件位置
    elif(type_num == 7):
        my_obj = re.compile(r'.*?Storing mpiP output in \[(?P<mpiP_dir>.*?)\]'
                            ,re.S)
    # 从mpip文件中读MPI时间
    elif(type_num == 8):
        my_obj = re.compile(r'.*?Mean .*?(?P<AppTime>\d+.\d+) .*?(?P<MPITime>\d+.\d+).*?'
                            r'Aggregate .*?\d+.\d+ .*?\d+.\d+ .*?(?P<MPI_ratio>\d+.\d+)\n'
                            ,re.S)
    return my_obj

# 获得异常数据的index
def check_result(result_content):
    erro_index = []
    erro_index = total_solve_time(result_content,get_re_obj(4),erro_index)
    return erro_index

def total_solve_time(result_content,my_obj,erro_index):
    result = my_obj.finditer(result_content)
    time_list = []
    for k in result:
        dict = k.groupdict()
        time_list.append(float(dict['Total_Solve_Time']))
    # 找到多次测量的最短时间，将超过最短时间两倍的数据剔除
    if len(time_list) != 0:
        list_min = np.min(time_list)
    for i in range(len(time_list)):
        if time_list[i] > 1.5 * list_min:
            erro_index.append(i+1)
    return erro_index

def init_my_dict():
    dict_tmp = {}
    return dict_tmp

def get_warning(result_content,my_obj,dict_tmp):
    result = my_obj.findall(result_content)
    if len(result)!=0 :
        dict_tmp["warning"] = 1
    else:
        dict_tmp["warning"] = 0
    return dict_tmp

def get_total_solve_time(result_content,my_obj,erro_index):
    result = my_obj.finditer(result_content)
    time_list = []
    for k in result:
        dict = k.groupdict()
        time_list.append(float(dict['Total_Solve_Time']))
    # 找到多次测量的最短时间，将超过最短时间两倍的数据剔除
    list_min = np.min(time_list)
    for i in range(len(time_list)):
        if time_list[i] > 1.5 * list_min:
            erro_index.append(i+1)
    print(erro_index)
    return erro_index

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

def get_stop_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = float(value)
        break
    return dict_tmp

def get_block_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:
        dict = k.groupdict()
        #print(dict)
        for key,value in dict.items():
            dict_tmp[key] = int(value)
        break
    return dict_tmp

def get_iters_info(result_content,my_obj,dict_tmp):
    result = my_obj.finditer(result_content)
    for k in result:     
        dict = k.groupdict()
        # result_list.append(dict)
        for key,value in dict.items():
            value = float(value)
            if(key == "Iters"):
                dict_tmp[key] = int(value)
            elif(key == "rel_res"):
                dict_tmp[key] = float(value)
        break   
    # print(my_dict)
    return dict_tmp

def get_all_level_info(result_content,my_obj,dict_tmp,erro_index):
    result = my_obj.finditer(result_content)
    my_dict = {}
    repeat_num = 0
    for k in result:
        repeat_num = repeat_num + 1       
        dict = k.groupdict()
        #print(dict)
        if repeat_num in erro_index:
            continue
        else:  
            for key,value in dict.items():
                value = float(value)
                if key in my_dict:
                    my_dict[key] += value
                else:
                    my_dict[key] = value
    # print(repeat_num)
    for key,value in my_dict.items():
        dict_tmp[key] = value/(repeat_num - len(erro_index))
        dict_tmp[key] = round(dict_tmp[key],4)              
    return dict_tmp

#提取每次运行的mpip文件的信息
# 1.找到对应的文件名
# 2.打开文件，用正则表达式提取信息
# 3.最后处理数据，写入到结果字典中
def get_mpiP_info(path, result_content,my_obj,dict_tmp,erro_index):
    result = my_obj.finditer(result_content)
    my_dict = {}
    repeat_num = 0
    for k in result:
        repeat_num = repeat_num + 1       
        dict = k.groupdict()
        #print(dict)
        if repeat_num in erro_index:
            continue
        else:  
            mpip_file = dict['mpiP_dir'].split(dict_tmp['mpiP_dir_name'])
            mpip_file = os.path.abspath(os.path.dirname(path))+'/'+dict_tmp['mpiP_dir_name']+mpip_file[1]
            #print(mpip_file)
            #TODO:这里还是要处理多个文件取平均值
            my_dict = read_mpip_file(mpip_file, get_re_obj(7), my_dict) 
    for key,value in my_dict.items():
        dict_tmp[key] = value/(repeat_num - len(erro_index))
        dict_tmp[key] = round(dict_tmp[key],2)  
    return dict_tmp

# 从文件名提取参数
def get_par_from_filename(filename,dict):
    list = filename.split("_")
    # print(list)
    for i in range(0, len(list), 1):
        if list[i] == 'np':
            dict["np"] = int(list[i+1])
        elif list[i] == 'pid':
            dict["pid"] = int(list[i+1])
        elif list[i] == 'level':
            dict["level"] = int(list[i+1])
        elif list[i] == 'threads':
            dict["threads"] = int(list[i+1])
        elif list[i] == 'subdomains':
            dict["subdomains"] = int(list[i+1])
        elif list[i] == 'ordering':
            dict["ordering"] = str(list[i+2])
        elif list[i] == 'overlap':
            dict["overlap"] = int(list[i+1])
    return dict

def read_mpip_file(mpip_file,my_obj,my_dict):
    with open(mpip_file, "r" ) as f:
        result_content = f.read()
        result = my_obj.finditer(result_content)
        for k in result:     
            dict = k.groupdict()
            for key,value in dict.items():
                value = float(value)
                if key in my_dict:
                    my_dict[key] += value
                else:
                    my_dict[key] = value
            break
    return my_dict

#TODO:画图
# 1. 
def myplot(data,level):
    setup_level = []
    setup_level[0] = "num_proccess"
    for i in range(1, level + 2, 1):
        setup_level[i] = "Setup_level"+str(i)
    print(setup_level)

#TODO:同一进程数下，同一l下m排序，再s
if __name__=="__main__":
    path = '/home/dyt/data/solver_petsc_06/result/'

    solve_dir = "/home/dyt/data/solver_petsc_06/result_06.xls"

    files = os.listdir(path) # 获得文件夹中所有文件的名称列表
    result_list= []
    for file in files:
        with open(path+"/"+file, "r") as fo:
            dict_tmp = init_my_dict()
            dict_tmp = get_par_from_filename(file, dict_tmp)
            result_content = fo.read()
            print("\nread" + " " + file + " success\n")

            # erro_index = []
            erro_index = check_result(result_content)

            dict_tmp = get_all_level_info(result_content,get_re_obj(4),dict_tmp,erro_index)   # solve time

            dict_tmp = get_iters_info(result_content,get_re_obj(5),dict_tmp)   # Iter
            
            dict_tmp = get_iters_info(result_content,get_re_obj(3),dict_tmp)   # residual

        # print(dict_tmp) 
        result_list.append(dict_tmp)

    my_data = pd.DataFrame(result_list)
    # problem_list = list(data.loc[:,"pid"])
    # problem_list = list(set(problem_list))
    writer = pd.ExcelWriter(solve_dir)
    my_data = my_data.sort_index(axis=1)
    # my_data = my_data.sort_values(by='subdomains', ascending=True)
    # my_data = my_data.sort_values(by='overlap', ascending=True)
    my_data = my_data.sort_values(by='np', ascending=True)
    my_data.to_excel(writer)

    writer.save()
    # data.to_csv(solve_dir)
