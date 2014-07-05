# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 09:51:35 2014

@author: uncle_bai
"""
import itertools
def loadData():
    return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]

def creatC1(dataSet):
    itlist=[]
    for itemlist in dataSet:
        for item in itemlist:
            itlist.append([item])
    return set(map(frozenset,map(list,itlist)))

def checkCk(dataSet,Ck,supportValue):
    supportDict=dict.fromkeys(Ck,0.)
    for item in Ck:
        for itemlist in dataSet:
            if item.issubset(itemlist):
                supportDict[item]+=1
    for item in supportDict.keys():
        if supportDict[item]/len(dataSet)>=supportValue:
            supportDict[item]=supportDict[item]/len(dataSet)
        else:
            del supportDict[item]
    return  supportDict

def apriori(dataSet,supportValue):
    supportDict=dict() 
    C1=creatC1(dataSet)
    D=checkCk(dataSet,C1,supportValue)
    while len(D)!=0:
        supportDict.update(D)
        C=set(map(lambda x:x[0]|x[1],itertools.combinations(D.keys(),2)))
        D=checkCk(dataSet,C,supportValue)
    return supportDict
    
def generateRules(supportDict,minconf):   
    resultList=[]
    for freqset in supportDict.keys():
        if len(freqset)>1:
            consequence='start'
            rulesFromConsequence(supportDict,freqset,consequence,minconf,resultList)
    return resultList
            
def rulesFromConsequence(supportdict,freqset,consequence,minconf,resultList):
    if consequence=='start':
        consequence=[]
        for i in freqset:
            consequence.append(frozenset([i]))
    else:
        m=len(consequence[0])
        consequence=list(set(map(lambda x:x[0]|x[1],itertools.combinations(consequence,2))))
        consequence=filter(lambda x:len(x)==m+1,consequence)
    consequence=calconf(supportdict,consequence,freqset,minconf,resultList)
    if len(consequence)>0 and len(consequence[0])+1<len(freqset) and len(consequence)>1:
        rulesFromConsequence(supportdict,freqset,consequence,minconf,resultList)

def calconf(supportdict,cons,freqset,minconf,resultList):
    result=[]
    for con in cons:
        try:
            conf=supportdict[freqset]/supportdict[freqset-con]
        except:
            print 'cons is ',cons
        if conf>=minconf:
            print freqset-con,'--->',con,'conf:',conf
            resultList.append((freqset-con,con,conf))
            result.append(con)
    return result
        
def test1():
    dataSet=loadData()
    supportDict=apriori(dataSet,0.5)
    rules=generateRules(supportDict,0.5)
    print rules

def test2():
    fr=open('mushroom.dat')
    dataSet=[]
    for line in fr.readlines():
        lineArr=map(float,line.strip().split())
        if lineArr[0]==2:
            dataSet.append(lineArr[1:])
    supportDict=apriori(dataSet,0.7)
    generateRules(supportDict,0.7)
    
    
test2()








    
    