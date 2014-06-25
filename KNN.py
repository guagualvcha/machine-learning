# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 12:45:22 2014

@author: uncle_bai
"""
from pylab import *
import operator
import os
from matplotlib  import pyplot as plt



"""
读取文本文件
"""
def files2matrix(filename,numOfFeatures):
    fr=open(filename)
    arrayOnLines=fr.readlines()
    shuffle(arrayOnLines) #打乱顺序
    numOfLines=len(arrayOnLines)
    returnmat=zeros((numOfLines,numOfFeatures))
    labels=[]
    index=0
    for line in arrayOnLines:
        lineFormat=(line.strip()).split('\t')
        returnmat[index,:]=lineFormat[0:numOfFeatures]
        labels.append(int(lineFormat[-1]))
        index+=1
    fr.close()
    return returnmat,array(labels)
    
"""
读取二进制图像文件
"""    
def files2vectors(dirname):
    fileDir=os.listdir(dirname)
    features=[]
    labels=[]
    for i in range(len(fileDir)):
        fr=open(dirname+'/'+fileDir[i])
        arrayOnLines=fr.readlines()
        vector=[]
        for line in arrayOnLines:
            line=line.strip()
            vector.extend(map(bool,map(int,line)))
        features.append(vector)
        labels.append(int(fileDir[i][0]))
        fr.close()
    return array(features),array(labels)

    




"""
定义归一化模型
"""
class scaleModel:
    def __init__(self,dataMax,dataMin,xmax=1,xmin=0):
        self.dataMax=dataMax
        self.dataMin=dataMin
        self.xmax=xmax
        self.xmin=xmin
    def scaleForData(self,data):
        dataRange=self.dataMax-self.dataMin
        m=data.shape[0]
        scaleData=((self.xmax-self.xmin)*(data-tile(self.dataMin,(m,1))))/tile(dataRange,(m,1))+self.xmin
        return scaleData     
        
        
        
        
"""
对训练样本进行归一化，并提取出归一化模型
"""     
def autoScale(dataSet,xmax=1,xmin=0):
    dataMin=dataSet.min(0)
    dataMax=dataSet.max(0)
    model=scaleModel(dataMax,dataMin,xmax,xmin)
    scaleData=model.scaleForData(dataSet)
    return scaleData,model
    
    
   
   
    
"""
分类预测
"""    
def classify(inx,dataSet,labels,k,model=None):
    if model==None:
        scaleinx=inx
    else:
        scaleinx=model.scaleForData(inx)
    m=dataSet.shape[0]
    result=array([labels[0]]*(inx.shape[0]))
    j=0
    for vector in scaleinx:
        diff=tile(vector,(m,1))-dataSet
        diff=diff**2
        diff=diff.sum(axis=1)
        classcount=dict()
        sortedIndex=diff.argsort(axis=0)
        for i in range(k):
            votelabel=labels[sortedIndex[i]]
            classcount[votelabel]=classcount.get(votelabel,0)+1
        sortedClasscount=sorted(classcount.iteritems(),key=operator.itemgetter(1),reverse=True)
        result[j]=sortedClasscount[0][0]
        j+=1
    return result
    
    
    
    
    
    
    
"""
test_case1 约会系统
"""    
#
if __name__=="__main__":
    #testcase_1
    features,labels=files2matrix('datingTestSet2.txt',3)
    rate=0.1
    k=int(features.shape[0]*rate)
    test_features,train_features=features[0:k],features[k+1:]
    test_labels,train_labels=labels[0:k],labels[k+1:]
    scale_test_features,model=autoScale(train_features)
    predict_labels=classify(test_features,scale_test_features,train_labels,20,model)
    error_rate=float(sum(test_labels-predict_labels!=0))/k
    print '约会对象分类错误识别率是： ',error_rate,sum(test_labels-predict_labels!=0)
    print '总测试个数：',k
    #test_case_2
    train_features,train_labels=files2vectors('trainingDigits')
    test_features,test_labels=files2vectors('testDigits')
    predict_labels=classify(test_features,train_features,train_labels,10)
    m=len(predict_labels)    
    error_rate=float(sum((predict_labels-test_labels)!=0))/m
    print '手写字体错误识别率是： ',error_rate
    print '总测试个数：',m

        
    
    
        
    
        
    
    
    
    

    
    
