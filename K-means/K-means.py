# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 12:05:25 2014

@author: uncle_bai
"""
from numpy import *
from  matplotlib import pyplot as plt 

class KistoBig(Exception):
    def __init__(self,data):
        self.__data = data
    def __str__(self):  # 相当于 str(#)
        return self.__data
    
def file2data(filename):
    fr=open(filename)
    dataList=[]
    for line in fr.readlines():
        lineArr=map(float,line.strip().split())
        dataList.append(lineArr)
    return array(dataList)

def distEclud(v1,v2):
    return sqrt(sum(pow(v1-v2,2)))

def randCent(dataSet,k,distMean=distEclud,numtry=20):
    m,n=dataSet.shape
    centpoints=zeros((k,n))
    trytime=1
    while trytime<numtry:
        for i in range(n):
            maxval=max(dataSet[:,i])
            minval=min(dataSet[:,i])
            rangep=maxval-minval
            for j in range(k):
                centpoints[j,i]=minval+random.random()*rangep
        if checkRandCent(dataSet,centpoints,k,distMean):
            break
        trytime+=1
        print 'try again'
    if trytime==numtry:
        raise KistoBig('k maybe too big for the data')
    return centpoints

def checkRandCent(dataSet,centpoints,k,distMean=distEclud):
    m=dataSet.shape[0]
    containSet=set()
    for i in  range(m):
        vector=dataSet[i,:]
        dist=[distMean(vector,centpoint) for centpoint in centpoints]
        mindis=min(dist)
        index=dist.index(mindis)
        containSet.add(index)
    return len(containSet)==k
    
def kMeans(dataSet,k,distMean=distEclud,creatCent=randCent):
    m,n=shape(dataSet)
    centpoints=creatCent(dataSet,k)
    centChanged=True
    clusterAss=zeros((m,2))
    while centChanged:
        centChanged=False
        for i in range(m):
            vector=dataSet[i,:]
            dist=[distMean(vector,centpoint) for centpoint in centpoints]
            mindis=min(dist)
            index=dist.index(mindis)
            clusterAss[i,1]=mindis**2
            if clusterAss[i,0]!=index:
                centChanged=True
                clusterAss[i,0]=index
        for i in range(k):
            clusteri=dataSet[nonzero(clusterAss[:,0]==i)[0],:]
            centpoints[i,:]=mean(clusteri,0)
    return centpoints,clusterAss
            
def test1():
    dataSet=file2data('testSet.txt')
    plt.scatter(dataSet[:,0],dataSet[:,1])
    centpoints,clusterAss=kMeans(dataSet,10)
    plt.scatter(centpoints[:,0],centpoints[:,1],c='r',linewidth=10)
    plt.show()
    
    
"""
后处理技术提高聚类效果，二分法
"""
def bikMeans(dataSet,k,distMean=distEclud,creatCent=randCent):
    m=dataSet.shape[0]    
    clusterAss=zeros((m,2))    
    centList=[mean(dataSet,0)]
    for j in range(m):
        clusterAss[j,1]=distMean(centList[0],dataSet[j,:])**2
    while len(centList)<k:
        print '有%d个聚类中心'%len(centList)
        lowestSSE=inf
        for i in range(len(centList)):
            print '对第%i聚类中心个进行切分'%i
            clusteridata=dataSet[nonzero(clusterAss[:,0]==i)[0],:]
            print '属于第%d个聚类中心的数据有%d'%(i,len(clusteridata))
            print '开始切分'
            centi,clusteriAss=kMeans(clusteridata,2,distMean,creatCent)
            print '切分为:',sum(clusteriAss[:,0]),len(clusteriAss)-sum(clusteriAss[:,0])

            sseSplit=sum(clusteriAss[:,1])
            sseNotSplit=sum(clusterAss[nonzero(clusterAss[:,0]!=i)[0],1])
            if sseNotSplit+sseSplit<lowestSSE:
                lowestSSE=sseNotSplit+sseSplit
                bestcentIndex=i
                bestAss=clusteriAss.copy()
                bestcent=centi.copy()
        print '最终选择聚类中心',bestcentIndex,'切分为',bestcentIndex,len(centList)
        print '坐标分别为',nonzero(bestAss[:,0]==0)[0],nonzero(bestAss[:,0]==1)[0]
        print 'bestAss',bestAss
#        bestAss[nonzero(bestAss[:,0]==0)[0],0]=bestcentIndex
#        bestAss[nonzero(bestAss[:,0]==1)[0],0]=len(centList)
        for i in range(bestAss.shape[0]):
            if bestAss[i,0]==0:
                bestAss[i,0]=bestcentIndex
            else:
                bestAss[i,0]=len(centList)
        
        
        print 'bestAss is',bestAss
#        print 'before'
#        print 'bestAss',bestAss
#        print 'clusterAss',clusterAss
        clusterAss[nonzero(clusterAss[:,0]==bestcentIndex)[0],:]=bestAss
        print '分别占',sum(clusterAss[:,0]==bestcentIndex),sum(clusterAss[:,0]==len(centList))
#        print 'after'
#        print 'clusterAss',clusterAss
        centList[bestcentIndex]=bestcent[0,:]
        centList.append(bestcent[1,:])      
    return array(centList),clusterAss

    
def test2():
    dataSet=file2data('testSet2.txt')
    plt.scatter(dataSet[:,0],dataSet[:,1])
    centpoints,clusterAss=bikMeans(dataSet,3)
    plt.scatter(centpoints[:,0],centpoints[:,1],c='r',linewidth=10)
    plt.show()
    print 'FinalclusterAss',clusterAss
        
test2()

        
        