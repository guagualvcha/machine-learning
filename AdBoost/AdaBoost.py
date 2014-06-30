# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 09:04:53 2014

@author: zjubfd
"""
from pylab import *
"""
单层决策数分类
"""
def stumpClassify(dataMat,dimen,threshVal,threshIneq):
    if threshIneq=='lt':
        retlist=[1 if dvector[dimen]<threshVal else -1 for dvector in dataMat]
        return array(retlist)
    else:
        retlist=[1 if dvector[dimen]>threshVal else -1 for dvector in dataMat]
        return array(retlist)
"""
构建最优单层决策数
"""
def buildStump(dataArr,labels,D):
    m,n=dataArr.shape
    min_rate=inf
    bestStump=dict()
    for dimen in range(n):
        maxrange=max(dataArr[:,dimen])
        minrange=min(dataArr[:,dimen])
        threshVals=linspace(minrange-1,maxrange+1,100)
        for threshVal in threshVals:
            for threshIneq in ['lt','gt']:
               retlist=stumpClassify(dataArr,dimen,threshVal,threshIneq)  
               errArr=(labels*retlist==-1)
               error_rate=sum(errArr*D)
               if error_rate<min_rate:
                   min_rate=error_rate
                   alpha=0.5*log((1-min_rate)/max(min_rate,1e-16))
                   newD=array([D[i]*exp(alpha) if errArr[i] else D[i]*exp(-alpha) for i in range(m) ])
                   newD=newD/sum(newD)
                   bestStump['dimen']=dimen
                   bestStump['threshVal']=threshVal
                   bestStump['threshIneq']=threshIneq
                   bestStump['minerror']=min_rate
                   bestStump['bestclass']=retlist
                   bestStump['newD']=newD
                   bestStump['alpha']=alpha
                   bestStump['D']=D
    return bestStump

"""
利用决策树模型单层决策树分类
"""
def predict(dataArr,bestStump):
    return stumpClassify(dataArr,bestStump['dimen'],bestStump['threshVal'],bestStump['threshIneq'])

"""
构建adaboost模型
"""   
def adaBoostTrainDs(dataArr,labels,numite=9):
    D=ones(len(labels))/len(labels)
    bss=[]
    plabels=zeros(dataArr.shape[0])   
    for i in range(numite):
        bs=buildStump(dataArr,labels,D)
        bss.append(bs)
        D=bs['newD']
        plabels+=bs['alpha']*bs['bestclass']
        perror=(array([1 if label>0 else -1 for label in plabels])*labels==-1)
        error_rate=float(sum(perror))/len(labels)
        print '%d iteration,error_rate is %f'%(i,error_rate)
        if error_rate==0:
            break
    return bss
 
"""
adaboost模型预测
"""   
def adaBoostPredictDs(dataArr,bss):
    labels=zeros(dataArr.shape[0])    
    for bs in bss:
        labels+=bs['alpha']*predict(dataArr,bs)
    return array([1. if label>0 else -1. for label in labels])
        
def file2data(filename):
    fr=open(filename)
    dataList=[]
    labelsList=[]
    for line in fr.readlines():
        lineArr=line.strip().split()
        dataList.append(map(float,lineArr[:-1]))
        labelsList.append(float(lineArr[-1]))
    return array(dataList),array(labelsList)
        
"""
testcase
"""      
if __name__=='__main__':
    #test1
    dataArr=array([[1.,2.1],[2.,1.1],[1.3,1.],[1.,1.],[2.,1.]])
    labels=array([1.,1.,-1.,-1.,1.])
    bss=adaBoostTrainDs(dataArr,labels)
    plabels=adaBoostPredictDs(dataArr,bss)
    print 'labels is',labels
    print 'plabels is ',plabels
    #test2
    dataArr,labels=file2data('horseColicTraining2.txt')
    bss=adaBoostTrainDs(dataArr,labels)
    testArr,tlabels=file2data('horseColicTest2.txt')
    plabels=adaBoostPredictDs(testArr,bss)
    print tlabels-plabels
    print float(sum(abs(tlabels-plabels)/2))/len(tlabels)
    


                   
                   