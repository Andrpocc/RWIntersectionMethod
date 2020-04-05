from colorama import init, Fore, Style
from prettytable import PrettyTable
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

import time
import os
from math import sin, cos, radians, sqrt, acos, degrees, asin
from random import normalvariate
from geo_tasks import *
init()

iterations = 10000


def accuracy_degree(p_data: list, degree, minute, sec):
    global iterations
    a = [400, 200]
    b = [400, 400]
    dx_list = []
    dy_list = []
    up_list = []
    for i in range(iterations):
        ug = degree + minute / 60 + sec / 3600
        fa = normalvariate(0, 9)
        fb = normalvariate(0, 9)
        ua = ug + fa / 3600
        ub = ug + fb / 3600
        g, m, c, ab = ogz(a[0], a[1], b[0], b[1])
        uab = g + m / 60 + c / 3600
        up = 180 - ua - ub
        ap = ab * sin(radians(ub)) / sin(radians(up))
        bp = ab * sin(radians(ua)) / sin(radians(up))
        uap = (uab + 180) + ua - 180
        ubp = uab - ub + 180
        p1 = [0, 0]
        p2 = [0, 0]
        p1[0] = a[0] + ap * cos(radians(uap))
        p1[1] = a[1] + ap * sin(radians(uap))
        p2[0] = b[0] + bp * cos(radians(ubp))
        p2[1] = b[1] + bp * sin(radians(ubp))
        x = (p1[0] + p2[0]) / 2
        y = (p1[1] + p2[1]) / 2
        p_result = [x, y]
        """Оценка точности"""
        dx = p_data[0] - x
        dy = p_data[1] - y
        dx_list.append(dx ** 2)
        dy_list.append(dy ** 2)
        up_list.append(up)
    sumx = 0
    for n in dx_list:
        sumx += n
    sumy = 0
    for n in dy_list:
        sumy += n
    sumup = 0
    for n in up_list:
        sumup += n
    mx = round(sqrt(sumx / iterations), 3)
    my = round(sqrt(sumy / iterations), 3)
    mt = round(sqrt(mx ** 2 + my ** 2), 3)
    mup = int(round(sumup / iterations, 0))
    return int(mx * 1000), int(my * 1000), int(mt * 1000), mup


def accuracy_line(p_data: list, line_data):
    global iterations
    a = [400, 200]
    b = [400, 400]
    dx_list = []
    dy_list = []
    up_list = []
    for i in range(iterations):
        ap = line_data
        bp = line_data
        fap = normalvariate(0, 2 + ap / 1000 * 2)
        fbp = normalvariate(0, 2 + bp / 1000 * 2)
        ap += fap / 1000
        bp += fbp / 1000
        g, m, c, ab = ogz(a[0], a[1], b[0], b[1])
        uab = g + m / 60 + c / 3600
        ub = degrees(acos((ab**2 + bp**2 - ap**2) / (2 * ab * bp)))
        ua = degrees(acos((ab**2 + ap**2 - bp**2) / (2 * ab * ap)))
        up = 180 - ub - ua
        uap = uab + ua
        ubp = uab - ub + 180
        p1 = [0, 0]
        p2 = [0, 0]
        p1[0] = a[0] + ap * cos(radians(uap))
        p1[1] = a[1] + ap * sin(radians(uap))
        p2[0] = b[0] + bp * cos(radians(ubp))
        p2[1] = b[1] + bp * sin(radians(ubp))
        x = (p1[0] + p2[0]) / 2
        y = (p1[1] + p2[1]) / 2
        p = [x, y]
        """Оценка точности"""
        dx = p_data[0] - x
        dy = p_data[1] - y
        dx_list.append(dx ** 2)
        dy_list.append(dy ** 2)
        up_list.append(up)
    sumx = 0
    for n in dx_list:
        sumx += n
    sumy = 0
    for n in dy_list:
        sumy += n
    sumup = 0
    for n in up_list:
        sumup += n
    mx = round(sqrt(sumx / iterations), 3)
    my = round(sqrt(sumy / iterations), 3)
    mt = round(sqrt(mx ** 2 + my ** 2), 3)
    mup = int(round(sumup / iterations, 0))
    return int(mx * 1000), int(my * 1000), int(mt * 1000), mup


