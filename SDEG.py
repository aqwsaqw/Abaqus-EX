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

odb_path='E:\\temp\\260106\\260106-conn.odb'
instance_name='PART-1-1'
element_set_name='AS_SET'
file_path="E:\\temp\\260106\\260106_sdeg_con.txt"
threshold=0.95  # 损伤大于xx的单元
outfile = open(file_path, 'w+')
def extract_sdeg_from_set(odb_path, instance_name, element_set_name, threshold=None):
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
        
        # 最后一帧
    last_frame = odb.steps.values()[-1].frames[2]
        
    if 'SDEG' in last_frame.fieldOutputs:
            # 使用getSubset提取特定单元集的SDEG
        sdeg_on_set = last_frame.fieldOutputs['SDEG'].getSubset(region=element_set)
            
            # 提取数据
        element_data = []
        all_data = []
        for value in sdeg_on_set.values:
            all_data.append(value.data)
            #print '1', file=outfile
            k = value.data
            print>>outfile,'%5f,'%(k)
            if threshold is None or value.data > threshold:
                element_data.append({
                        'element_label': value.elementLabel,
                        'integration_point': getattr(value, 'integrationPoint', 1),
                        'sdeg_value': value.data
                    })
            
        results[last_frame.frameId] = element_data
            
        lendata = len(element_data)
        alldata = len(all_data)
            # 统计信息
        if element_data:
            sdeg_array = np.array([d['sdeg_value'] for d in element_data])
            results['statistics'] = {
                    'min': float(sdeg_array.min()),
                    'max': float(sdeg_array.max()),
                    'mean': float(sdeg_array.mean()),
                    'count': len(element_data)
                }
        print(lendata,"/",alldata)           
        return results
        
    

result = extract_sdeg_from_set(odb_path,instance_name,element_set_name,threshold)

print ("AWWWW")
