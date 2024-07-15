# coding:utf-8
import os
import pandas as pd
import csv

def savecsv(path,item,model = 'a'):
    while True:
        try:
            with open(path, model, encoding='utf_8_sig', newline='') as f:#打开csv文件
            #with open(path, model, encoding='gb18030', newline='') as f:#打开csv文件
                w = csv.writer(f)
                w.writerow(item)#数据写入csv
                return True
        except:
            print('请关闭表格，否则程序无法写入')
            time.sleep(1)

def is_num(path):
    # 定义一个函数，判断一个字符串是否是纯数字
    def is_digit(s):
        try:
            int(s)  # 尝试把字符串转换为整数
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
            # file1 = files[j]
            file1 = path + '\\{}.xls'.format(j + 1)
            df = pd.read_excel(file1, sheet_name='Sheet1',header=None)
            col_data_e = df.iloc[:, 4]
            col_data_e = list(col_data_e)

            data_a = ''
            count = 1
            data_c = []
            for data_b in col_data_e:
                if data_b == data_a:
                    count = count + 1
                else:
                    data_c.append([data_a,count])
                    count = 1
                    data_a = data_b
            data_c.append([data_a, count])
            data_c = data_c[1:]
            data_d = [data for data in data_c if data[1]>4 and data[1]<21]
            for k in range(len(col_data_e)):
                d_1 = col_data_e[k]
                try:
                    d_2 = data_c[k]
                except:
                    d_2 = []
                try:
                    d_3 = data_d[k]
                except:
                    d_3 = []
                item = [d_1] + d_2 + d_3

                savecsv(path + '\\{}b.csv'.format(j + 1),item)

        print(i,len(folder1))



if __name__ == '__main__':
    main()
