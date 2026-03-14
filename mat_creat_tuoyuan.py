# -*-coding:utf-8-*-
import copy
import random
import math
import time
import matplotlib.pyplot as plt
import numpy as np
import random
import matplotlib.animation as animation
from scipy.spatial import Delaunay
from scipy.spatial import ConvexHull
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from tqdm import tqdm
from tqdm import trange
from copy import deepcopy
from mpl_toolkits.mplot3d import Axes3D

#%matplotlib qt5

star_time = time.time()
print('start at', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

# step1: 相关设置信息输入
# (1-1)3档级配
por = [0.40, 0.33, 0.05]  # 3档集料的体积比例，9.5~16、4.75~9.5、2.36~4.75

# (1-2)骨料顶点距离
dis_ver = 0  # 扩张收缩前骨料两个顶点间的距离，mm,去除一些相距太近的点，避免过于接近球体

# (1-3)集料顶点收缩倍数
shr_min, shr_max = -0.4, -0.6  # 集料顶点收缩shr_min,shr_max倍，避免集料接触

# (1-4)沥青顶点扩张倍数
exp_min, exp_max = 0.65, 0.7  # 沥青顶点扩张exp_min~exp_max倍，集料周围裹附沥青 #得扩张，不然没有A...可以只扩一个敷衍一下？

# (1-5)文件输出设置
outFile_path = 'E:\\temp\\260106\\'
outfile_name = 'matrix_260106_test.txt'
logfile_name = 'matrix_260106_log.txt'
outfile = open(outFile_path + outfile_name, 'w+')
logfile = open(outFile_path + logfile_name, 'w+')

step1_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step1：相关设置信息输入用时：', '%6f min' % ((step1_time - star_time) / 60))
print('已累计用时：', '%6f min' % ((step1_time - star_time) / 60))

dierc = []
# step1.5: 射线定义
for i in range(0,20):
    direction = (1*random.random(),1*random.random(),1*random.random())
    dierc.append(direction)
for i in range(0,20):
    direction = (1*random.random(),1*random.random(),-1*random.random())
    dierc.append(direction)
for i in range(0,20):
    direction = (1*random.random(),-1*random.random(),1*random.random())
    dierc.append(direction)
for i in range(0,20):
    direction = (1*random.random(),-1*random.random(),-1*random.random())
    dierc.append(direction)
for i in range(0,20):
    direction = (-1*random.random(),1*random.random(),1*random.random())
    dierc.append(direction)
for i in range(0,20):
    direction = (-1*random.random(),1*random.random(),-1*random.random())
    dierc.append(direction)
for i in range(0,20):
    direction = (-1*random.random(),-1*random.random(),1*random.random())
    dierc.append(direction)
for i in range(0,20):
    direction = (-1*random.random(),-1*random.random(),-1*random.random())
    dierc.append(direction)
    
print("向量随机化完成", file=logfile)
print(dierc, file=logfile)

#visulization
def ray_ellipsoid_intersection(P0, direction, a, b, c, normalize_dir=True): #TODO
    """
    计算从点P0出发沿给定方向的射线与椭球表面的交点距离
    
    参数:
    P0: 起点坐标 (x0, y0, z0)
    direction: 方向向量 (dx, dy, dz)
    a, b, c: 椭球半轴长
    normalize_dir: 是否将方向向量归一化
    
    返回:
    distance: 交点距离（如果存在）
    intersection_point: 交点坐标（如果存在）
    t: 参数t的值
    """
    
    # 提取坐标
    x0, y0, z0 = P0
    dx, dy, dz = direction
    
    # 归一化方向向量（可选）
    if normalize_dir:
        norm = math.sqrt(dx**2 + dy**2 + dz**2)
        if norm == 0:
            raise ValueError("方向向量长度不能为零")
        dx, dy, dz = dx/1, dy/1, dz/1
    
    # 计算二次方程系数
    A = (dx**2)/(a**2) + (dy**2)/(b**2) + (dz**2)/(c**2)
    B = 2*((x0*dx)/(a**2) + (y0*dy)/(b**2) + (z0*dz)/(c**2))
    C = (x0**2)/(a**2) + (y0**2)/(b**2) + (z0**2)/(c**2) - 1
    
    # 计算判别式
    discriminant = B**2 - 4*A*C
    #print(f"A={A} B={B} C={C} discriminant={discriminant}")
    if discriminant < 0:
        # 无实数解，不相交
        return None, None, None
    
    # 计算两个根
    sqrt_disc = math.sqrt(discriminant)
    t1 = (-B + sqrt_disc) / (2*A)
    t2 = (-B - sqrt_disc) / (2*A)
    
    # 选择满足 t >= 0 且最小的正根
    valid_t = []
    if t1 >= 0:
        valid_t.append(t1)
    if t2 >= 0:
        valid_t.append(t2)
    
    if not valid_t:
        # 没有正根，不相交
        return None, None, None
    
    # 取最小的正根（最近的交点）
    t = min(valid_t)
    
    # 计算交点和距离
    intersection_point = (
        x0 + dx * t,
        y0 + dy * t,
        z0 + dz * t
    )
    
    # 计算实际距离（如果方向向量已归一化，则t就是距离）
    if normalize_dir:
        distance = t
    else:
        # 计算射线长度
        distance = t * math.sqrt(dx**2 + dy**2 + dz**2)
    
    return distance, intersection_point, t

def ray_ellipsoid_distance(P0, direction, a, b, c, normalize_dir=True):
    """
    简化的函数，只返回距离
    """
    distance, _, _ = ray_ellipsoid_intersection(P0, direction, a, b, c, normalize_dir)
    return distance
'''
P0 = (0, 0, 0)
a_ellipsoid, b_ellipsoid, c_ellipsoid = 2.0, 3.0, 1.5
for i in dierc:
    print("direction:",i)
    distance = ray_ellipsoid_distance(P0, i, a_ellipsoid, b_ellipsoid, c_ellipsoid)
    if distance is not None:
        print(f"交点距离: {distance:.4f}")
    else:
        print("不相交")
'''
print("\n" + "="*50 + "\n")

# 可视化验证函数
def visualize_intersection():
    """生成可视化数据"""

    pointall = []
    # 生成椭球表面点
    u = np.linspace(0, 2*np.pi, 30)
    v = np.linspace(0, np.pi, 30)
    
    #x = a_ellipsoid * np.outer(np.cos(u), np.sin(v))
    #y = b_ellipsoid * np.outer(np.sin(u), np.sin(v))
    #z = c_ellipsoid * np.outer(np.ones_like(u), np.cos(v))
    

    # 创建图形

    
    # 绘制椭球        
    #P0 = (0, 0, 0.5)            
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    #ax.plot_surface(x, y, z, alpha=0.3, color='blue')
    
    # 射线        
    k = 0
    max_x = -99
    min_x = 99
    max_y = -99
    min_y = 99
    max_z = -99
    min_z = 99
    for i in dierc:
        direction = i
        k = k + 1
        #distance, point, _ = ray_ellipsoid_intersection(P0, direction, a_ellipsoid, b_ellipsoid, c_ellipsoid)
    # 绘制射线
        if distance is not None:
        # 射线线段
            t_vals = np.linspace(0, SLD[k-1], 10)
            ray_x = direction[0] * t_vals
            ray_y = direction[1] * t_vals
            ray_z = direction[2] * t_vals
           
            point = [0,0,0]
            point[0] = direction[0] * SLD[k-1]
            point[1] = direction[1] * SLD[k-1]
            point[2] = direction[2] * SLD[k-1]
            ax.plot(ray_x, ray_y, ray_z, 'r-', linewidth=2)
            pointall.append(point) 
            
            max_x = max(max_x, point[0])
            min_x = min(min_x, point[0])
            max_y = max(max_y, point[1])
            min_y = min(min_y, point[1])
            max_z = max(max_z, point[2])
            min_z = min(min_z, point[2])
            
        # 起点
            ax.scatter(0, 0, 0, c='green', s=100)          
        # 交点
            ax.scatter(point[0], point[1], point[2], c='red', s=100)            
            #ax.legend()
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    #ax.set_title(f'Ray-Ellipsoid Intersection\nDistance: {distance:.3f}' if distance else 'No Intersection')
    plt.tight_layout()
    ax.view_init(elev=5, azim=80)  # 仰角，方位角
    plt.savefig("sld1.jpg",dpi=600)
    plt.show()
    
    
    print(f"max_x = {max_x} min_x = {min_x}")
    print(f"max_y = {max_y} min_y = {min_y}")
    print(f"max_z = {max_z} min_z = {min_z}")
    #包络图
    pts = np.array(pointall)
    #print(pts)
    print("\n")
    hull = ConvexHull(pts)
    ax = plt.subplot(projection='3d')
    ax.scatter(pts[:,0], pts[:,1], pts[:,2])
    for i in hull.simplices:
        ax.plot_trisurf(pts[i, 0], pts[i, 1], pts[i,2], alpha=0.5)
        #print(f"{pts[i, 0]},{pts[i, 1]}, {pts[i,2]}")
    ax.view_init(elev=5, azim=80)  # 仰角，方位角
    plt.savefig("vertix.jpg",dpi=600)
    plt.show()
    


# 如果需要可视化，取消注释下面的行
#visualize_intersection()

def point_position(P0, ball_dic, ea, eb, ec):#TODO
    if (P0[0])**2/ea**2 + (P0[1])**2/eb**2 + (P0[2])**2/ec**2 <= ball_dic[1][0]**2:
        t = 0
    else:
        t = 1        
    return t

# step2: 函数定义与文件读取
# (1-1)圆心距离判断函数 
def judgemat(ball1, ball2, rate):  # rate为距离与半径之和的比
    loc = 0
    dis = math.sqrt(
        (ball1[0][0] - ball2[0][0]) ** 2 + (ball1[0][1] - ball2[0][1]) ** 2 + (ball1[0][2] - ball2[0][2]) ** 2)
    radius = ball1[1][0] + ball2[1][0]
    if dis >= rate * radius:  # 两圆心距离大于rate*半径之和则满足投放条件
        loc = 1
    return loc


step2_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step2：函数定义与文件读取用时：', '%6f min' % ((step2_time - step1_time) / 60))
print('已累计用时：', '%6f min' % ((step2_time - star_time) / 60))

# step3: 生成集料对应的球体 
#TODO:椭球体 x^2/a+y^2/b = r^2
# 包含3步：(3-1)投放粗集料球体；（3-2）在边缘投放粒径为3.0mm的填充料； (3-3)绘制图形
# (3-1)投放粗集料球体
ball_dic = {}  # 键为球体编号，值为一个列表，里面有2个元素，第1个元素是列表，里面是球心坐标[x0,y0,z0]；第2个元素为列表，里面是球体半径[r]；
judgenum = 0  # 判断数，为1时可以投放
ball_num = 0  # 球体编号
vol1 = 0  # 1档料的球体总体积
ea=1.0
eb=0.8
ec=0.6  #TODO yz轴偏率
#??? :预设椭圆离心率 r2=0.8r1 r3=0.6r1
for i in range(50000):
    # todo 疑问1：为什么三维的这里是×0.65，二维的却是×0.8
    if vol1 < 60 * 35 * 30 * por[0]:  # 1档料球体体积占关心区域体积比 去掉*0.65(不含水泥)
        pass
    else:
        break
    r1 = 12.0 / 2 + 5.0 * random.random() / 2  # 1档料对应球体的半径，粒径12-17
    vol_sin = (4.0 / 3) * math.pi * math.pow(r1, 3) * eb * ec  # 单颗集料球体的体积
    #质心坐标
    x = -30.0 + 60.0 * random.random()  # -30<x<=30
    y = 0.0 + 35.0 * random.random()  # 0<y<=35
    z = -15.0 + 30.0 * random.random()  # -15<z<=15
    br1 = eb * r1
    cr1 = ec * r1
    ball_temp = [[x, y, z], [r1], [br1], [cr1]]
    if ball_dic == {}:
        judgenum = 1
    else:
        for j in ball_dic.keys():
            if judgemat(ball_dic[j], ball_temp, 0.9) == 1:
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
print('1档料对应球体体积占比为：', vol1 / (60 * 35 * 30))

vol2 = 0  # 2档料的球体总体积
for i in range(100000):
    if vol2 < 60 * 35 * 30 * por[1]:  # 2档料球体体积占关心区域体积比
        pass
    else:
        break
    r2 = 6.0 / 2 + 4.0 * random.random() / 2  # 2档料对应球体的半径，粒径6~10
    vol_sin = (4.0 / 3) * math.pi * math.pow(r2, 3)  # 单颗集料球体的体积
    x = -30.0 + 60.0 * random.random()  # -30<x<=30
    y = 0.0 + 35.0 * random.random()  # 0<y<=35
    z = -15.0 + 30.0 * random.random()  # -15<z<=15
    br2 = eb * r2
    cr2 = ec * r2
    x_min, x_max, y_min, y_max, z_min, z_max = x - r2, x + r2, y - r2, y + r2, z - r2, z + r2
    if x_min < -30:  # 部分位于试件外的粗集料移动到边界上
        x = -30
    elif x_max > 30:
        x = 30
    elif y_min < 0:
        y = 0
    elif y_max > 35:
        y = 35
    elif z_min < -15:
        z = -15
    elif z_max > 15:
        z = 15
    else:
        pass
    ball_temp = [[x, y, z], [r2], [br2], [cr2]]
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
print('2档料对应球体体积占比为：', vol2 / (60 * 35 * 30))

vol3 = 0  # 3档料的球体总体积，粒径3~5
for i in range(1000000):
    if vol3 < 60 * 35 * 30 * por[2]:  # 3档料球体体积占关心区域体积比
        pass
    else:
        break
    r3 = 3.0 / 2 + 2.0 * random.random() / 2  # 3档料对应球体的半径，粒径3~5
    vol_sin = (4.0 / 3) * math.pi * math.pow(r3, 3)  # 单颗集料球体的体积
    x = -30.0 + 60.0 * random.random()  # -30<x<=30
    y = 0.0 + 35.0 * random.random()  # 0<y<=35
    z = -15.0 + 30.0 * random.random()  # -15<z<=15
    br3 = eb * r3
    cr3 = ec * r3
    x_min, x_max, y_min, y_max, z_min, z_max = x - r2, x + r2, y - r2, y + r2, z - r2, z + r2
    if x_min < -30:  # 部分位于试件外的粗集料移动到边界上
        x = -30
    elif x_max > 30:
        x = 30
    elif y_min < 0:
        y = 0
    elif y_max > 35:
        y = 35
    elif z_min < -15:
        z = -15
    elif z_max > 15:
        z = 15
    else:
        pass
    ball_temp = [[x, y, z], [r3], [br3], [cr3]]
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
print('3档料对应球体体积占比为：', vol3 / (60 * 35 * 30))

Coarse_num = ball_num  # 粗集料数量

# (3-2)只在边缘投放粒径为3mm的填充集料
r0 = 3.0 / 2  # 填充料对应球体的半径    
br0 = eb * r0
cr0 = ec * r0
vol0 = 0  # 填充料的球体总体积
vol_sin = (4.0 / 3) * math.pi * math.pow(r0, 3)  # 单颗集料球体的体积
core_lib = []  # 填充料球心坐标库，比关心区域每个方向多8mm
for x in range(-38, 39, 1):
    for y in range(-8, 44, 1):
        for z in range(-23, 24, 1):
            if 31 >= x >= -31 <= y <= 31 and -11 <= z <= 11:
                pass
            else:
                core_lib.append([x, y, z])
random.shuffle(core_lib)

for i in range(len(core_lib)):
    ball_temp = [core_lib[i], [r0], [br0], [cr0]]
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
        if judgemat(ball_dic[j], ball_temp, 3) == 1:
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
print('填充料对应球体体积占比为：', vol0 / (60 * 35 * 30))

# (3-3)绘制图形并计算SLD
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
u = np.linspace(0, 2 * np.pi, 10)  # 用参数方程画球 0~2pi
v = np.linspace(0, np.pi, 10)  #0~pi
#ball_temp = [[x, y, z], [r1], [r2], [r3]]

print('正在计算SLD')
distance = []
#TODO
timei = 0
i = 0
while i < 60:  #第i个点
    timei = timei + 1
    print(f"{i}编号，{timei}次尝试")
    if timei > 999:
        print("ERROR!")
        break
    ifinball = 0
    Px = -25.0 + 50.0 * random.random()  # -25<x<=25
    Py = 5.0 + 25.0 * random.random()  # 5<y<=30
    Pz = -10.0 + 20.0 * random.random()  # -10<z<=10 确保不要太靠边
    
    for j in range(1, ball_num2 + 1): #所有1/2档球
        P0 = (ball_dic[j][0][0]-Px, ball_dic[j][0][1]-Py, ball_dic[j][0][2]-Pz) #相对坐标
        if point_position(P0,ball_dic[j],ea,eb,ec) == 0: #若在球内
            print(P0)
            ifinball = 1
            break
    if ifinball:
        print("在球内重随")
        continue
    s = 0
    print("在球外")
    kdist = []
    for k in dierc:  #每条射线方向
        distmin = 999
        dk = 0
        for p in range(1, ball_num2 + 1):
            P0 = (ball_dic[p][0][0]-Px, ball_dic[p][0][1]-Py, ball_dic[p][0][2]-Pz)
            dist = ray_ellipsoid_distance(P0, k, ball_dic[p][1][0], ball_dic[p][2][0], ball_dic[p][3][0])
            #print(f"P0={P0} k={k} ballr={ball_dic[p][1][0]} {ball_dic[p][2][0]} {ball_dic[p][3][0]}")
            if dist != None:
                distmin = min(distmin, dist)
        kdist.append(distmin)  
        #print(f"dircton{k} dist:{distmin}")
        s = s + 1
    print(f"{s}条射线计算完成")
    distance.append(kdist)
    i = i + 1
    print(f"第{i}个点计算完成")
    
    #print("distance:",distance)
SLD = []
print('SLD-distance', file=logfile)
for j in range(0,160):
    pk = 0
    nump = 0
    for i in distance:
        if i[j] != 999:
            pk = pk + i[j]
            nump = nump + 1
    if nump !=0:
        sldind = pk / nump
    else:
        sldind = -1
    SLD.append(sldind)
    print(f'第{j+1}个方向的SLD为{sldind}')
    print('第%d个方向的SLD为%f',j+1, sldind, file=logfile)

visualize_intersection()
    
    
    

print('正在绘制1档料')
for i in range(1, ball_num1 + 1):
    x = ball_dic[i][0][0] + ball_dic[i][1][0] * np.outer(np.cos(u), np.sin(v)) #rsinv*cosu
    y = ball_dic[i][0][1] + ball_dic[i][2][0] * np.outer(np.sin(u), np.sin(v)) #rsinv*sinu
    z = ball_dic[i][0][2] + ball_dic[i][3][0] * np.outer(np.ones(np.size(u)), np.cos(v)) #rcosu
    ax.plot_surface(x, y, z, color="green")

print('正在绘制2档料')
for i in range(ball_num1 + 1, ball_num2 + 1):
    x = ball_dic[i][0][0] + ball_dic[i][1][0] * np.outer(np.cos(u), np.sin(v))
    y = ball_dic[i][0][1] + ball_dic[i][2][0] * np.outer(np.sin(u), np.sin(v))
    z = ball_dic[i][0][2] + ball_dic[i][3][0] * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color="yellow")
