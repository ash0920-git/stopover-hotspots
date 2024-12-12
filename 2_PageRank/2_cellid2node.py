# coding:utf-8
import os
import pandas as pd
import time
import csv

def readcsv(path):
    try:  
        with open(path, 'r', encoding='utf_8_sig') as f: 
            reader = csv.reader(f)  
            rows = [row for row in reader]  
        return rows  
    except Exception as e:  
        print(e)  
        with open(path, 'r', encoding='gb18030') as f:  
            reader = csv.reader(f)  
            rows = [row for row in reader]  
        return rows  

def savecsv(path,item,model = 'a'):

    while True: 
        try:  
            with open(path, model, encoding='utf_8_sig', newline='') as f:  
                w = csv.writer(f)  
                w.writerow(item)  
                return True  
        except Exception as e:  
            print(e)
            print('请关闭表格，否则程序无法写入')  
            time.sleep(1)  

def is_num(path):
    
    def is_digit(s):
        try:
            int(s.replace('a',''))  
            return True  
        except ValueError:  
            return False  

    files = []
    
    folder_path = path  

    
    for file in os.listdir(folder_path):
        
        file_path = os.path.join(folder_path, file)
        
        if os.path.isfile(file_path):
            
            file_name = os.path.splitext(file)[0]  
            if 'a' in file_name:
                if is_digit(file_name):  
                    files.append(file_path)  
    return files

def file_names(inputpath):
    namelist = []
    filePath = inputpath
    for i, j, k in os.walk(filePath):
        namelist.append([i, j, k])
    return namelist

def main():
    data_path = r'D:\Matlab\2017'
    excel_list = file_names(data_path)
    path = excel_list[0][0]
    folder_attribute = excel_list[0][1]  #
    folder1 = [[path,folder] for folder in folder_attribute]

    for i in range(len(folder1)):
        folder2 = folder1[i]
        path = '\\'.join(folder2)
        files = is_num(path)
        for k in range(len(files)):
            file1 = path + '\\{}a.csv'.format(k + 1)
            col_data = readcsv(file1)
            col_data = [data[1] for data in col_data if len(data)>1]
            if len(col_data) == 0:
                continue

            data1 = []
            is_need = 1
            for data2 in col_data:
                if not data2 or data2 == '0':
                    break
                if int(data2) < 0:
                    is_need = 0
                    break
                data1.append(data2)
            if is_need == 0:
                continue

            data2 = data1[1:]
            data1 = data1[:-1]
            for j in range(len(data2)):
                data3 = [data1[j],data2[j]]
                savecsv(data_path + '\\wl.csv',data3)
        print(i)



if __name__ == '__main__':
    main()
