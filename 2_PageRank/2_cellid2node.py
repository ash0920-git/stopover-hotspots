# coding:utf-8
import os
import pandas as pd
import time
import csv

def readcsv(path):# 参数path是文件路径
    try:  # 使用try-except语句捕获可能发生的异常
        with open(path, 'r', encoding='utf_8_sig') as f:  # 使用with语句打开csv文件，指定读取模式和编码
            reader = csv.reader(f)  # 创建一个csv读取器对象
            rows = [row for row in reader]  # 使用列表推导式，将读取器对象中的每一行数据添加到rows列表中
        return rows  # 返回rows列表
    except Exception as e:  # 如果发生异常，执行以下代码
        print(e)  # 打印异常信息
        with open(path, 'r', encoding='gb18030') as f:  # 使用with语句打开csv文件，指定读取模式和另一种编码
            reader = csv.reader(f)  # 创建一个csv读取器对象
            rows = [row for row in reader]  # 使用列表推导式，将读取器对象中的每一行数据添加到rows列表中
        return rows  # 返回rows列表

def savecsv(path,item,model = 'a'):

    while True:  # 使用一个无限循环，直到成功写入数据或者退出程序
        try:  # 使用try-except语句捕获可能发生的异常
            with open(path, model, encoding='utf_8_sig', newline='') as f:  # 使用with语句打开csv文件，指定模式、编码和换行符
                w = csv.writer(f)  # 创建一个csv写入器对象
                w.writerow(item)  # 将数据写入csv文件
                return True  # 写入成功后，返回True并退出函数
        except Exception as e:  # 如果发生异常，打印异常信息
            print(e)
            print('请关闭表格，否则程序无法写入')  # 提示用户关闭表格文件，否则无法写入数据
            time.sleep(1)  # 程序暂停1秒，等待用户操作

def is_num(path):
    # 定义一个函数，判断一个字符串是否是纯数字
    def is_digit(s):
        try:
            int(s.replace('a',''))  # 尝试把字符串转换为整数
            return True  # 如果成功，返回True
        except ValueError:  # 如果失败，抛出异常
            return False  # 返回False

    files = []
    # 定义一个文件夹的路径
    folder_path = path  # 请把这里替换为你的文件夹路径

    # 遍历文件夹中的所有文件和子文件夹
    for file in os.listdir(folder_path):
        # 拼接完整的文件路径
        file_path = os.path.join(folder_path, file)
        # 判断是否是文件，而不是子文件夹
        if os.path.isfile(file_path):
            # 判断文件名是否是纯数字，不包含扩展名
            file_name = os.path.splitext(file)[0]  # 分离文件名和扩展名
            if 'a' in file_name:
                if is_digit(file_name):  # 调用判断函数
                    files.append(file_path)  # 打印文件路径
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