# -*-coding:UTF-8-*-
#插入czm,定义不同区域的材料归属
import time
import math
from copy import copy
from tqdm import tqdm
from tqdm import trange
from scipy.spatial import Delaunay
from scipy.spatial import ConvexHull
from copy import deepcopy

star_time = time.time()
print('start at', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

# step1：相关设置信息输入
# (1-1)读取标准网格文件
Base_File_path = 'E://Abaqus_examples_2nd_edition/No_cement/'
Mesh_File_path = 'E://Abaqus_examples_2nd_edition/No_cement/test928/'
Model_File_path = 'E://temp/NOcement1/'

Nor_inp_name = 'mesh_1mm.inp'
Nor_inp = open(Base_File_path + Nor_inp_name, 'r')
Nor_line = Nor_inp.readlines()

# (1-2)读取水泥单元信息文件
Cem_inp_name = 'cement_fake_01.txt'
Cem_inp = open(Model_File_path + Cem_inp_name, 'r')
Cem_line = Cem_inp.readlines()

# (1-3)读取基体单元信息文件
Mat_inp_name = 'biper_2d_test.inp'
Mat_inp = open(Mesh_File_path + Mat_inp_name, 'r')
Mat_line = Mat_inp.readlines()

# (1-4)读取集料几何信息文件
Sto_inp_name = 'matrix_13.txt'
Sto_inp = open(Mesh_File_path + Sto_inp_name, 'r')
Sto_line = Sto_inp.readlines()

# (1-5)输出文件信息
outFile_name = 'biper_nocement_01.inp'
outfile = open(Model_File_path + outFile_name, 'w+')

step1_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step1：相关设置信息输入用时：', '%6f min' % ((step1_time - star_time) / 60))
print('已累计用时：', '%6f min' % ((step1_time - star_time) / 60))

# step2：读取标准网格节点和单元信息
# (2-1)读取标准网格的节点信息
Node_dic = {}
for i in range(len(Nor_line)):
    if Nor_line[i].startswith('*Node'):
        node_startline = i
        break
    else:
        pass
for i in range(node_startline + 1, len(Nor_line)):
    try:
        Node1 = [float(cor) for cor in Nor_line[i].split(',')]  # 列表Node1，首个元素为节点编号，后三个元素为该节点的坐标
        Node_num = int(Node1[0])
        Node_dic[Node_num] = [Node1[1], Node1[2], Node1[3]]
    except:
        break
TNode_Value = max(Node_dic.keys())
print('标准网格的初始节点总数为：', TNode_Value)

# (2-2)读取标准网格的单元信息
Element_dic = {}  # 键为单元编号，值为一个列表，里面是8个节点的编号
for i in range(len(Nor_line)):
    if Nor_line[i].startswith('*Element, type=C3D8R'):
        ele_startline = i
        break
    else:
        pass
for i in range(ele_startline + 1, len(Nor_line)):
    try:
        Ele = [int(cor) for cor in Nor_line[i].split(',')]
        Element_dic[Ele[0]] = [Ele[1], Ele[2], Ele[3], Ele[4], Ele[5], Ele[6], Ele[7], Ele[8]]
    except:
        break
TEle_Value = max(Element_dic.keys())
TEle_Value1 = TEle_Value
print('标准网格的初始单元总数为：', TEle_Value)

# (2-3)计算标准网格中每个单元的形心坐标
Element_core = {}  # 字典，键为单元编号，值为一个列表，里面是该单元的形心坐标
for i in Element_dic.keys():
    n1 = Element_dic[i][0]  # 该单元的节点1
    n2 = Element_dic[i][1]
    n3 = Element_dic[i][2]
    n4 = Element_dic[i][3]
    n5 = Element_dic[i][4]
    n6 = Element_dic[i][5]
    n7 = Element_dic[i][6]
    n8 = Element_dic[i][7]
    x1 = Node_dic[n1][0]
    y1 = Node_dic[n1][1]
    z1 = Node_dic[n1][2]
    x2 = Node_dic[n2][0]
    y2 = Node_dic[n2][1]
    z2 = Node_dic[n2][2]
    x3 = Node_dic[n3][0]
    y3 = Node_dic[n3][1]
    z3 = Node_dic[n3][2]
    x4 = Node_dic[n4][0]
    y4 = Node_dic[n4][1]
    z4 = Node_dic[n4][2]
    x5 = Node_dic[n5][0]
    y5 = Node_dic[n5][1]
    z5 = Node_dic[n5][2]
    x6 = Node_dic[n6][0]
    y6 = Node_dic[n6][1]
    z6 = Node_dic[n6][2]
    x7 = Node_dic[n7][0]
    y7 = Node_dic[n7][1]
    z7 = Node_dic[n7][2]
    x8 = Node_dic[n8][0]
    y8 = Node_dic[n8][1]
    z8 = Node_dic[n8][2]
    x0 = (x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8) / 8
    y0 = (y1 + y2 + y3 + y4 + y5 + y6 + y7 + y8) / 8
    z0 = (z1 + z2 + z3 + z4 + z5 + z6 + z7 + z8) / 8
    Element_core[i] = [x0, y0, z0]

step2_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step2：获取标准网格信息用时：', '%6f min' % ((step2_time - step1_time) / 60))
print('已累计用时：', '%6f min' % ((step2_time - star_time) / 60))

# step3: 读取水泥的单元信息
cem_ele = []
# 读取水泥单元信息
for i in range(1, len(Cem_line)):
    Node1 = [str(cor) for cor in Cem_line[i].split(',')]
    for j in range(len(Node1) - 1):
        label = int(Node1[j])
        x, y, z = Element_core[label][0], Element_core[label][1], Element_core[label][2]
        if x > -30 and x < 30 and y > 0 and y < 35 and z > -15 and z < 15:
            cem_ele.append(label)
        else:
            pass

step3_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step3：读取水泥的单元信息用时：', '%6f min' % ((step3_time - step2_time) / 60))
print('已累计用时：', '%6f min' % ((step3_time - star_time) / 60))

# step4：读取基体的单元信息
mat_ele = []  # 储存基体单元的编号，包括沥青单元和集料单元
for i in range(len(Mat_line)):
    if Mat_line[i].startswith('*Element, type=C3D8R'):
        ele_startline = i + 1
        break
    else:
        pass
for i in range(ele_startline, len(Mat_line)):
    try:
        Ele = [int(cor) for cor in Mat_line[i].split(',')]
        label = Ele[0]
        x, y, z = Element_core[label][0], Element_core[label][1], Element_core[label][2]
        if x > -30 and x < 30 and y > 0 and y < 35 and z > -15 and z < 15:
            mat_ele.append(label)
        else:
            pass
    except:
        break

step4_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step4：读取基体的单元信息用时：', '%6f min' % ((step4_time - step3_time) / 60))
print('已累计用时：', '%6f min' % ((step4_time - star_time) / 60))

# step5: 读取集料的几何信息
sto_dic = {}  # 键为集料编号，值为一个列表，里面有3个元素，第1个元素为列表，里面是形心坐标，第2个元素为列表，里面是[最小半径，最大半径]，
# 第3个元素为列表，里面为各个顶点坐标
for i in range(len(Sto_line)):
    if Sto_line[i].startswith('agg number'):
        agg_num = int(Sto_line[i + 1])  # 集料总数
        break
    else:
        pass

for i in range(1, agg_num + 1):
    vertex_temp = []  # 该集料的顶点信息
    for j in range(len(Sto_line)):
        if Sto_line[j].startswith('sto-vertex-' + str(i) + '-'):
            startline = j + 1
        else:
            pass
    for j in range(startline, len(Sto_line)):
        try:
            Node = [float(cor) for cor in Sto_line[j].split(',')]  # 列表Node，三个元素为该节点的坐标
            vertex_temp.append(Node)
        except:
            break
    x_sum = 0  # 所有x坐标值的和
    y_sum = 0  # 所有y坐标值的和
    z_sum = 0  # 所有z坐标值的和
    for j in range(len(vertex_temp)):  # 确定中心坐标
        x_sum += vertex_temp[j][0]
        y_sum += vertex_temp[j][1]
        z_sum += vertex_temp[j][2]
    x0 = x_sum / (len(vertex_temp))
    y0 = y_sum / (len(vertex_temp))
    z0 = z_sum / (len(vertex_temp))
    sto_dic[i] = []
    sto_dic[i].append([x0, y0, z0])
    rad_min = 100
    rad_max = 0
    for j in range(len(vertex_temp)):
        rad_temp = math.sqrt(
            (vertex_temp[j][0] - x0) ** 2 + (vertex_temp[j][1] - y0) ** 2 + (vertex_temp[j][2] - z0) ** 2)
        rad_min = min(rad_min, rad_temp)
        rad_max = max(rad_max, rad_temp)
    sto_dic[i].append([rad_min, rad_max])
    sto_dic[i].append(vertex_temp)

step5_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step5：读取集料的几何信息用时：', '%6f min' % ((step5_time - step4_time) / 60))
print('已累计用时：', '%6f min' % ((step5_time - star_time) / 60))

# step6:不同类型单元映射
cem_ele = sorted(set(cem_ele) - set(mat_ele))  #排除基体的水泥单元的标签(水泥)
sto_ele = []  # 列表，里面存储标准单元中集料单元的编号
print('集料内切球内单元映射进度为：')
for i in tqdm(mat_ele):  # 首先给集料内接球内的单元赋予属性
    for j in sto_dic.keys():  # 遍历集料编号
        x0 = sto_dic[j][0][0]
        y0 = sto_dic[j][0][1]
        z0 = sto_dic[j][0][2]
        rad_min = sto_dic[j][1][0]
        x = Element_core[i][0]
        y = Element_core[i][1]
        z = Element_core[i][2]
        if (x - x0) ** 2 + (y - y0) ** 2 + (z - z0) ** 2 <= rad_min ** 2:
            sto_ele.append(i)
            break
        else:
            pass
mat_ele = sorted(set(mat_ele) - set(sto_ele))
print('集料内外切球间单元映射进度为：')
for i in tqdm(mat_ele):  # 判断该单元是否位于集料外接球外，若在外面直接跳过该集料
    for j in sto_dic.keys():  # 遍历集料编号
        x0 = sto_dic[j][0][0]
        y0 = sto_dic[j][0][1]
        z0 = sto_dic[j][0][2]
        rad_max = sto_dic[j][1][1]
        x = Element_core[i][0]
        y = Element_core[i][1]
        z = Element_core[i][2]
        if (x - x0) ** 2 + (y - y0) ** 2 + (z - z0) ** 2 > rad_max ** 2:
            pass
        else:
            vertex_temp1 = deepcopy(sto_dic[j][2])
            vertex_temp2 = deepcopy(sto_dic[j][2])
            vertex_temp2.append(Element_core[i])
            if ConvexHull(vertex_temp2) == ConvexHull(vertex_temp1):
                sto_ele.append(i)
                break
            else:
                pass
asp_ele = sorted(set(mat_ele) - set(sto_ele)) #排除石头的基体单元的标签(沥青)

step6_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step6：不同单元类型映射用时：', '%6f min' % ((step6_time - step5_time) / 60))
print('已累计用时：', '%6f min' % ((step6_time - star_time) / 60))

# step7:生成沥青部分的面的信息并确定AA单元的插入位置
# 包含第1步：生成沥青部分的面的信息，第2步：确定AA单元的插入位置
# (7-1)生成沥青部分的面的信息
AFACEINEL = {}  # 字典AFACEINEL，键为沥青部分的单元编号，值为元组，里面是6个面
Aface_list = []  # 所有单元的所有面都记录进来，重复记录
for k in asp_ele:  # 遍历所有沥青单元编号
    n1 = Element_dic[k][0]  # 节点编号
    n2 = Element_dic[k][1]
    n3 = Element_dic[k][2]
    n4 = Element_dic[k][3]
    n5 = Element_dic[k][4]
    n6 = Element_dic[k][5]
    n7 = Element_dic[k][6]
    n8 = Element_dic[k][7]
    x1 = Node_dic[n1][0]
    y1 = Node_dic[n1][1]
    z1 = Node_dic[n1][2]
    x2 = Node_dic[n2][0]
    y2 = Node_dic[n2][1]
    z2 = Node_dic[n2][2]
    x3 = Node_dic[n3][0]
    y3 = Node_dic[n3][1]
    z3 = Node_dic[n3][2]
    x4 = Node_dic[n4][0]
    y4 = Node_dic[n4][1]
    z4 = Node_dic[n4][2]
    x5 = Node_dic[n5][0]
    y5 = Node_dic[n5][1]
    z5 = Node_dic[n5][2]
    x6 = Node_dic[n6][0]
    y6 = Node_dic[n6][1]
    z6 = Node_dic[n6][2]
    x7 = Node_dic[n7][0]
    y7 = Node_dic[n7][1]
    z7 = Node_dic[n7][2]
    x8 = Node_dic[n8][0]
    y8 = Node_dic[n8][1]
    z8 = Node_dic[n8][2]

    a1 = []  # 给第1个面的节点按顺时针顺序编号，该面的节点为1234
    face1_coord = {n1: [x1, y1, z1], n2: [x2, y2, z2], n3: [x3, y3, z3], n4: [x4, y4, z4]}
    if x1 == x2 == x3 == x4:  # 先判断是否在yz平面上
        y0 = (y1 + y2 + y3 + y4) / 4
        z0 = (z1 + z2 + z3 + z4) / 4
        for j in face1_coord.keys():
            if face1_coord[j][1] < y0 and face1_coord[j][2] < z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][1] < y0 and face1_coord[j][2] > z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][1] > y0 and face1_coord[j][2] > z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][1] > y0 and face1_coord[j][2] < z0:
                a1.append(j)
                break
            else:
                pass
    elif y1 == y2 == y3 == y4:  # 判断是否在xz平面上
        x0 = (x1 + x2 + x3 + x4) / 4
        z0 = (z1 + z2 + z3 + z4) / 4
        for j in face1_coord.keys():
            if face1_coord[j][0] < x0 and face1_coord[j][2] < z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0] < x0 and face1_coord[j][2] > z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0] > x0 and face1_coord[j][2] > z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0] > x0 and face1_coord[j][2] < z0:
                a1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0 = (x1 + x2 + x3 + x4) / 4
        y0 = (y1 + y2 + y3 + y4) / 4
        for j in face1_coord.keys():
            if face1_coord[j][0] < x0 and face1_coord[j][1] < y0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0] < x0 and face1_coord[j][1] > y0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0] > x0 and face1_coord[j][1] > y0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0] > x0 and face1_coord[j][1] < y0:
                a1.append(j)
                break
            else:
                pass
    a = (a1[0], a1[1], a1[2], a1[3])

    b1 = []  # 给第2个面的节点按顺时针顺序编号，该面的节点为5678
    face2_coord = {n5: [x5, y5, z5], n6: [x6, y6, z6], n7: [x7, y7, z7], n8: [x8, y8, z8]}
    if x5 == x6 == x7 == x8:  # 先判断是否在yz平面上
        y0 = (y5 + y6 + y7 + y8) / 4
        z0 = (z5 + z6 + z7 + z8) / 4
        for j in face2_coord.keys():
            if face2_coord[j][1] < y0 and face2_coord[j][2] < z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][1] < y0 and face2_coord[j][2] > z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][1] > y0 and face2_coord[j][2] > z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][1] > y0 and face2_coord[j][2] < z0:
                b1.append(j)
                break
            else:
                pass
    elif y5 == y6 == y7 == y8:  # 判断是否在xz平面上
        x0 = (x5 + x6 + x7 + x8) / 4
        z0 = (z5 + z6 + z7 + z8) / 4
        for j in face2_coord.keys():
            if face2_coord[j][0] < x0 and face2_coord[j][2] < z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0] < x0 and face2_coord[j][2] > z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0] > x0 and face2_coord[j][2] > z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0] > x0 and face2_coord[j][2] < z0:
                b1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0 = (x5 + x6 + x7 + x8) / 4
        y0 = (y5 + y6 + y7 + y8) / 4
        for j in face2_coord.keys():
            if face2_coord[j][0] < x0 and face2_coord[j][1] < y0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0] < x0 and face2_coord[j][1] > y0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0] > x0 and face2_coord[j][1] > y0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0] > x0 and face2_coord[j][1] < y0:
                b1.append(j)
                break
            else:
                pass
    b = (b1[0], b1[1], b1[2], b1[3])

    c1 = []  # 给第3个面的节点按顺时针顺序编号，该面的节点为1256
    face3_coord = {n1: [x1, y1, z1], n2: [x2, y2, z2], n5: [x5, y5, z5], n6: [x6, y6, z6]}
    if x1 == x2 == x5 == x6:  # 先判断是否在yz平面上
        y0 = (y1 + y2 + y5 + y6) / 4
        z0 = (z1 + z2 + z5 + z6) / 4
        for j in face3_coord.keys():
            if face3_coord[j][1] < y0 and face3_coord[j][2] < z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][1] < y0 and face3_coord[j][2] > z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][1] > y0 and face3_coord[j][2] > z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][1] > y0 and face3_coord[j][2] < z0:
                c1.append(j)
                break
            else:
                pass
    elif y1 == y2 == y5 == y6:  # 判断是否在xz平面上
        x0 = (x1 + x2 + x5 + x6) / 4
        z0 = (z1 + z2 + z5 + z6) / 4
        for j in face3_coord.keys():
            if face3_coord[j][0] < x0 and face3_coord[j][2] < z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0] < x0 and face3_coord[j][2] > z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0] > x0 and face3_coord[j][2] > z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0] > x0 and face3_coord[j][2] < z0:
                c1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0 = (x1 + x2 + x5 + x6) / 4
        y0 = (y1 + y2 + y5 + y6) / 4
        for j in face3_coord.keys():
            if face3_coord[j][0] < x0 and face3_coord[j][1] < y0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0] < x0 and face3_coord[j][1] > y0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0] > x0 and face3_coord[j][1] > y0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0] > x0 and face3_coord[j][1] < y0:
                c1.append(j)
                break
            else:
                pass
    c = (c1[0], c1[1], c1[2], c1[3])

    d1 = []  # 给第4个面的节点按顺时针顺序编号，该面的节点为3478
    face4_coord = {n3: [x3, y3, z3], n4: [x4, y4, z4], n7: [x7, y7, z7], n8: [x8, y8, z8]}
    if x3 == x4 == x7 == x8:  # 先判断是否在yz平面上
        y0 = (y3 + y4 + y7 + y8) / 4
        z0 = (z3 + z4 + z7 + z8) / 4
        for j in face4_coord.keys():
            if face4_coord[j][1] < y0 and face4_coord[j][2] < z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][1] < y0 and face4_coord[j][2] > z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][1] > y0 and face4_coord[j][2] > z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][1] > y0 and face4_coord[j][2] < z0:
                d1.append(j)
                break
            else:
                pass
    elif y3 == y4 == y7 == y8:  # 判断是否在xz平面上
        x0 = (x3 + x4 + x7 + x8) / 4
        z0 = (z3 + z4 + z7 + z8) / 4
        for j in face4_coord.keys():
            if face4_coord[j][0] < x0 and face4_coord[j][2] < z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0] < x0 and face4_coord[j][2] > z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0] > x0 and face4_coord[j][2] > z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0] > x0 and face4_coord[j][2] < z0:
                d1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0 = (x3 + x4 + x7 + x8) / 4
        y0 = (y3 + y4 + y7 + y8) / 4
        for j in face4_coord.keys():
            if face4_coord[j][0] < x0 and face4_coord[j][1] < y0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0] < x0 and face4_coord[j][1] > y0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0] > x0 and face4_coord[j][1] > y0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0] > x0 and face4_coord[j][1] < y0:
                d1.append(j)
                break
            else:
                pass
    d = (d1[0], d1[1], d1[2], d1[3])

    e1 = []  # 给第5个面的节点按顺时针顺序编号，该面的节点为2367
    face5_coord = {n2: [x2, y2, z2], n3: [x3, y3, z3], n6: [x6, y6, z6], n7: [x7, y7, z7]}
    if x2 == x3 == x6 == x7:  # 先判断是否在yz平面上
        y0 = (y2 + y3 + y6 + y7) / 4
        z0 = (z2 + z3 + z6 + z7) / 4
        for j in face5_coord.keys():
            if face5_coord[j][1] < y0 and face5_coord[j][2] < z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][1] < y0 and face5_coord[j][2] > z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][1] > y0 and face5_coord[j][2] > z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][1] > y0 and face5_coord[j][2] < z0:
                e1.append(j)
                break
            else:
                pass
    elif y2 == y3 == y6 == y7:  # 判断是否在xz平面上
        x0 = (x2 + x3 + x6 + x7) / 4
        z0 = (z2 + z3 + z6 + z7) / 4
        for j in face5_coord.keys():
            if face5_coord[j][0] < x0 and face5_coord[j][2] < z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0] < x0 and face5_coord[j][2] > z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0] > x0 and face5_coord[j][2] > z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0] > x0 and face5_coord[j][2] < z0:
                e1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0 = (x2 + x3 + x6 + x7) / 4
        y0 = (y2 + y3 + y6 + y7) / 4
        for j in face5_coord.keys():
            if face5_coord[j][0] < x0 and face5_coord[j][1] < y0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0] < x0 and face5_coord[j][1] > y0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0] > x0 and face5_coord[j][1] > y0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0] > x0 and face5_coord[j][1] < y0:
                e1.append(j)
                break
            else:
                pass
    e = (e1[0], e1[1], e1[2], e1[3])

    f1 = []  # 给第6个面的节点按顺时针顺序编号，该面的节点为1458
    face6_coord = {n1: [x1, y1, z1], n4: [x4, y4, z4], n5: [x5, y5, z5], n8: [x8, y8, z8]}
    if x1 == x4 == x5 == x8:  # 先判断是否在yz平面上
        y0 = (y1 + y4 + y5 + y8) / 4
        z0 = (z1 + z4 + z5 + z8) / 4
        for j in face6_coord.keys():
            if face6_coord[j][1] < y0 and face6_coord[j][2] < z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][1] < y0 and face6_coord[j][2] > z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][1] > y0 and face6_coord[j][2] > z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][1] > y0 and face6_coord[j][2] < z0:
                f1.append(j)
                break
            else:
                pass
    elif y1 == y4 == y5 == y8:  # 判断是否在xz平面上
        x0 = (x1 + x4 + x5 + x8) / 4
        z0 = (z1 + z4 + z5 + z8) / 4
        for j in face6_coord.keys():
            if face6_coord[j][0] < x0 and face6_coord[j][2] < z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0] < x0 and face6_coord[j][2] > z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0] > x0 and face6_coord[j][2] > z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0] > x0 and face6_coord[j][2] < z0:
                f1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0 = (x1 + x4 + x5 + x8) / 4
        y0 = (y1 + y4 + y5 + y8) / 4
        for j in face6_coord.keys():
            if face6_coord[j][0] < x0 and face6_coord[j][1] < y0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0] < x0 and face6_coord[j][1] > y0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0] > x0 and face6_coord[j][1] > y0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0] > x0 and face6_coord[j][1] < y0:
                f1.append(j)
                break
            else:
                pass
    f = (f1[0], f1[1], f1[2], f1[3])

    AFACEINEL[k] = (a, b, c, d, e, f)  # 字典AFACEINEL中该单元对应的值为一个元组，即不可变的列表
    Aface_list.extend([a, b, c, d, e, f])

