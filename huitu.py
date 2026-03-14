#-*- coding:UTF-8 -*-
import xlrd
import matplotlib.pyplot as plt
plt.rc('font',family='SimHei')
import numpy as np


#读取数据
#导入需要读取Excel表格的路径
data=xlrd.open_workbook(r'C:\Users\zs\Desktop\big_paper\huitu\data_sum.xlsx')



###绘制曲线图
table=data.sheet_by_name(sheet_name='Sheet1')    # 通过名称获取sheet
col0=table.col(colx=0)    # 返回第0列列中所有的单元格对象组成的列表，横坐标信息
u2=[]
for i in range(2,len(col0)):
    value=col0[i].value
    u2.append(value)

col1=table.col(colx=1)    # 返回第2列列中所有的单元格对象组成的列表，第一组纵坐标信息
ser01=[]
for i in range(2,len(col1)):
    value=col1[i].value
    ser01.append(value)

plt.plot(u2,ser01,color = 'black',linestyle = '-',linewidth = 0.5,\
         marker = 'x',markerfacecolor = 'white', \
         markersize = 3,markeredgewidth = 1, label = '轻度损伤')


col2=table.col(colx=3)    # 返回第3列列中所有的单元格对象组成的列表
ser02=[]
for i in range(2,len(col2)):
    value=col2[i].value
    ser02.append(value)

plt.plot(u2,ser02,color = 'black',linestyle = '-',linewidth = 0.5,\
         marker = '^',markerfacecolor = 'white', \
         markersize = 3,markeredgewidth = 1, label = '重度损伤')



col3=table.col(colx=5)    # 返回第4列列中所有的单元格对象组成的列表
ser03=[]
for i in range(2,len(col3)):
    value=col3[i].value
    ser03.append(value)

plt.plot(u2,ser03,color = 'black',linestyle = '-',linewidth = 0.5,\
         marker = 'o',markerfacecolor = 'white', \
         markersize = 3,markeredgewidth = 1, label='极重损伤')


'''
col4=table.col(colx=7)    # 返回第4列列中所有的单元格对象组成的列表
ser04=[]
for i in range(2,len(col4)):
    value=col4[i].value
    ser04.append(value)

plt.plot(u2,ser04,color = 'black',linestyle = '-',linewidth = 0.5,\
         marker = 'v',markerfacecolor = 'white', \
         markersize = 3,markeredgewidth = 1, label='方案10')

col5=table.col(colx=9)    # 返回第4列列中所有的单元格对象组成的列表
ser05=[]
for i in range(2,len(col5)):
    value=col5[i].value
    ser05.append(value)

plt.plot(u2,ser05,color = 'black',linestyle = '-',linewidth = 0.5,\
         marker = 's',markerfacecolor = 'white', \
         markersize = 3,markeredgewidth = 1, label='方案11')


col6=table.col(colx=11)    # 返回第4列列中所有的单元格对象组成的列表
ser06=[]
for i in range(2,len(col6)):
    value=col6[i].value
    ser06.append(value)

plt.plot(u2,ser06,color = 'black',linestyle = '-',linewidth = 0.5,\
         marker = 'd',markerfacecolor = 'white', \
         markersize = 3,markeredgewidth = 1, label='方案12')


col7=table.col(colx=13)    # 返回第4列列中所有的单元格对象组成的列表
ser07=[]
for i in range(2,len(col7)):
    value=col7[i].value
    ser07.append(value)

plt.plot(u2,ser07,color = 'black',linestyle = '-',linewidth = 0.5,\
         marker = 'p',markerfacecolor = 'white', \
         markersize = 3,markeredgewidth = 1, label='损伤度0.6~0.7')


col8=table.col(colx=15)    # 返回第4列列中所有的单元格对象组成的列表
ser08=[]
for i in range(2,len(col8)):
    value=col8[i].value
    ser08.append(value)

plt.plot(u2,ser08,color = 'black',linestyle = '-',linewidth = 0.5,\
         marker = '+',markerfacecolor = 'white', \
         markersize = 3,markeredgewidth = 1, label='损伤度0.7~0.8')

col9=table.col(colx=17)    # 返回第4列列中所有的单元格对象组成的列表
ser09=[]
for i in range(2,len(col9)):
    value=col9[i].value
    ser09.append(value)

plt.plot(u2,ser09,color = 'black',linestyle = '-',linewidth = 0.5,\
         marker = '<',markerfacecolor = 'white', \
         markersize = 3,markeredgewidth = 1, label='损伤度0.8~0.9')

col10=table.col(colx=19)    # 返回第4列列中所有的单元格对象组成的列表
ser10=[]
for i in range(2,len(col10)):
    value=col10[i].value
    ser10.append(value)

plt.plot(u2,ser10,color = 'black',linestyle = '-',linewidth = 0.5,\
         marker = '>',markerfacecolor = 'white', \
         markersize = 5,markeredgewidth = 1, label='损伤度0.9~0.99')

col11=table.col(colx=21)    # 返回第4列列中所有的单元格对象组成的列表
ser11=[]
for i in range(2,len(col11)):
    value=col11[i].value
    ser11.append(value)

plt.plot(u2,ser11,color = 'black',linestyle = '-',linewidth = 0.5,\
         marker = '*',markerfacecolor = 'white', \
         markersize = 5,markeredgewidth = 1, label='损伤度0.99~1')
'''


