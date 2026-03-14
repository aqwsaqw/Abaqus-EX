#-*- coding:UTF-8 -*-
from odbAccess import *
File_path='G:/'
odb=openOdb(File_path+'biper_val_08.odb')



###step1:获取CZM单元编号与单元类型的对应关系
assembly=odb.rootAssembly
care=assembly.instances['PART-1-1']

'''
aa_set=[]     #列表，储存所有aa单元的编号
aa_ele=care.elementSets['AA_SET'].elements
for i in range(len(aa_ele)):
    aa_set.append(aa_ele[i].label)

cc_set=[]
cc_ele=care.elementSets['CC_SET'].elements
for i in range(len(cc_ele)):
    cc_set.append(cc_ele[i].label)

ca_set=[]
ca_ele=care.elementSets['AC_SET'].elements
for i in range(len(ca_ele)):
    ca_set.append(ca_ele[i].label)

as_set=[]
as_ele=care.elementSets['AS_SET'].elements
for i in range(len(as_ele)):
    as_set.append(as_ele[i].label)

cs_set=[]
cs_ele=care.elementSets['CS_SET'].elements
for i in range(len(cs_ele)):
    cs_set.append(cs_ele[i].label)


print 'aa',len(aa_set)
print 'cc',len(cc_set)
print 'ca',len(ca_set)
print 'as',len(as_set)
print 'cs',len(cs_set)
'''



###step2:读取每帧每个单元的sdeg
sdegDic={}   #键为帧的编号，值为一个字典，即sdegDic[i]
             #sdegDic[i]={},该字典的键为单元编号，值为一个列表，列表里是该单元在这帧的sdeg
i=0
for frame in odb.steps['Step-1'].frames:             ####遍历每一帧
    sdegframe=frame.fieldOutputs['SDEG']
    sdegDic[i]={}
    for v in sdegframe.values:
        sdegDic[i][v.elementLabel]=[frame.frameValue,v.data]           ####存储帧时间以及帧SDEG
    i+=1
total_frame_num=i   #总帧数，包括第0帧


###step3:获取每帧加载点的位移
disDic={}     #键为帧的编号，值为一个列表，里面是加载点在这帧的竖向位移
i=0
top=odb.rootAssembly.nodeSets['TOP']
for frame in odb.steps['Step-1'].frames:
    dis=frame.fieldOutputs['U']
    topDis=dis.getSubset(region=top)
    for v in topDis.values:
        u2=v.data[1]
    disDic[i]=[u2]
    i+=1