print('正在绘制3档料')
for i in range(ball_num2 + 1, ball_num3 + 1):
    x = ball_dic[i][0][0] + ball_dic[i][1][0] * np.outer(np.cos(u), np.sin(v))
    y = ball_dic[i][0][1] + ball_dic[i][2][0] * np.outer(np.sin(u), np.sin(v))
    z = ball_dic[i][0][2] + ball_dic[i][3][0] * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color="purple")
print('正在绘制填充料')
for i in range(Coarse_num + 1, ball_numf + 1):
    x = ball_dic[i][0][0] + ball_dic[i][1][0] * np.outer(np.cos(u), np.sin(v))
    y = ball_dic[i][0][1] + ball_dic[i][2][0] * np.outer(np.sin(u), np.sin(v))
    z = ball_dic[i][0][2] + ball_dic[i][3][0] * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color="red")

x, y, z = -30, 0, -15  # 绘制长方体线框
dx, dy, dz = 60, 35, 30
k = 10
xx = [x, x + dx, x + dx, x, x]
yy = [y + dy, y + dy, y, y, y + dy]
kwargs1 = {'linewidth': 1, 'color': 'black', 'linestyle': '-'}
kwargs2 = {'linewidth': 1, 'color': 'black', 'linestyle': '--'}
ax.plot(xx, yy, [z + dz] * 5, **kwargs1)
ax.plot(xx[:3], yy[:3], [z] * 3, **kwargs1)
ax.plot(xx[2:], yy[2:], [z] * 3, **kwargs2)
for n in range(3):
    ax.plot([xx[n], xx[n]], [yy[n], yy[n]], [z, z + dz], **kwargs1)
