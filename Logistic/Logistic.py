# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 22:09:01 2014

@author: zjubfd
"""
from numpy import *
import operator
import   matplotlib.pyplot as plt

"""
读取数据
"""
def loadData(filename):
    fr=open(filename)
    readLines=fr.readlines()
    features=[]
    labels=[]
    for line in readLines:
        lineArr=line.strip().split()
        labels.append(int(lineArr[-1]))
        features.append(map(float,lineArr[:-1]))
    for feature in features:
        feature.append(1.0)
    return features,labels
        
    
"""
激活函数
"""
def sigmoid(z):
    return 1./(1+exp(-z))

"""
训练系数
"""    
def train(features,labels):
    featuresMatrix=mat(features)
    labelsMatrix=mat(labels).transpose()
    m,n=shape(featuresMatrix)
    alpha=0.01
    maxite=5000
    weights=ones((n,1))
    for i in range(maxite):
        z=featuresMatrix*weights
        h=sigmoid(z)
        error=labelsMatrix-h
        weights=weights+alpha*featuresMatrix.transpose()*error
    return array(weights)
"""
分类预测
"""    
def predict(features,weights):
    featuresMatrix=mat(features)  
    z=featuresMatrix*weights
    return z
    
    
if __name__=='__main__':
    features,labels=loadData('testSet.txt')
    weights=train(features,labels)
    plabels=map(lambda x:1 if x>0 else 0,predict(features,weights))
    error_num=sum(map(operator.xor,plabels,labels))
    error_rate=double(error_num)/len(labels)
    print 'error_rate is: ',error_rate
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.scatter([feature[0] for feature in features ],[feature[1] for feature in features]\
    ,c=[115 if label==1 else 200 for label in labels]) 
    x=arange(-3,3,0.1)
    y=(-(weights[0][0]*x+weights[2][0])/weights[1][0])
    ax.plot(x,y)
    plt.show()
    
    
    


