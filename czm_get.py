#-*-coding:UTF-8-*-
import time
import math
from copy import copy
from tqdm import tqdm
from tqdm import trange
from scipy.spatial import Delaunay
from scipy.spatial import ConvexHull
from copy import deepcopy



star_time=time.time()
print('start at',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))



###step1：相关设置信息输入
#(1-1)读取标准网格文件
File_path='F:/biper/'
Nor_inp_name='czm_mesh_01.inp'
Nor_inp=open(File_path+Nor_inp_name,'r')
Nor_line=Nor_inp.readlines()

outFile_path='G:/Temp/'
outFile_name='aa.inp'
outfile=open(outFile_path+outFile_name,'w+')




###step2：读取标准网格节点和单元信息
#(2-1)读取标准网格的节点信息
Node_dic={}
for i in range(len(Nor_line)):
    if Nor_line[i].startswith('*Node'):
        node_startline=i
        break
    else:
        pass
for i in range(node_startline+1, len(Nor_line)):
    try:
        Node1=[float(cor) for cor in Nor_line[i].split(',')]  # 列表Node1，首个元素为节点编号，后三个元素为该节点的坐标
        Node_num=int(Node1[0])
        Node_dic[Node_num]=[Node1[1],Node1[2],Node1[3]]
    except:
        break
TNode_Value=max(Node_dic.keys())
print('标准网格的初始节点总数为：',TNode_Value)

#(2-2)读取标准网格的单元信息
Element_dic={}    #键为单元编号，值为一个列表，里面是8个节点的编号
point8=[]    #C3D8R单元
point6=[]    #C3D6单元
for i in range(len(Nor_line)):
    if Nor_line[i].startswith('*Element, type=C3D8R'):
        ele_startline=i
        break
    else:
        pass
for i in range(ele_startline+1,len(Nor_line)):
    try:
        Ele=[int(cor) for cor in Nor_line[i].split(',')]
        point8.append(Ele[0])
        Element_dic[Ele[0]]=[Ele[1],Ele[2],Ele[3],Ele[4],Ele[5],Ele[6],Ele[7],Ele[8]]
    except:
        break

TEle_Value=max(Element_dic.keys())
TEle_Value1=TEle_Value
print('标准网格的初始单元总数为：',TEle_Value)

#(2-3)计算标准网格中每个单元的形心坐标
Element_core={}                #字典，键为单元编号，值为一个列表，里面是该单元的形心坐标
for i in Element_dic.keys():
    n1=Element_dic[i][0]  #该单元的节点1
    n2=Element_dic[i][1]
    n3=Element_dic[i][2]
    n4=Element_dic[i][3]
    n5=Element_dic[i][4]
    n6=Element_dic[i][5]
    n7=Element_dic[i][6]
    n8=Element_dic[i][7]
    x1=Node_dic[n1][0]
    y1=Node_dic[n1][1]
    z1=Node_dic[n1][2]
    x2=Node_dic[n2][0]
    y2=Node_dic[n2][1]
    z2=Node_dic[n2][2]
    x3=Node_dic[n3][0]
    y3=Node_dic[n3][1]
    z3=Node_dic[n3][2]
    x4=Node_dic[n4][0]
    y4=Node_dic[n4][1]
    z4=Node_dic[n4][2]
    x5=Node_dic[n5][0]
    y5=Node_dic[n5][1]
    z5=Node_dic[n5][2]
    x6=Node_dic[n6][0]
    y6=Node_dic[n6][1]
    z6=Node_dic[n6][2]
    x7=Node_dic[n7][0]
    y7=Node_dic[n7][1]
    z7=Node_dic[n7][2]
    x8=Node_dic[n8][0]
    y8=Node_dic[n8][1]
    z8=Node_dic[n8][2]
    x0=(x1+x2+x3+x4+x5+x6+x7+x8)/8
    y0=(y1+y2+y3+y4+y5+y6+y7+y8)/8
    z0=(z1+z2+z3+z4+z5+z6+z7+z8)/8
    Element_core[i]=[x0,y0,z0]



###step3: 提取上半部分单元和下半部分单元
asp_ele=[]     #上半部分
cem_ele=[]     #下半部分
for i in Element_core.keys():
    y=Element_core[i][1]
    if y>0:
        asp_ele.append(i)
    else:
        cem_ele.append(i)