'''
###step4:获取每帧sdeg比例
no_damage=0
slight=0
middle=0
serious=0
prono_damage={}             ###无损伤,键为帧数，值为一个列表，里面是该帧时的无损伤比例
proslight={}                ###轻微损伤
promiddle={}                ###中度损伤
proserious={}               ###重度损伤
total=float(len(sdegDic[1].keys()))
for i in sdegDic.keys():
    for j in sdegDic[i].keys():
        if sdegDic[i][j][1] == 0:
            no_damage+= 1
        elif 0<sdegDic[i][j][1]<=0.9:
            slight+=1
        elif sdegDic[i][j][1]>0.9 and sdegDic[i][j][1]<=0.99:
            middle +=1
        else:
            serious+=1
    prono_damage[i]=[float(no_damage)/total*100]
    proslight[i]=[float(slight)/total*100]
    promiddle[i]=[float(middle)/total*100]
    proserious[i]=[float(serious)/total*100]
    no_damage=0
    middle=0
    slight = 0
    serious = 0




###step4:获取每帧sdeg比例
no_damage=0
slight=0
middle=0
serious=0
prono_damage={}             ###无损伤,键为帧数，值为一个列表，里面是该帧时的无损伤单元集合
proslight={}                ###轻微损伤
promiddle={}                ###中度损伤
proserious={}               ###重度损伤
total=float(len(sdegDic[1].keys()))
for i in sdegDic.keys():
    prono_damage[i]=[]
    proslight[i]=[]
    promiddle[i]=[]
    proserious[i]=[]
    for j in sdegDic[i].keys():
        if sdegDic[i][j][1] == 0:
            prono_damage[i].append(j)
        elif 0<sdegDic[i][j][1]<=0.9:
            proslight[i].append(j)
        elif sdegDic[i][j][1]>0.9 and sdegDic[i][j][1]<=0.99:
            promiddle[i].append(j)
        else:
            proserious[i].append(j)



###step5:获取每一帧时不同单元损伤破坏的比例
difele_dic={}    #键为贞，值为列表，依次记录
for i in sdegDic.keys():
    slight_ele=proslight[i]
    middle_ele=promiddle[i]
    serious_ele=proserious[i]
    aa_slight=set(aa_set)&set(slight_ele)
    aa_slight_pro=float(len(aa_slight))/float(len(aa_set))
    aa_middle=set(aa_set)&set(middle_ele)
    aa_middle_pro=float(len(aa_middle))/float(len(aa_set))
    aa_serious=set(aa_set)&set(serious_ele)
    aa_serious_pro=float(len(aa_serious))/float(len(aa_set))

    cc_slight=set(cc_set)&set(slight_ele)
    cc_slight_pro=float(len(cc_slight))/float(len(cc_set))
    cc_middle=set(cc_set)&set(middle_ele)
    cc_middle_pro=float(len(cc_middle))/float(len(cc_set))
    cc_serious=set(cc_set)&set(serious_ele)
    cc_serious_pro=float(len(cc_serious))/float(len(cc_set))

    ca_slight=set(ca_set)&set(slight_ele)
    ca_slight_pro=float(len(ca_slight))/float(len(ca_set))
    ca_middle=set(ca_set)&set(middle_ele)
    ca_middle_pro=float(len(ca_middle))/float(len(ca_set))
    ca_serious=set(ca_set)&set(serious_ele)
    ca_serious_pro=float(len(ca_serious))/float(len(ca_set))

    as_slight=set(as_set)&set(slight_ele)
    as_slight_pro=float(len(as_slight))/float(len(as_set))
    as_middle=set(as_set)&set(middle_ele)
    as_middle_pro=float(len(as_middle))/float(len(as_set))
    as_serious=set(as_set)&set(serious_ele)
    as_serious_pro=float(len(as_serious))/float(len(as_set))

    cs_slight=set(cs_set)&set(slight_ele)
    cs_slight_pro=float(len(cs_slight))/float(len(cs_set))
    cs_middle=set(cs_set)&set(middle_ele)
    cs_middle_pro=float(len(cs_middle))/float(len(cs_set))
    cs_serious=set(cs_set)&set(serious_ele)
    cs_serious_pro=float(len(cs_serious))/float(len(cs_set))

    difele_dic[i]=[aa_slight_pro,aa_middle_pro,aa_serious_pro,cc_slight_pro,cc_middle_pro,cc_serious_pro,\
                   ca_slight_pro,ca_middle_pro,ca_serious_pro,as_slight_pro,as_middle_pro,as_serious_pro,\
                   cs_slight_pro,cs_middle_pro,cs_serious_pro]
'''






'''
分为12个等级
0~0.01
0.01~0.1
0.1~0.2
0.2-0.3
0.3-0.4
0.4-0.5
0.5-0.6
0.6-0.7
0.7-0.8
0.8-0.9
0.9-0.99
0.99-1.1
'''


dma01=0
dma02=0
dma03=0
dma04=0
dma05=0
dma06=0
dma07=0
dma08=0
dma09=0
dma10=0
dma11=0
dma12=0
dma01_lib={}             ###无损伤,键为帧数，值为一个列表，里面是该帧时的无损伤比例
dma02_lib={}
dma03_lib={}
dma04_lib={}
dma05_lib={}
dma06_lib={}
dma07_lib={}
dma08_lib={}
dma09_lib={}
dma10_lib={}
dma11_lib={}
dma12_lib={}
total=float(len(sdegDic[1].keys()))
for i in sdegDic.keys():
    for j in sdegDic[i].keys():
        if sdegDic[i][j][1]<=0.01:
            dma01+=1
        elif 0.01<sdegDic[i][j][1]<=0.1:
            dma02+=1
        elif 0.1<sdegDic[i][j][1]<=0.2:
            dma03+=1
        elif 0.2<sdegDic[i][j][1]<=0.3:
            dma04+=1
        elif 0.3<sdegDic[i][j][1]<=0.4:
            dma05+=1
        elif 0.4<sdegDic[i][j][1]<=0.5:
            dma06+=1
        elif 0.5<sdegDic[i][j][1]<=0.6:
            dma07+=1
        elif 0.6<sdegDic[i][j][1]<=0.7:
            dma08+=1
        elif 0.7<sdegDic[i][j][1]<=0.8:
            dma09+=1
        elif 0.8<sdegDic[i][j][1]<=0.9:
            dma10+=1
        elif 0.9<sdegDic[i][j][1]<=0.99:
            dma11+=1
        else:
            dma12+=1
    dma01_lib[i]=[float(dma01)/total*100]
    dma02_lib[i]=[float(dma02)/total*100]
    dma03_lib[i]=[float(dma03)/total*100]
    dma04_lib[i]=[float(dma04)/total*100]
    dma05_lib[i]=[float(dma05)/total*100]
    dma06_lib[i]=[float(dma06)/total*100]
    dma07_lib[i]=[float(dma07)/total*100]
    dma08_lib[i]=[float(dma08)/total*100]
    dma09_lib[i]=[float(dma09)/total*100]
    dma10_lib[i]=[float(dma10)/total*100]
    dma11_lib[i]=[float(dma11)/total*100]
    dma12_lib[i]=[float(dma12)/total*100]
    dma01=0
    dma02=0
    dma03=0
    dma04=0
    dma05=0
    dma06=0
    dma07=0
    dma08=0
    dma09=0
    dma10=0
    dma11=0
    dma12=0

