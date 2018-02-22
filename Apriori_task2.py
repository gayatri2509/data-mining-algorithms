import re
import Apriori_task1_final
import ast

rule_body1 = []
rule_body = []
rule_head = []

"""
Extracts the frequent itemsets from the list generated in task1 and passes it to the function generateRules() 
for generating rules.
"""

def getFreqSet():
    for i in range (0, len(Apriori_task1_final.finalList)):
        currentFreqSet = Apriori_task1_final.finalList[i]
        for key in currentFreqSet:
            generateRules(list(key), key)
            rule_body1.extend(rule_body[:])
            rule_body.clear()

"""
Recursively generates the rules for the given itemset and stores the body in one list and the head in other list such that 
there is one to one body head mapping. 
"""
def generateRules(freqItemList, freqItemSet):
    for i in range (len(freqItemList)-1, -1, -1):
        intermediateList = []
        for j in range(0, len(freqItemList)):
            if j!=i:
                intermediateList.append(freqItemList[j])

        if intermediateList not in rule_body:
            rule_body.append(intermediateList)
            complementaryList = list(freqItemSet - set(intermediateList))
            rule_head.append(complementaryList)

        if(len(intermediateList)>1):
            generateRules(intermediateList, freqItemSet)

"""
Computes the confidence for each rules generated above and filters out the rules whose confidence is less than the entered
value. These rules are deleted from the body and head list.(there is one to one mapping between the two lists).
"""

def filterOnConfidence(confidence):
    i = 0
    while i<len(rule_head):
        temp1 = rule_body1[i]
        temp2 = rule_head[i]
        list1 = list(sorted(set(temp1).union(temp2)))

        count_numerator = Apriori_task1_final.freqItemSetMinSup1[frozenset(list1)]
        if len(rule_body1[i])==1:
            count_denominator = Apriori_task1_final.L1[frozenset(rule_body1[i])]
        else:
            count_denominator = Apriori_task1_final.freqItemSetMinSup1[frozenset(rule_body1[i])]
        computedConfidence = float(count_numerator)/count_denominator

        if float(computedConfidence) < float(confidence):
            del rule_body1[i]
            del rule_head[i]
            i = i-1
        i=i+1
"""
template1 function takes the type (like "RULE"), countOfItems (like "ANY") and list of itemset as parameters and 
returns the count, bodylist and headlist as the result (such that there is one to one mapping between the two lists).
"""

def template1(type, countOfItems, itemSet):
   type = type.strip()
   countOfItems = countOfItems.strip()
   count =0
   queryResultBody = []
   queryResultHead = []
   if countOfItems == "\"ANY\"":
       for i in range(0, len(rule_body1)):
           for j in range(0, len(itemSet)):
               currentItem = itemSet[j]
               if (type == "\"RULE\"" or type == "\"BODY\"") and currentItem in rule_body1[i]:
                   count = count+1
                   queryResultBody.append(rule_body1[i])
                   queryResultHead.append(rule_head[i])
                   break
               elif (type == "\"RULE\"" or type == "\"HEAD\"") and currentItem in rule_head[i]:
                   count = count + 1
                   queryResultBody.append(rule_body1[i])
                   queryResultHead.append(rule_head[i])
                   break

   elif countOfItems == "\"NONE\"":
       for i in range(0, len(rule_body1)):
           c = 0
           for j in range(0, len(itemSet)):
               currentItem = itemSet[j]
               if (type == "\"RULE\""):
                   if (currentItem in rule_body1[i] or currentItem in rule_head[i]):
                       break
                   else:
                       c = c+1
               elif (type == "\"BODY\""):
                   if (currentItem in rule_body1[i]):
                       break
                   else:
                       c = c+1
               elif (type == "\"HEAD\""):
                   if(currentItem in rule_head[i]):
                       break
                   else:
                       c = c+1

           if c == len(itemSet):
               count = count + 1
               queryResultBody.append(rule_body1[i])
               queryResultHead.append(rule_head[i])

   elif int(countOfItems) == 1:
       for i in range(0, len(rule_body1)):
           c = 0
           for j in range(0, len(itemSet)):
               currentItem = itemSet[j]
               if (type=="\"RULE\"" or type=="\"BODY\"") and currentItem in rule_body1[i]:
                   c =c+1
                   if c>1:
                       break
               elif (type=="\"RULE\"" or type=="\"HEAD\"") and currentItem in rule_head[i]:
                   c =c+1
                   if c>1:
                       break
           if c==1:
               count = count + 1
               queryResultBody.append(rule_body1[i])
               queryResultHead.append(rule_head[i])

   else:
       print("invalid query")

   return count, queryResultBody, queryResultHead

"""
template2 function takes the type (like "RULE"), size (like "1") as parameters, computes the length based these parameters
and returns the count, bodylist and headlist as the result (such that there is one to one mapping between the two lists).
"""

