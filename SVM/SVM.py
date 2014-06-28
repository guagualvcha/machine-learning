# -*- coding: utf-8 -*-
"""
Created on Sat Jun 28 12:53:19 2014

@author: uncle_bai
"""
from pylab import *
import random
import operator

"""
定义svm模型对象，用以序列化到文件中
"""
class svmmodel:
    def __init__(self,alphas,b,features,labels):
        self.alphas=alphas
        self.b=b
        self.features=features
        self.labels=labels
    def predict(self,features):
        featuresMat=mat(features)
        h=multiply(self.alphas,self.labels).T*(self.features*featuresMat.T)+self.b  
        h=h.T
        labels=[-1 if x[0,0]<0 else 1 for x in h ]
        return labels
"""
创建一个只包含支持向量的svm模型
"""
def creatsvmmodel(alphas,b,features,labels):
    m,n=shape(features)
    index=[]
    for i in range(m):
        if alphas[i,0]!=0:
            index.append(i)
    k=len(index)
    newalphas=mat(zeros((k,1)))
    newfeatures=mat(zeros((k,n)))
    newlabels=mat(zeros((k,1)))
    k=0
    for i in index:
        newalphas[k]=alphas[i]
        newfeatures[k]=features[i]
        newlabels[k]=labels[i]
        k+=1
    return svmmodel(newalphas,b,newfeatures,newlabels)
        
            
"""
加载数据
"""
def loadDataSet(filename):
    features=[]
    labels=[]
    fr=open(filename)
    for line in fr.readlines():
        lineArr=line.strip().split()
        features.append([float(lineArr[0]),float(lineArr[1])])
        labels.append(float(lineArr[2]))
    return features,labels
"""
随机选择序列对
"""
def selectJrand(i,m):
    j=i
    while j==i:
        j=int(random.uniform(0,m))
    return j

def clipAlpha(aj,H,L):
    if aj>H:
        return H
    if aj<L:
        return L
    return aj
"""
简化SMO 算法
"""
def  smoSimple(features,labels,c,toler,maxite):
    featuresMat=mat(features)
    labelsMat=mat(labels).transpose()
    b=0.
    m,n=shape(featuresMat)
    alphas=mat(zeros((m,1)))
    ite=0
    while ite<maxite:
        alphaChanged=0
        for i in range(m):
            fxi=multiply(alphas,labelsMat).T*(featuresMat*featuresMat[i,:].T)+b
            Ei=fxi-labelsMat[i]
            if(((labelsMat[i]*Ei<-toler)and(alphas[i]<c))or((labelsMat[i]*Ei>toler)and(alphas[i]>0))):
                j=selectJrand(i,m)
                fxj=multiply(alphas,labelsMat).T*(featuresMat*featuresMat[j,:].T)+b
                Ej=fxj-labelsMat[j] 
                alphaIold=alphas[i].copy()
                alphaJold=alphas[j].copy()
                if labelsMat[i]!=labelsMat[j]:
                    L=max(0,alphas[j]-alphas[i])
                    H=min(c,c+alphas[j]-alphas[i])
                else:
                    L=max(0,alphas[j]+alphas[i]-c)
                    H=min(c,alphas[j]+alphas[i])
                if L==H:
                    print "L==h"
                    continue
                eta=2.0*featuresMat[i,:]*featuresMat[j,:].T-\
                featuresMat[i,:]*featuresMat[i,:].T-\
                featuresMat[j,:]*featuresMat[j,:].T
                if eta>0:
                    print "eta>0"
                    continue
                alphas[j]-=labelsMat[j]*(Ei-Ej)/eta
                alphas[j]=clipAlpha(alphas[j],H,L)
                if (abs(alphas[j]-alphaJold<0.00001)):
                    continue
                alphas[i]+=labelsMat[j]*labelsMat[i]*(alphaJold-alphas[j])
                b1=b-Ei-labelsMat[i]*(alphas[i]-alphaIold)*\
                featuresMat[i,:]*featuresMat[i,:].T-\
                labelsMat[j]*(alphas[j]-alphaJold)*\
                featuresMat[i,:]*featuresMat[j,:].T
                b2=b-Ej-labelsMat[i]*(alphas[i]-alphaIold)*\
                featuresMat[i,:]*featuresMat[j,:].T-\
                labelsMat[j]*(alphas[j]-alphaJold)*\
                featuresMat[j,:]*featuresMat[j,:].T
                if alphas[i]>0 and c>alphas[i]:
                    b=b1
                elif alphas[j]>0 and c>alphas[j]:
                    b=b2
                else:
                    b=(b1+b2)/2.
                alphaChanged==1
        if alphaChanged==0:
            ite+=1
        else:
            ite=0
        print 'iteration num is :',ite
    model=creatsvmmodel(alphas,b,featuresMat,labelsMat)
    return model

"""
test_case
"""
if __name__=='__main__':       
    features,labels=loadDataSet('testSet.txt')
    model=smoSimple(features,labels,0.6,0.001,40)   
    plabels=model.predict(features)
    error_rate=sum(map(operator.sub,labels,plabels))/len(labels)
    print error_rate
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        