# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 10:33:10 2014

@author: uncle_bai
"""
from numpy import *
from matplotlib import pyplot as py

"""
读取数据
"""
def file2data(filename):
    fr=open(filename)
    datax=[]
    for line in fr.readlines():
        lineArr=line.strip().split()
        datax.append(map(float,lineArr))
    fr.close()
    return array(datax)


"""
传统二乘法
"""
def ordinaryRegression(x,y):
    xMat=mat(x)
    yMat=mat(y).T
    xTx=xMat.T*xMat
    if linalg.det(xTx)==0:
        print 'This matrix is singular,cannot inverse!'
        return
    w=xTx.I*xMat.T*yMat
    return w  
    
"""
回归计算
"""
def calY(w,x):
    xmat=mat(x)
    y=xmat*w
    return array(y)
    
def test1():
    datax=file2data('abalone.txt')
    py.scatter(datax[:,1],datax[:,-1])
    w=ordinaryRegression(datax[:,:-1],datax[:,-1])
#    x1=reshape(linspace(0.,1.2,40),(40,1))
#    x=hstack((ones((40,1)),x1))
#    y=calY(w,x)
#    py.plot(x[:,1].flatten(),y.flatten())
#    py.show()
    print w


"""
局部加权线性回归
"""
def lwlr(testPoints,xArr,yArr,k=1.0):
    testPointsMat=mat(testPoints)
    xMat=mat(xArr)
    yMat=mat(yArr).T
    m=shape(xMat)[0]
    m0=testPointsMat.shape[0]
    y=mat(ones((m0,1)))
    for j in range(m0):
        testPoint=testPointsMat[j]
        W=mat(zeros((m,m)))
        for i in range(m):
            W[i,i]=exp(sqrt((xMat[i]-testPoint)*((xMat[i]-testPoint).T))/(-2*k*k))
        w=(xMat.T*W*xMat).I*xMat.T*W*yMat
        y[j]=testPoint*w
    return y

"""
局部线性回归测试
"""        
def test2():
    datax=file2data('ex0.txt')
    py.scatter(datax[:,1],datax[:,-1])
    datax=file2data('ex0.txt')
    y=lwlr(datax[:,:-1],datax[:,:-1],datax[:,-1],k=0.01)
    print y
    py.scatter(datax[:,1],array(y),c='r')
#    py.scatter(datax[:,1],y)
    py.show()

"""
岭回归,岭回归可以避免很大的相关的两个特征一个稀疏正很大，另一个负很大
"""
def ridgeRegres(x,y,lam=0.2):
    m,n=x.shape    
    xMat=mat(x)
    yMat=mat(y).T
    xTx=xMat.T*xMat+lam*mat(eye(n))
    if linalg.det(xTx)==0:
        print 'This matrix is singular,cannot inverse!'
        return
    w=xTx.I*xMat.T*yMat
    return w
"""
回归系数随lam变化的过程测试
"""   
def ridgeTest(xArr,yArr):
    n=xArr.shape[1]
    xArr=(xArr-mean(xArr,0))/var(xArr,0)
    yArr=yArr-mean(yArr)
    wmat=mat(zeros((60,n)))
    for i in range(30):
        w=ridgeRegres(xArr,yArr,exp(i-10))
        wmat[i,:]=w.T
    return wmat
        
    
def test3(): 
    data=file2data('abalone.txt')
    xArr=data[:,:-1]
    yArr=data[:,-1]
    wmat=ridgeTest(xArr,yArr)
    print wmat
    py.plot(wmat)
    py.show()


    
"""
前向逐步回归
"""
def stageWise(xArr,yArr,eps=0.01,numIte=100):
    xMat=mat(xArr)
    m,n=xMat.shape
    yMat=mat(yArr).T
    xMat=(xMat-mean(xMat,0))/var(xMat,0)
    yMat=yMat-mean(yMat,0)
    returnMat=mat(zeros((numIte,n)))
    wbest=mat(zeros(n)).T
    for ite in range(numIte):
        bestCost=inf
        for i in range(n):
            for op in [1,-1]:
                w=wbest.copy()
                w[i]=w[i]+eps*op
                pyMat=xMat*w
                cost=sqrt(sum((pyMat-yMat).T*(pyMat-yMat)))
                if cost<bestCost:
                    bestCost=cost
                    wbest=w
        returnMat[ite,:]=wbest.copy().T
    return returnMat
    
def stageWiseTest():
    data=file2data('abalone.txt')
    xArr=data[:,:-1]
    yArr=data[:,-1]    
    returnMat=stageWise(xArr,yArr,eps=0.001,numIte=3000)
    returnMat=stageWiseTest()
    py.plot(returnMat)
    py.show()




    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




