
import treeplot
import pydot

def loadDataSet(filepath):
    '''
    Returns
    -----------------
    data: 2-D list
        each row is the feature and label of one instance
    featNames: 1-D list
        feature names
    '''
    data=[]
    featNames = None
    fr = open(filepath)
    for (i,line) in enumerate(fr.readlines()):
        array=line.strip().split(',')
        if i == 0:
            featNames = array[:-1]
        else:
            data.append(array)
    return data, featNames


def splitData(dataSet, axis, value):
    '''
    Split the dataset based on the given axis and feature value

    Parameters
    -----------------
    dataSet: 2-D list
        [n_sampels, m_features + 1]
        the last column is class label
    axis: int 
        index of which feature to split on
    value: string
        the feature value to split on

    Returns
    ------------------
    subset: 2-D list 
        the subset of data by selecting the instances that have the given feature value
        and removing the given feature columns
    '''
    subset = []
    for instance in dataSet:
        if instance[axis] == value:    # if contains the given feature value
            reducedVec = instance[:axis] + instance[axis+1:] # remove the given axis
            subset.append(reducedVec)
    return subset


def chooseBestFeature(dataSet):
    '''
    choose best feature to split based on Gini index
    
    Parameters
    -----------------
    dataSet: 2-D list
        [n_sampels, m_features + 1]
        the last column is class label

    Returns
    ------------------
    bestFeatId: int
        index of the best feature
    '''
    gain = []

    def gini_index(input_dict, data_list):
        result = 1
        for freq in input_dict.values():
            result -= (freq / len(data_list))**2
        return result

    def classDict(recordList):
        result = dict()
        for record in recordList:
            label = record[len(record) - 1]  # class label
            if label in result:
                result[label] += 1
            else:
                result[label] = 1
        return result

    for featureIndex in range(len(dataSet[0]) - 1):
        parentDict = dict()                 # dict of parent node labels
        childrenDict = dict()               # dict of child node labels  
        childrenGiniSum = 0                 # rhs of Gain formula
        valueList = []                      # list of values for an attribute of a record
        # create parent dictionary
        parentDict = classDict(dataSet)
        for record in dataSet:
            value = record[featureIndex]
            if value not in valueList:
                valueList.append(value)
        # calculate parent gini index
        parentGiniIndex = gini_index(parentDict, dataSet)
        for value in valueList:
            subset = splitData(dataSet, featureIndex, value)
            childrenDict.clear()
            # create children dictionary
            childrenDict = classDict(subset)
            # calculate children gini index
            childrenGiniIndex = gini_index(childrenDict, subset)
            childrenGiniSum += ((len(subset) / len(dataSet)) *  childrenGiniIndex)
        gain.append(parentGiniIndex - childrenGiniSum)

    bestFeatId = gain.index(max(gain))
    #TODO
    return bestFeatId  


def stopCriteria(dataSet):
    '''
    Criteria to stop splitting: 
    1) if all the classe labels are the same, then return the class label;
    2) if there are no more features to split, then return the majority label of the subset.

    Parameters
    -----------------
    dataSet: 2-D list
        [n_sampels, m_features + 1]
        the last column is class label

    Returns
    ------------------
    assignedLabel: string
        if satisfying stop criteria, assignedLabel is the assigned class label;
        else, assignedLabel is None 
    '''
    assignedLabel = None 
    classLabels = dict()
    
    # populate dictionary with class labels
    for record in dataSet:
        try: 
            label = record[(len(record) - 1)]
        except Exception as exceptionMsg:
            print('Couldn\'t parse first record', exceptionMsg)
        if label in classLabels:
            classLabels[label] += 1
        else:
            classLabels[label] = 2

    # assign the stopping criteria assignedLabel
    if len(classLabels) == 1:
        assignedLabel = label
    elif len(record) == 1:
        assignedLabel = max(classLabels.keys())
    # TODO
    return assignedLabel



def buildTree(dataSet, featNames):
    '''
    Build the decision tree

    Parameters
    -----------------
    dataSet: 2-D list
        [n'_sampels, m'_features + 1]
        the last column is class label

    Returns
    ------------------
        myTree: nested dictionary
    '''
    assignedLabel = stopCriteria(dataSet)
    if assignedLabel:
        return assignedLabel

    bestFeatId = chooseBestFeature(dataSet)
    bestFeatName = featNames[bestFeatId]

    myTree = {bestFeatName:{}}
    subFeatName = featNames[:]
    del(subFeatName[bestFeatId])
    featValues = [d[bestFeatId] for d in dataSet]
    uniqueVals = list(set(featValues))
    for value in uniqueVals:
        myTree[bestFeatName][value] = buildTree(splitData(dataSet, bestFeatId, value), subFeatName)
    
    return myTree



if __name__ == "__main__":
    data, featNames = loadDataSet('golf.csv')
    dtTree = buildTree(data, featNames)
    print (dtTree) 
