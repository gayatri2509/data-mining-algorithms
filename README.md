# data-mining-algorithms	                            
#### Date completed: Fall 2017

This project was a part of course CSE602 - Data Mining for MS in CS at University at Buffalo

* Technologies used: python

This repository consists of implementation of different data mining algorithms like association (apriori), dbscan and decision tree algorithm for various data mining techniques.

1) Apriori Algorithm:  
* Apriori algorithm is a classical algorithm used for mining frequent itemsets and generating relevant association rules. 
* The task1 of this algorithm reads the input file and creates a list of transactions in the dataset. It then generates frequent item sets and stores them in a set along with the support count. 
* The task2 of this algorithm recursively generates the association rules for the itemsets from task1. Then it computes the confidence for each of the rules generated and filters out the rules whose confidence is less than the entered value. 
* For the given query the output is displayed in the form of association rules.

2) DBScan:  
* Desity Based Scan is a clustering algorithm commonly used in data mining. DBScan groups together points that are close to each other based on a distance measurement (usually Euclidean distance) and a minimum number of points. It also marks as outliers the points that are in low-density regions.   
* DBScan takes two parameters as input: i) eps - maximum radius of the neighborhood from point p ii) minPos - minimum number of points required to form a dense region. 
* It starts with an arbitrary starting point that has not been visited. This point's ε-neighborhood is retrieved, and if it contains sufficiently many points, a cluster is started. Otherwise, the point is labeled as noise. Note that this point might later be found in a sufficiently sized ε-environment of a different point and hence be made part of a cluster.  
* If a point is found to be a dense part of a cluster, its ε-neighborhood is also part of that cluster. Hence, all points that are found within the ε-neighborhood are added, as is their own ε-neighborhood when they are also dense. This process continues until the density-connected cluster is completely found. Then, a new unvisited point is retrieved and processed, leading to the discovery of a further cluster or noise.

3) Decision Tree:  
* Decision tree is a classification technique in data mining. It is a hierarchial structure consisting of nodes and directed edges. 
* In decision tree, each leaf node is assigned a class label. The internal nodes, contain attribute conditions to separate records that have different characteristics. 
* In this project, the decision tree is implemented using CART algorithm on a biomedical dataset. The output is to determine the category for a given observation, or for prediction. Also computed Accuracy, Precision, Recall and F-measure for validation. 

