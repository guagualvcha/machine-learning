# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 15:14:56 2014

@author: uncle_bai
"""
import re
from  numpy import sum  
import os
import operator

"""
创建字典
"""
def creatWordDict(dataSet):
    wordDict=set()
    for data in dataSet:
        wordDict=wordDict|set(data)
    return wordDict
"""
将一段文本转换为二进制向量
"""
def word2vector(dataSet,wordDict):
    vectors=[]
    for data in dataSet:
        vector=[0]*len(wordDict)
        for word in data:
            if word in wordDict:
                vector[wordDict.index(word)]=1
        vectors.append(vector)
    return vectors
"""
从文件读取数据
"""    
def file2dataSet(filename):
    fr=open(filename)
    regEx=re.compile('[^\w*]?[\d*]?')
    readLines=fr.readlines()
    splitwords=[]
    for line in readLines:
        line=line.strip()
        words=regEx.split(line)
        finalwords=map(str.lower,filter(lambda x:len(x)>3,words))
        splitwords.extend(finalwords)
    return splitwords
"""
从指定路径读取数据集
"""
def filedir2dataSet(filedir):
    dirlist=os.listdir(filedir)
    dataSet=[]
    for filename in dirlist:
        splitwords=file2dataSet(filedir+'/'+filename)
        dataSet.append(splitwords)
    return dataSet
    
"""
生成一个Bayes模型，用到了拉斯平滑
"""
def form2model(vectors):
    result=(sum(vectors,0)+1.)/(len(vectors)+2.)
    return list(result)
"""
用生成的Bayes模型预测分类
"""    
def predict(total_model,wordList,test_dataSet,labels):
    test_dataSet_vectors= word2vector(test_dataSet,wordList)
    result_labels=[]
    for test_dataSet_vector in test_dataSet_vectors:
        index=-1
        maxprob=0
        for i in range(len(total_model)):
            model=total_model[i]
            prob=reduce(operator.mul,filter(lambda x:x!=0,map(operator.mul,model,test_dataSet_vector)))
            if prob>maxprob:
                maxprob=prob
                index=i
        result_labels.append(labels[index])
    return result_labels
        
"""
test_case
"""           
if __name__=='__main__':
    ham_train_data=filedir2dataSet('email/ham')
    spam_train_data=filedir2dataSet('email/spam')
    
    wordSet1=creatWordDict(ham_train_data)
    wordSet2=creatWordDict(spam_train_data)
    wordList=list(wordSet1|wordSet2)
    
    ham_train_data_vectors=word2vector(ham_train_data,wordList)
    spam_train_data_vectors=word2vector(spam_train_data,wordList)
    
    ham_model=form2model(ham_train_data_vectors)
    spam_model=form2model(spam_train_data_vectors)
    total_model=[ham_model,spam_model]
    
    spam_predictLabel=predict(total_model,wordList,spam_train_data,['ham email','spam email'])
    ham_predictLabel=predict(total_model,wordList,ham_train_data,['ham email','spam email'])
    
    print ham_predictLabel
    print spam_predictLabel








    


