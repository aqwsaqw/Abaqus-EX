#-*-coding:utf-8-*-
from abaqus import *
from abaqusConstants import *
import time
print "===begin==="
jobs=mdb.jobs.keys()
#获得所有任务名称
for i in jobs:
    myJob=mdb.jobs[i]
    if myJob.status==None:
        t0=time.time()
        myJob.submit()
        myJob.waitForCompletion()
        print '%s has finished, cost %f min' %(i,(time.time()-t0)/60)

print "===finish==="
