# -*- coding:utf-8 -*-

import numpy as np

def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    # 1代表侮辱性文字
    print len(postingList)
    return postingList, classVec

#使用set类型，可以创建一个包含在所有文档中出现的不重复的词汇列表
def createVocabList(dataSet):
    vocabSet = set([])          # 创建一个空集
    for doucment in dataSet:
        vocabSet = vocabSet | set(doucment)#创建两个集合的并集
    return list(vocabSet)


def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList)          #创建一个所有元素都为0的向量
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else: print ("the word %s is not in my vocabulary!") % word
    return returnVec


def trainNBO(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    print("numWords是")
    print numWords
    pAbusive = sum(trainCategory)/float(numTrainDocs)#文档属于该屏蔽范畴的概率
    p0Num = np.zeros(numWords)
    p1Num = np.zeros(numWords)
    p0Denom = 0.0
    p1Denom = 0.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])# trainMatrix[i] 是无重复词汇数组在第一个词汇本下的零一分布。
    p1Vect = p1Num/p1Denom
    p0Vect = p0Num/p0Denom
    return p0Vect, p1Vect, pAbusive


lis, cla = loadDataSet()
#print lis
#print cla

dataSetNoCopy = createVocabList(lis)
#print dataSetNoCopy

#print setOfWords2Vec(dataSetNoCopy, lis[0])
#print setOfWords2Vec(dataSetNoCopy, lis[3])

trainMat = []
for postinDoc in lis:
    print postinDoc
    trainMat.append(setOfWords2Vec(dataSetNoCopy, postinDoc))
    print np.size(trainMat)


print len(trainMat)
print trainMat[2]
print sum(trainMat[2])

print trainNBO(trainMat, cla)[0]
#print trainNBO(trainMat, cla)[1]
#print trainNBO(trainMat, cla)[2]