ax.plot([xx[3], xx[3]], [yy[3], yy[3]], [z, z + dz], **kwargs2)
# ax.set_aspect('equal')
ax.set_aspect('auto')
ax.set_xlabel('X', fontsize=10)
ax.set_ylabel('Y', fontsize=10)
ax.set_zlabel('Z', fontsize=10)
ax.view_init(elev=25, azim=85)  # 仰角，方位角
plt.savefig("demo.jpg",dpi=600)
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
ax = fig.add_subplot(projection='3d')
for i in range(len(tri.simplices)):
    point1 = tri.simplices[i][0]  # 该四面体所包含的球心点编号，共4个，认为前3个点构成底面，最后一个点为顶点（4球链接
    point2 = tri.simplices[i][1]
    point3 = tri.simplices[i][2]
    point4 = tri.simplices[i][3]
    x = [Cores[point1][0], Cores[point2][0], Cores[point3][0], Cores[point1][0]]  # 画底边3条线
    y = [Cores[point1][1], Cores[point2][1], Cores[point3][1], Cores[point1][1]]
    z = [Cores[point1][2], Cores[point2][2], Cores[point3][2], Cores[point1][2]]
    ax.plot(x, y, z)
    x1 = [Cores[point4][0], Cores[point1][0], Cores[point2][0], Cores[point4][0], Cores[point3][0]]  # 连接其它的线
    y1 = [Cores[point4][1], Cores[point1][1], Cores[point2][1], Cores[point4][1], Cores[point3][1]]
    z1 = [Cores[point4][2], Cores[point1][2], Cores[point2][2], Cores[point4][2], Cores[point3][2]]
    ax.plot(x1, y1, z1)
