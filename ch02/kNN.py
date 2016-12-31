#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from numpy import *
import matplotlib
import matplotlib.pyplot as plt
import operator
from os import listdir

def createDataSet():
	group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
	labels = ['A', 'A', 'B', 'B']
	return group, labels

def classify0(inX, dataSet, labels, k):     #用于分类的输入变量inX，训练集dataSet，标签labels，最近邻居数目
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()     
    classCount={}          
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1

    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def file2matrix(filename):
    fr = open(filename)
    numberOfLines = len(fr.readlines())         #get the number of lines in the file
    returnMat = zeros((numberOfLines,3))        #prepare matrix to return
    classLabelVector = []                       #prepare labels return
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]
        if listFromLine[-1] == 'largeDoses':
            level = 3
        elif listFromLine[-1] == 'smallDoses':
            level = 2
        else:
            level = 1
        classLabelVector.append(level)
        index += 1
    return returnMat,classLabelVector

def normalization(dataSet):
    minVals = dataSet.min(0)    #max_per_col = X.max(axis=0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    lines = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (lines, 1))
    normDataSet = normDataSet/tile(ranges, (lines, 1))
    return normDataSet, ranges, minVals, lines

def datingClassTest(filename):
    hoRation = 0.10         # 10% as test data
    datingDataMat , datingLabels = file2matrix(filename)
    normMat, ranges, minVals, lines = normalization(datingDataMat)
    numTestVecs = int(lines * hoRation)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:], normMat[numTestVecs:lines, :],
                                     datingLabels[numTestVecs:lines], 10)#用于分类的输入变量inX，训练集dataSet，标签labels，最近邻居数目
        print("the classifier came back with: %d, the real answer is: %d" %(classifierResult, datingLabels[i]))
        if(classifierResult != datingLabels[i]):
            errorCount += 1
    print "the total error rate is: %f" %(errorCount/float(numTestVecs))

def classifyPerson(filename):
    resultList = ['not at all', 'in small doses', 'in large doses']
    percentTts = float(raw_input("percentage of time spent playing video games?"))
    ffMiles = float(raw_input("frequent flier miles earned per year?"))
    iceCream = float(raw_input("liters of ice cream consumed per year?"))
    datingDataMat, datingLabels = file2matrix(filename)
    normMat, max_min, minVals, lines = normalization(datingDataMat)
    dataToTest = array([(ffMiles-minVals[0])/max_min[0], (percentTts-minVals[1])/max_min[1], (iceCream-minVals[2])/max_min][2])
    classifierResult = classify0(dataToTest,normMat,datingLabels, 3)
    print "You will probably like ths person: ", resultList[classifierResult -1 ]


g ,l= createDataSet()
a = classify0([0,0], g, l, 3)
print ("预测类型为：" + a)

returnmat, classLabelVector= file2matrix('/Users/xuesong/machineLearning/MachineLearningInAction/ch02/datingTestSet.txt')
#print(classLabelVector)
fig = plt.figure()
ax = fig.add_subplot(111)       #"111" means "1x1 grid, first subplot"
ax.scatter(returnmat[:,1], returnmat[:,2],
           15.0*array(classLabelVector), 15.0*array(classLabelVector))
plt.xlabel('玩视频游戏所消耗时间百分比')
plt.ylabel('每周消费的冰淇淋公升数')
plt.show()
plt.cla()

normDataSet, max_min, minVals, lines= normalization(returnmat)

print (max_min)
print(lines)
print(normDataSet)

#datingClassTest('/Users/xuesong/machineLearning/MachineLearningInAction/ch02/datingTestSet.txt')

#classifyPerson('/Users/xuesong/machineLearning/MachineLearningInAction/ch02/datingTestSet2.txt')

print("程序运行完毕")


# 将一个32*32的二进制图像矩阵转换为1*1024的向量
def img2Vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect

def handwritingClassTest(trainFilename, testFileName):
    hwLabels = []
    trainingFileList = listdir(trainFilename)    #returns a list containing the names of the entries in the direcotry
    number = len(trainingFileList)
    trainingMat = zeros((number, 1024))
    for i in range(number):
        fileNameStr = trainingFileList[i]           #
        fileStr = fileNameStr.split('.')[0]         #get the number from file name
        classNumStr = int(fileStr.split('_')[0])    #
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2Vector(trainFilename+'/'+fileNameStr)
    testFileList = listdir(testFileName)
    errorCount = 0.0
    testNumber = len(testFileList)
    for i in range(testNumber):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2Vector(testFileName+'/'+fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 5)
        print "the classifier came back with: %d, the real answer is: %d" %(classifierResult, classNumStr)
        if(classifierResult != classNumStr):
            errorCount += 1.0
    print "\nthe total number of errors is: %d" %errorCount
    print "\nthe total lerror rate is: %f" %(errorCount/float(testNumber))

handwritingClassTest('/Users/xuesong/OneDrive/machinelearninginaction/Ch02/digits/trainingDigits',
                     '/Users/xuesong/OneDrive/machinelearninginaction/Ch02/digits/testDigits')

