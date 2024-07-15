# coding:utf-8
import os
import pandas as pd
import csv

def savetxt(path,item,model = 'a'):
    while True:
        try:
            with open(path, model,encoding='gb18030') as f:  # 打开txt文件，使用utf-8编码并忽略错误，有些标题里有特殊字符，存入txt会报错
                f.write(item)  # 数据写入txt
                f.write('\n')  # 换行
                return True
        except Exception as e:
            print(e)
            print('请关闭txt文档，否则程序无法写入')
            time.sleep(1)

# 定义一个函数，用于从csv文件中读取数据
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