'''
###step5:获取最后一帧时不同单元重度破坏的比例
serious_ele=[]     #列表，储存重度损伤单元的编号
for i in sdegDic[total_frame_num-1].keys():
    if sdegDic[total_frame_num-1][i]>=0.99:
        serious_ele.append(i)
    else:
        pass

aa_serious=set(aa_set)&set(serious_ele)     #最后一帧aa单元重度损伤的单元号集合
aa_serious_pro=float(len(aa_serious))/float(len(serious_ele))    #最后一帧aa单元重度损伤的比例
cc_serious=set(cc_set)&set(serious_ele)
cc_serious_pro=float(len(cc_serious))/float(len(serious_ele))
ca_serious=set(ca_set)&set(serious_ele)
ca_serious_pro=float(len(ca_serious))/float(len(serious_ele))
as_serious=set(as_set)&set(serious_ele)
as_serious_pro=float(len(as_serious))/float(len(serious_ele))
cs_serious=set(cs_set)&set(serious_ele)
cs_serious_pro=float(len(cs_serious))/float(len(serious_ele))
'''


###step6:输出数据到txt
outFile_path='F:/biper/'
outfile=open(outFile_path+'biper_040902.txt', 'w+')

Title='total frame number'
print>>outfile,Title
outfile.flush()
print>>outfile,total_frame_num
outfile.flush()

Title='u2 in each frame'
print>>outfile,Title
outfile.flush()
for i in range(total_frame_num):
    print>>outfile, "%5f"%(disDic[i][0])
    outfile.flush()


'''
#依次输出无损伤，轻度损伤，中度损伤，重度损伤单元的比例
Title='sdeg pro in each frame'
print>>outfile,Title
outfile.flush()
for i in range(total_frame_num):
    print>>outfile,"%5f, %5f, %5f, %5f" %(prono_damage[i][0],proslight[i][0],promiddle[i][0],proserious[i][0])
    outfile.flush()

#依次输出最后一帧aa,cc,ca,as,cs单元占重度损伤的比例
Title='serious sdeg pro in lastframe'
print>>outfile,Title
outfile.flush()
print>>outfile,"%5d, %5d, %5d, %5d, %5d" %(len(aa_serious),len(cc_serious),len(ca_serious),len(as_serious),len(cs_serious))
outfile.flush()
print>>outfile,"%5f, %5f, %5f, %5f, %5f" %(aa_serious_pro,cc_serious_pro,ca_serious_pro,as_serious_pro,cs_serious_pro)
outfile.flush()
'''
Title='sdeg pro in each frame'
print>>outfile,Title
outfile.flush()
for i in range(total_frame_num):
    print>>outfile,"%5f, %5f, %5f, %5f, %5f, %5f, %5f, %5f, %5f, %5f, %5f, %5f" \
                   %(dma01_lib[i][0],dma02_lib[i][0],dma03_lib[i][0],dma04_lib[i][0],dma05_lib[i][0],dma06_lib[i][0],\
                     dma07_lib[i][0],dma08_lib[i][0],dma09_lib[i][0],dma10_lib[i][0],dma11_lib[i][0],dma12_lib[i][0])
    outfile.flush()

'''
Title='sdeg pro in each frame'
print>>outfile,Title
outfile.flush()
for i in range(total_frame_num):
    print>>outfile,"%5f, %5f, %5f, %5f, %5f, %5f, %5f, %5f, %5f, %5f, %5f, %5f, %5f, %5f, %5f" \
                   %(difele_dic[i][0],difele_dic[i][1],difele_dic[i][2],difele_dic[i][3],difele_dic[i][4],difele_dic[i][5],\
                     difele_dic[i][6],difele_dic[i][7],difele_dic[i][8],difele_dic[i][9],difele_dic[i][10],difele_dic[i][11],\
                     difele_dic[i][12],difele_dic[i][13],difele_dic[i][14],)
    outfile.flush()
'''
print 'finish'





