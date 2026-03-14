# -*-coding:UTF-8-*-
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
#current_directory="E:/Abaqus_examples_2nd_edition/No_cement/test928/"
# step1: 相关设置信息输入
# (1-1)标准网格文件读取设置
inFile_path = "E:/Abaqus_examples_2nd_edition/No_cement/"
File_path = 'E:\\temp\\260106\\'

Nor_inp_name = 'mesh_1mm.inp'
Nor_inp = open(inFile_path + Nor_inp_name, 'r')
Nor_line = Nor_inp.readlines()

# (1-2)基体几何信息文件读取设置
inFile_path = File_path
Mat_inp_name = 'matrix_260106_test.txt'
Mat_inp = open(inFile_path + Mat_inp_name, 'r')
Mat_line = Mat_inp.readlines()

# (1-3)输出文件设置
outFile_path = File_path
outFile_name = 'matrix_260106_test.inp'
outfile = open(outFile_path + outFile_name, 'w+')

# (1-4)模型关心区域单元数量
ele_num = 60 * 35 * 30

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
    #Element_core[i] = [x0, y0]

# (2-4)读取关心区域单元编号
care_ele = []  # 储存在关心区域的单元的编号
type = 1  # 判断是否generate形式，是的话就为1，不是的话为2
for i in range(len(Nor_line)):
    if Nor_line[i].startswith('*Elset, elset=down, generate'):
        type = 1
        Startline = i
        break
    elif Nor_line[i].startswith('*Elset, elset=down'):
        type = 2
        Startline = i
        break
    else:
        pass
if type == 1:
    Ele = [int(cor) for cor in Nor_line[Startline + 1].split(',')]
    care_ele.extend(range(Ele[0], Ele[1] + 1))
elif type == 2:
    for i in range(Startline + 1, len(Nor_line)):
        try:
            Ele = [int(cor) for cor in Nor_line[i].split(',')]
            care_ele.extend(Ele)
        except:
            break

# (2-5)读取边界单元编号
bound_ele = []  # 储存边界单元的编号
type = 1  # 判断是否generate形式，是的话就为1，不是的话为2
for i in range(len(Nor_line)):
    if Nor_line[i].startswith('*Elset, elset=bound, generate'):
        type = 1
        Startline = i
        break
    elif Nor_line[i].startswith('*Elset, elset=bound'):
        type = 2
        Startline = i
        break
    else:
        pass
if type == 1:
    Ele = [int(cor) for cor in Nor_line[Startline + 1].split(',')]
    bound_ele.extend(range(Ele[0], Ele[1] + 1))
elif type == 2:
    for i in range(Startline + 1, len(Nor_line)):
        try:
            Ele = [int(cor) for cor in Nor_line[i].split(',')]
            bound_ele.extend(Ele)
        except:
            break

# (2-6)读取上部单元编号
top_ele = []  # 储存上部单元的编号
type = 1  # 判断是否generate形式，是的话就为1，不是的话为2
for i in range(len(Nor_line)):
    if Nor_line[i].startswith('*Elset, elset=top, generate'):
        type = 1
        Startline = i
        break
    elif Nor_line[i].startswith('*Elset, elset=top'):
        type = 2
        Startline = i
        break
    else:
        pass
if type == 1:
    Ele = [int(cor) for cor in Nor_line[Startline + 1].split(',')]
    top_ele.extend(range(Ele[0], Ele[1] + 1))
elif type == 2:
    for i in range(Startline + 1, len(Nor_line)):
        try:
            Ele = [int(cor) for cor in Nor_line[i].split(',')]
            top_ele.extend(Ele)
        except:
            break

step2_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step2：获取标准网格信息用时：', '%6f min' % ((step2_time - step1_time) / 60))
print('已累计用时：', '%6f min' % ((step2_time - star_time) / 60))

# step3：读取并处理基体的几何信息
# (3-1)读取基体的几何信息
mat_dic = {}  # 键为基体编号，值为一个列表，里面有3个元素，第1个元素为列表，里面是形心坐标，第2个元素为列表，里面是[最小半径，最大半径]，
# 第3个元素为列表，里面包含顶点信息
for i in range(len(Mat_line)):
    if Mat_line[i].startswith('agg number'):
        agg_num = int(Mat_line[i + 1])  # 骨料总数
        break
    else:
        pass