def accuracy_backlinedegree(p_data, p_degree, p_minute, p_sec, line_data):
    a = [400, 200]
    b = [400, 400]
    dx_list = []
    dy_list = []
    for i in range(iterations):
        up = p_degree + p_minute / 60 + p_sec / 3600
        up += normalvariate(0, 9) / 3600
        ap = line_data
        ap += normalvariate(0, 2 + ap / 1000 * 2) / 1000
        bp = line_data
        bp += normalvariate(0, 2 + bp / 1000 * 2) / 1000
        g, m, c, ab = ogz(a[0], a[1], b[0], b[1])
        uab = g + m / 60 + c / 3600
        ub = degrees(asin(sin(radians(up)) * ap / ab))
        ua = degrees(asin(sin(radians(up)) * bp / ab))
        uap = (uab + 180) + ua - 180
        ubp = uab - ub + 180
        p1 = [0, 0]
        p2 = [0, 0]
        p1[0] = a[0] + ap * cos(radians(uap))
        p1[1] = a[1] + ap * sin(radians(uap))
        p2[0] = b[0] + bp * cos(radians(ubp))
        p2[1] = b[1] + bp * sin(radians(ubp))
        x = (p1[0] + p2[0]) / 2
        y = (p1[1] + p2[1]) / 2
        p_result = [x, y]
        """Оценка точности"""
        dx = p_data[0] - x
        dy = p_data[1] - y
        dx_list.append(dx ** 2)
        dy_list.append(dy ** 2)
    sumx = 0
    for n in dx_list:
        sumx += n
    sumy = 0
    for n in dy_list:
        sumy += n
    mx = round(sqrt(sumx / iterations), 3)
    my = round(sqrt(sumy / iterations), 3)
    mt = round(sqrt(mx ** 2 + my ** 2), 3)
    mup = round(up)
    return int(mx * 1000), int(my * 1000), int(mt * 1000), mup


with open('data_p.txt', 'r') as data:
    data_p_x_list = data.readlines()
data_px = []
for data in data_p_x_list:
    data_px.append(float(data.replace('\n', '')))

with open('data_degrees.txt', 'r') as data:
    data_degrees_list = data.readlines()
data_degrees = []
for data in data_degrees_list:
    data_degrees.append(float(data.replace('\n', '')))
with open('data_minutes.txt', 'r') as data:
    data_minutes_list = data.readlines()
data_minutes = []
for data in data_minutes_list:
    data_minutes.append(float(data.replace('\n', '')))
with open('data_seconds.txt', 'r') as data:
    data_seconds_list = data.readlines()
data_seconds = []
for data in data_seconds_list:
    data_seconds.append(float(data.replace('\n', '')))

with open('data_line.txt', 'r') as data:
    data_line_list = data.readlines()
data_line = []
for data in data_line_list:
    data_line.append(float(data.replace('\n', '')))

with open('p_degrees.txt', 'r') as data:
    data_degrees_list = data.readlines()
p_degrees = []
for data in data_degrees_list:
    p_degrees.append(float(data.replace('\n', '')))
with open('p_minutes.txt', 'r') as data:
    data_minutes_list = data.readlines()
p_minutes = []
for data in data_minutes_list:
    p_minutes.append(float(data.replace('\n', '')))
with open('p_seconds.txt', 'r') as data:
    data_seconds_list = data.readlines()
p_seconds = []
for data in data_seconds_list:
    p_seconds.append(float(data.replace('\n', '')))


time_start = time.time()
print(Style.BRIGHT)

print(Fore.RED)
tb = PrettyTable()
tb.title = 'Прямая угловая засечка'
tb.min_table_width = 100
tb.field_names = ['mx, mm', 'my, mm', 'mt, mm', 'p, deg']
accuracy_degree_data_mt = []
accuracy_degree_data_p = []
frame_degree = pd.DataFrame(index=range(1, 41), columns=['mx', 'my', 'mt', 'p'])
for n in range(40):
    mx, my, mt, p = accuracy_degree([data_px[n], 300], data_degrees[n], data_minutes[n], data_seconds[n])
    accuracy_degree_data_mt.append(mt)
    accuracy_degree_data_p.append(p)
    tb.add_row([mx, my, mt, p])
    frame_degree.iloc[n] = [mx, my, mt, p]
