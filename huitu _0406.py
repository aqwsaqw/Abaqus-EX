#-*- coding:UTF-8 -*-
import xlrd
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
plt.rc('font',family='SimHei')
import numpy as np


#读取数据
#导入需要读取Excel表格的路径
data=xlrd.open_workbook(r'C:\Users\zs\Desktop\big_paper\huitu\data_sum.xlsx')



###绘制曲线图
table=data.sheet_by_name(sheet_name='Sheet1')    # 通过名称获取sheet

###曲线1
col0=table.col(colx=0)    # 返回第0列列中所有的单元格对象组成的列表，横坐标信息
u1=[]
for i in range(2,len(col0)):
    value=col0[i].value
    if type(value)==float:
        u1.append(value)
    else:
        pass

col1=table.col(colx=1)    # 返回第2列列中所有的单元格对象组成的列表，第一组纵坐标信息
ser01=[]
for i in range(2,len(col1)):
    value=col1[i].value
    if type(value)==float:
        ser01.append(value)
    else:
        pass

plt.plot(u1,ser01,color = 'black',linestyle = '-',linewidth = 0.5)
         #marker = 'x',markerfacecolor = 'white', \
         #markersize = 3,markeredgewidth = 1, label = '小梁试件1'


k=int(len(u1)/43)
x=[]
y=[]
for i in range(45):
    x.append(u1[k*i])
    y.append(ser01[k*i])

plt.scatter(x,y,color = 'black',marker = 'x', s = 12,label = '小梁试件1')

###曲线2
col2=table.col(colx=2)    # 返回第0列列中所有的单元格对象组成的列表，横坐标信息
u2=[]
for i in range(2,len(col2)):
    value=col2[i].value
    if type(value)==float:
        u2.append(value)
    else:
        pass


col3=table.col(colx=3)    # 返回第2列列中所有的单元格对象组成的列表，第一组纵坐标信息
ser02=[]
for i in range(2,len(col3)):
    value=col3[i].value
    if type(value)==float:
        ser02.append(value)
    else:
        pass


plt.plot(u2,ser02,color = 'black',linestyle = '-',linewidth = 0.5,\
         #marker = 'x',markerfacecolor = 'white', \
         #markersize = 3,markeredgewidth = 1, label = '小梁试件1'
         )

k=int(len(u2)/43)
x=[]
y=[]
for i in range(44):
    x.append(u2[k*i])
    y.append(ser02[k*i])


plt.scatter(x,y,color = 'black',marker = '^', s = 12,label = '小梁试件2')


###曲线3
col4=table.col(colx=4)    # 返回第0列列中所有的单元格对象组成的列表，横坐标信息
u3=[]
for i in range(2,len(col4)):
    value=col4[i].value
    if type(value)==float:
        u3.append(value)
    else:
        pass


col5=table.col(colx=5)    # 返回第2列列中所有的单元格对象组成的列表，第一组纵坐标信息
ser03=[]
for i in range(2,len(col5)):
    value=col5[i].value
    if type(value)==float:
        ser03.append(value)
    else:
        pass


plt.plot(u3,ser03,color = 'black',linestyle = '-',linewidth = 0.5,\
         #marker = 'x',markerfacecolor = 'white', \
         #markersize = 3,markeredgewidth = 1, label = '小梁试件1'
         )

k=int(len(u3)/45)
x=[]
y=[]
for i in range(46):
    x.append(u3[k*i])
    y.append(ser03[k*i])


plt.scatter(x,y,color = 'black',marker = 'o', s = 12,label = '小梁试件3')




###曲线4
col6=table.col(colx=6)    # 返回第0列列中所有的单元格对象组成的列表，横坐标信息
u4=[]
for i in range(2,len(col6)):
    value=col6[i].value
    if type(value)==float:
        u4.append(value)
    else:
        pass


col7=table.col(colx=7)    # 返回第2列列中所有的单元格对象组成的列表，第一组纵坐标信息
ser04=[]
for i in range(2,len(col7)):
    value=col7[i].value
    if type(value)==float:
        ser04.append(value)
    else:
        pass


plt.plot(u4,ser04,color = 'black',linestyle = '-',linewidth = 0.5,\
         #marker = 'x',markerfacecolor = 'white', \
         #markersize = 3,markeredgewidth = 1, label = '小梁试件1'
         )

