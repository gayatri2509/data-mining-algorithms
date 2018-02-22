from __future__ import division
import math
from collections import Counter
import numpy as np
import copy


categoricalLabels = dict()
GIList = []
AttributeSplitValueList = []

'''
{createInputList}: Reads the file line by line, splits each line using tab,
create the dataset
.................................................................................................
{Input}: input file containing the data
{Output}: list of all dataset records
'''
def createInputList(file):
    inputList = []
    for line in iter(file):
        record = line.strip().split("\t")
        list1 = []
        for i in range(0, len(record)):
            list1.append(record[i])
        inputList.append(list1)
    file.close()
    return inputList

'''
{createColumnwiseList}: Creates a column wise list os all dataset column
.................................................................................................
{Input}: inputList containing all the records of the dataset
{Output}: column wise list of all the dataset columns
'''
def createColumnwiseList(inputList):
    columnwiseList = []
    for row in zip(*inputList):
        columnwiseList.append(list(row))
    return columnwiseList


'''
{countOnesAndZeros}: Returns number of zeros and ones of class labels in the given list
.................................................................................................
{Input}: inputList containing all the records of the dataset
{Output}: number of zeros and ones
'''
def countOnesAndZeros(inputList):
    ones, zeros = 0,0
    size = len(inputList[0])-1
    for i in range(0, len(inputList)):
        if inputList[i][size] == '0':
            zeros += 1
        elif inputList[i][size] == '1':
            ones += 1
    return ones, zeros

'''
{createCategoryDict}: Creates a dictionary of categorical labels
'''
def createCategoryDict(columnwiseList):
    for i in range(0, len(columnwiseList)):
        try:
            if type(np.float(columnwiseList[i][0])) == float:
                continue
        except:
            unique_categories = np.unique(columnwiseList[i])
            categoriesList = []
            for j in range(0, len(unique_categories)):
                categoriesList.append(unique_categories[j])
            categoricalLabels[i] = categoriesList

'''
{computeGiniIndex}: computes gini index using given no. of ones and zeros
'''
def computeGiniIndex(ones, zeros):
    size = ones + zeros
    if ones ==0  or zeros ==0:
        giniIndex = 0.0
    else:
        giniIndex = 1 - (math.pow((ones / size), 2) + math.pow((zeros / size), 2))
    return giniIndex


'''
{computeGiniIndex1}: computes gini index for different types of attributes 
'''
def computeGiniIndex1(columnwiseList, initialGiniIndex, inputList):
    GIList.clear()
    AttributeSplitValueList.clear()
    for i in range(0, len(columnwiseList) - 1):
        try:
            if type(np.float(columnwiseList[i][0])) == float:
                computeGiniIndex_Numerical(columnwiseList[i], inputList, initialGiniIndex)
        except:
            computeGiniIndex_Categorical(columnwiseList[i], inputList, initialGiniIndex)
    giniIndex = min(GIList)
    return giniIndex

'''
{computeGiniIndex_Categorical}: computes gini index for categorical attributes
'''
def computeGiniIndex_Categorical(attributeList, inputList, initialGiniIndex):
    size = len(inputList[0])
    numRows = len(inputList)
    Gini = float("inf")
    splitCategory_val, splitCategory_index = -1, -1

    unique_categories = []
    for i in range(0, len(attributeList)):
        if attributeList[i] not in unique_categories:
            unique_categories.append(attributeList[i])

    for i in range(0, len(unique_categories)):
        cat1_ones, cat1_zeros, cat2_ones, cat2_zeros = 0, 0, 0, 0
        for j in range(0, len(attributeList)):
            if attributeList[j] == unique_categories[i]:
                if inputList[j][size - 1] == '1':
                    cat1_ones += 1
                elif inputList[j][size - 1] == '0':
                    cat1_zeros += 1
            else:
                if inputList[j][size - 1] == '1':
                    cat2_ones += 1
                elif inputList[j][size - 1] == '0':
                    cat2_zeros += 1

        category1GiniIndex = computeGiniIndex(cat1_ones, cat1_zeros)
        category2GiniIndex = computeGiniIndex(cat2_ones, cat2_zeros)
        category1Size = cat1_ones + cat1_zeros
        category2Size = cat2_ones + cat2_zeros
        attributeWeightedGiniIndex = (category1Size / numRows) * category1GiniIndex + (category2Size / numRows) * category2GiniIndex

        if attributeWeightedGiniIndex < Gini:
            Gini = attributeWeightedGiniIndex
            splitCategory_val = unique_categories[i]
            splitCategory_index = attributeList.index(splitCategory_val)

    GIList.append(Gini)
    AttributeSplitValueList.append(splitCategory_val)

