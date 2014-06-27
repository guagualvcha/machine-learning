# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 22:09:01 2014

@author: zjubfd
"""
from numpy import *
import operator

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
        
    

def sigmoid(z):
    return 1./(1+exp(-z))

    
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
    return weights
    
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
    print error_rate


