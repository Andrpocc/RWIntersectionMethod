from colorama import init, Fore, Style
import time
import os
from math import sin, cos, radians, sqrt, acos, degrees
from random import normalvariate
from geo_tasks import *
init()



def accuracy_degree(p_data: list, degree, minute, sec):
    a = [400, 200]
    b = [400, 400]
    dx_list = []
    dy_list = []
    up_list = []
    for i in range(10000):
        ug = degree + minute / 60 + sec / 3600
        fa = normalvariate(0, 5)
        fb = normalvariate(0, 5)
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
    mx = sqrt(sumx / 10000)
    my = sqrt(sumy / 10000)
    mt = sqrt(mx ** 2 + my ** 2)
    mup = round(sumup / 10000, 0)
    print(Fore.CYAN, mx, my, mt, mup, sep='\t')


def accuracy_line(p_data: list, line_data):
    a = [400, 200]
    b = [400, 400]
    dx_list = []
    dy_list = []
    up_list = []
    for i in range(10000):
        ap = line_data
        bp = line_data
        fap = normalvariate(0, 4)
        fbp = normalvariate(0, 4)
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
    mx = sqrt(sumx / 10000)
    my = sqrt(sumy / 10000)
    mt = sqrt(mx ** 2 + my ** 2)
    mup = round(sumup / 10000, 0)
    print(Fore.GREEN, mx, my, mt, mup, sep='\t')


with open('data_p.txt', 'r') as data:
    data_p_y_list = data.readlines()
data_py = []
for data in data_p_y_list:
    data_py.append(float(data.replace('\n', '')))
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


time_start = time.time()

print(Fore.RED, 'Угловая засечка')
print(Fore.RED, 'mx\t\t', 'my\t\t', 'mt\t\t', 'P', sep='\t')
for n in range(21):
    accuracy_degree([data_py[n], 300], data_degrees[n], data_minutes[n], data_seconds[n])

print(Fore.RED, 'Линейная засечка')
print(Fore.RED, 'mx\t\t', 'my\t\t', 'mt\t\t', 'P', sep='\t')
for n in range(21):
    accuracy_line([data_py[n], 300], data_line[n])

time_end = time.time() - time_start
print(Fore.RED, time_end)