ax.set(xlim=[-40, 40], ylim=[-10, 45], zlim=[-25, 25])
ax.set_xlabel('X', fontsize=14)
ax.set_ylabel('Y', fontsize=14)
ax.set_zlabel('Z', fontsize=14)
ax.view_init(elev=25, azim=85)  # 仰角，方位角
plt.savefig("delaunay.jpg",dpi=600)
plt.show()

step4_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step4：第1次Delaunay划分用时：', '%6f min' % ((step4_time - step3_time) / 60))
print('已累计用时：', '%6f min' % ((step4_time - star_time) / 60))

# step5: 第2次Delaunay划分
# (5-1)对集料球心和顶点进行Delaunay划分
Vertexs = []
Vertexs.extend(Cores)  # 列表，里面是若干列表，每个列表里面是球心或顶点的坐标
for i in range(len(tri.simplices)):
    point1, point2, point3, point4 = tri.simplices[i][0], tri.simplices[i][1], tri.simplices[i][2], tri.simplices[i][
        3]  # 该四面体所包含的球心点编号，共4个，认为前3个点构成底面，最后一个点为顶点
    radius1, radius2, radius3, radius4 = ball_dic[point1 + 1][1][0], ball_dic[point2 + 1][1][0], \
                                         ball_dic[point3 + 1][1][0], ball_dic[point4 + 1][1][0]  # 4个球的半径1
    radius1b, radius2b, radius3b, radius4b = ball_dic[point1 + 1][2][0], ball_dic[point2 + 1][2][0], \
                                         ball_dic[point3 + 1][2][0], ball_dic[point4 + 1][2][0]  # 4个球的半径2
    radius1c, radius2c, radius3c, radius4c = ball_dic[point1 + 1][3][0], ball_dic[point2 + 1][3][0], \
                                         ball_dic[point3 + 1][3][0], ball_dic[point4 + 1][3][0]  # 4个球的半径3                                        
    x = ball_dic[point1 + 1][0][0] + (ball_dic[point2 + 1][0][0] - ball_dic[point1 + 1][0][0]) * radius1 / (
            radius1 + radius2)  # 第1个顶点的x坐标
    #p1[x]+(p2[x]-p1[x])*r1/(r1/r2) 即比例分割
    y = ball_dic[point1 + 1][0][1] + (ball_dic[point2 + 1][0][1] - ball_dic[point1 + 1][0][1]) * radius1b / (
            radius1b + radius2b)
    z = ball_dic[point1 + 1][0][2] + (ball_dic[point2 + 1][0][2] - ball_dic[point1 + 1][0][2]) * radius1c / (
            radius1c + radius2c)
    Vertexs.append([x, y, z])
    x = ball_dic[point1 + 1][0][0] + (ball_dic[point3 + 1][0][0] - ball_dic[point1 + 1][0][0]) * radius1 / (
            radius1 + radius3)  # 第2个顶点的x坐标
    y = ball_dic[point1 + 1][0][1] + (ball_dic[point3 + 1][0][1] - ball_dic[point1 + 1][0][1]) * radius1b / (
            radius1b + radius3b)
    z = ball_dic[point1 + 1][0][2] + (ball_dic[point3 + 1][0][2] - ball_dic[point1 + 1][0][2]) * radius1c / (
            radius1c + radius3c)
    Vertexs.append([x, y, z])
    x = ball_dic[point1 + 1][0][0] + (ball_dic[point4 + 1][0][0] - ball_dic[point1 + 1][0][0]) * radius1 / (
            radius1 + radius4)  # 第3个顶点的x坐标
    y = ball_dic[point1 + 1][0][1] + (ball_dic[point4 + 1][0][1] - ball_dic[point1 + 1][0][1]) * radius1b / (
            radius1b + radius4b)
    z = ball_dic[point1 + 1][0][2] + (ball_dic[point4 + 1][0][2] - ball_dic[point1 + 1][0][2]) * radius1c / (
            radius1c + radius4c)
    Vertexs.append([x, y, z])
    x = ball_dic[point2 + 1][0][0] + (ball_dic[point3 + 1][0][0] - ball_dic[point2 + 1][0][0]) * radius2 / (
            radius2 + radius3)  # 第4个顶点的x坐标
    y = ball_dic[point2 + 1][0][1] + (ball_dic[point3 + 1][0][1] - ball_dic[point2 + 1][0][1]) * radius2b / (
            radius2b + radius3b)
    z = ball_dic[point2 + 1][0][2] + (ball_dic[point3 + 1][0][2] - ball_dic[point2 + 1][0][2]) * radius2c / (
            radius2c + radius3c)
    Vertexs.append([x, y, z])
    x = ball_dic[point2 + 1][0][0] + (ball_dic[point4 + 1][0][0] - ball_dic[point2 + 1][0][0]) * radius2 / (
            radius2 + radius4)  # 第5个顶点的x坐标
    y = ball_dic[point2 + 1][0][1] + (ball_dic[point4 + 1][0][1] - ball_dic[point2 + 1][0][1]) * radius2b / (
            radius2b + radius4b)
    z = ball_dic[point2 + 1][0][2] + (ball_dic[point4 + 1][0][2] - ball_dic[point2 + 1][0][2]) * radius2c / (
            radius2c + radius4c)
    Vertexs.append([x, y, z])
    x = ball_dic[point3 + 1][0][0] + (ball_dic[point4 + 1][0][0] - ball_dic[point3 + 1][0][0]) * radius3 / (
            radius3 + radius4)  # 第6个顶点的x坐标
    y = ball_dic[point3 + 1][0][1] + (ball_dic[point4 + 1][0][1] - ball_dic[point3 + 1][0][1]) * radius3b / (
            radius3b + radius4b)
    z = ball_dic[point3 + 1][0][2] + (ball_dic[point4 + 1][0][2] - ball_dic[point3 + 1][0][2]) * radius3c / (
            radius3c + radius4c)
    Vertexs.append([x, y, z])
