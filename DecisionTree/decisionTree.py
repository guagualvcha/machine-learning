# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 09:45:53 2014

@author: uncle_bai
"""

from math import log
import operator


"""
计算香农值
"""
def calShannonEnt(dataSet):
    numEntries=len(dataSet)
    classDict=dict()
    for dataVector in dataSet:
        label=dataVector[-1]
        classDict[label]=classDict.get(label,0)+1
    ShannonEnt=0.
    for item in classDict.values():
        p=float(item)/numEntries
        ShannonEnt-=p*log(p,2)
    return ShannonEnt
  

"""
根据固定列的固定值提取数据子集合
"""  
def splitDataSet(dataSet,axis,value):
    result=[]
    for dataVector in dataSet:
        if dataVector[axis]==value:
            newVector=[]
            newVector.extend(dataVector[:axis])
            newVector.extend(dataVector[axis+1:])
            result.append(newVector)
    return result

"""
选择最大信息增益的特征值
"""
def chooseBestFeature(dataSet):
    baseEntropt=calShannonEnt(dataSet)
    numFeature=len(dataSet[0])-1
    bestInfoGain=0.0
    bestFeature=-1
    for axis in range(numFeature):
        featuresList=[example[axis] for example in dataSet]
        uniqueSet=set(featuresList)
        newEntropy=0.0
        for item in uniqueSet:
            splitdataSet=splitDataSet(dataSet,axis,item)
            prob=float(len(splitdataSet))/len(dataSet)
            newEntropy+=prob*calShannonEnt(splitdataSet)
        infoGain=baseEntropt-newEntropy
        if infoGain>bestInfoGain:
            bestInfoGain=infoGain
            bestFeature=axis
    return bestFeature
 
"""
当特征用完但是仍然没有统一分类的时候，多数投票表决分类值
"""
def majorityVote(classList):
    classDict=dict()
    for c in classList:
        classDict[c[0]]=classDict.get(c[0],0)+1
    sortResult=sorted(classDict.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortResult[0][0]

"""
判断是否分类统一
"""
def isSameClass(dataSet):
    classList=[example[-1] for example in dataSet]
    uniqueSet=set(classList)
    if len(uniqueSet)>1:
        return False
    return dataSet[0][-1]
 
 
"""
生成决策树
"""
def creatTree(dataSet):
    if dataSet==[]:
        return
    issameClass=isSameClass(dataSet)
    if issameClass:
        return issameClass
    if len(dataSet[0])==1:
        return majorityVote(dataSet)
    bestFeature=chooseBestFeature(dataSet)
    myTree={bestFeature:{}}
    labels=[example[bestFeature] for example in dataSet]
    uniqueLabels=set(labels)
    for label in uniqueLabels:
        myTree[bestFeature][label]=creatTree(splitDataSet(dataSet,bestFeature,label))
    return myTree
"""
存储决策树
"""
def storeTree(myTree,filename):
    import pickle
    fw=open(filename,'w')
    pickle.dump(myTree,fw)
    fw.close()
    
"""
加载决策树
"""
def grabTree(filename):
    import pickle
    fr=open(filename)
    model=pickle.load(fr)
    fr.close()
    return model
"""
利用决策树预测单条数据类型
"""
def predict(test_features,decision_tree):
    if type(decision_tree).__name__=='dict':
        firstString=decision_tree.keys()[0]
        secondDict=decision_tree[firstString]
        for value in secondDict.keys():
            if test_features[firstString]==value:
                return predict(test_features,secondDict[value])
    else:
        return decision_tree


"""
利用决策数预测多条数据类型
"""
def predictAll(test_features,decision_tree):
    labels=[]
    for test_feature in test_features:
        label=predict(test_feature,decision_tree)
        labels.append(label)
    return labels

"""
读取数据
"""
def file2dataSet(filename):
    fp=open(filename)
    readLines=fp.readlines()
    dataSet=[]
    for line in readLines:
        line=line.strip()
        vector=line.split('\t')
        dataSet.append(vector)
    return dataSet
    
"""
test_case 隐形眼镜推荐
"""
if __name__=='__main__':
    dataSet=file2dataSet('lenses.txt')
    mytree=creatTree(dataSet)
    storeTree(mytree,'mytree')
    treemodel=grabTree('mytree')
    print predictAll(dataSet,treemodel)
    
    
    
    
    