Aface_set = list(set(Aface_list))  # 所有A单元的所有面，不重复
A_count_pos = {}  # 键为Aface_set中的面，值为列表，里面依次是出现次数，各个面的在Aface_list中的索引位置
for i in Aface_set:
    A_count_pos[i] = [0]
k = -1  # 计数，记录Aface_list的索引位置
print('A单元重复次数获取进度为：')
for i in tqdm(Aface_list):
    k += 1
    A_count_pos[i][0] += 1
    A_count_pos[i].append(k)

# (7-2)确定AA单元的插入位置
AAloc_dic = {}  # 键为拟生成的AA单元的编号，值为其8个节点分别在两个单元中的索引位置，列表形式
print('AA单元位置获取进度为：')
for i in tqdm(A_count_pos.keys()):
    if A_count_pos[i][0] == 2:
        TEle_Value += 1
        ele1 = asp_ele[A_count_pos[i][1] // 6]  # 含重复面的第一个单元的编号
        ele2 = asp_ele[A_count_pos[i][2] // 6]
        FA1 = AFACEINEL[ele1][A_count_pos[i][1] % 6]
        FA2 = AFACEINEL[ele2][A_count_pos[i][2] % 6]
        loc1 = Element_dic[ele1].index(FA1[0])
        loc2 = Element_dic[ele1].index(FA1[1])
        loc3 = Element_dic[ele1].index(FA1[2])
        loc4 = Element_dic[ele1].index(FA1[3])
        loc5 = Element_dic[ele2].index(FA2[0])
        loc6 = Element_dic[ele2].index(FA2[1])
        loc7 = Element_dic[ele2].index(FA2[2])
        loc8 = Element_dic[ele2].index(FA2[3])
        AAloc_dic.update({TEle_Value: [ele1, ele2, loc1, loc2, loc3, loc4, loc5, loc6, loc7, loc8]})

step7_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step7：生成沥青部分的面的信息并确定AA单元的插入位置用时：', '%6f min' % ((step7_time - step6_time) / 60))
print('已累计用时：', '%6f min' % ((step7_time - star_time) / 60))

# step8:生成水泥部分的面的信息并确定CC单元的插入位置
# 包含第1步：生成水泥部分的面的信息，第2步：确定CC单元的插入位置
# (8-1)生成水泥部分的面的信息
CFACEINEL = {}  # 字典CFACEINEL，键为水泥部分的单元编号，值为元组，里面是6个面
Cface_list = []  # 所有单元的所有面都记录进来，重复记录
for k in cem_ele:  # 遍历所有水泥单元编号
    n1 = Element_dic[k][0]  # 节点编号
    n2 = Element_dic[k][1]
    n3 = Element_dic[k][2]
    n4 = Element_dic[k][3]
    n5 = Element_dic[k][4]
    n6 = Element_dic[k][5]
    n7 = Element_dic[k][6]
    n8 = Element_dic[k][7]
    x1 = Node_dic[n1][0]
    y1 = Node_dic[n1][1]
    z1 = Node_dic[n1][2]
    x2 = Node_dic[n2][0]
    y2 = Node_dic[n2][1]
    z2 = Node_dic[n2][2]
    x3 = Node_dic[n3][0]
    y3 = Node_dic[n3][1]
    z3 = Node_dic[n3][2]
    x4 = Node_dic[n4][0]
    y4 = Node_dic[n4][1]
    z4 = Node_dic[n4][2]
    x5 = Node_dic[n5][0]
    y5 = Node_dic[n5][1]
    z5 = Node_dic[n5][2]
    x6 = Node_dic[n6][0]
    y6 = Node_dic[n6][1]
    z6 = Node_dic[n6][2]
    x7 = Node_dic[n7][0]
    y7 = Node_dic[n7][1]
    z7 = Node_dic[n7][2]
    x8 = Node_dic[n8][0]
    y8 = Node_dic[n8][1]
    z8 = Node_dic[n8][2]

    a1 = []  # 给第1个面的节点按顺时针顺序编号，该面的节点为1234
    face1_coord = {n1: [x1, y1, z1], n2: [x2, y2, z2], n3: [x3, y3, z3], n4: [x4, y4, z4]}
    if x1 == x2 == x3 == x4:  # 先判断是否在yz平面上
        y0 = (y1 + y2 + y3 + y4) / 4
        z0 = (z1 + z2 + z3 + z4) / 4
        for j in face1_coord.keys():
            if face1_coord[j][1] < y0 and face1_coord[j][2] < z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][1] < y0 and face1_coord[j][2] > z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][1] > y0 and face1_coord[j][2] > z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][1] > y0 and face1_coord[j][2] < z0:
                a1.append(j)
                break
            else:
                pass
    elif y1 == y2 == y3 == y4:  # 判断是否在xz平面上
        x0 = (x1 + x2 + x3 + x4) / 4
        z0 = (z1 + z2 + z3 + z4) / 4
        for j in face1_coord.keys():
            if face1_coord[j][0] < x0 and face1_coord[j][2] < z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0] < x0 and face1_coord[j][2] > z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0] > x0 and face1_coord[j][2] > z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0] > x0 and face1_coord[j][2] < z0:
                a1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0 = (x1 + x2 + x3 + x4) / 4
        y0 = (y1 + y2 + y3 + y4) / 4
        for j in face1_coord.keys():
            if face1_coord[j][0] < x0 and face1_coord[j][1] < y0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0] < x0 and face1_coord[j][1] > y0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0] > x0 and face1_coord[j][1] > y0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0] > x0 and face1_coord[j][1] < y0:
                a1.append(j)
                break
            else:
                pass
    a = (a1[0], a1[1], a1[2], a1[3])

    b1 = []  # 给第2个面的节点按顺时针顺序编号，该面的节点为5678
    face2_coord = {n5: [x5, y5, z5], n6: [x6, y6, z6], n7: [x7, y7, z7], n8: [x8, y8, z8]}
    if x5 == x6 == x7 == x8:  # 先判断是否在yz平面上
        y0 = (y5 + y6 + y7 + y8) / 4
        z0 = (z5 + z6 + z7 + z8) / 4
        for j in face2_coord.keys():
            if face2_coord[j][1] < y0 and face2_coord[j][2] < z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][1] < y0 and face2_coord[j][2] > z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][1] > y0 and face2_coord[j][2] > z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][1] > y0 and face2_coord[j][2] < z0:
                b1.append(j)
                break
            else:
                pass
    elif y5 == y6 == y7 == y8:  # 判断是否在xz平面上
        x0 = (x5 + x6 + x7 + x8) / 4
        z0 = (z5 + z6 + z7 + z8) / 4
        for j in face2_coord.keys():
            if face2_coord[j][0] < x0 and face2_coord[j][2] < z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0] < x0 and face2_coord[j][2] > z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0] > x0 and face2_coord[j][2] > z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0] > x0 and face2_coord[j][2] < z0:
                b1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0 = (x5 + x6 + x7 + x8) / 4
        y0 = (y5 + y6 + y7 + y8) / 4
        for j in face2_coord.keys():
            if face2_coord[j][0] < x0 and face2_coord[j][1] < y0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0] < x0 and face2_coord[j][1] > y0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0] > x0 and face2_coord[j][1] > y0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0] > x0 and face2_coord[j][1] < y0:
                b1.append(j)
                break
            else:
                pass
    b = (b1[0], b1[1], b1[2], b1[3])

    c1 = []  # 给第3个面的节点按顺时针顺序编号，该面的节点为1256
    face3_coord = {n1: [x1, y1, z1], n2: [x2, y2, z2], n5: [x5, y5, z5], n6: [x6, y6, z6]}
    if x1 == x2 == x5 == x6:  # 先判断是否在yz平面上
        y0 = (y1 + y2 + y5 + y6) / 4
        z0 = (z1 + z2 + z5 + z6) / 4
        for j in face3_coord.keys():
            if face3_coord[j][1] < y0 and face3_coord[j][2] < z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][1] < y0 and face3_coord[j][2] > z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][1] > y0 and face3_coord[j][2] > z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][1] > y0 and face3_coord[j][2] < z0:
                c1.append(j)
                break
            else:
                pass
    elif y1 == y2 == y5 == y6:  # 判断是否在xz平面上
        x0 = (x1 + x2 + x5 + x6) / 4
        z0 = (z1 + z2 + z5 + z6) / 4
        for j in face3_coord.keys():
            if face3_coord[j][0] < x0 and face3_coord[j][2] < z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0] < x0 and face3_coord[j][2] > z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0] > x0 and face3_coord[j][2] > z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0] > x0 and face3_coord[j][2] < z0:
                c1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0 = (x1 + x2 + x5 + x6) / 4
        y0 = (y1 + y2 + y5 + y6) / 4
        for j in face3_coord.keys():
            if face3_coord[j][0] < x0 and face3_coord[j][1] < y0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0] < x0 and face3_coord[j][1] > y0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0] > x0 and face3_coord[j][1] > y0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0] > x0 and face3_coord[j][1] < y0:
                c1.append(j)
                break
            else:
                pass
    c = (c1[0], c1[1], c1[2], c1[3])

    d1 = []  # 给第4个面的节点按顺时针顺序编号，该面的节点为3478
    face4_coord = {n3: [x3, y3, z3], n4: [x4, y4, z4], n7: [x7, y7, z7], n8: [x8, y8, z8]}
    if x3 == x4 == x7 == x8:  # 先判断是否在yz平面上
        y0 = (y3 + y4 + y7 + y8) / 4
        z0 = (z3 + z4 + z7 + z8) / 4
        for j in face4_coord.keys():
            if face4_coord[j][1] < y0 and face4_coord[j][2] < z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][1] < y0 and face4_coord[j][2] > z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][1] > y0 and face4_coord[j][2] > z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][1] > y0 and face4_coord[j][2] < z0:
                d1.append(j)
                break
            else:
                pass
    elif y3 == y4 == y7 == y8:  # 判断是否在xz平面上
        x0 = (x3 + x4 + x7 + x8) / 4
        z0 = (z3 + z4 + z7 + z8) / 4
        for j in face4_coord.keys():
            if face4_coord[j][0] < x0 and face4_coord[j][2] < z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0] < x0 and face4_coord[j][2] > z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0] > x0 and face4_coord[j][2] > z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0] > x0 and face4_coord[j][2] < z0:
                d1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0 = (x3 + x4 + x7 + x8) / 4
        y0 = (y3 + y4 + y7 + y8) / 4
        for j in face4_coord.keys():
            if face4_coord[j][0] < x0 and face4_coord[j][1] < y0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0] < x0 and face4_coord[j][1] > y0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0] > x0 and face4_coord[j][1] > y0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0] > x0 and face4_coord[j][1] < y0:
                d1.append(j)
                break
            else:
                pass
    d = (d1[0], d1[1], d1[2], d1[3])

    e1 = []  # 给第5个面的节点按顺时针顺序编号，该面的节点为2367
    face5_coord = {n2: [x2, y2, z2], n3: [x3, y3, z3], n6: [x6, y6, z6], n7: [x7, y7, z7]}
    if x2 == x3 == x6 == x7:  # 先判断是否在yz平面上
        y0 = (y2 + y3 + y6 + y7) / 4
        z0 = (z2 + z3 + z6 + z7) / 4
        for j in face5_coord.keys():
            if face5_coord[j][1] < y0 and face5_coord[j][2] < z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][1] < y0 and face5_coord[j][2] > z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][1] > y0 and face5_coord[j][2] > z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][1] > y0 and face5_coord[j][2] < z0:
                e1.append(j)
                break
            else:
                pass
    elif y2 == y3 == y6 == y7:  # 判断是否在xz平面上
        x0 = (x2 + x3 + x6 + x7) / 4
        z0 = (z2 + z3 + z6 + z7) / 4
        for j in face5_coord.keys():
            if face5_coord[j][0] < x0 and face5_coord[j][2] < z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0] < x0 and face5_coord[j][2] > z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0] > x0 and face5_coord[j][2] > z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0] > x0 and face5_coord[j][2] < z0:
                e1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0 = (x2 + x3 + x6 + x7) / 4
        y0 = (y2 + y3 + y6 + y7) / 4
        for j in face5_coord.keys():
            if face5_coord[j][0] < x0 and face5_coord[j][1] < y0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0] < x0 and face5_coord[j][1] > y0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0] > x0 and face5_coord[j][1] > y0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0] > x0 and face5_coord[j][1] < y0:
                e1.append(j)
                break
            else:
                pass
    e = (e1[0], e1[1], e1[2], e1[3])

    f1 = []  # 给第6个面的节点按顺时针顺序编号，该面的节点为1458
    face6_coord = {n1: [x1, y1, z1], n4: [x4, y4, z4], n5: [x5, y5, z5], n8: [x8, y8, z8]}
    if x1 == x4 == x5 == x8:  # 先判断是否在yz平面上
        y0 = (y1 + y4 + y5 + y8) / 4
        z0 = (z1 + z4 + z5 + z8) / 4
        for j in face6_coord.keys():
            if face6_coord[j][1] < y0 and face6_coord[j][2] < z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][1] < y0 and face6_coord[j][2] > z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][1] > y0 and face6_coord[j][2] > z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][1] > y0 and face6_coord[j][2] < z0:
                f1.append(j)
                break
            else:
                pass
    elif y1 == y4 == y5 == y8:  # 判断是否在xz平面上
        x0 = (x1 + x4 + x5 + x8) / 4
        z0 = (z1 + z4 + z5 + z8) / 4
        for j in face6_coord.keys():
            if face6_coord[j][0] < x0 and face6_coord[j][2] < z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0] < x0 and face6_coord[j][2] > z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0] > x0 and face6_coord[j][2] > z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0] > x0 and face6_coord[j][2] < z0:
                f1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0 = (x1 + x4 + x5 + x8) / 4
        y0 = (y1 + y4 + y5 + y8) / 4
        for j in face6_coord.keys():
            if face6_coord[j][0] < x0 and face6_coord[j][1] < y0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0] < x0 and face6_coord[j][1] > y0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0] > x0 and face6_coord[j][1] > y0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0] > x0 and face6_coord[j][1] < y0:
                f1.append(j)
                break
            else:
                pass
    f = (f1[0], f1[1], f1[2], f1[3])

    CFACEINEL[k] = (a, b, c, d, e, f)  # 字典CFACEINEL中该单元对应的值为一个元组，即不可变的列表
    Cface_list.extend([a, b, c, d, e, f])