tri2 = Delaunay(Vertexs)

# (5-2)绘图
fig = plt.figure()  # 绘图
ax = fig.add_subplot(projection='3d')
for i in range(len(tri2.simplices)): #tri2里共i个四边型
    point1 = tri2.simplices[i][0]  # 该四面体所包含的顶点编号，共4个，认为前3个点构成底面，最后一个点为顶点
    point2 = tri2.simplices[i][1]
    point3 = tri2.simplices[i][2]
    point4 = tri2.simplices[i][3]
    x = [Vertexs[point1][0], Vertexs[point2][0], Vertexs[point3][0], Vertexs[point1][0]]  # 画底边3条线
    y = [Vertexs[point1][1], Vertexs[point2][1], Vertexs[point3][1], Vertexs[point1][1]]
    z = [Vertexs[point1][2], Vertexs[point2][2], Vertexs[point3][2], Vertexs[point1][2]]
    ax.plot(x, y, z)
    x1 = [Vertexs[point4][0], Vertexs[point1][0], Vertexs[point2][0], Vertexs[point4][0], Vertexs[point3][0]]  # 连接其它的线
    y1 = [Vertexs[point4][1], Vertexs[point1][1], Vertexs[point2][1], Vertexs[point4][1], Vertexs[point3][1]]
    z1 = [Vertexs[point4][2], Vertexs[point1][2], Vertexs[point2][2], Vertexs[point4][2], Vertexs[point3][2]]
    ax.plot(x1, y1, z1)
