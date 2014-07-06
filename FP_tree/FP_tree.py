# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 15:25:16 2014

@author: uncle_bai
"""
def loadData():
    simpleData=[['r','z','h','j','p'],
                ['z','y','x','w','v','u','t','s'],
                ['z'],
                ['r','x','n','o','s'],
                ['y','r','x','z','q','s','t','m'],
                ['y','z','x','e','q','s','t','m']]
    return simpleData
    
    
class treeNode:
    def __init__(self,nameValue,count=1,nextnode=None,parent=None):
        self.nameValue=nameValue
        self.nextnode=nextnode
        self.count=count
        self.parent=parent
        self.children=dict()
    def countadd(self):
        self.count+=1
    def __eq__(self,treenode):
        return self.nameValue==treenode.nameValue
    def disp(self,dep=0):
        print 'depth:',dep,'name:',self.nameValue,'count:',self.count
        for node in self.children:
            self.children[node].disp(dep+1)
            
def treeBuild(data,number,minfreq=3):
    itemDict=dict()
    for i in range(len(data)):
        event=data[i]
        for item in event:
            if itemDict.has_key(item):
                itemDict[item]+=number[i]
            else:
                itemDict[item]=number[i]
    for item in itemDict.keys():
        if itemDict[item]<minfreq:
            del itemDict[item]
    itemSet=set(itemDict.keys())
    for i in range(len(data)):
        data[i]=filter(lambda x:x in itemSet,data[i])
        data[i].sort(key=lambda x:itemDict[x],reverse=True)

    headDict=dict()
    for item in itemSet:
        headDict[item]=treeNode(item,itemDict[item])
        
    root=treeNode('root')
    
    for i in range(len(data)):
        event=data[i]
        num=number[i]
        update(event,root,headDict,num)
        
    return headDict,root

def update(event,root,headDict,num,index=0):
    if index<len(event):
        if event[index] in root.children:
            root.children[event[index]].count+=num
            update(event,root.children[event[index]],headDict,num,index+1)
        else:
            newNode=treeNode(event[index],parent=root,count=num)
            root.children[event[index]]=newNode
            point=headDict[event[index]]
            while point.nextnode!=None:
                point=point.nextnode
            point.nextnode=newNode
            update(event,newNode,headDict,num,index+1)

def getprebase(headDict,root,base):
    p=headDict[base].nextnode
    preList=[]
    number=[]
    while p!=None:
        pre=[]
        q=p.parent
        while q.nameValue!='root':
            pre.append(q.nameValue)
            q=q.parent
        if pre!=[]:
            preList.append(pre)
            number.append(p.count)
        p=p.nextnode
    disp(root)
    return preList,number
    
def getfreItems(preList,number,base,resultFreqItems,minfreq=3):
    headDict,root=treeBuild(preList,number,minfreq)
    for item in headDict.keys():
        temp=list(base)
        temp.append(item)
        resultFreqItems.append(temp)
        temppreList,tempnumber=getprebase(headDict,root,item)
#        print 'base is',temp
#        print 'prelist is ',temppreList
#        print 'number is',tempnumber
        if len(number)!=0:
            getfreItems(temppreList,tempnumber,temp,resultFreqItems,minfreq) 

def calFreqItems(data,minfreq=3):
    base=[]
    number=[1]*len(data)
    resultFreqItems=[]
    getfreItems(data,number,base,resultFreqItems,minfreq)
    return resultFreqItems
    
def disp(root,dep=0):
    for node in root.children.values():
        disp(node,dep+1)

if __name__=='__main__':
    data=loadData()
    resultFreqItems=calFreqItems(data,minfreq=3)
    print resultFreqItems

            
    
    




    

            
            
            
            
            
            
            
            


