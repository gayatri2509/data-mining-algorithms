# -*- coding: utf-8 -*-
import time

'''
{createTrancDatabase}: Reads the file line by line, splits each line using tab, 
creates a set of items per record, and adds each record in the transactionList
................................................................................
{Input}: file, input file containing the dataset
{Output}: transactionList, list of transactions in dataset
'''
finalList = []

def createTrancDatabase(file):
    transactionList = []
    for line in iter(file):
        record = line.strip().split("\t")
        i = 1
        for r in range(len(record)):
            if record[r] == 'Up':
                record[r] = 'G' + str(i) + '_Up'
            elif record[r] == 'Down':
                record[r] = 'G' + str(i) + '_Down'
            i = i + 1
        # print 'record' ,record
        transactionList.append(frozenset(record))
    file.close()
    # print 'transactionList',transactionList
    return transactionList


'''
{createLengthOneItemSet}: Reads each record in transaction list and
creates a unique set of length 1 item from the transactions and finds
those items which satisfy the miniumum support
................................................................................
{Input}: transactionList, list of transactions in dataset
{Input}: support, minimum support
{Output}: freqItemSet, length-1 frequent itemset
'''

L1 = {}
def createLengthOneFrequentItemSet(transactionList, support):
    itemset = {}
    for record in transactionList:
        for item in record:
            if not frozenset([item]) in itemset:
                itemset[frozenset([item])] = 1
            else:
                itemset[frozenset([item])] = itemset[frozenset([item])] + 1
    # print 'length 1 itemset',itemset
    freqItemSet = {}
    for item in itemset:
        itemSupport = float(itemset[item]) / len(transactionList)
        if (itemSupport >= support):
            L1[item] = itemset[item]
    # return freqItemSet


'''
{createCandidateSet}: Generate the candidate itemset for (K+1) level by joining 
the length-k frequent itemset with itself whose first k-2 elements are common
................................................................................
{Input}: Lk, length-k frequent itemset
{Input}: k, current iteration
{Output}: Ck, candidate itemset for (k+1)next level of scan
'''


def createCandidateSet(Lk, k):
    # print Lk
    n = len(Lk)
    Ck = set()
    for item1 in Lk:
        for item2 in Lk:
            unionSet = item1.union(item2)
            if (len(unionSet) == k):
                Ck.add(unionSet)
                # print 'candidate set',Ck
    return Ck


'''
{createFrequentItemSet}: Reads each item in candidate itemset and finds
those candidates that are present in the transaction list to create the frequent 
itemset and filter those frequent itemset which satisfy the miniumum support
................................................................................
{Input}: candidateSet, length-k candidate itemset
{Input}: transactionList, list of transactions in dataset
{Input}: support, minimum support
{Output}: Lk, length-k frequent itemset that satisfy minimum support
'''

freqItemSetMinSup1 = {}
def createFrequentItemSet(candidateSet, transactionList, support):
    freqItemSet = {}
    for item in candidateSet:
        for record in transactionList:
            if (item.issubset(record)):
                if (frozenset(item) in freqItemSet):
                    freqItemSet[frozenset(item)] = freqItemSet[frozenset(item)] + 1
                else:
                    freqItemSet[frozenset(item)] = 1

    freqItemSetMinSup = {}
    for item in freqItemSet:
        itemSupport = float(freqItemSet[item]) / len(transactionList)
        if (itemSupport >= support):
            freqItemSetMinSup[item] = freqItemSet[item]
            # print 'frequent itemset with min sup',freqItemSetMinSup
            freqItemSetMinSup1[item] = freqItemSetMinSup[item]
    return freqItemSetMinSup


'''
{aprioriWithSupport}: runs the apriori algorithm for different support values
and prints the number of length-k frequent itemsets each level of scan
................................................................................
{Input}: support, minimum support
{Input}: transactionList, list of transactions in dataset
'''


def aprioriWithSupport(support, transactionList):
    createLengthOneFrequentItemSet(transactionList, support)
    print('number of length: 1 frequent itemsets:', len(L1))
    totalCount = len(L1)
    Lk = {}
    Ck = {}
    k = 2
    isFirstIteration = True
    while ((len(Lk) >= 1) or isFirstIteration):
        if not Lk:
            Lk = L1
            isFirstIteration = False
        Ck = createCandidateSet(Lk, k)
        Lk = createFrequentItemSet(Ck, transactionList, support)
        finalList.append(Lk)
        print('number of length:', k, 'frequent itemsets:', len(Lk))
        k += 1
        totalCount += len(Lk)

    print("total length of all frequent itemsets:", totalCount)
    return finalList


'''
{apriori}: main function that runs apriori algorithm for different minimum support
on the given dataset
................................................................................
'''


def apriori():
    fileName = input('Enter the filename: ')
    file = open(fileName)
    support = input('Enter the minimum support: ')
    support = float(support) / 100
    transactionList = createTrancDatabase(file)
    print('Support is set to be', int((support) * 100), '%')
    finalList = aprioriWithSupport(support, transactionList)
