# -*-coding:utf-8-*-
import math
import random
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay
from tqdm import trange

star_time = time.time()
print('start at', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

# step1: 相关设置信息输入
# (1-1)3档级配
por = [0.74, 0.26, 0]  # 3档集料的体积比，9.5~16、4.75~9.5、2.36~4.75

# (1-2)骨料顶点距离
dis_ver = 3.5  # 扩张收缩前骨料两个顶点间的距离，mm

# (1-3)集料顶点收缩倍数
shr_min, shr_max = 0.05, 0.10  # 集料顶点收缩shr_min,shr_max倍

# (1-4)沥青顶点扩张倍数
exp_min, exp_max = 0, 0.95  # 沥青顶点扩张exp_min~exp_max倍

# (1-5)文件输出设置
outFile_path = 'E:/Abaqus_examples_2nd_edition/2D/biper/'
outfile_name = 'matrix_2d.txt'
outfile = open(outFile_path + outfile_name, 'w+')

step1_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step1：相关设置信息输入用时：', '%6f min' % ((step1_time - star_time) / 60))
print('已累计用时：', '%6f min' % ((step1_time - star_time) / 60))


# step2: 函数定义与文件读取
# (1-1)圆心距离判断函数
def judgemat(ball1, ball2, rate):  # rate为距离与半径之和的比
    loc = 0
    dis = math.sqrt((ball1[0][0] - ball2[0][0]) ** 2 + (ball1[0][1] - ball2[0][1]) ** 2)
    radius = ball1[1][0] + ball2[1][0]
    if dis >= rate * radius:  # 两圆心距离大于rate*半径之和则满足投放条件
        loc = 1
    return loc


step2_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step2：函数定义与文件读取用时：', '%6f min' % ((step2_time - step1_time) / 60))
print('已累计用时：', '%6f min' % ((step2_time - star_time) / 60))

# step3: 生成集料对应的球体
# 包含3步：(3-1)投放粗集料球体；（3-2）在边缘投放粒径为3.0mm的填充料； (3-3)绘制图形
# (3-1)投放粗集料球体
ball_dic = {}  # 键为球体编号，值为一个列表，里面有2个元素，第1个元素是列表，里面是球心坐标[x0,y0,z0]；第2个元素为列表，里面是球体半径[r]；
judgenum = 0  # 判断数，为1时可以投放
ball_num = 0  # 球体编号
vol1 = 0  # 1档料的球体总体积
for i in range(10000):
    if vol1 < 60 * 35 * 0.8 * por[0]:  # 1档料球体体积占关心区域体积比
        pass
    else:
        break
    r1 = 12.0 / 2 + 5.0 * random.random() / 2  # 1档料对应球体的半径，粒径12-17
    vol_sin = math.pi * r1 * r1  # 单颗集料球体的体积
    x = -30.0 + 60.0 * random.random()  # -30<x<=30
    y = 0.0 + 35.0 * random.random()  # 0<y<=35
    ball_temp = [[x, y], [r1]]
    if ball_dic == {}:
        judgenum = 1
    else:
        for j in ball_dic.keys():
            if judgemat(ball_dic[j], ball_temp, 1) == 1:
                judgenum = 1
            else:
                judgenum = 0
                break
    if judgenum == 1:
        vol1 += vol_sin
        ball_num += 1
        ball_dic[ball_num] = ball_temp
    else:
        pass
ball_num1 = ball_num
print('1档料循环次数为：', i)
print('1档料数量为：', ball_num1)
print('1档料对应圆面积占比为：', vol1 / (60 * 35))

vol2 = 0  # 2档料的球体总体积
for i in range(1000000):
    if vol2 < 60 * 35 * 0.8 * por[1]:  # 2档料球体体积占关心区域体积比
        pass
    else:
        break
    r2 = 6.0 / 2 + 4.0 * random.random() / 2  # 2档料对应球体的半径，粒径6~10
    vol_sin = math.pi * r2 * r2  # 单颗集料球体的体积
    x = -30.0 + 60.0 * random.random()  # -30<x<=30
    y = 0.0 + 35.0 * random.random()  # 0<y<=35
    x_min, x_max, y_min, y_max = x - r2, x + r2, y - r2, y + r2
    if x_min < -30:  # 部分位于试件外的粗集料移动到边界上
        x = -30
    elif x_max > 30:
        x = 30
    elif y_min < 0:
        y = 0
    elif y_max > 35:
        y = 35
    else:
        pass
    ball_temp = [[x, y], [r2]]
    if ball_dic == {}:
        judgenum = 1
    else:
        for j in ball_dic.keys():
            if judgemat(ball_dic[j], ball_temp, 1) == 1:
                judgenum = 1
            else:
                judgenum = 0
                break
    if judgenum == 1:
        vol2 += vol_sin
        ball_num += 1
        ball_dic[ball_num] = ball_temp
    else:
        pass
ball_num2 = ball_num
print('2档料循环次数为：', i)
print('2档料数量为：', ball_num2 - ball_num1)
print('2档料对应球体体积占比为：', vol2 / (60 * 35))

vol3 = 0  # 3档料的球体总体积，粒径3~5
for i in range(1000000):
    if vol3 < 60 * 35 * 0.8 * por[2]:  # 3档料球体体积占关心区域体积比
        pass
    else:
        break
    r3 = 3.0 / 2 + 2.0 * random.random() / 2  # 3档料对应球体的半径，粒径3~5
    vol_sin = math.pi * r3 * r3  # 单颗集料球体的体积
    x = -30.0 + 60.0 * random.random()  # -30<x<=30
    y = 0.0 + 35.0 * random.random()  # 0<y<=35
    x_min, x_max, y_min, y_max, z_min, z_max = x - r2, x + r2, y - r2, y + r2
    if x_min < -30:  # 部分位于试件外的粗集料移动到边界上
        x = -30
    elif x_max > 30:
        x = 30
    elif y_min < 0:
        y = 0
    elif y_max > 35:
        y = 35
    else:
        pass
    ball_temp = [[x, y], [r3]]
    if ball_dic == {}:
        judgenum = 1
    else:
        for j in ball_dic.keys():
            if judgemat(ball_dic[j], ball_temp, 1) == 1:
                judgenum = 1
            else:
                judgenum = 0
                break
    if judgenum == 1:
        vol3 += vol_sin
        ball_num += 1
        ball_dic[ball_num] = ball_temp
    else:
        pass
ball_num3 = ball_num
print('3档料循环次数为：', i)
print('3档料数量为：', ball_num3 - ball_num2)
print('3档料对应球体体积占比为：', vol3 / (60 * 35))

Coarse_num = ball_num  # 粗集料数量

# (3-2)只在边缘投放粒径为3mm的填充集料
r0 = 3.0 / 2  # 填充料对应球体的半径
vol0 = 0  # 填充料的球体总体积
vol_sin = math.pi * r0 * r0  # 单颗集料球体的体积
core_lib = []  # 填充料球心坐标库，比关心区域每个方向多8mm
for x in range(-38, 39, 1):
    for y in range(-8, 44, 1):
        if x >= -31 and x <= 31 and y >= 4 and y <= 31:
            pass
        else:
            core_lib.append([x, y])
random.shuffle(core_lib)
for i in range(len(core_lib)):
    ball_temp = [core_lib[i], [r0]]
    for j in range(1, Coarse_num + 1):  # 与集料球不相交
        if judgemat(ball_dic[j], ball_temp, 1) == 1:
            judgenum = 1
        else:
            judgenum = 0
            break
    if judgenum == 1:
        pass
    else:
        continue
    for j in range(Coarse_num + 1, max(ball_dic.keys()) + 1):  # 灌浆料之间距离要间隔3倍半径之和
        if judgemat(ball_dic[j], ball_temp, 2) == 1:
            judgenum = 1
        else:
            judgenum = 0
            break
    if judgenum == 1:
        vol0 += vol_sin
        ball_num += 1
        ball_dic[ball_num] = ball_temp
    else:
        pass
ball_numf = ball_num
print('填充料循环次数为：', i)
print('填充料数量为：', ball_numf - Coarse_num)
print('填充料对应球体体积占比为：', vol0 / (60 * 35))

# (3-3)绘制图形
fig = plt.figure()
ax = fig.add_subplot(111)
u = np.linspace(0, 2 * np.pi, 100)  # 用参数方程画球
print('正在绘制1档料')
for i in range(1, ball_num1 + 1):
    x = ball_dic[i][0][0] + ball_dic[i][1][0] * np.cos(u)
    y = ball_dic[i][0][1] + ball_dic[i][1][0] * np.sin(u)
    ax.plot(x, y, color="green")
print('正在绘制2档料')
for i in range(ball_num1 + 1, ball_num2 + 1):
    x = ball_dic[i][0][0] + ball_dic[i][1][0] * np.cos(u)
    y = ball_dic[i][0][1] + ball_dic[i][1][0] * np.sin(u)
    ax.plot(x, y, color="yellow")
print('正在绘制3档料')
for i in range(ball_num2 + 1, ball_num3 + 1):
    x = ball_dic[i][0][0] + ball_dic[i][1][0] * np.cos(u)
    y = ball_dic[i][0][1] + ball_dic[i][1][0] * np.sin(u)
    ax.plot(x, y, color="purple")
print('正在绘制填充料')
for i in range(Coarse_num + 1, ball_numf + 1):
    x = ball_dic[i][0][0] + ball_dic[i][1][0] * np.cos(u)
    y = ball_dic[i][0][1] + ball_dic[i][1][0] * np.sin(u)
    ax.plot(x, y, color="red")

plt.plot([-30, 30], [35, 35], color='black', linewidth=2)
plt.plot([-30, 30], [0, 0], color='black', linewidth=2)
plt.plot([-30, -30], [0, 35], color='black', linewidth=2)
plt.plot([30, 30], [0, 35], color='black', linewidth=2)

ax.set(xlim=[-40, 40], ylim=[-10, 45])
ax.set_xlabel('X', fontsize=14)
ax.set_ylabel('Y', fontsize=14)
plt.show()

step3_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step3：生成集料对应的球体用时：', '%6f min' % ((step3_time - step2_time) / 60))
print('已累计用时：', '%6f min' % ((step3_time - star_time) / 60))

# step4: 第1次Delaunay划分
# (4-1)利用集料球心进行Delaunay划分
Cores = []  # 列表，里面是若干列表，每个列表里面是一个球心的坐标
for i in ball_dic.keys():
    Cores.append(ball_dic[i][0])
tri = Delaunay(Cores)

# (4-2)绘图
fig = plt.figure()  # 绘图
ax = fig.add_subplot(111)
for i in range(len(tri.simplices)):
    point1 = tri.simplices[i][0]  # 该四面体所包含的球心点编号，共4个，认为前3个点构成底面，最后一个点为顶点
    point2 = tri.simplices[i][1]
    point3 = tri.simplices[i][2]
    x = [Cores[point1][0], Cores[point2][0], Cores[point3][0], Cores[point1][0]]  # 画底边3条线
    y = [Cores[point1][1], Cores[point2][1], Cores[point3][1], Cores[point1][1]]
    ax.plot(x, y)

plt.plot([-30, 30], [35, 35], color='black', linewidth=2)
plt.plot([-30, 30], [0, 0], color='black', linewidth=2)
plt.plot([-30, -30], [0, 35], color='black', linewidth=2)
plt.plot([30, 30], [0, 35], color='black', linewidth=2)

ax.set(xlim=[-40, 40], ylim=[-10, 45])
ax.set_xlabel('X', fontsize=14)
ax.set_ylabel('Y', fontsize=14)

plt.show()

step4_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step4：第1次Delaunay划分用时：', '%6f min' % ((step4_time - step3_time) / 60))
print('已累计用时：', '%6f min' % ((step4_time - star_time) / 60))

# step5: 第2次Delaunay划分
# (5-1)对集料球心和顶点进行Delaunay划分
Vertexs = []
Vertexs.extend(Cores)  # 列表，里面是若干列表，每个列表里面是球心或顶点的坐标
for i in trange(len(tri.simplices)):
    point1, point2, point3 = tri.simplices[i][0], tri.simplices[i][1], tri.simplices[i][
        2]  # 该四面体所包含的球心点编号，共4个，认为前3个点构成底面，最后一个点为顶点
    radius1, radius2, radius3 = ball_dic[point1 + 1][1][0], ball_dic[point2 + 1][1][0], ball_dic[point3 + 1][1][
        0]  # 第1个球的半径

    x = ball_dic[point1 + 1][0][0] + (ball_dic[point2 + 1][0][0] - ball_dic[point1 + 1][0][0]) * radius1 / (
            radius1 + radius2)  # 第1个顶点的x坐标
    y = ball_dic[point1 + 1][0][1] + (ball_dic[point2 + 1][0][1] - ball_dic[point1 + 1][0][1]) * radius1 / (
            radius1 + radius2)
    Vertexs.append([x, y])

    x = ball_dic[point1 + 1][0][0] + (ball_dic[point3 + 1][0][0] - ball_dic[point1 + 1][0][0]) * radius1 / (
            radius1 + radius3)  # 第2个顶点的x坐标
    y = ball_dic[point1 + 1][0][1] + (ball_dic[point3 + 1][0][1] - ball_dic[point1 + 1][0][1]) * radius1 / (
            radius1 + radius3)
    Vertexs.append([x, y])

    x = ball_dic[point2 + 1][0][0] + (ball_dic[point3 + 1][0][0] - ball_dic[point2 + 1][0][0]) * radius2 / (
            radius2 + radius3)  # 第4个顶点的x坐标
    y = ball_dic[point2 + 1][0][1] + (ball_dic[point3 + 1][0][1] - ball_dic[point2 + 1][0][1]) * radius2 / (
            radius2 + radius3)
    Vertexs.append([x, y])
# print("Vertexs中的数量",len(Vertexs))
# # 定义一个二维列表
# # 将二维列表转换为元组列表
# tuple_list = [tuple(l) for l in Vertexs]
# # 利用set()函数去除重复元素并转换回列表形式
# new_list = [list(t) for t in set(tuple_list)]
#
# print("去重后Vertexs中的数量",len(new_list))
# 输出结果为：[[1, 2], [3, 4], [5, 6]]

print(Vertexs)
tri2 = Delaunay(Vertexs)

fig = plt.figure()  # 绘图
ax = fig.add_subplot(111)
for i in range(len(tri2.simplices)):
    point1 = tri2.simplices[i][0]  # 该四面体所包含的顶点编号，共4个，认为前3个点构成底面，最后一个点为顶点
    point2 = tri2.simplices[i][1]
    point3 = tri2.simplices[i][2]
    x = [Vertexs[point1][0], Vertexs[point2][0], Vertexs[point3][0], Vertexs[point1][0]]  # 画底边3条线
    y = [Vertexs[point1][1], Vertexs[point2][1], Vertexs[point3][1], Vertexs[point1][1]]
    ax.plot(x, y)

plt.plot([-30, 30], [35, 35], color='black', linewidth=2)
plt.plot([-30, 30], [0, 0], color='black', linewidth=2)
plt.plot([-30, -30], [0, 35], color='black', linewidth=2)
plt.plot([30, 30], [0, 35], color='black', linewidth=2)

ax.set(xlim=[-40, 40], ylim=[-10, 45])
ax.set_xlabel('X', fontsize=14)
ax.set_ylabel('Y', fontsize=14)
plt.show()

step5_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step5：第2次Delaunay划分用时：', '%6f min' % ((step5_time - step4_time) / 60))
print('已累计用时：', '%6f min' % ((step5_time - star_time) / 60))

# step6: 整理每颗集料对应的顶点信息
agg_dic = {}  # 键为集料编号，值为1个列表，里面是各个顶点的坐标
for i in range(1, Coarse_num + 1):
    agg_dic[i] = []

judgenum = 0
for i in range(len(tri2.simplices)):
    point1 = tri2.simplices[i][0]  # 该四面体所包含的顶点在Vertexs中的编号
    point2 = tri2.simplices[i][1]
    point3 = tri2.simplices[i][2]
    node_list = [point1, point2, point3]  # 该四面体所包含的顶点在Vertexs中的4个编号
    for j in range(3):
        if node_list[j] < Coarse_num:
            agg_dic[node_list[j] + 1].extend([point1, point2, point3])
            break
        else:
            pass

for i in agg_dic.keys():
    vertex_temp = list(set(agg_dic[i]))
    agg_dic[i] = []
    for j in range(len(vertex_temp)):
        if vertex_temp[j] < Coarse_num:
            pass
        else:
            agg_dic[i].append(Vertexs[vertex_temp[j]])

step6_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step6：整理每颗集料对应的顶点信息用时：', '%6f min' % ((step6_time - step5_time) / 60))
print('已累计用时：', '%6f min' % ((step6_time - star_time) / 60))

# step7: 输出集料信息
# (6-1)输出agg_cen信息
print('coarse number', file=outfile)
print(Coarse_num, file=outfile)
print('number of 3 aggregates', file=outfile)
print('%d,%d,%d' % (ball_num1, ball_num2 - ball_num1, 0), file=outfile)
for i in range(1, Coarse_num + 1):
    print('vertex-' + str(i) + '-', file=outfile)
    for j in range(len(agg_dic[i])):
        x = agg_dic[i][j][0]
        y = agg_dic[i][j][1]
        print('%12f,%12f' % (x, y), file=outfile)
    outfile.flush()  # 刷新缓冲区，否则可能漏数据

step7_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step7：生成沥青和集料信息用时：', '%6f min' % ((step7_time - step6_time) / 60))
print('已累计用时：', '%6f min' % ((step7_time - star_time) / 60))

print('基体顶点信息生成完成，已输出文件' + outfile_name)
