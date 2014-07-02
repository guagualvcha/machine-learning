# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 20:35:54 2014

@author: uncle_bai
"""

from numpy import *
from matplotlib import pyplot as plt
"""
回归类型的节点表示
"""
def regLeaf(dataSet):
    return mean(dataSet[:,-1])
"""
回归类型的方差计算
"""
def regErr(dataSet):
    return var(dataSet[:,-1])*shape(dataSet)[0]
"""
读取数据
"""
def file2data(filename):
    data=[]
    fr=open(filename)
    for line in fr.readlines():
        lineArr=line.strip().split()
        data.append(map(double,lineArr))
    return data
"""
二切分数据
"""
def binsplitDataset(dataSet,feature,value):
    data0=dataSet[array(nonzero(dataSet[:,feature]<=value)[0]).flatten(),:]
    data1=dataSet[array(nonzero(dataSet[:,feature]>value)[0]).flatten(),:]
    return data0,data1
"""
构建回归树或者分类树
"""    
def creatTree(dataSet,leafType=regLeaf,errType=regErr,ops=(1,4)):
    feat,val=chooseBestSplit(dataSet,leafType,errType,ops)
    if feat==None:
        return val
    retTree=dict()
    retTree['spInd']=feat
    retTree['spVal']=val
    lSet,rSet=binsplitDataset(dataSet,feat,val)
    retTree['left']=creatTree(lSet,leafType,errType,ops)
    retTree['right']=creatTree(rSet,leafType,errType,ops)
    return retTree
    
"""
选择最优切分特征和特征值
"""
def chooseBestSplit(dataSet,leafType=regLeaf,errType=regErr,ops=(1,4)):
    tolS=ops[0]
    tolN=ops[1]
    if len(set(dataSet[:,-1].T.tolist()[0]))==1:
        return None,leafType(dataSet)
    m,n=shape(dataSet)
    S=errType(dataSet)
    bestS=inf
    bestIndex=0
    bestVal=0
    for featIndex in range(n-1):
        for splitVal in set(dataSet[:,featIndex].T.tolist()[0]):
            d0,d1=binsplitDataset(dataSet,featIndex,splitVal)
            if shape(d0)[0]<tolN or shape(d1)[0]<tolN:
                continue
            newS=errType(d0)+errType(d1)
            if newS<bestS:
                bestIndex=featIndex
                bestVal=splitVal
                bestS=newS
    if  S-bestS<tolS:
        return None,leafType(dataSet)
    return bestIndex,bestVal
    
"""
后剪枝
"""  
def istree(obj):
    return type(obj).__name__=='dict'      

def getMean(tree):
    if istree(tree['right']):
        r=getMean(tree['right'])
    else:
        r=tree['right']
    if istree(tree['left']):
        l=getMean(tree['left'])
    else:
        l=tree['left']
    return (r+l)/2
"""
对树后剪枝，rate控制剪枝强度
"""
def prune(tree,testData,rate=1.0):
    if shape(testData)[0]==0:
        return getmean(tree)
    if istree(tree['right']) or istree(tree['left']):
        lSet,rSet=binsplitDataset(testData,tree['spInd'],tree['spVal'])
    if istree(tree['right']):
        tree['right']=prune(tree['right'],rSet,rate)
    if istree(tree['left']):
        tree['left']=prune(tree['left'],lSet,rate)
    if not istree(tree['right']) and not istree(tree['left']):
        lSet,rSet=binsplitDataset(testData,tree['spInd'],tree['spVal'])
        errorNoMerge=sum(power(lSet[:,-1]-tree['left'],2))+\
        sum(power(rSet[:,-1]-tree['right'],2))
        treemean=(tree['right']+tree['left'])/2
        errorMerge=sum(power(testData[:,-1]-treemean,2))
        if errorMerge<rate*errorNoMerge:
            return treemean
        else:
            return tree
    else:
        return tree

def test1():
    data=file2data('ex2.txt')
    data=mat(data)
    tree=creatTree(data[:150,:],ops=(1,4))
    tree=prune(tree,data[150:,:],rate=1.2)
    print tree
    
"""
模型树
"""
def linearSolver(dataSet):
    dataMat=mat(dataSet)
    xMat=dataMat[:,:-1]
    yMat=dataMat[:,-1]
    xTx=xMat.T*xMat
    if linalg.det(xTx)==0:
        print 'This matrix is singular,cannot inverse!'
        return
    w=xTx.I*xMat.T*yMat
    return w,xMat,yMat

def modelLeaf(dataSet):
    w,x,y=linearSolver(dataSet)
    return w

def modelErr(dataSet):
    w,x,y=linearSolver(dataSet)
    yHat=x*w
    return sum(power(y-yHat,2))

def test2():
    data=file2data('exp2.txt')
    data=mat(data)
    m=shape(data)[0]
    data=hstack((ones((m,1)),data))
    tree=creatTree(data,ops=(1,4),leafType=modelLeaf,errType=modelErr)
    print tree

"""
回归预测
"""
def regTreeEval(model,indata):
    return model
def modelTreeEval(model,indata):
    return indata*model
def predictForOne(tree,indata,treeEval=regTreeEval):
    if indata[0,tree['spInd']]<=tree['spVal']:
        if not istree(tree['left']):
            return treeEval(tree['left'],indata)
        else:
            return predictForOne(tree['left'],indata,treeEval)
    else:
        if not istree(tree['right']):
            return treeEval(tree['right'],indata)
        else:
            return predictForOne(tree['right'],indata,treeEval)
def predict(tree,datax,EvalType=regTreeEval):
    m=shape(datax)[0]    
    ypredict=mat(zeros((m,1)))
    for i in range(m):
        ypredict[i]=predictForOne(tree,datax[i,:],EvalType)
    return ypredict
    
    
def test3():
    #回归树测试
    data=file2data('exp2.txt')
    data=mat(data)
    tree=creatTree(data[:150,:],ops=(1,4))
    tree=prune(tree,data[150:,:],rate=1.2)
    py=predict(tree,data)
    print '方差是：',var(py-data[:,-1])
    print '误差均值是：',mean(abs(py-data[:,-1]))
    print '相关洗漱是：',corrcoef(py,data[:,-1],rowvar=0)
    #模型树测试
    data=file2data('exp2.txt')
    data=mat(data)
    m=shape(data)[0]
    data=hstack((ones((m,1)),data))
    tree=creatTree(data,ops=(1,4),leafType=modelLeaf,errType=modelErr)
    py=predict(tree,data[:,:-1],modelTreeEval)
    print '方差是：',var(py-data[:,-1])
    print '误差均值是',mean(abs(py-data[:,-1]))
    print '相关洗漱是：',corrcoef(py,data[:,-1],rowvar=0)
    
if __name__=='__main__':
    data=file2data('sine.txt')
    data=mat(data)
    print data
    plt.scatter(array(data[:,0]),array(data[:,1]))
    plt.show()
        









