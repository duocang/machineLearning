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

#把无重复数据按照原文第一二三。。
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
    pAbusive = sum(trainCategory)/float(numTrainDocs)#文档属于该屏蔽范畴的概率
    p0Num = np.ones(numWords)
    p1Num = np.ones(numWords)
    p0Denom = 2.0
    p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])# trainMatrix[i] 是无重复词汇数组在第一个词汇本下的零一分布。
    p1Vect = np.log(p1Num/p1Denom)#p(wi|c1)   防止程序下溢出
    p0Vect = np.log(p0Num/p0Denom)
    return p0Vect, p1Vect, pAbusive

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + np.log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + np.log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0

def testingNB():
    listOPosts, listClasss = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    p0V, p1V, pAb = trainNBO(np.array(trainMat), np.array(listClasss))
    testEntry = ['love', 'my', 'dalmation']
    thisDoc = np.array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry, "classified as:", classifyNB(thisDoc, p0V, p1V, pAb)
    testEntry = ["stupid", "garbage"]
    thisDoc = np.array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry, "classified as:", classifyNB(thisDoc, p0V, p1V, pAb)


lis, cla = loadDataSet()
#print lis
#print cla

dataSetNoCopy = createVocabList(lis)
#print dataSetNoCopy

#print setOfWords2Vec(dataSetNoCopy, lis[0])
#print setOfWords2Vec(dataSetNoCopy, lis[3])

trainMat = []
for postinDoc in lis:
    trainMat.append(setOfWords2Vec(dataSetNoCopy, postinDoc))


print trainMat[2]
print sum(trainMat[2])

print trainNBO(trainMat, cla)[0]

testingNB()
