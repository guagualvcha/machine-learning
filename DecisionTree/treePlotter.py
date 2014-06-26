# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 12:09:30 2014

@author: uncle_bai
"""

import matplotlib.pyplot as plt

decisionNode=dict(boxstyle='sawtooth',fc='0.8')
leafNode=dict(boxstyle='round4',fc='0.8')
arrow_args=dict(arrowstyle='<-')

def createPlot():
    fig=plt.figure(1,facecolor='white')
    fig.clf()
    createPlot.ax1=plt.subplot(111,frameon=False)
    plotNode('Decision Node ',(1,1),(0.1,0.5),decisionNode)
    plotNode('Leaf Node',(0.8,0.1),(0.3,0.8),leafNode)
    plt.show()
    
    
def plotNode(nodeTxt,centerPt,parentPt,nodeType):
    createPlot.ax1.annotate(nodeTxt,xy=parentPt,xycoords='axes fraction',\
    xytext=centerPt,textcoords='axes fraction',va='center',ha='center',\
    bbox=nodeType,arrowprops=arrow_args)

    
def getNumLeaves(myTree):
    firstString=myTree.keys()[0]
    numofLeaves=0
    secondDict=myTree[firstString]
    print secondDict
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            numofLeaves+=getNumLeaves(secondDict[key])
        else:
            numofLeaves+=1
    return numofLeaves

def getTreeDepth(myTree):
    maxDepth=0
    firstString=myTree.keys()[0]
    secondDict=myTree[firstString]
    for value in  secondDict.values():
        if type(value).__name__=='dict':
            thisDepth=1+getTreeDepth(value)
        else:
            thisDepth=1
        if thisDepth>maxDepth:
            maxDepth=thisDepth
    return maxDepth
            
    

myTree={1:{2:3,4:{3:{1:2,2:2}}}}
print getTreeDepth(myTree)