'''
{computeGiniIndex_Numerical}: computes gini index for numerical attributes
'''
def computeGiniIndex_Numerical(attributeList, inputList, initialGiniIndex):
    size = len(inputList[0])
    numRows = len(inputList)
    Gini = float("inf")
    splitCategory_val, splitCategory_index = -1, -1
    attributeList1 = []
    for i in range(0, len(attributeList)):
        attributeList1.append(np.float(attributeList[i]))

    unique_categories = []
    for i in range(0, len(attributeList1)):
        if attributeList1[i] not in unique_categories:
            unique_categories.append(attributeList1[i])

    for i in range(0, len(unique_categories)):
        cat1_ones, cat1_zeros, cat2_ones, cat2_zeros = 0,0,0,0
        for j in range(0, len(attributeList1)):
            if attributeList1[j] < unique_categories[i]:
                if inputList[j][size-1] == '1':
                    cat1_ones += 1
                elif inputList[j][size - 1] == '0':
                    cat1_zeros += 1
            else:
                if inputList[j][size - 1] == '1':
                    cat2_ones += 1
                elif inputList[j][size - 1] == '0':
                    cat2_zeros += 1

        category1GiniIndex = computeGiniIndex(cat1_ones, cat1_zeros)
        category2GiniIndex = computeGiniIndex(cat2_ones, cat2_zeros)
        category1Size = cat1_ones + cat1_zeros
        category2Size = cat2_ones + cat2_zeros
        attributeWeightedGiniIndex = (category1Size / numRows) * category1GiniIndex + (category2Size / numRows) * category2GiniIndex

        if attributeWeightedGiniIndex < Gini:
            Gini = attributeWeightedGiniIndex
            splitCategory_val = unique_categories[i]
            splitCategory_index = attributeList1.index(splitCategory_val)

    GIList.append(Gini)
    AttributeSplitValueList.append(splitCategory_val)

'''
{findSplitAttribute}: Find the best attribute to split at each node by computing the gini index for each attribute and find the attribute that minimizes the gini index
'''
def findSplitAttribute(currentList):
    splitNode = GIList.index(min(GIList))
    splitValue = AttributeSplitValueList[splitNode]
    if splitNode in categoricalLabels:
        groupDict = formGroups_Categorical(splitNode, splitValue, currentList)
    else:
        groupDict = formGroups_Numerical(splitNode, splitValue, currentList)
    return {'splitNode': splitNode, 'splitValue': splitValue, 'groupDict': groupDict}


'''
{formGroups_Categorical}: Forms the left and right groups for categorical attributes
'''
def formGroups_Categorical(splitNode, splitValue, currentList):
    leftList, rightList = [], []
    groupDict = dict()
    for i in range(0, len(currentList)):
        if currentList[i][splitNode] == splitValue:
            leftList.append(currentList[i])
        else:
            rightList.append(currentList[i])

    groupDict["left"] = leftList
    groupDict["right"] = rightList
    return groupDict

'''
{formGroups_Numerical}: Forms the left and right groups for numerical attributes
'''
def formGroups_Numerical(splitNode, splitValue, currentList):
    groupDict = dict()
    leftList, rightList = [], []
    for i in range(0, len(currentList)):
        if np.float(currentList[i][splitNode]) < splitValue:
            leftList.append(currentList[i])
        else:
            rightList.append(currentList[i])
    groupDict["left"] = leftList
    groupDict["right"] = rightList
    return groupDict

'''
{getChildNode}: Forms the child node of the current node
'''
def getChildNode(currentNode, Gini):
    groupDict = currentNode['groupDict']
    keyList = getSortedKeys(groupDict)

    for key in keyList:
        currentGroupList = groupDict[key]
        columnwiseList = createColumnwiseList(currentGroupList)
        ones, zeros = countOnesAndZeros(currentGroupList)
        initialGiniIndex = computeGiniIndex(ones, zeros)
        Gini = computeGiniIndex1(columnwiseList, initialGiniIndex, currentGroupList)
        if len(set(columnwiseList[-1])) == 1:
            currentNode[key] = terminateTree(groupDict[key])
        else:
            currentNode[key] = findSplitAttribute(groupDict[key])
            getChildNode(currentNode[key], Gini)

'''
{getSortedKeys}: Sorts the keys of group dictionary
'''
def getSortedKeys(groupDict):
    keyList = []
    for key, value in groupDict.items():
        keyList.append(key)
    keyList.sort()
    return keyList