k=int(len(u4)/45)
x=[]
y=[]
for i in range(48):
    x.append(u4[k*i])
    y.append(ser04[k*i])


plt.scatter(x,y,color = 'black',marker = 'v', s = 12,label = '小梁试件4')



###曲线5
col8=table.col(colx=8)    # 返回第0列列中所有的单元格对象组成的列表，横坐标信息
u5=[]
for i in range(2,len(col8)):
    value=col8[i].value
    if type(value)==float:
        u5.append(value)
    else:
        pass


col9=table.col(colx=9)    # 返回第2列列中所有的单元格对象组成的列表，第一组纵坐标信息
ser05=[]
for i in range(2,len(col9)):
    value=col9[i].value
    if type(value)==float:
        ser05.append(value)
    else:
        pass


plt.plot(u5,ser05,color = 'black',linestyle = '-',linewidth = 0.5,\
         #marker = 'x',markerfacecolor = 'white', \
         #markersize = 3,markeredgewidth = 1, label = '小梁试件1'
         )

k=int(len(u5)/42)
x=[]
y=[]
for i in range(44):
    x.append(u5[k*i])
    y.append(ser05[k*i])


plt.scatter(x,y,color = 'black',marker = 's', s = 12,label = '小梁试件5')


###曲线6
col10=table.col(colx=10)    # 返回第0列列中所有的单元格对象组成的列表，横坐标信息
u6=[]
for i in range(2,len(col10)):
    value=col10[i].value
    if type(value)==float:
        u6.append(value)
    else:
        pass


col11=table.col(colx=11)    # 返回第2列列中所有的单元格对象组成的列表，第一组纵坐标信息
ser06=[]
for i in range(2,len(col11)):
    value=col11[i].value
    if type(value)==float:
        ser06.append(value)
    else:
        pass


plt.plot(u6,ser06,color = 'black',linestyle = '-',linewidth = 0.5,\
         #marker = 'x',markerfacecolor = 'white', \
         #markersize = 3,markeredgewidth = 1, label = '小梁试件1'
         )

k=int(len(u6)/40)
x=[]
y=[]
for i in range(43):
    x.append(u6[k*i])
    y.append(ser06[k*i])


plt.scatter(x,y,color = 'black',marker = 'd', s = 12,label = '小梁试件6')

'''
###曲线7
col12=table.col(colx=12)    # 返回第0列列中所有的单元格对象组成的列表，横坐标信息
u7=[]
for i in range(2,len(col12)):
    value=col12[i].value
    if type(value)==float:
        u7.append(value)
    else:
        pass

col13=table.col(colx=13)    # 返回第2列列中所有的单元格对象组成的列表，第一组纵坐标信息
ser07=[]
for i in range(2,len(col13)):
    value=col13[i].value
    if type(value)==float:
        ser07.append(value)
    else:
        pass


plt.plot(u7,ser07,color = 'black',linestyle = '-',linewidth = 2,\
         #marker = 'x',markerfacecolor = 'white', \
         #markersize = 3,markeredgewidth = 1, label = '小梁试件1'
         )

k=int(len(u7)/40)
x=[]
y=[]
for i in range(40):
    x.append(u7[k*i])
    y.append(ser07[k*i])


plt.scatter(x,y,color = 'black',marker = 'p', s = 24,label = '模拟结果')

'''




#绘制图片的坐标轴
#x_major_locator=MultipleLocator(0.5)
#y_major_locator=MultipleLocator(0.2)
ax1=plt.gca()
#ax1.xaxis.set_major_locator(x_major_locator)
#ax1.yaxis.set_major_locator(y_major_locator)
#plt.xlim(-0.5,4.0)
#plt.ylim(0,1.2)

#设置x轴和y轴的标签
ax1.set_xlabel('位移/mm',fontsize = 11)
ax1.set_ylabel('荷载/kN',fontsize = 11)






plt.yticks(fontproperties ='Times New Roman', size =11)
plt.xticks(fontproperties ='Times New Roman', size =11)

ax1.tick_params(axis='both',direction = 'in')

#plt.legend(prop={'family':'Times New Roman','size':14})
plt.legend(frameon=True,loc='upper right',fontsize='x-small')






###图像显示
plt.figure(dpi=300)
plt.show()        #显示图片