for i in range(1, agg_num + 1):  # TODO读取基体的顶点信息(按照沥青生成)
    mat_dic[i] = []
    vertex_temp = []
    for j in range(len(Mat_line)):
        if Mat_line[j].startswith('asp-vertex-' + str(i) + '-'):
            startline = j + 1
            break
        else:
            pass
    for j in range(startline, len(Mat_line)):
        try:
            Node = [float(cor) for cor in Mat_line[j].split(',')]  # 列表Node，三个元素为该节点的坐标
            vertex_temp.append(Node) #沥青节点
        except:
            break

    x_sum, y_sum, z_sum = 0, 0, 0
    for j in range(len(vertex_temp)):
        x_sum += vertex_temp[j][0]
        y_sum += vertex_temp[j][1]
        z_sum += vertex_temp[j][2]
    x0 = x_sum / len(vertex_temp)
    y0 = y_sum / len(vertex_temp)
    z0 = z_sum / len(vertex_temp)
    mat_dic[i].append([x0, y0, z0])

    rad_min = 100
    rad_max = 0
    for j in range(len(vertex_temp)):
        rad_temp = math.sqrt((vertex_temp[j][0] - x0) ** 2 + (vertex_temp[j][1] - y0) ** 2 + (vertex_temp[j][2] - z0) ** 2)
        rad_min = min(rad_min, rad_temp)
        rad_max = max(rad_max, rad_temp)
    mat_dic[i].append([rad_min, rad_max])
    print("min=%5d max=%5d",rad_min, rad_max)
    mat_dic[i].append(vertex_temp)

step3_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step3：读取并处理基体的几何信息用时：', '%6f min' % ((step3_time - step2_time) / 60))
print('已累计用时：', '%6f min' % ((step3_time - star_time) / 60))

# step4:基体单元映射
M_nor = []  # 列表，里面存储标准单元中基体单元和边界单元的编号
Left_ele = care_ele
for i in Left_ele:  # 首先给基体内接球内的单元赋予属性
    if Element_core[i][1] < 35:  # y>35的单元不考虑
        pass
    else:
        continue
    for j in mat_dic.keys():  # 遍历集料编号
        x0 = mat_dic[j][0][0]
        y0 = mat_dic[j][0][1]
        z0 = mat_dic[j][0][2]
        rad_min = mat_dic[j][1][0]
        x = Element_core[i][0]
        y = Element_core[i][1]
        z = Element_core[i][2]
        if (x - x0) ** 2 + (y - y0) ** 2 /0.8/0.8+ (z - z0) ** 2 /0.6/0.6<= rad_min ** 2:
        #if (x - x0) ** 2 + (y - y0) ** 2 <= rad_min ** 2:
            M_nor.append(i)
            break
        else:
            pass
Left_ele = sorted(set(Left_ele) - set(M_nor))
print('基体内外切球间单元映射进度为：')
for i in tqdm(Left_ele):  # 判断该单元是否位于集料外接球外，若在外面直接跳过该集料
    if Element_core[i][1] < 35:
        pass
    else:
        continue
    for j in mat_dic.keys():  # 遍历集料编号
        x0 = mat_dic[j][0][0]
        y0 = mat_dic[j][0][1]
        z0 = mat_dic[j][0][2]
        rad_max = mat_dic[j][1][1]
        x = Element_core[i][0]
        y = Element_core[i][1]
        z = Element_core[i][2]
        if (x - x0) ** 2 + (y - y0) ** 2 + (z - z0) ** 2 > rad_max ** 2:
        #if (x - x0) ** 2 + (y - y0) ** 2 > rad_max ** 2:
            pass
        else:
            vertex_temp1 = deepcopy(mat_dic[j][2])
            vertex_temp2 = deepcopy(mat_dic[j][2])
            #mat_dic[i][[x0, y0, z0],[rad_min, rad_max],[vertex_temp]]
            vertex_temp2.append(Element_core[i])
            if ConvexHull(vertex_temp2) == ConvexHull(vertex_temp1):
                M_nor.append(i)
                break
            else:
                pass