frame_degree.to_csv('frame_degree.txt', sep='\t')
print(tb)

print(Fore.GREEN)
tb = PrettyTable()
tb.title = 'Прямая линейная засечка'
tb.field_names = ['mx, mm', 'my, mm', 'mt, mm', 'p, deg']
tb.min_table_width = 100
accuracy_line_data_mt = []
accuracy_line_data_p = []
frame_line = pd.DataFrame(index=range(1, 41), columns=['mx', 'my', 'mt', 'p'])
for n in range(40):
    mx, my, mt, p = accuracy_line([data_px[n], 300], data_line[n])
    accuracy_line_data_mt.append(mt)
    accuracy_line_data_p.append(p)
    tb.add_row([mx, my, mt, p])
    frame_line.iloc[n] = [mx, my, mt, p]
frame_line.to_csv('frame_line.txt', sep='\t')
print(tb)

print(Fore.BLUE)
tb = PrettyTable()
tb.title = 'Обратная линейно-угловая засечка'
tb.field_names = ['mx, mm', 'my, mm', 'mt, mm', 'p, deg']
tb.min_table_width = 100
accuracy_backlinedegree_data_mt = []
accuracy_backlinedegree_data_p = []
frame_linedegree = pd.DataFrame(index=range(1, 41), columns=['mx', 'my', 'mt', 'p'])
for n in range(40):
    mx, my, mt, p = accuracy_backlinedegree([data_px[n], 300], p_degrees[n], p_minutes[n], p_seconds[n], data_line[n])
    accuracy_backlinedegree_data_mt.append(mt)
    accuracy_backlinedegree_data_p.append(p)
    tb.add_row([mx, my, mt, p])
    frame_linedegree.iloc[n] = [mx, my, mt, p]
frame_linedegree.to_csv('frame_linedegree.txt', sep='\t')
print(tb)

time_end = time.time() - time_start
print(Fore.RED, time_end)
input()

sns.set(style='whitegrid')

plt.figure('Регрессия')
#plt.subplots_adjust(hspace=0.35)
#plt.subplot(311)
plt.ylim(0, 20)
plt.title('Прямая угловая засечка')
plt.scatter(accuracy_degree_data_p, accuracy_degree_data_mt, color='r')
x_array = np.array(accuracy_degree_data_p)
slope, intercept, r_value, p_value, std_err = stats.linregress(accuracy_degree_data_p, accuracy_degree_data_mt)
plt.plot(accuracy_degree_data_p, intercept + x_array * slope, color='c')
plt.show()
input()


plt.title('Прямая линейная засечка')
plt.scatter(accuracy_line_data_p, accuracy_line_data_mt, color='b')
x_array = np.array(accuracy_line_data_p)
slope, intercept, r_value, p_value, std_err = stats.linregress(accuracy_line_data_p, accuracy_line_data_mt)
plt.plot(accuracy_line_data_p, intercept + x_array * slope, color='c')
plt.show()
input()

plt.title('Обратная линейно-угловая засечка')
plt.scatter(accuracy_backlinedegree_data_p, accuracy_backlinedegree_data_mt, color='g')
x_array = np.array(accuracy_backlinedegree_data_p)
slope, intercept, r_value, p_value, std_err = stats.linregress(accuracy_backlinedegree_data_p, accuracy_backlinedegree_data_mt)
plt.plot(accuracy_backlinedegree_data_p, intercept + x_array * slope, color='c')
plt.show()
input()
#plt.subplot(312)
#plt.ylim(0, 20)
#plt.title('Прямая линейная засечка')
#plt.scatter(accuracy_line_data_p, accuracy_line_data_mt, color='g')
#plt.subplot(313)
#plt.ylim(0, 20)
#plt.title('Обратная линейно-угловая засечка')
#plt.scatter(accuracy_backlinedegree_data_p, accuracy_backlinedegree_data_mt, color='b')


