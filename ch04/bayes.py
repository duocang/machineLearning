# -*- coding:utf-8 -*-

def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    # 1代表侮辱性文字
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

lis, cla = loadDataSet()
print lis
print cla

dataSetNoCopy = createVocabList(lis)
print dataSetNoCopy

print setOfWords2Vec(dataSetNoCopy, lis[0])
print setOfWords2Vec(dataSetNoCopy, lis[3])
