import math
import numpy as np
import os
import ExternalIndex_Computation
from pca_visualization import pca
import importlib

importlib.reload(ExternalIndex_Computation)
clusterList = []
noiseList = []
labels = []

"""
The createInputMatrix reads the data set from file line by line and stores it in the list named inputList. 
"""
def createInputMatrix(file, groundTruthMap, file_name):
    geneList = []
    k = 1
    for line in iter(file):
        record = line.strip().split("\t")
        groundTruthMap[k] = int(record[1])
        labels.append(int(record[1]))
        k += 1
        list = []
        for i in range(2, len(record)):
            list.append(float(record[i]))
        geneList.append(list)
    no_of_clusters = int(np.unique(int(record[1])))
    #file.close()
    graph_label = "DBScan Original (" + file_name + ")"
    pca(geneList, labels, graph_label, no_of_clusters)
    return geneList


"""
The function formClusters() takes the epsilon (esp) and minpts value as input and forms a list of clusters. It 
iterates over the inputList of row points, checks if the point is a noise or core point and calls expandCluster()
if it is a core point to form a cluster for that row point.
"""

def formClusters(esp, Minpts):
    visitedArray = np.zeros(len(geneList))
    markedArray = np.zeros(len(geneList))

    for i in range(0,len(geneList)):
        if(visitedArray[i]==0):
            visitedArray[i]=1
            distanceList = getDistanceList(i)
            NeighborPts = regionQuery(distanceList, esp)
            if (len(NeighborPts) < int(Minpts)):
                markedArray[i] = 0
                noiseList.append(i+1)
            else:
                markedArray[i] = 1  #core point
                C = []
                expandCluster(i, NeighborPts, C, esp, Minpts, visitedArray)

    print("clusterList " ,clusterList)
    print("noiseList ", noiseList)
    print("length of clusterList ",len(clusterList))
    print("length of noiseList ", len(noiseList))

"""
The getDistance() function takes the row number as input and is used to compute the distanceList for a that row point 
i.e a list of distances from that row (list) to all other rows in the inputList and returns it to the caller. 
To get the distance between any two given rows (lists), it gives call to computeEuclideanDistance(). 
"""

def getDistanceList(i):
    list1 = geneList[i]
    distanceList = []
    for j in range(0, len(geneList)):
        list2 = geneList[j]
        value = computeEuclideanDistance(list1, list2)
        distanceList.append(value)
    return distanceList

"""
The computeEuclideanDistance() function takes two lists (two row points) as input, computes euclidean distance
between them by using the features and returns the distance value.
"""

def computeEuclideanDistance(list1, list2):
    sum =0
    for i in range(0,len(list1)):
        sum = sum + (float(list1[i]) - float(list2[i]))**2
    value = math.sqrt(sum)
    return value

"""
The function regionQuery() takes the distanceList of a row point and esp value as the input parameters and is used
to get a list of Neighbors that contain the values from distanceList which are within the epsilon radius circle from
the row point.
"""

def regionQuery(distanceList, esp):
    NeighborPts = []
    for i in range(0, len(distanceList)):
        if(distanceList[i] <= float(esp)):
            NeighborPts.append(i)
    return NeighborPts


"""
The expandCluster() function takes the Point, its NeighborPts, a new cluster C, esp and minpts values and the 
visitedArray as input parameters and forms a cluster in the end which is added to the clusterList. It does so by 
expanding the NeighborPts list in every iteration to accommodate the neighbors of current point that satisfy the 
minpts criteria.  
"""

def expandCluster(P, NeighborPts, C, esp, Minpts, visitedArray):
    C.append(P+1)
    i=0
    while i < len(NeighborPts):
        P1 = NeighborPts[i]
        if (visitedArray[P1] ==0):
            visitedArray[P1] = 1
            distanceList1 = getDistanceList(P1)
            NeighborPts1 = regionQuery(distanceList1, esp)
            if (len(NeighborPts1) >= int(Minpts)):
                NeighborPts = NeighborPts + list(set(NeighborPts1) - set(NeighborPts))
        if P1+1 not in C:
            C.append(P1+1)
        if P1+1 in noiseList:
            noiseList.remove(P1+1)
        i += 1
    clusterList.append(C)


"""
This function gives calls to functions from ExternalIndex_Computation.py by passing appropriate parameters in order
to compute jacard and rand index for dbscan.
"""

def dbscanClusterValidation(groundTruthMap, geneList, clusterList, noiseList, file_name):
    dbscanAlgoClusterMap = {}
    size = len(geneList)
    ExternalIndex_Computation.computeAlgoClusterMap(clusterList, dbscanAlgoClusterMap, noiseList)
    groundTruthClusterMatrix = np.zeros((size, size), dtype=np.int)
    algoClusterMatrix = np.zeros((size, size), dtype=np.int)
    ExternalIndex_Computation.computeGroundTruthAndAlgoClusterMatrix(groundTruthMap, geneList, groundTruthClusterMatrix,
                                                                     dbscanAlgoClusterMap, algoClusterMatrix)
    ExternalIndex_Computation.computeJaccardCoefficient(groundTruthClusterMatrix, algoClusterMatrix, size)

    lab = []
    new_list = []
    for i in range(0, len(clusterList)):
        for j in range(0, len(clusterList[i])):
            new_list.append(geneList[clusterList[i][j]-1])
    k=1
    for i in range(0, len(geneList)):
        lab.append(dbscanAlgoClusterMap[k])
        k+=1

    no_of_clusters = len(np.unique(labels))
    for i in range(len(labels)):
        if labels[i] == -1:
           no_of_clusters += 1

    graph_label = "DBScan Result (" + file_name + ")"
    pca(geneList, lab, graph_label, len(clusterList))


"""
The dbscan function is the main function takes the filename (file path), epsilon and minpts value as the input and
calls createInputMatrix to store the file dataset and formClusters to perform the clustering algorithm.
"""

def dbscan():
    global geneList
    file_path = input('Enter the file path: ')
    file_name = os.path.basename(file_path)
    file = open(file_path)
    esp = input('Enter the value of epsilon: ')
    Minpts = input('Enter the value of Minpts: ')
    groundTruthMap = {}
    clusterMap = {}
    geneList = createInputMatrix(file, groundTruthMap, file_name)
    formClusters(esp, Minpts)
    dbscanClusterValidation(groundTruthMap, geneList, clusterList, noiseList, file_name)

dbscan()