#(7-1)生成沥青部分的面的信息
AFACEINEL={}       #字典AFACEINEL，键为沥青部分的单元编号，值为元组，里面是6个面
Aface_list=[]     #所有单元的所有面都记录进来，重复记录
for k in asp_ele:      #遍历所有沥青单元编号
    n1=Element_dic[k][0]         #节点编号
    n2=Element_dic[k][1]
    n3=Element_dic[k][2]
    n4=Element_dic[k][3]
    n5=Element_dic[k][4]
    n6=Element_dic[k][5]
    n7=Element_dic[k][6]
    n8=Element_dic[k][7]
    x1=Node_dic[n1][0]
    y1=Node_dic[n1][1]
    z1=Node_dic[n1][2]
    x2=Node_dic[n2][0]
    y2=Node_dic[n2][1]
    z2=Node_dic[n2][2]
    x3=Node_dic[n3][0]
    y3=Node_dic[n3][1]
    z3=Node_dic[n3][2]
    x4=Node_dic[n4][0]
    y4=Node_dic[n4][1]
    z4=Node_dic[n4][2]
    x5=Node_dic[n5][0]
    y5=Node_dic[n5][1]
    z5=Node_dic[n5][2]
    x6=Node_dic[n6][0]
    y6=Node_dic[n6][1]
    z6=Node_dic[n6][2]
    x7=Node_dic[n7][0]
    y7=Node_dic[n7][1]
    z7=Node_dic[n7][2]
    x8=Node_dic[n8][0]
    y8=Node_dic[n8][1]
    z8=Node_dic[n8][2]

    a1=[]                         #给第1个面的节点按顺时针顺序编号，该面的节点为1234
    face1_coord={n1:[x1,y1,z1],n2:[x2,y2,z2],n3:[x3,y3,z3],n4:[x4,y4,z4]}
    if x1==x2==x3==x4:         #先判断是否在yz平面上
        y0=(y1+y2+y3+y4)/4
        z0=(z1+z2+z3+z4)/4
        for j in face1_coord.keys():
            if face1_coord[j][1]<y0 and face1_coord[j][2]<z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][1]<y0 and face1_coord[j][2]>z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][1]>y0 and face1_coord[j][2]>z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][1]>y0 and face1_coord[j][2]<z0:
                a1.append(j)
                break
            else:
                pass
    elif y1==y2==y3==y4:        #判断是否在xz平面上
        x0=(x1+x2+x3+x4)/4
        z0=(z1+z2+z3+z4)/4
        for j in face1_coord.keys():
            if face1_coord[j][0]<x0 and face1_coord[j][2]<z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0]<x0 and face1_coord[j][2]>z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0]>x0 and face1_coord[j][2]>z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0]>x0 and face1_coord[j][2]<z0:
                a1.append(j)
                break
            else:
                pass
    else:        #最后一定在xy平面上
        x0=(x1+x2+x3+x4)/4
        y0=(y1+y2+y3+y4)/4
        for j in face1_coord.keys():
            if face1_coord[j][0]<x0 and face1_coord[j][1]<y0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0]<x0 and face1_coord[j][1]>y0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0]>x0 and face1_coord[j][1]>y0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0]>x0 and face1_coord[j][1]<y0:
                a1.append(j)
                break
            else:
                pass
    a=(a1[0],a1[1],a1[2],a1[3])

    b1=[]  # 给第2个面的节点按顺时针顺序编号，该面的节点为5678
    face2_coord={n5: [x5, y5, z5], n6: [x6, y6, z6], n7: [x7, y7, z7], n8: [x8, y8, z8]}
    if x5==x6==x7==x8:  # 先判断是否在yz平面上
        y0=(y5+y6+y7+y8)/4
        z0=(z5+z6+z7+z8)/4
        for j in face2_coord.keys():
            if face2_coord[j][1]<y0 and face2_coord[j][2]<z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][1]<y0 and face2_coord[j][2]>z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][1]>y0 and face2_coord[j][2]>z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][1]>y0 and face2_coord[j][2]<z0:
                b1.append(j)
                break
            else:
                pass
    elif y5==y6==y7==y8:  # 判断是否在xz平面上
        x0=(x5+x6+x7+x8)/4
        z0=(z5+z6+z7+z8)/4
        for j in face2_coord.keys():
            if face2_coord[j][0]<x0 and face2_coord[j][2]<z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0]<x0 and face2_coord[j][2]>z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0]>x0 and face2_coord[j][2]>z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0]>x0 and face2_coord[j][2]<z0:
                b1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0=(x5+x6+x7+x8)/4
        y0=(y5+y6+y7+y8)/4
        for j in face2_coord.keys():
            if face2_coord[j][0]<x0 and face2_coord[j][1]<y0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0]<x0 and face2_coord[j][1]>y0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0]>x0 and face2_coord[j][1]>y0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0]>x0 and face2_coord[j][1]<y0:
                b1.append(j)
                break
            else:
                pass
    b=(b1[0], b1[1], b1[2], b1[3])

    c1=[]  # 给第3个面的节点按顺时针顺序编号，该面的节点为1256
    face3_coord={n1: [x1, y1, z1], n2: [x2, y2, z2], n5: [x5, y5, z5], n6: [x6, y6, z6]}
    if x1==x2==x5==x6:  # 先判断是否在yz平面上
        y0=(y1+y2+y5+y6)/4
        z0=(z1+z2+z5+z6)/4
        for j in face3_coord.keys():
            if face3_coord[j][1]<y0 and face3_coord[j][2]<z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][1]<y0 and face3_coord[j][2]>z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][1]>y0 and face3_coord[j][2]>z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][1]>y0 and face3_coord[j][2]<z0:
                c1.append(j)
                break
            else:
                pass
    elif y1==y2==y5==y6:  # 判断是否在xz平面上
        x0=(x1+x2+x5+x6)/4
        z0=(z1+z2+z5+z6)/4
        for j in face3_coord.keys():
            if face3_coord[j][0]<x0 and face3_coord[j][2]<z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0]<x0 and face3_coord[j][2]>z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0]>x0 and face3_coord[j][2]>z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0]>x0 and face3_coord[j][2]<z0:
                c1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0=(x1+x2+x5+x6)/4
        y0=(y1+y2+y5+y6)/4
        for j in face3_coord.keys():
            if face3_coord[j][0]<x0 and face3_coord[j][1]<y0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0]<x0 and face3_coord[j][1]>y0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0]>x0 and face3_coord[j][1]>y0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0]>x0 and face3_coord[j][1]<y0:
                c1.append(j)
                break
            else:
                pass
    c=(c1[0], c1[1], c1[2], c1[3])

    d1=[]  # 给第4个面的节点按顺时针顺序编号，该面的节点为3478
    face4_coord={n3: [x3, y3, z3], n4: [x4, y4, z4], n7: [x7, y7, z7], n8: [x8, y8, z8]}
    if x3==x4==x7==x8:  # 先判断是否在yz平面上
        y0=(y3+y4+y7+y8)/4
        z0=(z3+z4+z7+z8)/4
        for j in face4_coord.keys():
            if face4_coord[j][1]<y0 and face4_coord[j][2]<z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][1]<y0 and face4_coord[j][2]>z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][1]>y0 and face4_coord[j][2]>z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][1]>y0 and face4_coord[j][2]<z0:
                d1.append(j)
                break
            else:
                pass
    elif y3==y4==y7==y8:  # 判断是否在xz平面上
        x0=(x3+x4+x7+x8)/4
        z0=(z3+z4+z7+z8)/4
        for j in face4_coord.keys():
            if face4_coord[j][0]<x0 and face4_coord[j][2]<z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0]<x0 and face4_coord[j][2]>z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0]>x0 and face4_coord[j][2]>z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0]>x0 and face4_coord[j][2]<z0:
                d1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0=(x3+x4+x7+x8)/4
        y0=(y3+y4+y7+y8)/4
        for j in face4_coord.keys():
            if face4_coord[j][0]<x0 and face4_coord[j][1]<y0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0]<x0 and face4_coord[j][1]>y0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0]>x0 and face4_coord[j][1]>y0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0]>x0 and face4_coord[j][1]<y0:
                d1.append(j)
                break
            else:
                pass
    d=(d1[0], d1[1], d1[2], d1[3])

    e1=[]  # 给第5个面的节点按顺时针顺序编号，该面的节点为2367
    face5_coord={n2: [x2, y2, z2], n3: [x3, y3, z3], n6: [x6, y6, z6], n7: [x7, y7, z7]}
    if x2==x3==x6==x7:  # 先判断是否在yz平面上
        y0=(y2+y3+y6+y7)/4
        z0=(z2+z3+z6+z7)/4
        for j in face5_coord.keys():
            if face5_coord[j][1]<y0 and face5_coord[j][2]<z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][1]<y0 and face5_coord[j][2]>z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][1]>y0 and face5_coord[j][2]>z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][1]>y0 and face5_coord[j][2]<z0:
                e1.append(j)
                break
            else:
                pass
    elif y2==y3==y6==y7:  # 判断是否在xz平面上
        x0=(x2+x3+x6+x7)/4
        z0=(z2+z3+z6+z7)/4
        for j in face5_coord.keys():
            if face5_coord[j][0]<x0 and face5_coord[j][2]<z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0]<x0 and face5_coord[j][2]>z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0]>x0 and face5_coord[j][2]>z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0]>x0 and face5_coord[j][2]<z0:
                e1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0=(x2+x3+x6+x7)/4
        y0=(y2+y3+y6+y7)/4
        for j in face5_coord.keys():
            if face5_coord[j][0]<x0 and face5_coord[j][1]<y0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0]<x0 and face5_coord[j][1]>y0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0]>x0 and face5_coord[j][1]>y0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0]>x0 and face5_coord[j][1]<y0:
                e1.append(j)
                break
            else:
                pass
    e=(e1[0], e1[1], e1[2], e1[3])

    f1=[]  # 给第6个面的节点按顺时针顺序编号，该面的节点为1458
    face6_coord={n1: [x1, y1, z1], n4: [x4, y4, z4], n5: [x5, y5, z5], n8: [x8, y8, z8]}
    if x1==x4==x5==x8:  # 先判断是否在yz平面上
        y0=(y1+y4+y5+y8)/4
        z0=(z1+z4+z5+z8)/4
        for j in face6_coord.keys():
            if face6_coord[j][1]<y0 and face6_coord[j][2]<z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][1]<y0 and face6_coord[j][2]>z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][1]>y0 and face6_coord[j][2]>z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][1]>y0 and face6_coord[j][2]<z0:
                f1.append(j)
                break
            else:
                pass
    elif y1==y4==y5==y8:  # 判断是否在xz平面上
        x0=(x1+x4+x5+x8)/4
        z0=(z1+z4+z5+z8)/4
        for j in face6_coord.keys():
            if face6_coord[j][0]<x0 and face6_coord[j][2]<z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0]<x0 and face6_coord[j][2]>z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0]>x0 and face6_coord[j][2]>z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0]>x0 and face6_coord[j][2]<z0:
                f1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0=(x1+x4+x5+x8)/4
        y0=(y1+y4+y5+y8)/4
        for j in face6_coord.keys():
            if face6_coord[j][0]<x0 and face6_coord[j][1]<y0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0]<x0 and face6_coord[j][1]>y0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0]>x0 and face6_coord[j][1]>y0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0]>x0 and face6_coord[j][1]<y0:
                f1.append(j)
                break
            else:
                pass
    f=(f1[0], f1[1], f1[2], f1[3])

    AFACEINEL[k]=(a,b,c,d,e,f)     #字典AFACEINEL中该单元对应的值为一个元组，即不可变的列表
    Aface_list.extend([a,b,c,d,e,f])

