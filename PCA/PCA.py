# -*- coding: utf-8 -*-
"""
Created on Mon Jul  7 13:02:37 2014

@author: uncle_bai
"""
from numpy import *
from matplotlib import pyplot as plt

def file2data(filename):
    data=[]
    fr=open(filename)
    for line in fr.readlines():
        data.append(map(float,line.strip().split()))
    return mat(data)
    
def pca(data,topN=99999):
    meanVals=mean(data,0)
    meanRemoved=data-meanVals
    covMat=meanRemoved.T*meanRemoved
    eigVals,eigVects=linalg.eig(mat(covMat))
    eigValInd=argsort(eigVals)
    eigValInd=eigValInd[:-(topN+1):-1]
    redEigVects=eigVects[:,eigValInd]
    lowData=meanRemoved*redEigVects#特征值
    reconMat=(lowData*redEigVects.T)+meanVals#重建数据
    return lowData,reconMat


def test1():
    data=file2data('testSet.txt')
    lowData,reconMat=pca(data,1)
    plt.scatter(data[:,0].flatten().A[0],data[:,1].flatten().A[0])
    plt.scatter(reconMat[:,0].flatten().A[0],reconMat[:,1].flatten().A[0],c='r')
    plt.show()

test1()
    

