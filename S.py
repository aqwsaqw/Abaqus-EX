# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 11:55:44 2026

@author: aqwsa
"""

from abaqus import *
from odbAccess import *
from abaqusConstants import *
from caeModules import *
import numpy as np

odb_path='E:\\temp\\260106\\260106_cal.odb'
instance_name='PART-1-1'
element_set_name='A_SET'
file_path="E:\\temp\\260106\\260106_s11.txt"
threshold=0.95  # 损伤大于xx的单元
outfile = open(file_path, 'w+')
def extract_s_from_set(odb_path, instance_name, element_set_name, threshold=None):
    """
    从指定单元集中提取SDEG数据
    odb_path = ""
    参数:
        odb_path: ODB文件路径
        instance_name: 部件实例名称
        element_set_name: 单元集名称
        threshold: 损伤阈值（可选），只提取大于该值的数据
    
    返回:
        dictionary: 包含SDEG数据的字典
    """
    odb=openOdb(path=odb_path)
    

    instance = odb.rootAssembly.instances[instance_name]
    element_set = instance.elementSets[element_set_name]
        
    results = {}
        
        # 帧
    frame=odb.steps['Step-1'].frames[6]            
        
    stress_field = frame.fieldOutputs['S']
    i = 0
       # 提取S11数据          
    stress_on_set = frame.fieldOutputs['S'].getSubset(region=element_set)
    data = []
    for value in stress_field.values:
           i = i + 1
           # S11是应力张量的第一个分量
           s11_value = value.data[0]  # 对于张量输出，data[0]是S11
           
 
           # 获取单元标签和积分点信息
           element_label = value.elementLabel
           int_point = getattr(value, 'integrationPoint', 1)
           
           # 获取节点标签（如果存在）
           node_label = getattr(value, 'nodeLabel', None)
           '''
           data.append({
            'frame_id': frame.frameId,
            'element': element_label,
            'integration_point': int_point,
            'node': node_label,
            's11': s11_value
        })
           '''
           print("%d",i)
           print>>outfile,'%5f,'%(s11_value)
            
    #lendata = len(element_data)
    #alldata = len(all_data)
            # 统计信息

    print(lendata,"/",alldata)           
    return results
        
    

result = extract_s_from_set(odb_path,instance_name,element_set_name,threshold)

print ("AWWWW")