ax.set(xlim=[-40, 40], ylim=[-10, 45], zlim=[-25, 25])
ax.set_xlabel('X', fontsize=14)
ax.set_ylabel('Y', fontsize=14)
ax.set_zlabel('Z', fontsize=14)
ax.view_init(elev=25, azim=85)  # 仰角，方位角
plt.savefig("plot.jpg",dpi=600)
plt.show()

step5_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step5：第2次Delaunay划分用时：', '%6f min' % ((step5_time - step4_time) / 60))
print('已累计用时：', '%6f min' % ((step5_time - star_time) / 60))

# step6: 整理每颗集料对应的顶点信息 
#HACK 
agg_dic = {}  # 键为集料编号，值为1个列表，里面有2个元素，第1个元素是形心坐标，第2个元素是列表，里面是各个顶点的坐标
#[[a,b,c],[[p1a,p1b,pic],[p2a,p2b,p2c],[p3...]]]
for i in range(1, Coarse_num + 1):  #i个delaunry四面体
    agg_dic[i] = []
judgenum = 0
for i in range(len(tri2.simplices)):
    point1 = tri2.simplices[i][0]  # 该四面体所包含的顶点在Vertexs中的编号
    point2 = tri2.simplices[i][1]
    point3 = tri2.simplices[i][2]
    point4 = tri2.simplices[i][3]
    node_list = [point1, point2, point3, point4]  # 该四面体所包含的顶点在Vertexs中的4个编号
    for j in range(4):
        if node_list[j] < Coarse_num:
            agg_dic[node_list[j] + 1].extend([point1, point2, point3, point4]) #第node_list[j] + 1集料的一个面
            break
        else:
            pass