#绘制图片的坐标轴
ax1=plt.gca()

#设置x轴和y轴的标签
ax1.set_xlabel('加载位移/mm',fontsize = 11)
ax1.set_ylabel('单元比例/%',fontsize = 11)
#ax1.set_xlabel('Displacement/mm',fontname = 'Times New Roman',fontsize = 11)
#ax1.set_ylabel('Load/kN',fontname = 'Times New Roman',fontsize = 11)


plt.yticks(fontproperties ='Times New Roman', size =11)
plt.xticks(fontproperties ='Times New Roman', size =11)

ax1.tick_params(axis='both',direction = 'in')

#plt.legend(prop={'family':'Times New Roman','size':14})
plt.legend(frameon=True,loc='upper left',fontsize='x-small')

#bbox_to_anchor=(0.88,0.6),



'''
###绘制散点图
table=data.sheet_by_name(sheet_name='Sheet2')    # 通过名称获取sheet


row0=table.row(rowx=0)    # 返回第0列列中所有的单元格对象组成的列表，横坐标信息
x=[]
for i in range(1,len(row0)):
    value=row0[i].value
    x.append(value)

row1=table.row(rowx=1)
y=[]
for i in range(1,len(row1)):
    value=row1[i].value
    y.append(value)



plt.scatter(x, y, s=50, c='black')

y1_value=0.8*max(y)
y1=[y1_value,y1_value,y1_value,y1_value,y1_value,y1_value]

plt.plot(x,y1,color = 'black',linestyle = ':',linewidth = 0.5, dashes=(5, 5), \
         marker = 'x',markerfacecolor = 'white', \
         markersize = 5,markeredgewidth = 1, label='最大极差80%分界线')


y2_value=0.5*max(y)
y2=[y2_value,y2_value,y2_value,y2_value,y2_value,y2_value]

plt.plot(x,y2,color = 'black',linestyle = ':',linewidth = 0.5, dashes=(5, 5), \
         marker = 'o',markerfacecolor = 'white', \
         markersize =5 ,markeredgewidth = 1, label='最大极差50%分界线')


#绘制图片的坐标轴
ax1=plt.gca()

#设置x轴和y轴的标签
ax1.set_xlabel('断裂功影响因素',fontsize = 11)
ax1.set_ylabel('极差',fontsize = 11)


plt.yticks(fontproperties ='Times New Roman', size =11)
plt.xticks(fontproperties ='Times New Roman', size =11)

ax1.tick_params(axis='both',direction = 'in')

#plt.legend(prop={'family':'Times New Roman','size':14})
plt.legend(frameon=True,loc='upper right',fontsize='small')
'''


###图像显示
plt.figure(dpi=300)
plt.show()        #显示图片