'''
{terminateTree}: Terminates the key by computing leaf node
'''
def terminateTree(inputList):
    columnwiseList = createColumnwiseList(inputList)
    size = len(inputList[0])
    countDict = Counter(columnwiseList[size-1])
    maxCount = -1
    value = -1
    for key in countDict:
        if countDict[key] > maxCount:
            maxCount = countDict[key]
            value = key
    return value


'''
{predictClassLabel}: Predicts the class label for a given tuple/row using the tree
'''
def predictClassLabel(node, row):
    if node['splitNode'] in categoricalLabels:
        groupDict = node['groupDict']
        if row[node['splitNode']] == node['splitValue']:
            if isinstance(node['left'], dict):
                return predictClassLabel(node['left'], row)
            else:
                return node['left']
        else:
            if isinstance(node['right'], dict):
                return predictClassLabel(node['right'], row)
            else:
                return node['right']

    else:
        if np.float(row[node['splitNode']]) < node['splitValue']:
            if isinstance(node['left'], dict):
                return predictClassLabel(node['left'], row)
            else:
                return node['left']
        else:
            if isinstance(node['right'], dict):
                return predictClassLabel(node['right'], row)
            else:
                return node['right']

'''
{tenFoldCrossValidation}:adopts a 10-fold cross validation on the dataset to split
it into train and test data and computes the average accuracy, precision, recall, f-1measure
..................................................................................................
{Input}: data
{Output}: accuracy,precision, recall and f1-measure for the given dataset
'''
def tenFoldCrossValidation(data):
    size = len(data) / 10
    carry = len(data) % 10
    iterCount = 1
    beginIndex = 0
    endIndex = size
    finalAccuracy = finalPrecision = finalRecall = finalfMeasure = 0
    while iterCount <= 10:
        train_data = copy.deepcopy(data)
        if iterCount == 10:
            test_data = train_data[int(beginIndex):int(endIndex) + int(carry)]
            del train_data[int(beginIndex):int(endIndex) + int(carry)]
        else:
            test_data = train_data[int(beginIndex):int(endIndex)]
            del train_data[int(beginIndex):int(endIndex)]
        beginIndex = beginIndex + size
        endIndex = endIndex + size

        ones, zeros = countOnesAndZeros(train_data)
        columnwiseList = createColumnwiseList(train_data)
        createCategoryDict(columnwiseList)
        initialGiniIndex = computeGiniIndex(ones, zeros)
        Gini = computeGiniIndex1(columnwiseList, initialGiniIndex, train_data)
        root = findSplitAttribute(train_data)
        getChildNode(root, Gini)

        accuracy, recall, precision, fMeasure = validate(root, train_data, test_data)
        print('Fold: ', iterCount)
        print('Accuracy: ', accuracy)
        print('Precision: ', precision)
        print('Recall: ', recall)
        print('F-measure: ', fMeasure)
        finalAccuracy = finalAccuracy + accuracy
        finalPrecision = finalPrecision + precision
        finalRecall = finalRecall + recall
        finalfMeasure = finalfMeasure + fMeasure

        iterCount = iterCount + 1

    print('\n')
    finalAccuracy = finalAccuracy / 10
    finalPrecision = finalPrecision / 10
    finalRecall = finalRecall / 10
    finalfMeasure = finalfMeasure / 10
    print('final accuracy', finalAccuracy)
    print('final precision', finalPrecision)
    print('final recall', finalRecall)
    print('final f-measure', finalfMeasure)


'''
{validate}:calculates the probabilities for the train data and predicts a class label for 
for each record in the test data and computes the accuracy, precision recall,f1-measure
in terms of the no of true positives, true negatives,false positives and false negatives
....................................................................................................
{Input}: trainData, training dataset
{Input}: testData, test dataset
{Output}: accuracy, recall, precision, fMeasure - for the given training dataset and test dataset
'''
def validate(root, train_data, test_data):
    TP = TN = FP = FN = 0
    for record in test_data:
        true_label = record[-1]

        predicted_label = predictClassLabel(root, record)
        if int(true_label) == 1 and int(predicted_label) == 1:
            TP += 1
        elif int(true_label) == 0 and int(predicted_label) == 0:
            TN += 1
        elif int(true_label) == 1 and int(predicted_label) == 0:
            FN += 1
        elif int(true_label) == 0 and int(predicted_label) == 1:
            FP += 1

    accuracy = float(TP + TN) / (TP + TN + FP + FN)
    precision = float(TP) / (TP + FP)
    recall = float(TP) / (TP + FN)
    fMeasure = (2 * recall * precision) / (recall + precision)
    return accuracy, recall, precision, fMeasure



def main():
    fileName = input('Enter the filename: ')
    file = open(fileName)
    inputList = createInputList(file)
    tenFoldCrossValidation(inputList)


main()