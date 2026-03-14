#-*- coding:UTF-8 -*-
import xlsxwriter


###step1:读取文件信息
File_path='F:/biper/'
infile=open(File_path+'biper_040902.txt','r')
Inp_line=infile.readlines()
#读取模型帧数total_frame_num，包括第0帧
for i in range(len(Inp_line)):
    if Inp_line[i].startswith('total frame number'):
        total_frame_num=int(Inp_line[i+1])
        break
    else:
        pass

#读取每帧的位移，包括第0帧
u2=[]     #列表，里面依次存储加载点在每帧的竖向位移
for i in range(len(Inp_line)):
    if Inp_line[i].startswith('u2 in each frame'):
        u2_startline=i+1
        break
    else:
        pass
for j in range(u2_startline,u2_startline+total_frame_num):
    u2.append(float(Inp_line[j]))

#读取每帧的损伤比例
sdegDic={}    #键为帧数（包括第0帧），值为一个列表，里面依次是无损伤，轻度损伤，中度损伤和重度损伤的单元比例
for i in range(len(Inp_line)):
    if Inp_line[i].startswith('sdeg pro in each frame'):
        sdegDic_startline=i+1
        break
    else:
        pass
for i in range(total_frame_num):
    sdegDic[i]=[]
    sdeg_temp=[float (j) for j in Inp_line[sdegDic_startline+i].split(',')]
    sdegDic[i].extend(sdeg_temp)
'''
#读取最后一帧不同单元的重度损伤个数和比例
serious_num=[]     #最后一帧aa,cc,ca,as,cs的重度损伤单元的个数
serious_pro=[]     #最后一帧aa,cc,ca,as,cs的重度损伤单元的比例
for i in range(len(Inp_line)):
    if Inp_line[i].startswith('serious sdeg pro in lastframe'):
        serious_startline=i
        break
    else:
        pass
serious_num=[float (j) for j in Inp_line[serious_startline+1].split(',')]
serious_pro=[float (j) for j in Inp_line[serious_startline+2].split(',')]
'''


###step2:输出信息到excel中
#create a new Excel file and add a worksheet
#创建工作薄 workbook('demo.xlsx')
workbook=xlsxwriter.Workbook(File_path+'biper_040901.xlsx')
#创建工作表
worksheet = workbook.add_worksheet()

# Widen the first column to make the text clearer
# 设置一列或者多列单元属性
worksheet.set_column('C:F',16)
worksheet.set_column('I:J',14)
# Add a bold format to use to highlight cells
# 在工作表中创建一个新的格式对象来格式化单元格，实现加粗
bold = workbook.add_format({'bold': True})

worksheet.write('A1', 'frame', bold)
for i in range(total_frame_num):
    worksheet.write('A'+str(2+i), str(i))
worksheet.write('B1', 'u2/mm', bold)
for i in range(total_frame_num):
    worksheet.write('B'+str(2+i), str(-1*u2[i]))
'''
worksheet.write('C1', 'no_damage_pro/%', bold)
for i in range(total_frame_num):
    worksheet.write('C'+str(2+i), str(sdegDic[i][0]))
worksheet.write('D1', 'slight_pro/%', bold)
for i in range(total_frame_num):
    worksheet.write('D'+str(2+i), str(sdegDic[i][1]))
worksheet.write('E1', 'middle_pro/%', bold)
for i in range(total_frame_num):
    worksheet.write('E'+str(2+i), str(sdegDic[i][2]))
worksheet.write('F1', 'serious_pro/%', bold)
for i in range(total_frame_num):
    worksheet.write('F'+str(2+i), str(sdegDic[i][3]))

worksheet.write('I1', 'serious_num', bold)
worksheet.write('J1', 'serious_pro', bold)
worksheet.write('H2', 'aa', bold)
worksheet.write('H3', 'cc', bold)
worksheet.write('H4', 'ca', bold)
worksheet.write('H5', 'as', bold)
worksheet.write('H6', 'cs', bold)
for i in range(5):
    worksheet.write('I'+str(2+i), str(serious_num[i]))
    worksheet.write('J'+str(2+i), str(serious_pro[i]))
'''
worksheet.write('C1', '0-0.01/%', bold)
for i in range(total_frame_num):
    worksheet.write('C'+str(2+i), str(sdegDic[i][0]))
worksheet.write('D1', '0.01-0.1/%', bold)
for i in range(total_frame_num):
    worksheet.write('D'+str(2+i), str(sdegDic[i][1]))
worksheet.write('E1', '0.1-0.2/%', bold)
for i in range(total_frame_num):
    worksheet.write('E'+str(2+i), str(sdegDic[i][2]))
worksheet.write('F1', '0.2-0.3/%', bold)
for i in range(total_frame_num):
    worksheet.write('F'+str(2+i), str(sdegDic[i][3]))
worksheet.write('G1', '0.3-0.4/%', bold)
for i in range(total_frame_num):
    worksheet.write('G'+str(2+i), str(sdegDic[i][4]))
worksheet.write('H1', '0.4-0.5/%', bold)
for i in range(total_frame_num):
    worksheet.write('H'+str(2+i), str(sdegDic[i][5]))
worksheet.write('I1', '0.5-0.6/%', bold)
for i in range(total_frame_num):
    worksheet.write('I'+str(2+i), str(sdegDic[i][6]))
worksheet.write('J1', '0.6-0.7/%', bold)
for i in range(total_frame_num):
    worksheet.write('J'+str(2+i), str(sdegDic[i][7]))
worksheet.write('K1', '0.7-0.8/%', bold)
for i in range(total_frame_num):
    worksheet.write('K'+str(2+i), str(sdegDic[i][8]))
worksheet.write('L1', '0.8-0.9/%', bold)
for i in range(total_frame_num):
    worksheet.write('L'+str(2+i), str(sdegDic[i][9]))
worksheet.write('M1', '0.9-0.99/%', bold)
for i in range(total_frame_num):
    worksheet.write('M'+str(2+i), str(sdegDic[i][10]))
worksheet.write('N1', '0.99-1.1/%', bold)
for i in range(total_frame_num):
    worksheet.write('N'+str(2+i), str(sdegDic[i][11]))


'''
worksheet.write('O1', '0.99-1.1/%', bold)
for i in range(total_frame_num):
    worksheet.write('O'+str(2+i), str(sdegDic[i][12]))
worksheet.write('P1', '0.99-1.1/%', bold)
for i in range(total_frame_num):
    worksheet.write('P'+str(2+i), str(sdegDic[i][13]))
worksheet.write('Q1', '0.99-1.1/%', bold)
for i in range(total_frame_num):
    worksheet.write('Q'+str(2+i), str(sdegDic[i][14]))
'''

#关闭工作薄
workbook.close()