Aface_set=list(set(Aface_list))     #所有A单元的所有面，不重复
A_count_pos={}      #键为Aface_set中的面，值为列表，里面依次是出现次数，各个面的在Aface_list中的索引位置
for i in Aface_set:
    A_count_pos[i]=[0]
k=-1   #计数，记录Aface_list的索引位置
print('A单元重复次数获取进度为：')
for i in tqdm(Aface_list):
    k+=1
    A_count_pos[i][0]+=1
    A_count_pos[i].append(k)


#(7-2)确定AA单元的插入位置
AAloc_dic={}        #键为拟生成的AA单元的编号，值为其8个节点分别在两个单元中的索引位置，列表形式
print('AA单元位置获取进度为：')
for i in tqdm(A_count_pos.keys()):
    if A_count_pos[i][0]==2:
        TEle_Value+=1
        ele1=asp_ele[A_count_pos[i][1]//6]         #含重复面的第一个单元的编号
        ele2=asp_ele[A_count_pos[i][2]//6]
        FA1=AFACEINEL[ele1][A_count_pos[i][1]%6]
        FA2=AFACEINEL[ele2][A_count_pos[i][2]%6]
        loc1=Element_dic[ele1].index(FA1[0])
        loc2=Element_dic[ele1].index(FA1[1])
        loc3=Element_dic[ele1].index(FA1[2])
        loc4=Element_dic[ele1].index(FA1[3])
        loc5=Element_dic[ele2].index(FA2[0])
        loc6=Element_dic[ele2].index(FA2[1])
        loc7=Element_dic[ele2].index(FA2[2])
        loc8=Element_dic[ele2].index(FA2[3])
        AAloc_dic.update({TEle_Value: [ele1, ele2, loc1, loc2, loc3, loc4, loc5, loc6, loc7, loc8]})



#(8-1)生成水泥部分的面的信息
CFACEINEL={}       #字典CFACEINEL，键为水泥部分的单元编号，值为元组，里面是6个面
Cface_list=[]     #所有单元的所有面都记录进来，重复记录
for k in cem_ele:      #遍历所有水泥单元编号
    n1=Element_dic[k][0]         #节点编号
    n2=Element_dic[k][1]
    n3=Element_dic[k][2]
    n4=Element_dic[k][3]
    n5=Element_dic[k][4]
    n6=Element_dic[k][5]
    n7=Element_dic[k][6]
    n8=Element_dic[k][7]
    x1=Node_dic[n1][0]
    y1=Node_dic[n1][1]
    z1=Node_dic[n1][2]
    x2=Node_dic[n2][0]
    y2=Node_dic[n2][1]
    z2=Node_dic[n2][2]
    x3=Node_dic[n3][0]
    y3=Node_dic[n3][1]
    z3=Node_dic[n3][2]
    x4=Node_dic[n4][0]
    y4=Node_dic[n4][1]
    z4=Node_dic[n4][2]
    x5=Node_dic[n5][0]
    y5=Node_dic[n5][1]
    z5=Node_dic[n5][2]
    x6=Node_dic[n6][0]
    y6=Node_dic[n6][1]
    z6=Node_dic[n6][2]
    x7=Node_dic[n7][0]
    y7=Node_dic[n7][1]
    z7=Node_dic[n7][2]
    x8=Node_dic[n8][0]
    y8=Node_dic[n8][1]
    z8=Node_dic[n8][2]

    a1=[]                         #给第1个面的节点按顺时针顺序编号，该面的节点为1234
    face1_coord={n1:[x1,y1,z1],n2:[x2,y2,z2],n3:[x3,y3,z3],n4:[x4,y4,z4]}
    if x1==x2==x3==x4:         #先判断是否在yz平面上
        y0=(y1+y2+y3+y4)/4
        z0=(z1+z2+z3+z4)/4
        for j in face1_coord.keys():
            if face1_coord[j][1]<y0 and face1_coord[j][2]<z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][1]<y0 and face1_coord[j][2]>z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][1]>y0 and face1_coord[j][2]>z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][1]>y0 and face1_coord[j][2]<z0:
                a1.append(j)
                break
            else:
                pass
    elif y1==y2==y3==y4:        #判断是否在xz平面上
        x0=(x1+x2+x3+x4)/4
        z0=(z1+z2+z3+z4)/4
        for j in face1_coord.keys():
            if face1_coord[j][0]<x0 and face1_coord[j][2]<z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0]<x0 and face1_coord[j][2]>z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0]>x0 and face1_coord[j][2]>z0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0]>x0 and face1_coord[j][2]<z0:
                a1.append(j)
                break
            else:
                pass
    else:        #最后一定在xy平面上
        x0=(x1+x2+x3+x4)/4
        y0=(y1+y2+y3+y4)/4
        for j in face1_coord.keys():
            if face1_coord[j][0]<x0 and face1_coord[j][1]<y0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0]<x0 and face1_coord[j][1]>y0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0]>x0 and face1_coord[j][1]>y0:
                a1.append(j)
                break
            else:
                pass
        for j in face1_coord.keys():
            if face1_coord[j][0]>x0 and face1_coord[j][1]<y0:
                a1.append(j)
                break
            else:
                pass
    a=(a1[0],a1[1],a1[2],a1[3])

    b1=[]  # 给第2个面的节点按顺时针顺序编号，该面的节点为5678
    face2_coord={n5: [x5, y5, z5], n6: [x6, y6, z6], n7: [x7, y7, z7], n8: [x8, y8, z8]}
    if x5==x6==x7==x8:  # 先判断是否在yz平面上
        y0=(y5+y6+y7+y8)/4
        z0=(z5+z6+z7+z8)/4
        for j in face2_coord.keys():
            if face2_coord[j][1]<y0 and face2_coord[j][2]<z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][1]<y0 and face2_coord[j][2]>z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][1]>y0 and face2_coord[j][2]>z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][1]>y0 and face2_coord[j][2]<z0:
                b1.append(j)
                break
            else:
                pass
    elif y5==y6==y7==y8:  # 判断是否在xz平面上
        x0=(x5+x6+x7+x8)/4
        z0=(z5+z6+z7+z8)/4
        for j in face2_coord.keys():
            if face2_coord[j][0]<x0 and face2_coord[j][2]<z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0]<x0 and face2_coord[j][2]>z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0]>x0 and face2_coord[j][2]>z0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0]>x0 and face2_coord[j][2]<z0:
                b1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0=(x5+x6+x7+x8)/4
        y0=(y5+y6+y7+y8)/4
        for j in face2_coord.keys():
            if face2_coord[j][0]<x0 and face2_coord[j][1]<y0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0]<x0 and face2_coord[j][1]>y0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0]>x0 and face2_coord[j][1]>y0:
                b1.append(j)
                break
            else:
                pass
        for j in face2_coord.keys():
            if face2_coord[j][0]>x0 and face2_coord[j][1]<y0:
                b1.append(j)
                break
            else:
                pass
    b=(b1[0], b1[1], b1[2], b1[3])

    c1=[]  # 给第3个面的节点按顺时针顺序编号，该面的节点为1256
    face3_coord={n1: [x1, y1, z1], n2: [x2, y2, z2], n5: [x5, y5, z5], n6: [x6, y6, z6]}
    if x1==x2==x5==x6:  # 先判断是否在yz平面上
        y0=(y1+y2+y5+y6)/4
        z0=(z1+z2+z5+z6)/4
        for j in face3_coord.keys():
            if face3_coord[j][1]<y0 and face3_coord[j][2]<z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][1]<y0 and face3_coord[j][2]>z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][1]>y0 and face3_coord[j][2]>z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][1]>y0 and face3_coord[j][2]<z0:
                c1.append(j)
                break
            else:
                pass
    elif y1==y2==y5==y6:  # 判断是否在xz平面上
        x0=(x1+x2+x5+x6)/4
        z0=(z1+z2+z5+z6)/4
        for j in face3_coord.keys():
            if face3_coord[j][0]<x0 and face3_coord[j][2]<z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0]<x0 and face3_coord[j][2]>z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0]>x0 and face3_coord[j][2]>z0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0]>x0 and face3_coord[j][2]<z0:
                c1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0=(x1+x2+x5+x6)/4
        y0=(y1+y2+y5+y6)/4
        for j in face3_coord.keys():
            if face3_coord[j][0]<x0 and face3_coord[j][1]<y0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0]<x0 and face3_coord[j][1]>y0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0]>x0 and face3_coord[j][1]>y0:
                c1.append(j)
                break
            else:
                pass
        for j in face3_coord.keys():
            if face3_coord[j][0]>x0 and face3_coord[j][1]<y0:
                c1.append(j)
                break
            else:
                pass
    c=(c1[0], c1[1], c1[2], c1[3])

    d1=[]  # 给第4个面的节点按顺时针顺序编号，该面的节点为3478
    face4_coord={n3: [x3, y3, z3], n4: [x4, y4, z4], n7: [x7, y7, z7], n8: [x8, y8, z8]}
    if x3==x4==x7==x8:  # 先判断是否在yz平面上
        y0=(y3+y4+y7+y8)/4
        z0=(z3+z4+z7+z8)/4
        for j in face4_coord.keys():
            if face4_coord[j][1]<y0 and face4_coord[j][2]<z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][1]<y0 and face4_coord[j][2]>z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][1]>y0 and face4_coord[j][2]>z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][1]>y0 and face4_coord[j][2]<z0:
                d1.append(j)
                break
            else:
                pass
    elif y3==y4==y7==y8:  # 判断是否在xz平面上
        x0=(x3+x4+x7+x8)/4
        z0=(z3+z4+z7+z8)/4
        for j in face4_coord.keys():
            if face4_coord[j][0]<x0 and face4_coord[j][2]<z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0]<x0 and face4_coord[j][2]>z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0]>x0 and face4_coord[j][2]>z0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0]>x0 and face4_coord[j][2]<z0:
                d1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0=(x3+x4+x7+x8)/4
        y0=(y3+y4+y7+y8)/4
        for j in face4_coord.keys():
            if face4_coord[j][0]<x0 and face4_coord[j][1]<y0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0]<x0 and face4_coord[j][1]>y0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0]>x0 and face4_coord[j][1]>y0:
                d1.append(j)
                break
            else:
                pass
        for j in face4_coord.keys():
            if face4_coord[j][0]>x0 and face4_coord[j][1]<y0:
                d1.append(j)
                break
            else:
                pass
    d=(d1[0], d1[1], d1[2], d1[3])

    e1=[]  # 给第5个面的节点按顺时针顺序编号，该面的节点为2367
    face5_coord={n2: [x2, y2, z2], n3: [x3, y3, z3], n6: [x6, y6, z6], n7: [x7, y7, z7]}
    if x2==x3==x6==x7:  # 先判断是否在yz平面上
        y0=(y2+y3+y6+y7)/4
        z0=(z2+z3+z6+z7)/4
        for j in face5_coord.keys():
            if face5_coord[j][1]<y0 and face5_coord[j][2]<z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][1]<y0 and face5_coord[j][2]>z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][1]>y0 and face5_coord[j][2]>z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][1]>y0 and face5_coord[j][2]<z0:
                e1.append(j)
                break
            else:
                pass
    elif y2==y3==y6==y7:  # 判断是否在xz平面上
        x0=(x2+x3+x6+x7)/4
        z0=(z2+z3+z6+z7)/4
        for j in face5_coord.keys():
            if face5_coord[j][0]<x0 and face5_coord[j][2]<z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0]<x0 and face5_coord[j][2]>z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0]>x0 and face5_coord[j][2]>z0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0]>x0 and face5_coord[j][2]<z0:
                e1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0=(x2+x3+x6+x7)/4
        y0=(y2+y3+y6+y7)/4
        for j in face5_coord.keys():
            if face5_coord[j][0]<x0 and face5_coord[j][1]<y0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0]<x0 and face5_coord[j][1]>y0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0]>x0 and face5_coord[j][1]>y0:
                e1.append(j)
                break
            else:
                pass
        for j in face5_coord.keys():
            if face5_coord[j][0]>x0 and face5_coord[j][1]<y0:
                e1.append(j)
                break
            else:
                pass
    e=(e1[0], e1[1], e1[2], e1[3])

    f1=[]  # 给第6个面的节点按顺时针顺序编号，该面的节点为1458
    face6_coord={n1: [x1, y1, z1], n4: [x4, y4, z4], n5: [x5, y5, z5], n8: [x8, y8, z8]}
    if x1==x4==x5==x8:  # 先判断是否在yz平面上
        y0=(y1+y4+y5+y8)/4
        z0=(z1+z4+z5+z8)/4
        for j in face6_coord.keys():
            if face6_coord[j][1]<y0 and face6_coord[j][2]<z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][1]<y0 and face6_coord[j][2]>z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][1]>y0 and face6_coord[j][2]>z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][1]>y0 and face6_coord[j][2]<z0:
                f1.append(j)
                break
            else:
                pass
    elif y1==y4==y5==y8:  # 判断是否在xz平面上
        x0=(x1+x4+x5+x8)/4
        z0=(z1+z4+z5+z8)/4
        for j in face6_coord.keys():
            if face6_coord[j][0]<x0 and face6_coord[j][2]<z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0]<x0 and face6_coord[j][2]>z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0]>x0 and face6_coord[j][2]>z0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0]>x0 and face6_coord[j][2]<z0:
                f1.append(j)
                break
            else:
                pass
    else:  # 最后一定在xy平面上
        x0=(x1+x4+x5+x8)/4
        y0=(y1+y4+y5+y8)/4
        for j in face6_coord.keys():
            if face6_coord[j][0]<x0 and face6_coord[j][1]<y0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0]<x0 and face6_coord[j][1]>y0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0]>x0 and face6_coord[j][1]>y0:
                f1.append(j)
                break
            else:
                pass
        for j in face6_coord.keys():
            if face6_coord[j][0]>x0 and face6_coord[j][1]<y0:
                f1.append(j)
                break
            else:
                pass
    f=(f1[0], f1[1], f1[2], f1[3])

    CFACEINEL[k]=(a,b,c,d,e,f)     #字典CFACEINEL中该单元对应的值为一个元组，即不可变的列表
    Cface_list.extend([a,b,c,d,e,f])