judgenum = 0
for i in agg_dic.keys():
    vertex_temp1 = []  # 从二次DT网格中读取的原始顶点坐标信息,任意两点间距必须大于dis_ver
    for j in range(len(agg_dic[i])):  #i个拟合集料
        if agg_dic[i][j] < Coarse_num:  #i个拟合集料的第j个面？
            judgenum = 0
        else:
            if not vertex_temp1: #if blank
                judgenum = 1
            else:
                x, y, z = Vertexs[agg_dic[i][j]][0], Vertexs[agg_dic[i][j]][1], Vertexs[agg_dic[i][j]][2] 
                # [点i][point j]
                for k in range(len(vertex_temp1)):
                    x1, y1, z1 = vertex_temp1[k][0], vertex_temp1[k][1], vertex_temp1[k][2]
                    if math.sqrt((x1 - x) ** 2 + (y1 - y) ** 2 + (z1 - z) ** 2) < dis_ver:
                        judgenum = 0
                        break
                    else:
                        judgenum = 1
        if judgenum == 1:
            vertex_temp1.append(Vertexs[agg_dic[i][j]])
        else:
            pass
    vertex_temp2 = []  # ConvexHull凸包顶点坐标信息
    vertexs_key = ConvexHull(vertex_temp1).vertices
    for j in range(len(vertexs_key)):
        vertex_temp2.append(vertex_temp1[vertexs_key[j]])
    x_sum = 0  # 所有x坐标值的和
    y_sum = 0  # 所有y坐标值的和
    z_sum = 0  # 所有z坐标值的和
    for j in range(len(vertex_temp2)):  # 确定中心坐标  vertex_temp2[i]是第i个顶点的坐标列表
        x_sum += vertex_temp2[j][0]
        y_sum += vertex_temp2[j][1]
        z_sum += vertex_temp2[j][2]
    x0 = x_sum / (len(vertex_temp2))
    y0 = y_sum / (len(vertex_temp2))
    z0 = z_sum / (len(vertex_temp2))
    agg_dic[i] = []
    agg_dic[i].append([x0, y0, z0])  #中点
    agg_dic[i].append(vertex_temp2)  #一个元素，包含数个顶点