MB_nor = sorted(set(M_nor) | set(bound_ele))
MB_nod = []  # 储存基体和边界单元需要的节点编号
for i in MB_nor:
    MB_nod.extend(Element_dic[i])
MB_nod = sorted(set(MB_nod))

cem_ele = sorted(set(top_ele) | set(care_ele) | set(bound_ele))  # 欧拉体区域的单元编号
cem_nod = []  # 欧拉体区域内的节点编号
for i in cem_ele:
    cem_nod.extend(Element_dic[i])
cem_nod = sorted(set(cem_nod))

step4_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step4：基体单元类型映射用时：', '%6f min' % ((step4_time - step3_time) / 60))
print('已累计用时：', '%6f min' % ((step4_time - star_time) / 60))

# step5:生成新的inp文件
# (5-1)文件头的书写
Heading = ['*Heading', '** Job name: cohesive Model name: Model-1', '** Generated by: Abaqus/CAE 2020',
           '*Preprint, echo=NO, model=NO, history=NO, contact=NO', '**', '**PARTS', '**']
for i in range(len(Heading)):
    print(Heading[i], file=outfile)
# (5-2)基体Part节点及单元信息写入
print('*Part, name=matrix', file=outfile)

print('*Node', file=outfile)
for NO in MB_nod:
    print("%9d, %9f, %9f, %9f" % (NO, Node_dic[NO][0], Node_dic[NO][1], Node_dic[NO][2]), file=outfile)
print('\n', file=outfile)

CO_TYPE = "*Element, type=C3D8R"
print(CO_TYPE, file=outfile)
for EL in MB_nor:
    print(
        "%5d, %5d, %5d, %5d, %5d, %5d, %5d, %5d, %5d" % (EL, Element_dic[EL][0], Element_dic[EL][1], Element_dic[EL][2],
                                                         Element_dic[EL][3], Element_dic[EL][4], Element_dic[EL][5],
                                                         Element_dic[EL][6], Element_dic[EL][7]), file=outfile)
print('\n', file=outfile)
print('*End Part', file=outfile)
print('**', file=outfile)

# (5-3)欧拉体Part节点及单元信息写入
print('*Part, name=cement', file=outfile)

print('*Node', file=outfile)
for NO in cem_nod:
    print("%9d, %9f, %9f, %9f" % (NO, Node_dic[NO][0], Node_dic[NO][1], Node_dic[NO][2]), file=outfile)
print('\n', file=outfile)

CO_TYPE = "*Element, type=EC3D8R"
print(CO_TYPE, file=outfile)
for EL in cem_ele:
    print(
        "%5d, %5d, %5d, %5d, %5d, %5d, %5d, %5d, %5d" % (EL, Element_dic[EL][0], Element_dic[EL][1], Element_dic[EL][2],
                                                         Element_dic[EL][3], Element_dic[EL][4], Element_dic[EL][5],
                                                         Element_dic[EL][6], Element_dic[EL][7]), file=outfile)
print('\n', file=outfile)
print('*End Part', file=outfile)
print('**', file=outfile)

# (5-4)写入尾文件
end = ['**', '** ASSEMBLY', '**', '*Assembly, name=Assembly', '**', '*Instance, name=matrix-1, part=matrix',
       '*End Instance',
       '**', '*Instance, name=cement-1, part=cement', '*End Instance', '**', '*End Assembly']
for i in end:
    print(i, file=outfile)

outfile.close()

end_time = time.time()
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('step5：生成新的inp文件用时：', '%6f min' % ((end_time - step4_time) / 60))
print('已累计用时：', '%6f min' % ((end_time - star_time) / 60))

print('映射模型基体单元数量为：', len(M_nor), '映射模型单元总量为：', ele_num)
print('映射模型孔隙率为：', 1.0 - float(len(M_nor)) / ele_num)
print('基体顶点信息生成完成，已输出文件' + outFile_name)