Cface_set=list(set(Cface_list))     #所有C单元的所有面，不重复
C_count_pos={}      #键为Cface_set中的面，值为列表，里面依次是出现次数，各个面的在Cface_list中的索引位置
for i in Cface_set:
    C_count_pos[i]=[0]
k=-1   #计数，记录Cface_list的索引位置
print('C单元重复次数获取进度为：')
for i in tqdm(Cface_list):
    k+=1
    C_count_pos[i][0]+=1
    C_count_pos[i].append(k)

#(8-2)确定CC单元的插入位置
CCloc_dic={}        #键为拟生成的CC单元的编号，值为其8个节点分别在两个单元中的索引位置，列表形式
print('CC单元位置获取进度为：')
for i in tqdm(C_count_pos.keys()):
    if C_count_pos[i][0]==2:
        TEle_Value+=1
        ele1=cem_ele[C_count_pos[i][1]//6]         #含重复面的第一个单元的编号
        ele2=cem_ele[C_count_pos[i][2]//6]
        FA1=CFACEINEL[ele1][C_count_pos[i][1]%6]
        FA2=CFACEINEL[ele2][C_count_pos[i][2]%6]
        loc1=Element_dic[ele1].index(FA1[0])
        loc2=Element_dic[ele1].index(FA1[1])
        loc3=Element_dic[ele1].index(FA1[2])
        loc4=Element_dic[ele1].index(FA1[3])
        loc5=Element_dic[ele2].index(FA2[0])
        loc6=Element_dic[ele2].index(FA2[1])
        loc7=Element_dic[ele2].index(FA2[2])
        loc8=Element_dic[ele2].index(FA2[3])
        CCloc_dic.update({TEle_Value: [ele1, ele2, loc1, loc2, loc3, loc4, loc5, loc6, loc7, loc8]})


ACloc_dic={}        #键为拟生成的AC单元的编号，值为其8个节点分别在两个单元中的索引位置，列表形式
ACface_set=list(set(Aface_list)&set(Cface_list))
print('AC单元位置获取进度为：')
for i in tqdm(ACface_set):
    TEle_Value+=1
    ele1=asp_ele[A_count_pos[i][1]//6]
    ele2=cem_ele[C_count_pos[i][1]//6]
    FA1=AFACEINEL[ele1][A_count_pos[i][1]%6]
    FA2=CFACEINEL[ele2][C_count_pos[i][1]%6]
    loc1=Element_dic[ele1].index(FA1[0])
    loc2=Element_dic[ele1].index(FA1[1])
    loc3=Element_dic[ele1].index(FA1[2])
    loc4=Element_dic[ele1].index(FA1[3])
    loc5=Element_dic[ele2].index(FA2[0])
    loc6=Element_dic[ele2].index(FA2[1])
    loc7=Element_dic[ele2].index(FA2[2])
    loc8=Element_dic[ele2].index(FA2[3])
    ACloc_dic.update({TEle_Value: [ele1, ele2, loc1, loc2, loc3, loc4, loc5, loc6, loc7, loc8]})


#(12-1)寻找沥青材料内部重复出现的节点并统计其出现次数
CO_ANODE=[]         #列表CO_ANODE里面是沥青单元对应的节点编号，直接写在一个大列表CO_ANODE里
ANODECO_DIC={}        ###字典ANODECO_DIC，键为节点编号，值为一个列表，里面依次是该节点在沥青内部出现的次数，每次出现在CO_ANODE中的索引号
ANODECO=[]        ###储存沥青内部重复出现的节点编号
for i in asp_ele:
    CO_ANODE.extend(Element_dic[i])
CO_ANODE_SET=sorted(set(CO_ANODE))          ###节点集，除去重复节点
for i in CO_ANODE_SET:
    ANODECO_DIC[i]=[0]
k=-1    #计数
for i in CO_ANODE:
    k+=1
    ANODECO_DIC[i][0]+=1
    ANODECO_DIC[i].append(k)

for i in ANODECO_DIC.keys():
    if ANODECO_DIC[i][0]>1:
        ANODECO.append(i)
    else:
        pass

#(12-2)生成新的节点赋予编号较大的单元，使所有沥青单元均不会共节点
print('沥青内部节点分裂进度为：')
for i in tqdm(ANODECO_DIC.keys()):
    if ANODECO_DIC[i][0]>1:
        EL_RE=[]    #列表EL_RE，记录节点i所在的所有单元
        for j in range(1,len(ANODECO_DIC[i])):
            EL=asp_ele[ANODECO_DIC[i][j]//8]
            EL_RE.append(EL)
        EL_RE.sort()  # 对列表进行排序，里面是重复出现的节点所在的单元
        for LS in range(len(EL_RE)-1):  # 遍历节点i所在的所有单元，编号从小到大
            TNode_Value+=1  # 新产生的节点的编号
            Node_dic.update({TNode_Value: Node_dic[i]})  # 新生成的节点添加到统一的节点字典里
            Loc=Element_dic[EL_RE[LS+1]].index(i)  # 节点i在该单元中的索引位置，便于下面将其替换为新生成的节点
            Element_dic[EL_RE[LS+1]][Loc]=TNode_Value



#(13-1)寻找水泥材料内部重复出现的节点并统计其出现次数
CO_CNODE=[]         #列表CO_CNODE里面是水泥单元对应的节点编号，直接写在一个大列表CO_CNODE里
CNODECO_DIC={}        ###字典CNODECO_DIC，键为节点编号，值为一个列表，里面依次是该节点在水泥内部出现的次数，每次出现在CO_CNODE中的索引号
CNODECO=[]        ###储存水泥内部重复出现的节点编号
for i in cem_ele:
    CO_CNODE.extend(Element_dic[i])
CO_CNODE_SET=sorted(set(CO_CNODE))          ###节点集，除去重复节点
for i in CO_CNODE_SET:
    CNODECO_DIC[i]=[0]
k=-1    #计数
for i in CO_CNODE:
    k+=1
    CNODECO_DIC[i][0]+=1
    CNODECO_DIC[i].append(k)

for i in CNODECO_DIC.keys():
    if CNODECO_DIC[i][0]>1:
        CNODECO.append(i)
    else:
        pass

#(13-2)生成新的节点赋予编号较大的单元，使所有水泥单元均不会共节点
print('水泥内部节点分裂进度为：')
for i in tqdm(CNODECO_DIC.keys()):
    if CNODECO_DIC[i][0]>1:
        EL_RE=[]    #列表EL_RE，记录节点i所在的所有单元
        for j in range(1,len(CNODECO_DIC[i])):
            EL=cem_ele[CNODECO_DIC[i][j]//8]
            EL_RE.append(EL)
        EL_RE.sort()  # 对列表进行排序，里面是重复出现的节点所在的单元
        for LS in range(len(EL_RE)-1):  # 遍历节点i所在的所有单元，编号从小到大
            TNode_Value+=1  # 新产生的节点的编号
            Node_dic.update({TNode_Value: Node_dic[i]})  # 新生成的节点添加到统一的节点字典里
            Loc=Element_dic[EL_RE[LS+1]].index(i)  # 节点i在该单元中的索引位置，便于下面将其替换为新生成的节点
            Element_dic[EL_RE[LS+1]][Loc]=TNode_Value



#(14-1)寻找沥青水泥界面重复出现的节点
CO_ANODE=[]         #列表CO_ANODE里面是沥青单元对应的节点编号，直接写在一个大列表CO_ANODE里
for i in asp_ele:
    CO_ANODE.extend(Element_dic[i])
CO_ANODE_SET=set(CO_ANODE)          ###节点集，除去重复节点并排序

CO_CNODE=[]         #列表CO_CNODE里面是水泥单元对应的节点编号，直接写在一个大列表CO_CNODE里
for i in cem_ele:
    CO_CNODE.extend(Element_dic[i])
CO_CNODE_SET=set(CO_CNODE)          ###水泥节点集，除去重复节点并排序

ACNODECO=sorted(set(CO_ANODE_SET)&set(CO_CNODE_SET))    #同时在水泥和沥青出现的节点编号

ACNODECO_DIC={}        ###字典ACNODECO_DIC，键为沥青节点编号，值为一个列表，里面依次是该节点在沥青内部出现的次数，每次出现在CO_ANODE中的索引号
k=-1    #计数
for i in CO_ANODE:
    k+=1
    ACNODECO_DIC[i]=[1]
    ACNODECO_DIC[i].append(k)

#(14-2)生成新的节点赋予与水泥共节点的沥青单元，使水泥与沥青不共节点
print('沥青水泥界面节点分裂进度为：')
for i in tqdm(ACNODECO):       #对于同时在沥青和水泥出现的节点的编号i
    EL=asp_ele[ACNODECO_DIC[i][1]//8]
    TNode_Value+=1  # 新产生的节点的编号
    Node_dic.update({TNode_Value:Node_dic[i]})  # 新生成的节点添加到统一的节点字典里并且初始坐标与原节点相同
    Loc=Element_dic[EL].index(i)  # 节点i在该单元中的索引位置，便于下面将其替换为新生成的节点
    Element_dic[EL][Loc]=TNode_Value



#(17-1)插入AA单元
AAnum1=TEle_Value1+1
for i in AAloc_dic.keys():
    NODE1=Element_dic[AAloc_dic[i][0]][AAloc_dic[i][2]]
    NODE2=Element_dic[AAloc_dic[i][0]][AAloc_dic[i][3]]
    NODE3=Element_dic[AAloc_dic[i][0]][AAloc_dic[i][4]]
    NODE4=Element_dic[AAloc_dic[i][0]][AAloc_dic[i][5]]
    NODE5=Element_dic[AAloc_dic[i][1]][AAloc_dic[i][6]]
    NODE6=Element_dic[AAloc_dic[i][1]][AAloc_dic[i][7]]
    NODE7=Element_dic[AAloc_dic[i][1]][AAloc_dic[i][8]]
    NODE8=Element_dic[AAloc_dic[i][1]][AAloc_dic[i][9]]
    Element_dic.update({i:[NODE1, NODE2, NODE3, NODE4, NODE5, NODE6, NODE7, NODE8]})

AAnum2=max(Element_dic.keys())       #AA单元中编号最大的单元编号
AA_SET=range(AAnum1,AAnum2+1)     #列表，里面是所有AA单元的编号

#(17-2)插入CC单元
CCnum1=max(Element_dic.keys())+1
for i in CCloc_dic.keys():
    NODE1=Element_dic[CCloc_dic[i][0]][CCloc_dic[i][2]]
    NODE2=Element_dic[CCloc_dic[i][0]][CCloc_dic[i][3]]
    NODE3=Element_dic[CCloc_dic[i][0]][CCloc_dic[i][4]]
    NODE4=Element_dic[CCloc_dic[i][0]][CCloc_dic[i][5]]
    NODE5=Element_dic[CCloc_dic[i][1]][CCloc_dic[i][6]]
    NODE6=Element_dic[CCloc_dic[i][1]][CCloc_dic[i][7]]
    NODE7=Element_dic[CCloc_dic[i][1]][CCloc_dic[i][8]]
    NODE8=Element_dic[CCloc_dic[i][1]][CCloc_dic[i][9]]
    Element_dic.update({i:[NODE1, NODE2, NODE3, NODE4, NODE5, NODE6, NODE7, NODE8]})

CCnum2=max(Element_dic.keys())       #CC单元中编号最大的单元编号
CC_SET=range(CCnum1,CCnum2+1)     #列表，里面是所有CC单元的编号

#(17-3)插入AC单元
ACnum1=max(Element_dic.keys())+1
for i in ACloc_dic.keys():
    NODE1=Element_dic[ACloc_dic[i][0]][ACloc_dic[i][2]]
    NODE2=Element_dic[ACloc_dic[i][0]][ACloc_dic[i][3]]
    NODE3=Element_dic[ACloc_dic[i][0]][ACloc_dic[i][4]]
    NODE4=Element_dic[ACloc_dic[i][0]][ACloc_dic[i][5]]
    NODE5=Element_dic[ACloc_dic[i][1]][ACloc_dic[i][6]]
    NODE6=Element_dic[ACloc_dic[i][1]][ACloc_dic[i][7]]
    NODE7=Element_dic[ACloc_dic[i][1]][ACloc_dic[i][8]]
    NODE8=Element_dic[ACloc_dic[i][1]][ACloc_dic[i][9]]
    Element_dic.update({i:[NODE1, NODE2, NODE3, NODE4, NODE5, NODE6, NODE7, NODE8]})

ACnum2=max(Element_dic.keys())       #AC单元中编号最大的单元编号
AC_SET=range(ACnum1,ACnum2+1)     #列表，里面是所有AC单元的编号

TEle_Value2=ACnum2

shangxia_ele=list(AA_SET)+list(CC_SET)
mid_ele=AC_SET

###step18:生成新的inp文件
val_ele=sorted(asp_ele+cem_ele)
val_nod=[]
for i in val_ele:
    val_nod.extend(Element_dic[i])
val_nod=sorted(set(val_nod))
#文件头的书写
Heading=[]
Heading.append('*Heading')
Heading.append('** Job name: cohesive Model name: Model-3')
Heading.append('** Generated by: Abaqus/CAE 2020')
Heading.append('*Preprint, echo=NO, model=NO, history=NO, contact=NO')
Heading.append('**')
Heading.append('**PARTS')
Heading.append('**')
Heading.append('*Part, name=cohesive')
Heading.append('*Node')
#Part相关节点及单元信息写入
#NODE
for i in range(len(Heading)):
    print(Heading[i],file=outfile)
#字典按照keys大小排
for NO in val_nod:
    print("%9d, %9f, %9f, %9f" %(NO, Node_dic[NO][0],Node_dic[NO][1],Node_dic[NO][2]),file=outfile)
print('\n',file=outfile)

#ELement首先判断单元的类型
CO_TYPE="*Element, type=C3D8R"
print(CO_TYPE,file=outfile)
for EL in point8:
    print("%5d, %5d, %5d, %5d, %5d, %5d, %5d, %5d, %5d" %(EL,Element_dic[EL][0],Element_dic[EL][1],Element_dic[EL][2],\
            Element_dic[EL][3],Element_dic[EL][4],Element_dic[EL][5],Element_dic[EL][6],Element_dic[EL][7]),file=outfile)
print('\n',file=outfile)

CO_TYPE='*Element, type=COH3D8'
print(CO_TYPE,file=outfile)
for EL in range(TEle_Value1, TEle_Value2):
    print("%5d, %5d, %5d, %5d, %5d, %5d, %5d, %5d, %5d" % (EL+1,Element_dic[EL+1][0],Element_dic[EL+1][1],Element_dic[EL+1][2],\
            Element_dic[EL+1][3],Element_dic[EL+1][4],Element_dic[EL+1][5],Element_dic[EL+1][6],Element_dic[EL+1][7]),file=outfile)
print('\n',file=outfile)

COINP_SET='*Elset, elset=TOP_SET'
print(COINP_SET,file=outfile)
L=0
for EL in asp_ele:
    L=L+1
    if L>15:
        print('%6d,' %(EL),file=outfile)
        L=0
    else:
        print('%6d,' %(EL),end='',file=outfile)
print('\n',file=outfile)

COINP_SET='*Elset, elset=DOWN_SET'
print(COINP_SET,file=outfile)
L=0
for EL in cem_ele:
    L=L+1
    if L>15:
        print('%6d,' %(EL),file=outfile)
        L=0
    else:
        print('%6d,' %(EL),end='',file=outfile)
print('\n',file=outfile)

COINP_SET='*Elset, elset=SHANGXIA_SET'
print(COINP_SET,file=outfile)
L=0
for EL in shangxia_ele:
    L=L+1
    if L>15:
        print('%6d,' %(EL),file=outfile)
        L=0
    else:
        print('%6d,' %(EL),end='',file=outfile)
print('\n',file=outfile)

COINP_SET='*Elset, elset=MID_SET'
print(COINP_SET,file=outfile)
L=0
for EL in mid_ele:
    L=L+1
    if L>15:
        print('%6d,' %(EL),file=outfile)
        L=0
    else:
        print('%6d,' %(EL),end='',file=outfile)
print('\n',file=outfile)

print('*End Part',file=outfile)
end=['**','** ASSEMBLY','**','*Assembly, name=Assembly','**','*Instance, name=PART-1-1, part=cohesive',\
     '*End Instance','**','*End Assembly']
for i in end:
    print(i,file=outfile)
outfile.close()

end_time=time.time()
print('已累计用时：', '%6f min' %((end_time-star_time)/60))