agg_lib = {}  # 最终存储集料顶点信息的字典，键为集料编号，值为一个列表，里面有2个元素，第1个元素是形心坐标，第2个元素是各个顶点的坐标
# 本步骤的目的的去掉顶点数少于4个的集料
agg_count = 0  # 集料重新编号
for i in agg_dic.keys():
    if len(agg_dic[i][1]) < 4:
        pass
    else:
        agg_count += 1
        agg_lib[agg_count] = agg_dic[i]

step6_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step6：整理每颗集料对应的顶点信息用时：', '%6f min' % ((step6_time - step5_time) / 60))
print('已累计用时：', '%6f min' % ((step6_time - star_time) / 60))

# step7: 生成集料和沥青信息
# (7-1)顶点收缩生成集料
sto_lib = {}  # 键为集料编号，值为一个列表，里面是骨料顶点收缩后的顶点坐标
for i in agg_lib.keys():
    sto_lib[i] = []
    x0, y0, z0 = agg_lib[i][0][0], agg_lib[i][0][1], agg_lib[i][0][2]
    rate = random.random()
    for j in range(len(agg_lib[i][1])):    
        x = x0 + (1.0 - shr_min - (shr_max - shr_min) * rate) * (agg_lib[i][1][j][0] - x0)
        y = y0 + eb * (1.0 - shr_min - (shr_max - shr_min) * rate) * (agg_lib[i][1][j][1] - y0)
        z = z0 + ec * (1.0 - shr_min - (shr_max - shr_min) * rate) * (agg_lib[i][1][j][2] - z0)
        sto_lib[i].append([x, y, z])

# (7-2)顶点扩张生成沥青(只有沥青和集料时，要如何？)
asp_lib = {}  # 键为沥青编号，值为一个列表，里面是骨料顶点扩张后的顶点坐标
for i in sto_lib.keys():
    asp_lib[i] = []
    x0, y0, z0 = agg_lib[i][0][0], agg_lib[i][0][1], agg_lib[i][0][2]
    rate = random.random()
    for j in range(len(sto_lib[i])):
        #if j == 1:  # 当扩张系数小于0.3时，直接不扩张，为了确保存在CS界面，意思就是有30%的概率不扩张
            #x = sto_lib[i][j][0]
            #y = sto_lib[i][j][1]
            #z = sto_lib[i][j][2]
        #都扩张
        #else:
        x = x0 + (1.0 + exp_min + (exp_max - exp_min) * rate) * (sto_lib[i][j][0] - x0)
        y = y0 + eb * (1.0 + exp_min + (exp_max - exp_min) * rate) * (sto_lib[i][j][1] - y0)
        z = z0 + ec * (1.0 + exp_min + (exp_max - exp_min) * rate) * (sto_lib[i][j][2] - z0)
        asp_lib[i].append([x, y, z])

step7_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step7：生成沥青和集料信息用时：', '%6f min' % ((step7_time - step6_time) / 60))
print('已累计用时：', '%6f min' % ((step7_time - star_time) / 60))

# step8: 输出沥青和集料信息
# (8-1)输出骨料信息
print('agg number', file=outfile)
print('%12d' % Coarse_num, file=outfile)
# print(Coarse_num,file=outfile)
print('number of 3 aggregates', file=outfile)
print('%12d,%12d,%12d' % (ball_num1, ball_num2 - ball_num1, ball_num3 - ball_num2), file=outfile) #3档集料数目

# (8-2)输出沥青顶点信息
for i in asp_lib.keys():
    print('asp-vertex-' + str(i) + '-', file=outfile)
    for j in range(len(asp_lib[i])):
        x = asp_lib[i][j][0]
        y = asp_lib[i][j][1]
        z = asp_lib[i][j][2]
        print('%12f,%12f,%12f' % (x, y, z), file=outfile)
    outfile.flush()  # 刷新缓冲区，否则可能漏数据

# (8-3)输出集料顶点信息
for i in sto_lib.keys():
    print('sto-vertex-' + str(i) + '-', file=outfile)
    for j in range(len(sto_lib[i])):
        x = sto_lib[i][j][0]
        y = sto_lib[i][j][1]
        z = sto_lib[i][j][2]
        print('%12f,%12f,%12f' % (x, y, z), file=outfile)
    outfile.flush()  # 刷新缓冲区，否则可能漏数据

step8_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step8：输出沥青和集料信息用时：', '%6f min' % ((step8_time - step7_time) / 60))
print('已累计用时：', '%6f min' % ((step8_time - star_time) / 60))

print('基体顶点信息生成完成，已输出文件' + outfile_name)
