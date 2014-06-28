# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 22:09:01 2014
改进的随机梯度上升法速度更快，效果更好
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
    maxite=150
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
    weightsMatrix=mat(weights)
    print weightsMatrix,weightsMatrix.shape
    z=featuresMatrix*weightsMatrix
    return z
"""
改进的随机梯度训练方法，在线训练
"""
def gradAscent(features,labels,numiter=150):
    m,n=shape(features)
    weights=ones((n,1))
    for j in range(numiter):
        dataIndex=range(m)
        for i in range(m):
            alpha=4/(1.0+i+j)+0.01
            randIndex=int(random.uniform(0,len(dataIndex)))
            h=sigmoid(sum(map(operator.mul,features[randIndex],weights)))
            weights+=alpha*(labels[randIndex]-h)*(reshape(array(features[randIndex]),(n,1)))
            del(dataIndex[randIndex])
    return weights
    
    
if __name__=='__main__':
    features,labels=loadData('testSet.txt')
    weights=gradAscent(features,labels)
    print weights.shape
    plabels=map(lambda x:1 if x>0 else 0,predict(features,weights))
    error_num=sum(map(operator.xor,plabels,labels))
    error_rate=double(error_num)/len(labels)
    print 'error_rate is: ',error_rate#计算错误分类比率
    
    #画出决策边界
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.scatter([feature[0] for feature in features ],[feature[1] for feature in features]\
    ,c=[115 if label==1 else 200 for label in labels]) 
    x=arange(-3,3,0.1)
    y=(-(weights[0][0]*x+weights[2][0])/weights[1][0])
    ax.plot(x,y)
    plt.show()
    
    
    


