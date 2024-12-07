# -*- coding: utf-8 -*-
import csv
import time
import os
from datetime import datetime
import pandas as pd
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from Part_2_Main_paths_estiamtion import part2
import random




def readcsv(path):
    try:
        with open(path, 'r',encoding='utf_8_sig') as f:
        #with open(path, 'r',encoding='gb18030') as f:
            reader = csv.reader(f)
            rows = [row for row in reader]
        return rows
    except:
        #with open(path, 'r',encoding='utf_8_sig') as f:
        with open(path, 'r',encoding='gb18030') as f:
            reader = csv.reader(f)
            rows = [row for row in reader]
        return rows

def savecsv(path,item,model = 'a'):
    while True:
        try:
            with open(path, model, encoding='utf_8_sig', newline='') as f:
            #with open(path, model, encoding='gb18030', newline='') as f:
                w = csv.writer(f)
                w.writerow(item)
                return True
        except:
            print('Close')
            time.sleep(1)

#Save csv files
def savecsvs(path,item,model = 'a'):
    while True:
        try:
            with open(path, model, encoding='utf_8_sig', newline='') as f:
            #with open(path, model, encoding='gb18030', newline='') as f:
                w = csv.writer(f)
                w.writerows(item)
                return True
        except Exception as e:
            print(e)
            print('请关闭表格，否则程序无法写入')
            time.sleep(1)

#Read the names of all files and folders within the directory
def file_names(inputpath):
    namelist = []
    filePath = inputpath
    for i, j, k in os.walk(filePath):
        namelist.append([i, j, k])
    return namelist

#Show the raw data
def Map_2(save_path,csv_name):
    m = Basemap(llcrnrlat=-60, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=-20)  # Instantiate a map
    m.drawcoastlines()  # Draw the coastline
    m.drawmapboundary(fill_color='white')
    m.fillcontinents(lake_color='white')  # Draw the continents and fill them in white

    parallels = np.arange(-90., 90., 10.)  # Draw latitudes with ranges [-90,90] and intervals of 10
    m.drawparallels(parallels, labels=[False, True, True, False], color='none')
    meridians = np.arange(-180., 180., 20.)  # Draw the longitude with a range of [-180,180] and an interval of 10
    m.drawmeridians(meridians, labels=[True, False, False, True], color='none')

    # plt.rcParams['figure.figsize'] = (28, 8)
    # plt.show()

    datalist = readcsv(save_path + csv_name)
    datalist = datalist[1:]

    LON = []
    LAT = []
    for i in range(1):
        Lat = [[float(data[0]),int(data[2])] for data in datalist]
        Lon = [[float(data[1]),int(data[2])] for data in datalist]
        LON.append(Lon)
        LAT.append(Lat)

    for doc in range(1):
        colorMap = ['red', 'darkorange', 'gold', 'greenyellow', 'pink', 'limegreen', 'mediumturquoise',
                    'dodgerblue',
                    'navy', 'blue', 'mediumorchid', 'fuchsia']
        # Show labels
        label = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                 'November', 'December']

        marker = ['x', 'o', '.', '+', '<', '_', '^', 'v', 'H', '|', 's', '*']
        j = 0
        # print(len(lon))
        flag = True

        col1 = 43101
        for i in range(13):
            # print(i)
            if doc == 0:
                # m.plot(LON[doc][i:i + 30], LAT[doc][i:i + 30], marker=marker[doc], linewidth=0.4,
                #        color=colorMap[j],
                #        markersize=0.5, label=label[
                #         j])
                LON1 = [data[0] for data in LON[doc] if data[1]>=col1 and data[1]<col1 + 30]
                LAT1 = [data[0] for data in LAT[doc] if data[1]>=col1 and data[1]<col1 + 30]
                col1 = col1 + 30
                m.scatter(LON1, LAT1, color=colorMap[j],s=1, label=label[j])
                # plt.show()
                j += 1
                if j == 12:
                    j = 0
                    if flag:
                        plt.legend(loc='lower left', shadow=True)
                        flag = False
                    continue

    plt.xlabel('Lon', labelpad=10)
    plt.ylabel('Lat')
    plt.savefig(save_path + '{}.jpg'.format(csv_name.replace('.csv', '')), dpi=1000)
    # plt.show()
    plt.close()

# def random_100(datalist):
#     date_count = {}
#     for datas in datalist:
#         if date_count.get(datas[2]):
#             date_count[datas[2]] = date_count[datas[2]] + [datas]
#         else:
#             date_count[datas[2]] = [datas]
#
#     data1 = []
#     date_list = list(date_count.keys())
#     for dates in date_list:
#         if len(date_count[dates]) > 100:
#             random_data = random.sample(date_count[dates], 100) #每天只保留最多100个
#             data1 = data1 + random_data
#         else:
#             data1 = data1 + date_count[dates]
#
#     return data1


def main():
    #Absolute path
    path1 = './2017/'
    path2 = './source/'
    #Terminal
    # path1 = input('Please set part1 input folder ')
    # path1 = path1 + '/'
    # path2 = input('Please set part1 output folder')
    # path2 = path2 + '/'

#Extract three columns: LONGITUDE,LATITUDE, and OBS_DATE
    csv_list = file_names(path1)[0][2]
    csv_list = [name for name in csv_list if '.csv' in name]
    for i in range(len(csv_list)):
        csv_path = path1 + csv_list[i]
        datalist = readcsv(csv_path)
        # datalist = [[data[11]] + data[29:32] for data in datalist]

        savecsvs(path2 + csv_list[i],datalist)
        Map_2(path2, csv_list[i])
        print(csv_list[i])
    print('Part 1 finished')
    #part2()



if __name__ == '__main__':
    main()