Cface_set = list(set(Cface_list))  # 所有C单元的所有面，不重复
C_count_pos = {}  # 键为Cface_set中的面，值为列表，里面依次是出现次数，各个面的在Cface_list中的索引位置
for i in Cface_set:
    C_count_pos[i] = [0]
k = -1  # 计数，记录Cface_list的索引位置
print('C单元重复次数获取进度为：')
for i in tqdm(Cface_list):
    k += 1
    C_count_pos[i][0] += 1
    C_count_pos[i].append(k)

# (8-2)确定CC单元的插入位置
CCloc_dic = {}  # 键为拟生成的CC单元的编号，值为其8个节点分别在两个单元中的索引位置，列表形式
print('CC单元位置获取进度为：')
for i in tqdm(C_count_pos.keys()):
    if C_count_pos[i][0] == 2:
        TEle_Value += 1
        ele1 = cem_ele[C_count_pos[i][1] // 6]  # 含重复面的第一个单元的编号
        ele2 = cem_ele[C_count_pos[i][2] // 6]
        FA1 = CFACEINEL[ele1][C_count_pos[i][1] % 6]
        FA2 = CFACEINEL[ele2][C_count_pos[i][2] % 6]
        loc1 = Element_dic[ele1].index(FA1[0])
        loc2 = Element_dic[ele1].index(FA1[1])
        loc3 = Element_dic[ele1].index(FA1[2])
        loc4 = Element_dic[ele1].index(FA1[3])
        loc5 = Element_dic[ele2].index(FA2[0])
        loc6 = Element_dic[ele2].index(FA2[1])
        loc7 = Element_dic[ele2].index(FA2[2])
        loc8 = Element_dic[ele2].index(FA2[3])
        CCloc_dic.update({TEle_Value: [ele1, ele2, loc1, loc2, loc3, loc4, loc5, loc6, loc7, loc8]})

step8_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step8：生成水泥部分的面的信息并确定CC单元的插入位置用时：', '%6f min' % ((step8_time - step7_time) / 60))
print('已累计用时：', '%6f min' % ((step8_time - star_time) / 60))

# step9:确定AC单元的插入位置
ACloc_dic = {}  # 键为拟生成的AC单元的编号，值为其8个节点分别在两个单元中的索引位置，列表形式
ACface_set = list(set(Aface_list) & set(Cface_list))
print('AC单元位置获取进度为：')
for i in tqdm(ACface_set):
    TEle_Value += 1
    ele1 = asp_ele[A_count_pos[i][1] // 6]
    ele2 = cem_ele[C_count_pos[i][1] // 6]
    FA1 = AFACEINEL[ele1][A_count_pos[i][1] % 6]
    FA2 = CFACEINEL[ele2][C_count_pos[i][1] % 6]
    loc1 = Element_dic[ele1].index(FA1[0])
    loc2 = Element_dic[ele1].index(FA1[1])
    loc3 = Element_dic[ele1].index(FA1[2])
    loc4 = Element_dic[ele1].index(FA1[3])
    loc5 = Element_dic[ele2].index(FA2[0])
    loc6 = Element_dic[ele2].index(FA2[1])
    loc7 = Element_dic[ele2].index(FA2[2])
    loc8 = Element_dic[ele2].index(FA2[3])
    ACloc_dic.update({TEle_Value: [ele1, ele2, loc1, loc2, loc3, loc4, loc5, loc6, loc7, loc8]})

step9_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step9：确定AC单元的插入位置用时：', '%6f min' % ((step9_time - step8_time) / 60))
print('已累计用时：', '%6f min' % ((step9_time - star_time) / 60))

# step10:生成集料部分的面的信息并确定AS单元的插入位置
# 包含第1步：生成集料部分的面的信息，第2步：确定AS单元的插入位置
# (10-1)生成集料部分的面的信息
SFACEINEL = {}  # 字典SFACEINEL，键为集料部分的单元编号，值为元组，里面是6个面
Sface_list = []  # 所有单元的所有面都记录进来，重复记录
for k in sto_ele:  # 遍历所有水泥单元编号
    n1 = Element_dic[k][0]  # 节点编号
    n2 = Element_dic[k][1]
    n3 = Element_dic[k][2]
    n4 = Element_dic[k][3]
    n5 = Element_dic[k][4]
    n6 = Element_dic[k][5]
    n7 = Element_dic[k][6]
    n8 = Element_dic[k][7]
    x1 = Node_dic[n1][0]
    y1 = Node_dic[n1][1]
    z1 = Node_dic[n1][2]
    x2 = Node_dic[n2][0]
    y2 = Node_dic[n2][1]
    z2 = Node_dic[n2][2]
    x3 = Node_dic[n3][0]
    y3 = Node_dic[n3][1]
    z3 = Node_dic[n3][2]
    x4 = Node_dic[n4][0]
    y4 = Node_dic[n4][1]
    z4 = Node_dic[n4][2]
    x5 = Node_dic[n5][0]
    y5 = Node_dic[n5][1]
    z5 = Node_dic[n5][2]
    x6 = Node_dic[n6][0]
    y6 = Node_dic[n6][1]
    z6 = Node_dic[n6][2]
    x7 = Node_dic[n7][0]
    y7 = Node_dic[n7][1]
    z7 = Node_dic[n7][2]
    x8 = Node_dic[n8][0]
    y8 = Node_dic[n8][1]
    z8 = Node_dic[n8][2]

    a1 = []  # 给第1个面的节点按顺时针顺序编号，该面的节点为1234
    face1_coord = {n1: [x1, y1, z1], n2: [x2, y2, z2], n3: [x3, y3, z3], n4: [x4, y4, z4]}
    if x1 == x2 == x3 == x4:  # 先判断是否在yz平面上
        y0 = (y1 + y2 + y3 + y4) / 4
        z0 = (z1 + z2 + z3 + z4) / 4
        for j in face1_coord.keys():
            if face1_coord[j][1] < y0 and face1_coord[j][2] < z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][1] < y0 and face1_coord[j][2] > z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][1] > y0 and face1_coord[j][2] > z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][1] > y0 and face1_coord[j][2] < z0:
                a1.append(j)
                break
            else:
                pass
    elif y1 == y2 == y3 == y4:  # 判断是否在xz平面上
        x0 = (x1 + x2 + x3 + x4) / 4
        z0 = (z1 + z2 + z3 + z4) / 4
        for j in face1_coord.keys():
            if face1_coord[j][0] < x0 and face1_coord[j][2] < z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0] < x0 and face1_coord[j][2] > z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0] > x0 and face1_coord[j][2] > z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0] > x0 and face1_coord[j][2] < z0:
                a1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0 = (x1 + x2 + x3 + x4) / 4
        y0 = (y1 + y2 + y3 + y4) / 4
        for j in face1_coord.keys():
            if face1_coord[j][0] < x0 and face1_coord[j][1] < y0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0] < x0 and face1_coord[j][1] > y0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0] > x0 and face1_coord[j][1] > y0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0] > x0 and face1_coord[j][1] < y0:
                a1.append(j)
                break
            else:
                pass
    a = (a1[0], a1[1], a1[2], a1[3])

    b1 = []  # 给第2个面的节点按顺时针顺序编号，该面的节点为5678
    face2_coord = {n5: [x5, y5, z5], n6: [x6, y6, z6], n7: [x7, y7, z7], n8: [x8, y8, z8]}
    if x5 == x6 == x7 == x8:  # 先判断是否在yz平面上
        y0 = (y5 + y6 + y7 + y8) / 4
        z0 = (z5 + z6 + z7 + z8) / 4
        for j in face2_coord.keys():
            if face2_coord[j][1] < y0 and face2_coord[j][2] < z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][1] < y0 and face2_coord[j][2] > z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][1] > y0 and face2_coord[j][2] > z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][1] > y0 and face2_coord[j][2] < z0:
                b1.append(j)
                break
            else:
                pass
    elif y5 == y6 == y7 == y8:  # 判断是否在xz平面上
        x0 = (x5 + x6 + x7 + x8) / 4
        z0 = (z5 + z6 + z7 + z8) / 4
        for j in face2_coord.keys():
            if face2_coord[j][0] < x0 and face2_coord[j][2] < z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0] < x0 and face2_coord[j][2] > z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0] > x0 and face2_coord[j][2] > z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0] > x0 and face2_coord[j][2] < z0:
                b1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0 = (x5 + x6 + x7 + x8) / 4
        y0 = (y5 + y6 + y7 + y8) / 4
        for j in face2_coord.keys():
            if face2_coord[j][0] < x0 and face2_coord[j][1] < y0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0] < x0 and face2_coord[j][1] > y0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0] > x0 and face2_coord[j][1] > y0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0] > x0 and face2_coord[j][1] < y0:
                b1.append(j)
                break
            else:
                pass
    b = (b1[0], b1[1], b1[2], b1[3])

    c1 = []  # 给第3个面的节点按顺时针顺序编号，该面的节点为1256
    face3_coord = {n1: [x1, y1, z1], n2: [x2, y2, z2], n5: [x5, y5, z5], n6: [x6, y6, z6]}
    if x1 == x2 == x5 == x6:  # 先判断是否在yz平面上
        y0 = (y1 + y2 + y5 + y6) / 4
        z0 = (z1 + z2 + z5 + z6) / 4
        for j in face3_coord.keys():
            if face3_coord[j][1] < y0 and face3_coord[j][2] < z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][1] < y0 and face3_coord[j][2] > z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][1] > y0 and face3_coord[j][2] > z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][1] > y0 and face3_coord[j][2] < z0:
                c1.append(j)
                break
            else:
                pass
    elif y1 == y2 == y5 == y6:  # 判断是否在xz平面上
        x0 = (x1 + x2 + x5 + x6) / 4
        z0 = (z1 + z2 + z5 + z6) / 4
        for j in face3_coord.keys():
            if face3_coord[j][0] < x0 and face3_coord[j][2] < z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0] < x0 and face3_coord[j][2] > z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0] > x0 and face3_coord[j][2] > z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0] > x0 and face3_coord[j][2] < z0:
                c1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0 = (x1 + x2 + x5 + x6) / 4
        y0 = (y1 + y2 + y5 + y6) / 4
        for j in face3_coord.keys():
            if face3_coord[j][0] < x0 and face3_coord[j][1] < y0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0] < x0 and face3_coord[j][1] > y0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0] > x0 and face3_coord[j][1] > y0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0] > x0 and face3_coord[j][1] < y0:
                c1.append(j)
                break
            else:
                pass
    c = (c1[0], c1[1], c1[2], c1[3])

    d1 = []  # 给第4个面的节点按顺时针顺序编号，该面的节点为3478
    face4_coord = {n3: [x3, y3, z3], n4: [x4, y4, z4], n7: [x7, y7, z7], n8: [x8, y8, z8]}
    if x3 == x4 == x7 == x8:  # 先判断是否在yz平面上
        y0 = (y3 + y4 + y7 + y8) / 4
        z0 = (z3 + z4 + z7 + z8) / 4
        for j in face4_coord.keys():
            if face4_coord[j][1] < y0 and face4_coord[j][2] < z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][1] < y0 and face4_coord[j][2] > z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][1] > y0 and face4_coord[j][2] > z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][1] > y0 and face4_coord[j][2] < z0:
                d1.append(j)
                break
            else:
                pass
    elif y3 == y4 == y7 == y8:  # 判断是否在xz平面上
        x0 = (x3 + x4 + x7 + x8) / 4
        z0 = (z3 + z4 + z7 + z8) / 4
        for j in face4_coord.keys():
            if face4_coord[j][0] < x0 and face4_coord[j][2] < z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0] < x0 and face4_coord[j][2] > z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0] > x0 and face4_coord[j][2] > z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0] > x0 and face4_coord[j][2] < z0:
                d1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0 = (x3 + x4 + x7 + x8) / 4
        y0 = (y3 + y4 + y7 + y8) / 4
        for j in face4_coord.keys():
            if face4_coord[j][0] < x0 and face4_coord[j][1] < y0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0] < x0 and face4_coord[j][1] > y0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0] > x0 and face4_coord[j][1] > y0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0] > x0 and face4_coord[j][1] < y0:
                d1.append(j)
                break
            else:
                pass
    d = (d1[0], d1[1], d1[2], d1[3])

    e1 = []  # 给第5个面的节点按顺时针顺序编号，该面的节点为2367
    face5_coord = {n2: [x2, y2, z2], n3: [x3, y3, z3], n6: [x6, y6, z6], n7: [x7, y7, z7]}
    if x2 == x3 == x6 == x7:  # 先判断是否在yz平面上
        y0 = (y2 + y3 + y6 + y7) / 4
        z0 = (z2 + z3 + z6 + z7) / 4
        for j in face5_coord.keys():
            if face5_coord[j][1] < y0 and face5_coord[j][2] < z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][1] < y0 and face5_coord[j][2] > z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][1] > y0 and face5_coord[j][2] > z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][1] > y0 and face5_coord[j][2] < z0:
                e1.append(j)
                break
            else:
                pass
    elif y2 == y3 == y6 == y7:  # 判断是否在xz平面上
        x0 = (x2 + x3 + x6 + x7) / 4
        z0 = (z2 + z3 + z6 + z7) / 4
        for j in face5_coord.keys():
            if face5_coord[j][0] < x0 and face5_coord[j][2] < z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0] < x0 and face5_coord[j][2] > z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0] > x0 and face5_coord[j][2] > z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0] > x0 and face5_coord[j][2] < z0:
                e1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0 = (x2 + x3 + x6 + x7) / 4
        y0 = (y2 + y3 + y6 + y7) / 4
        for j in face5_coord.keys():
            if face5_coord[j][0] < x0 and face5_coord[j][1] < y0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0] < x0 and face5_coord[j][1] > y0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0] > x0 and face5_coord[j][1] > y0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0] > x0 and face5_coord[j][1] < y0:
                e1.append(j)
                break
            else:
                pass
    e = (e1[0], e1[1], e1[2], e1[3])

    f1 = []  # 给第6个面的节点按顺时针顺序编号，该面的节点为1458
    face6_coord = {n1: [x1, y1, z1], n4: [x4, y4, z4], n5: [x5, y5, z5], n8: [x8, y8, z8]}
    if x1 == x4 == x5 == x8:  # 先判断是否在yz平面上
        y0 = (y1 + y4 + y5 + y8) / 4
        z0 = (z1 + z4 + z5 + z8) / 4
        for j in face6_coord.keys():
            if face6_coord[j][1] < y0 and face6_coord[j][2] < z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][1] < y0 and face6_coord[j][2] > z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][1] > y0 and face6_coord[j][2] > z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][1] > y0 and face6_coord[j][2] < z0:
                f1.append(j)
                break
            else:
                pass
    elif y1 == y4 == y5 == y8:  # 判断是否在xz平面上
        x0 = (x1 + x4 + x5 + x8) / 4
        z0 = (z1 + z4 + z5 + z8) / 4
        for j in face6_coord.keys():
            if face6_coord[j][0] < x0 and face6_coord[j][2] < z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0] < x0 and face6_coord[j][2] > z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0] > x0 and face6_coord[j][2] > z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0] > x0 and face6_coord[j][2] < z0:
                f1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0 = (x1 + x4 + x5 + x8) / 4
        y0 = (y1 + y4 + y5 + y8) / 4
        for j in face6_coord.keys():
            if face6_coord[j][0] < x0 and face6_coord[j][1] < y0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0] < x0 and face6_coord[j][1] > y0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0] > x0 and face6_coord[j][1] > y0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0] > x0 and face6_coord[j][1] < y0:
                f1.append(j)
                break
            else:
                pass
    f = (f1[0], f1[1], f1[2], f1[3])

    SFACEINEL[k] = (a, b, c, d, e, f)  # 字典SFACEINEL中该单元对应的值为一个元组，即不可变的列表
    Sface_list.extend([a, b, c, d, e, f])