def template2(type, size):
    type = type.strip()
    count = 0
    length = 0
    queryResultBody = []
    queryResultHead = []
    for i in range(0,len(rule_body1)):
        if type == "\"RULE\"":
            length = len(rule_body1[i]) + len(rule_head[i])
        elif type == "\"BODY\"":
            length = len(rule_body1[i])
        elif type == "\"HEAD\"":
            length = len(rule_head[i])
        else:
            print("invalid query")

        if length >= int(size):
            count = count+1
            queryResultBody.append(rule_body1[i])
            queryResultHead.append(rule_head[i])

    return count, queryResultBody, queryResultHead

"""
template3 function takes multiple parameters (since there is no fixed size), and calls template1 or template2 according
to the two numbers given in the argument, combines both the results (if "and" then intersection, if "or" then union )
and returns the count, bodylist and headlist as the result (such that there is one to one mapping between the two lists).
"""

def template3(parameters):
    global queryResultBody1, queryResultHead1, queryResultBody2, queryResultHead2
    secondNumber = 0
    countOfParam = 0
    queryResultBody = []
    queryResultHead = []

    logicalCondition = parameters[0]
    firstNumber = logicalCondition[1]
    if "or" in logicalCondition:
        secondNumber= logicalCondition[4]
    elif "and" in logicalCondition:
        secondNumber = logicalCondition[5]

    global count1, count2
    if(int(firstNumber)==1):
        countOfParam = 3
        count1, queryResultBody1, queryResultHead1 = template1(parameters[1],parameters[2],ast.literal_eval(parameters[3].strip()))
    elif(int(firstNumber)==2):
        countOfParam = 2
        count1, queryResultBody1, queryResultHead1 = template2(parameters[1],parameters[2])

    if(int(secondNumber)==1):
        count2, queryResultBody2, queryResultHead2 = template1(parameters[countOfParam+1],parameters[countOfParam+2],ast.literal_eval(parameters[countOfParam+3].strip()))
    elif(int(secondNumber)==2):
        count2, queryResultBody2, queryResultHead2 = template2(parameters[countOfParam+1],parameters[countOfParam+2])

    combinedBodyHead1 = []
    for i in zip(queryResultBody1, queryResultHead1):
        combinedBodyHead1.append(i)

    combinedBodyHead2 = []
    for i in zip(queryResultBody2, queryResultHead2):
        combinedBodyHead2.append(i)

    joinedList = []
    if "and" in logicalCondition:
        for element in combinedBodyHead1:
            if element in combinedBodyHead2:
                joinedList.append(element)

        for i in range(0,len(joinedList)):
            queryResultBody.append(joinedList[i][0])
            queryResultHead.append(joinedList[i][1])

    elif "or" in logicalCondition:
        joinedList = [*combinedBodyHead1, *combinedBodyHead2]
        queryResultBody, queryResultHead = removeDuplicates(joinedList)

    count = len(queryResultBody)
    return count, queryResultBody, queryResultHead

"""
This function gets called from template3()
It is used to remove the duplicate rules that arise while combining two lists in template3() and returns the list
of unique rules (bodylist and headlist such that there is one to one mapping between the two lists)
"""
def removeDuplicates(joinedList):
    queryResultBody = []
    queryResultHead = []
    tempSet = set()
    for i in range(0, len(joinedList)):
        temp1 = ",".join(str(x) for x in joinedList[i][0])
        temp2 = ",".join(str(x) for x in joinedList[i][1])
        tempSet.add(temp1 + ":" + temp2)

    for element in tempSet:
        data = element.split(":")
        LHS = data[0]
        RHS = data[1]
        LHS_set = LHS.split(",")
        RHS_set = RHS.split(",")
        queryResultBody.append(LHS_set)
        queryResultHead.append(RHS_set)

    return (queryResultBody, queryResultHead)

"""
This function basically parses the input query string to extract the required parameters and calls the respective function
by passing them as the arguments. In the end it prints the final count and the association rules generated.
"""
def getResultsForQuery(query):
    global count, queryResultBody, queryResultHead
    if len(query.strip()) != 0:
            index1 = query.find('(', query.find('(') + 1)
            index2 = query.find(')', query.find(')') + 1)
            query1 = query[index1 + 1:index2]
            query1 = re.split(r',(?![^\(\[]*[\]\)])', query1)
            if 'template1' in query:
                count, queryResultBody, queryResultHead = template1(query1[0],query1[1],ast.literal_eval(query1[2].strip()))
            elif 'template2' in query:
                count, queryResultBody, queryResultHead = template2(query1[0],query1[1])
            elif 'template3' in query:
                count, queryResultBody, queryResultHead = template3(query1)
            else:
                print('not matching template')

            print("Association Rules:")
            for i in range(0,len(queryResultBody)):
                print(queryResultBody[i], "->", queryResultHead[i])
            print("Number of Rules:", count)

"""
Main function which takes the confidence and queries as input as entered by user are passes it to the above 
function getResultsForQuery().
"""
def maintask():
    getFreqSet()
    confidence = input('Enter the confidence: ')
    confidence = float(confidence) / 100
    filterOnConfidence(confidence)
    query = ""
    while(1):
        print('If no further query, then input "quit"')
        query = input('Enter the query: ')
        if(query.strip()=="quit"):
            break
        getResultsForQuery(query)




