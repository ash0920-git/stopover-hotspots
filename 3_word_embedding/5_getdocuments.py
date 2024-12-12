# coding:utf-8
import os
import pandas as pd
import csv

def savetxt(path,item,model = 'a'):
    while True:
        try:
            with open(path, model,encoding='gb18030') as f:  
                f.write(item)  
                f.write('\n')  
                return True
        except Exception as e:
            print(e)
            print('请关闭txt文档，否则程序无法写入')
            time.sleep(1)

# Read csv files
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
        for j in range(len(files)):
            file1 = path + '\\{}a.csv'.format(j + 1)
            data1 = readcsv(file1)
            col_data = [data[1:3] for data in data1]
            col_data = [data for data in col_data if data]
            data1 = []
            is_need = 1
            for data2 in col_data:
                if not data2[1] or data2[1] == '0':
                    break
                if int(data2[0]) < 0:
                    is_need = 0
                    break
                data1.append(data2[0])
            if is_need == 0:
                continue
            col_data = ' '.join(data1)
            savetxt(data_path + '\\xs.txt',col_data)
        print(i)



if __name__ == '__main__':
    main()