Sface_set = list(set(Sface_list))  # 所有S单元的所有面，不重复
S_count_pos = {}  # 键为Sface_set中的面，值为列表，里面依次是出现次数，各个面的在Sface_list中的索引位置
for i in Sface_set:
    S_count_pos[i] = [0]
k = -1  # 计数，记录Cface_list的索引位置
print('S单元重复次数获取进度为：')
for i in tqdm(Sface_list):
    k += 1
    S_count_pos[i][0] += 1
    S_count_pos[i].append(k)

# (10-2)确定AS单元的插入位置
ASloc_dic = {}  # 键为拟生成的AS单元的编号，值为其8个节点分别在两个单元中的索引位置，列表形式
ASface_set = list(set(Aface_list) & set(Sface_list))
print('AS单元位置获取进度为：')
for i in tqdm(ASface_set):
    TEle_Value += 1
    ele1 = asp_ele[A_count_pos[i][1] // 6]
    ele2 = sto_ele[S_count_pos[i][1] // 6]
    FA1 = AFACEINEL[ele1][A_count_pos[i][1] % 6]
    FA2 = SFACEINEL[ele2][S_count_pos[i][1] % 6]
    loc1 = Element_dic[ele1].index(FA1[0])
    loc2 = Element_dic[ele1].index(FA1[1])
    loc3 = Element_dic[ele1].index(FA1[2])
    loc4 = Element_dic[ele1].index(FA1[3])
    loc5 = Element_dic[ele2].index(FA2[0])
    loc6 = Element_dic[ele2].index(FA2[1])
    loc7 = Element_dic[ele2].index(FA2[2])
    loc8 = Element_dic[ele2].index(FA2[3])
    ASloc_dic.update({TEle_Value: [ele1, ele2, loc1, loc2, loc3, loc4, loc5, loc6, loc7, loc8]})

step10_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step10：生成集料部分的面的信息并确定AS单元的插入位置用时：', '%6f min' % ((step10_time - step9_time) / 60))
print('已累计用时：', '%6f min' % ((step10_time - star_time) / 60))

# step11：确定CS单元的插入位置
CSloc_dic = {}  # 键为拟生成的CS单元的编号，值为其8个节点分别在两个单元中的索引位置，列表形式
CSface_set = list(set(Cface_list) & set(Sface_list))
print('CS单元位置获取进度为：')
for i in tqdm(CSface_set):
    TEle_Value += 1
    ele1 = cem_ele[C_count_pos[i][1] // 6]
    ele2 = sto_ele[S_count_pos[i][1] // 6]
    FA1 = CFACEINEL[ele1][C_count_pos[i][1] % 6]
    FA2 = SFACEINEL[ele2][S_count_pos[i][1] % 6]
    loc1 = Element_dic[ele1].index(FA1[0])
    loc2 = Element_dic[ele1].index(FA1[1])
    loc3 = Element_dic[ele1].index(FA1[2])
    loc4 = Element_dic[ele1].index(FA1[3])
    loc5 = Element_dic[ele2].index(FA2[0])
    loc6 = Element_dic[ele2].index(FA2[1])
    loc7 = Element_dic[ele2].index(FA2[2])
    loc8 = Element_dic[ele2].index(FA2[3])
    CSloc_dic.update({TEle_Value: [ele1, ele2, loc1, loc2, loc3, loc4, loc5, loc6, loc7, loc8]})

step11_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step11：确定CS单元的插入位置用时：', '%6f min' % ((step11_time - step10_time) / 60))
print('已累计用时：', '%6f min' % ((step11_time - star_time) / 60))

# step12：寻找沥青材料内部重复出现的节点并统计其出现次数，再生成新的节点赋予编号较大的单元，使所有单元均不会共节点
# 包含第1步：寻找沥青材料内部重复出现的节点并统计其出现次数，第2步：生成新的节点赋予编号较大的单元，使所有沥青单元均不会共节点
# (12-1)寻找沥青材料内部重复出现的节点并统计其出现次数
CO_ANODE = []  # 列表CO_ANODE里面是沥青单元对应的节点编号，直接写在一个大列表CO_ANODE里
ANODECO_DIC = {}  # 字典ANODECO_DIC，键为节点编号，值为一个列表，里面依次是该节点在沥青内部出现的次数，每次出现在CO_ANODE中的索引号
ANODECO = []  # 储存沥青内部重复出现的节点编号
for i in asp_ele:
    CO_ANODE.extend(Element_dic[i])
CO_ANODE_SET = sorted(set(CO_ANODE))  # 节点集，除去重复节点
for i in CO_ANODE_SET:
    ANODECO_DIC[i] = [0]
k = -1  # 计数
for i in CO_ANODE:
    k += 1
    ANODECO_DIC[i][0] += 1
    ANODECO_DIC[i].append(k)

for i in ANODECO_DIC.keys():
    if ANODECO_DIC[i][0] > 1:
        ANODECO.append(i)
    else:
        pass

# (12-2)生成新的节点赋予编号较大的单元，使所有沥青单元均不会共节点
print('沥青内部节点分裂进度为：')
for i in tqdm(ANODECO_DIC.keys()):
    if ANODECO_DIC[i][0] > 1:
        EL_RE = []  # 列表EL_RE，记录节点i所在的所有单元
        for j in range(1, len(ANODECO_DIC[i])):
            EL = asp_ele[ANODECO_DIC[i][j] // 8]
            EL_RE.append(EL)
        EL_RE.sort()  # 对列表进行排序，里面是重复出现的节点所在的单元
        for LS in range(len(EL_RE) - 1):  # 遍历节点i所在的所有单元，编号从小到大
            TNode_Value += 1  # 新产生的节点的编号
            Node_dic.update({TNode_Value: Node_dic[i]})  # 新生成的节点添加到统一的节点字典里
            Loc = Element_dic[EL_RE[LS + 1]].index(i)  # 节点i在该单元中的索引位置，便于下面将其替换为新生成的节点
            Element_dic[EL_RE[LS + 1]][Loc] = TNode_Value

step12_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step12：寻找沥青内部重复节点并统计次数，再生成新节点用时：', '%6f min' % ((step12_time - step11_time) / 60))
print('已累计用时：', '%6f min' % ((step12_time - star_time) / 60))

# step13：寻找水泥材料内部重复出现的节点并统计其出现次数，再生成新的节点赋予编号较大的单元，使所有单元均不会共节点
# 包含第1步：寻找水泥材料内部重复出现的节点并统计其出现次数，第2步：生成新的节点赋予编号较大的单元，使所有水泥单元均不会共节点
# (13-1)寻找水泥材料内部重复出现的节点并统计其出现次数
CO_CNODE = []  # 列表CO_CNODE里面是水泥单元对应的节点编号，直接写在一个大列表CO_CNODE里
CNODECO_DIC = {}  # 字典CNODECO_DIC，键为节点编号，值为一个列表，里面依次是该节点在水泥内部出现的次数，每次出现在CO_CNODE中的索引号
CNODECO = []  # 储存水泥内部重复出现的节点编号
for i in cem_ele:
    CO_CNODE.extend(Element_dic[i])
CO_CNODE_SET = sorted(set(CO_CNODE))  # 节点集，除去重复节点
for i in CO_CNODE_SET:
    CNODECO_DIC[i] = [0]
k = -1  # 计数
for i in CO_CNODE:
    k += 1
    CNODECO_DIC[i][0] += 1
    CNODECO_DIC[i].append(k)

for i in CNODECO_DIC.keys():
    if CNODECO_DIC[i][0] > 1:
        CNODECO.append(i)
    else:
        pass

# (13-2)生成新的节点赋予编号较大的单元，使所有水泥单元均不会共节点
print('水泥内部节点分裂进度为：')
for i in tqdm(CNODECO_DIC.keys()):
    if CNODECO_DIC[i][0] > 1:
        EL_RE = []  # 列表EL_RE，记录节点i所在的所有单元
        for j in range(1, len(CNODECO_DIC[i])):
            EL = cem_ele[CNODECO_DIC[i][j] // 8]
            EL_RE.append(EL)
        EL_RE.sort()  # 对列表进行排序，里面是重复出现的节点所在的单元
        for LS in range(len(EL_RE) - 1):  # 遍历节点i所在的所有单元，编号从小到大
            TNode_Value += 1  # 新产生的节点的编号
            Node_dic.update({TNode_Value: Node_dic[i]})  # 新生成的节点添加到统一的节点字典里
            Loc = Element_dic[EL_RE[LS + 1]].index(i)  # 节点i在该单元中的索引位置，便于下面将其替换为新生成的节点
            Element_dic[EL_RE[LS + 1]][Loc] = TNode_Value

step13_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step13：寻找水泥内部重复节点并统计次数，再生成新节点用时：', '%6f min' % ((step13_time - step12_time) / 60))
print('已累计用时：', '%6f min' % ((step13_time - star_time) / 60))

# step14:寻找沥青水泥界面重复出现的节点，再生成新的节点赋予与水泥共节点的沥青单元，使水泥与沥青不共节点
# 包含第1步：寻找沥青水泥界面重复出现的节点，第2步：生成新的节点赋予与水泥共节点的沥青单元，使水泥与沥青不共节点
# (14-1)寻找沥青水泥界面重复出现的节点
CO_ANODE = []  # 列表CO_ANODE里面是沥青单元对应的节点编号，直接写在一个大列表CO_ANODE里
for i in asp_ele:
    CO_ANODE.extend(Element_dic[i])
CO_ANODE_SET = set(CO_ANODE)  # 节点集，除去重复节点并排序

CO_CNODE = []  # 列表CO_CNODE里面是水泥单元对应的节点编号，直接写在一个大列表CO_CNODE里
for i in cem_ele:
    CO_CNODE.extend(Element_dic[i])
CO_CNODE_SET = set(CO_CNODE)  # 水泥节点集，除去重复节点并排序

ACNODECO = sorted(set(CO_ANODE_SET) & set(CO_CNODE_SET))  # 同时在水泥和沥青出现的节点编号

ACNODECO_DIC = {}  # 字典ACNODECO_DIC，键为沥青节点编号，值为一个列表，里面依次是该节点在沥青内部出现的次数，每次出现在CO_ANODE中的索引号
k = -1  # 计数
for i in CO_ANODE:
    k += 1
    ACNODECO_DIC[i] = [1]
    ACNODECO_DIC[i].append(k)

# (14-2)生成新的节点赋予与水泥共节点的沥青单元，使水泥与沥青不共节点
print('沥青水泥界面节点分裂进度为：')
for i in tqdm(ACNODECO):  # 对于同时在沥青和水泥出现的节点的编号i
    EL = asp_ele[ACNODECO_DIC[i][1] // 8]
    TNode_Value += 1  # 新产生的节点的编号
    Node_dic.update({TNode_Value: Node_dic[i]})  # 新生成的节点添加到统一的节点字典里并且初始坐标与原节点相同
    Loc = Element_dic[EL].index(i)  # 节点i在该单元中的索引位置，便于下面将其替换为新生成的节点
    Element_dic[EL][Loc] = TNode_Value

step14_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step14：寻找沥青水泥边界的重复节点并统计次数，再生成新节点用时：', '%6f min' % ((step14_time - step13_time) / 60))
print('已累计用时：', '%6f min' % ((step14_time - star_time) / 60))

# step15:寻找沥青集料界面重复出现的节点，再生成新的节点赋予与集料共节点的沥青单元，使集料与沥青不共节点
# 包含第1步：寻找沥青集料界面重复出现的节点，第2步：生成新的节点赋予与集料共节点的沥青单元，使集料与沥青不共节点
# (15-1)寻找沥青集料界面重复出现的节点
CO_ANODE = []  # 列表CO_ANODE里面是沥青单元对应的节点编号，直接写在一个大列表CO_ANODE里
for i in asp_ele:
    CO_ANODE.extend(Element_dic[i])
CO_ANODE_SET = set(CO_ANODE)  # 节点集，除去重复节点并排序

CO_SNODE = []  # 列表CO_SNODE里面是集料单元对应的节点编号，直接写在一个大列表CO_SNODE里
for i in sto_ele:
    CO_SNODE.extend(Element_dic[i])
CO_SNODE_SET = set(CO_SNODE)  # 集料节点集，除去重复节点并排序

ASNODECO = sorted(set(CO_ANODE_SET) & set(CO_SNODE_SET))  # 同时在集料和沥青出现的节点编号

ASNODECO_DIC = {}  # 字典ASNODECO_DIC，键为沥青节点编号，值为一个列表，里面依次是该节点在沥青内部出现的次数，每次出现在CO_ANODE中的索引号
k = -1  # 计数
for i in CO_ANODE:
    k += 1
    ASNODECO_DIC[i] = [1]
    ASNODECO_DIC[i].append(k)

# (15-2)生成新的节点赋予与集料共节点的沥青单元，使集料与沥青不共节点
print('沥青集料界面节点分裂进度为：')
for i in tqdm(ASNODECO):  # 对于同时在沥青和水泥出现的节点的编号i
    EL = asp_ele[ASNODECO_DIC[i][1] // 8]
    TNode_Value += 1  # 新产生的节点的编号
    Node_dic.update({TNode_Value: Node_dic[i]})  # 新生成的节点添加到统一的节点字典里并且初始坐标与原节点相同
    Loc = Element_dic[EL].index(i)  # 节点i在该单元中的索引位置，便于下面将其替换为新生成的节点
    Element_dic[EL][Loc] = TNode_Value

step15_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step15：寻找沥青集料边界的重复节点并统计次数，再生成新节点用时：', '%6f min' % ((step15_time - step14_time) / 60))
print('已累计用时：', '%6f min' % ((step15_time - star_time) / 60))

# step16:寻找水泥集料界面重复出现的节点，再生成新的节点赋予与集料共节点的水泥单元，使集料与水泥不共节点
# 包含第1步：寻找水泥集料界面重复出现的节点，第2步：生成新的节点赋予与集料共节点的水泥单元，使集料与水泥不共节点
# (16-1)寻找水泥集料界面重复出现的节点
CO_CNODE = []  # 列表CO_CNODE里面是水泥单元对应的节点编号，直接写在一个大列表CO_CNODE里
for i in cem_ele:
    CO_CNODE.extend(Element_dic[i])
CO_CNODE_SET = set(CO_CNODE)  # 节点集，除去重复节点并排序

CO_SNODE = []  # 列表CO_SNODE里面是集料单元对应的节点编号，直接写在一个大列表CO_SNODE里
for i in sto_ele:
    CO_SNODE.extend(Element_dic[i])
CO_SNODE_SET = set(CO_SNODE)  # 集料节点集，除去重复节点并排序

CSNODECO = sorted(set(CO_CNODE_SET) & set(CO_SNODE_SET))  # 同时在集料和水泥出现的节点编号

CSNODECO_DIC = {}  # 字典CSNODECO_DIC，键为水泥节点编号，值为一个列表，里面依次是该节点在水泥内部出现的次数，每次出现在CO_CNODE中的索引号
k = -1  # 计数
for i in CO_CNODE:
    k += 1
    CSNODECO_DIC[i] = [1]
    CSNODECO_DIC[i].append(k)

# (16-2)生成新的节点赋予与集料共节点的水泥单元，使集料与水泥不共节点
print('水泥集料界面节点分裂进度为：')
for i in tqdm(CSNODECO):  # 对于同时在水泥和集料出现的节点的编号i
    EL = cem_ele[CSNODECO_DIC[i][1] // 8]
    TNode_Value += 1  # 新产生的节点的编号
    Node_dic.update({TNode_Value: Node_dic[i]})  # 新生成的节点添加到统一的节点字典里并且初始坐标与原节点相同
    Loc = Element_dic[EL].index(i)  # 节点i在该单元中的索引位置，便于下面将其替换为新生成的节点
    Element_dic[EL][Loc] = TNode_Value

step16_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step16：寻找水泥集料边界的重复节点并统计次数，再生成新节点用时：', '%6f min' % ((step16_time - step15_time) / 60))
print('已累计用时：', '%6f min' % ((step16_time - star_time) / 60))

# step17:插入内聚力单元
# 包含第1步：插入AA单元，第2步：插入CC单元，第3步：插入AC单元，第4步：插入AS单元，第5步：插入CS单元
# (17-1)插入AA单元
AAnum1 = TEle_Value1 + 1
for i in AAloc_dic.keys():
    NODE1 = Element_dic[AAloc_dic[i][0]][AAloc_dic[i][2]]
    NODE2 = Element_dic[AAloc_dic[i][0]][AAloc_dic[i][3]]
    NODE3 = Element_dic[AAloc_dic[i][0]][AAloc_dic[i][4]]
    NODE4 = Element_dic[AAloc_dic[i][0]][AAloc_dic[i][5]]
    NODE5 = Element_dic[AAloc_dic[i][1]][AAloc_dic[i][6]]
    NODE6 = Element_dic[AAloc_dic[i][1]][AAloc_dic[i][7]]
    NODE7 = Element_dic[AAloc_dic[i][1]][AAloc_dic[i][8]]
    NODE8 = Element_dic[AAloc_dic[i][1]][AAloc_dic[i][9]]
    Element_dic.update({i: [NODE1, NODE2, NODE3, NODE4, NODE5, NODE6, NODE7, NODE8]})

AAnum2 = max(Element_dic.keys())  # AA单元中编号最大的单元编号
AA_SET = range(AAnum1, AAnum2 + 1)  # 列表，里面是所有AA单元的编号

# (17-2)插入CC单元
CCnum1 = max(Element_dic.keys()) + 1
for i in CCloc_dic.keys():
    NODE1 = Element_dic[CCloc_dic[i][0]][CCloc_dic[i][2]]
    NODE2 = Element_dic[CCloc_dic[i][0]][CCloc_dic[i][3]]
    NODE3 = Element_dic[CCloc_dic[i][0]][CCloc_dic[i][4]]
    NODE4 = Element_dic[CCloc_dic[i][0]][CCloc_dic[i][5]]
    NODE5 = Element_dic[CCloc_dic[i][1]][CCloc_dic[i][6]]
    NODE6 = Element_dic[CCloc_dic[i][1]][CCloc_dic[i][7]]
    NODE7 = Element_dic[CCloc_dic[i][1]][CCloc_dic[i][8]]
    NODE8 = Element_dic[CCloc_dic[i][1]][CCloc_dic[i][9]]
    Element_dic.update({i: [NODE1, NODE2, NODE3, NODE4, NODE5, NODE6, NODE7, NODE8]})

CCnum2 = max(Element_dic.keys())  # CC单元中编号最大的单元编号
CC_SET = range(CCnum1, CCnum2 + 1)  # 列表，里面是所有CC单元的编号

# (17-3)插入AC单元
ACnum1 = max(Element_dic.keys()) + 1
for i in ACloc_dic.keys():
    NODE1 = Element_dic[ACloc_dic[i][0]][ACloc_dic[i][2]]
    NODE2 = Element_dic[ACloc_dic[i][0]][ACloc_dic[i][3]]
    NODE3 = Element_dic[ACloc_dic[i][0]][ACloc_dic[i][4]]
    NODE4 = Element_dic[ACloc_dic[i][0]][ACloc_dic[i][5]]
    NODE5 = Element_dic[ACloc_dic[i][1]][ACloc_dic[i][6]]
    NODE6 = Element_dic[ACloc_dic[i][1]][ACloc_dic[i][7]]
    NODE7 = Element_dic[ACloc_dic[i][1]][ACloc_dic[i][8]]
    NODE8 = Element_dic[ACloc_dic[i][1]][ACloc_dic[i][9]]
    Element_dic.update({i: [NODE1, NODE2, NODE3, NODE4, NODE5, NODE6, NODE7, NODE8]})

ACnum2 = max(Element_dic.keys())  # AC单元中编号最大的单元编号
AC_SET = range(ACnum1, ACnum2 + 1)  # 列表，里面是所有AC单元的编号

# (17-4)插入AS单元
ASnum1 = max(Element_dic.keys()) + 1
for i in ASloc_dic.keys():
    NODE1 = Element_dic[ASloc_dic[i][0]][ASloc_dic[i][2]]
    NODE2 = Element_dic[ASloc_dic[i][0]][ASloc_dic[i][3]]
    NODE3 = Element_dic[ASloc_dic[i][0]][ASloc_dic[i][4]]
    NODE4 = Element_dic[ASloc_dic[i][0]][ASloc_dic[i][5]]
    NODE5 = Element_dic[ASloc_dic[i][1]][ASloc_dic[i][6]]
    NODE6 = Element_dic[ASloc_dic[i][1]][ASloc_dic[i][7]]
    NODE7 = Element_dic[ASloc_dic[i][1]][ASloc_dic[i][8]]
    NODE8 = Element_dic[ASloc_dic[i][1]][ASloc_dic[i][9]]
    Element_dic.update({i: [NODE1, NODE2, NODE3, NODE4, NODE5, NODE6, NODE7, NODE8]})

ASnum2 = max(Element_dic.keys())  # AS单元中编号最大的单元编号
AS_SET = range(ASnum1, ASnum2 + 1)  # 列表，里面是所有AS单元的编号

# (17-5)插入CS单元
CSnum1 = max(Element_dic.keys()) + 1
for i in CSloc_dic.keys():
    NODE1 = Element_dic[CSloc_dic[i][0]][CSloc_dic[i][2]]
    NODE2 = Element_dic[CSloc_dic[i][0]][CSloc_dic[i][3]]
    NODE3 = Element_dic[CSloc_dic[i][0]][CSloc_dic[i][4]]
    NODE4 = Element_dic[CSloc_dic[i][0]][CSloc_dic[i][5]]
    NODE5 = Element_dic[CSloc_dic[i][1]][CSloc_dic[i][6]]
    NODE6 = Element_dic[CSloc_dic[i][1]][CSloc_dic[i][7]]
    NODE7 = Element_dic[CSloc_dic[i][1]][CSloc_dic[i][8]]
    NODE8 = Element_dic[CSloc_dic[i][1]][CSloc_dic[i][9]]
    Element_dic.update({i: [NODE1, NODE2, NODE3, NODE4, NODE5, NODE6, NODE7, NODE8]})

CSnum2 = max(Element_dic.keys())  # CS单元中编号最大的单元编号
CS_SET = range(CSnum1, CSnum2 + 1)  # 列表，里面是所有CS单元的编号

step17_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step17：插入内聚力单元用时：', '%6f min' % ((step17_time - step16_time) / 60))
print('已累计用时：', '%6f min' % ((step17_time - star_time) / 60))

TEle_Value2 = max(Element_dic.keys())
print('模型插入内聚力单元后的单元总数为：', TEle_Value2)

# step18:生成新的inp文件
val_ele = sorted(asp_ele + sto_ele + cem_ele)
val_nod = []
for i in val_ele:
    val_nod.extend(Element_dic[i])
val_nod = sorted(set(val_nod))
# 文件头的书写
Heading = []
Heading.append('*Heading')
Heading.append('** Job name: cohesive Model name: Model-3')
Heading.append('** Generated by: Abaqus/CAE 2020')
Heading.append('*Preprint, echo=NO, model=NO, history=NO, contact=NO')
Heading.append('**')
Heading.append('**PARTS')
Heading.append('**')
Heading.append('*Part, name=cohesive')
Heading.append('*Node')
# Part相关节点及单元信息写入
# NODE
for i in range(len(Heading)):
    print(Heading[i], file=outfile)
# 字典按照keys大小排
for NO in val_nod:
    print("%9d, %9f, %9f, %9f" % (NO, Node_dic[NO][0], Node_dic[NO][1], Node_dic[NO][2]), file=outfile)
print('\n', file=outfile)

# ELement首先判断单元的类型
CO_TYPE = "*Element, type=C3D8R"
print(CO_TYPE, file=outfile)
for EL in val_ele:
    print(
        "%5d, %5d, %5d, %5d, %5d, %5d, %5d, %5d, %5d" % (EL, Element_dic[EL][0], Element_dic[EL][1],Element_dic[EL][2],
                                                         Element_dic[EL][3], Element_dic[EL][4], Element_dic[EL][5],
                                                         Element_dic[EL][6], Element_dic[EL][7]), file=outfile)
print('\n', file=outfile)

CO_TYPE = '*Element, type=COH3D8'
print(CO_TYPE, file=outfile)
for EL in range(TEle_Value1, TEle_Value2):
    print("%5d, %5d, %5d, %5d, %5d, %5d, %5d, %5d, %5d" % (
    EL + 1, Element_dic[EL + 1][0], Element_dic[EL + 1][1], Element_dic[EL + 1][2], \
    Element_dic[EL + 1][3], Element_dic[EL + 1][4], Element_dic[EL + 1][5], Element_dic[EL + 1][6],
    Element_dic[EL + 1][7]), file=outfile)
print('\n', file=outfile)

COINP_SET = '*Elset, elset=A_SET'
print(COINP_SET, file=outfile)
L = 0
for EL in asp_ele:
    L = L + 1
    if L > 15:
        print('%6d,' % (EL), file=outfile)
        L = 0
    else:
        print('%6d,' % (EL), end='', file=outfile)
print('\n', file=outfile)

COINP_SET = '*Elset, elset=C_SET'
print(COINP_SET, file=outfile)
L = 0
for EL in cem_ele:
    L = L + 1
    if L > 15:
        print('%6d,' % (EL), file=outfile)
        L = 0
    else:
        print('%6d,' % (EL), end='', file=outfile)
print('\n', file=outfile)

COINP_SET = '*Elset, elset=S_SET'
print(COINP_SET, file=outfile)
L = 0
for EL in sto_ele:
    L = L + 1
    if L > 15:
        print('%6d,' % (EL), file=outfile)
        L = 0
    else:
        print('%6d,' % (EL), end='', file=outfile)
print('\n', file=outfile)

COINP_SET = '*Elset, elset=AA_SET'
print(COINP_SET, file=outfile)
L = 0
for EL in AA_SET:
    L = L + 1
    if L > 15:
        print('%6d,' % (EL), file=outfile)
        L = 0
    else:
        print('%6d,' % (EL), end='', file=outfile)
print('\n', file=outfile)

COINP_SET = '*Elset, elset=CC_SET'
print(COINP_SET, file=outfile)
L = 0
for EL in CC_SET:
    L = L + 1
    if L > 15:
        print('%6d,' % (EL), file=outfile)
        L = 0
    else:
        print('%6d,' % (EL), end='', file=outfile)
print('\n', file=outfile)

COINP_SET = '*Elset, elset=AC_SET'
print(COINP_SET, file=outfile)
L = 0
for EL in AC_SET:
    L = L + 1
    if L > 15:
        print('%6d,' % (EL), file=outfile)
        L = 0
    else:
        print('%6d,' % (EL), end='', file=outfile)
print('\n', file=outfile)

COINP_SET = '*Elset, elset=AS_SET'
print(COINP_SET, file=outfile)
L = 0
for EL in AS_SET:
    L = L + 1
    if L > 15:
        print('%6d,' % (EL), file=outfile)
        L = 0
    else:
        print('%6d,' % (EL), end='', file=outfile)
print('\n', file=outfile)

COINP_SET = '*Elset, elset=CS_SET'
print(COINP_SET, file=outfile)
L = 0
for EL in CS_SET:
    L = L + 1
    if L > 15:
        print('%6d,' % (EL), file=outfile)
        L = 0
    else:
        print('%6d,' % (EL), end='', file=outfile)
print('\n', file=outfile)

print('*End Part', file=outfile)
end = ['**', '** ASSEMBLY', '**', '*Assembly, name=Assembly', '**', '*Instance, name=PART-1-1, part=cohesive', \
       '*End Instance', '**', '*End Assembly']
for i in end:
    print(i, file=outfile)
outfile.close()

end_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step18：生成新的inp文件用时：', '%6f min' % ((end_time - step17_time) / 60))
print('已累计用时：', '%6f min' % ((end_time - star_time) / 60))
print('模型插入内聚力单元已完成，输出的模型文件为：', outFile_name)
void_rate = 1 - (len(asp_ele) + len(sto_ele)) / (60 * 35 * 30)
print('沥青混合料基体孔隙率为：', void_rate)
grout_rate = len(cem_ele) / (60 * 35 * 30 * void_rate)
print('模型灌浆率为：', grout_rate)



