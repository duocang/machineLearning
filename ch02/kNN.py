#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from numpy import *
import matplotlib
import matplotlib.pyplot as plt
import operator

def createDataSet():
	group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
	labels = ['A', 'A', 'B', 'B']
	return group, labels

def classify0(inX, dataSet, labels, k):
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

normDataSet, ranges, minVals, lines= normalization(returnmat)
print (ranges)
print(lines)
print(normDataSet)

print("程序运行完毕")