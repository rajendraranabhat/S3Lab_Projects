
from scipy.cluster.vq import kmeans, whiten, vq
from math import log
import pandas as pd
import numpy as np

"""
Substitutes values of the nominal variables (such as surgeon's ID) and categorical variables with more than two levels
with the corresponding log ratios

input : feature_input, outcome - Series Objects
        limit - int (minimum number of records for a categorical feature level in order not to be labeled as "other"
                     level)
        number_of_clusters - int (number of clusters in the "other" level in order to run a k-means algorithm and
                                  create number_of_clusters "new" levels instead of "other" level)

returns : output - dictionary with the following fields
                : d - ndarray (new levels of each input data record in feature_input)
                : vocabulary - ndarray (original levels)
                : cl_vocabulary (optional) - Pandas DataFrame (correspondence between the original "other" levels and
                                             the clusters)
                : p - ndarray (new levels)
                : cl_p (optional) - ndarray ("new" levels in the "other" level)

"""

def train_categorical_feature(feature_input, outcome, limit, number_of_clusters):
    
    input = feature_input.values
    
    if len(pd.unique(input)) == 2:
        vocabulary = np.unique(input)
        p = np.array([0, 1])
        d = np.zeros(len(input), dtype = np.int)
        d[input == vocabulary[1]] = 1
        output = dict(zip(["d", "vocabulary", "p"], [d, vocabulary, p]))
        print output
        return output
    
    vocabulary_t = pd.unique(input)
    count_1 = np.zeros(len(vocabulary_t), dtype = int)
    count_0 = np.copy(count_1)
    
    
    outcome_1 = outcome.values == 1
    outcome_0 = outcome.values == 0
    for index, item in enumerate(vocabulary_t):
        if pd.notnull(item):
            count_1[index] = sum((input == item) * (outcome_1))
            count_0[index] = sum((input == item) * (outcome_0))
        else:
            count_1[index] = sum(pd.isnull(input) * (outcome_1))
            count_0[index] = sum(pd.isnull(input) * (outcome_0))
    
    condition = (count_0 + count_1) >= limit
    condition[pd.isnull(vocabulary_t)] = True
#    n = sum(condition)
#    vocabulary = np.zeros(n, dtype = str)
#    p = np.zeros(n)
    
    def log_ratio(count_1, count_0):
        if count_1 == 0:
            return log(1/(2*float(count_0)))
        elif count_0 == 0:
            return log(2*count_1)
        else:
            return log(count_1/float(count_0))
        
    v_log_ratio = np.vectorize(log_ratio)
    
    vocabulary = vocabulary_t[condition]
    p = v_log_ratio(count_1[condition], count_0[condition])
    
#    index = 0
#    for i in range(len(vocabulary_t)):
#        if (condition[i]):
#            vocabulary[index] = str(vocabulary_t[index])
#            p[index] = log_ratio(count_1[index], count_0[index])
#            index = index + 1
#            if (count_1[index] == 0):
#                p[index] = log(1./(2*count_0[index]))
#            elif (count_0[index] == 0):
#                p[index] = log(2*count_1[index])
#            else:
#                p[index] = log(count_1[index]./count_0[index])
    # print "sum(condition == 0) is {0}".format(sum(condition == 0))
    if sum(condition == 0) <= 1:
        if sum(condition == 0) == 1:
            p = np.append(p, log_ratio(count_1[condition == 0][0], count_0[condition == 0][0]))
#           if (count_1[condition == 0][0] == 0):
#                p[condition == 0] = log(1./(2*count_0[condition == 0][0]))
#           elif (count_0[condition == 0] == 0):
#                p[condition == 0] = log(2*count_1[condition == 0][0])
#           else:
#                p[condition == 0] = log(count_1[condition == 0][0]./count_0[condtion == 0][0])
            vocabulary = np.append(vocabulary, vocabulary_t[condition == 0])
    else:
        # print "number of clusters {0}".format(number_of_clusters)
        cl = min(number_of_clusters, sum(condition == 0) - 1) # why is it -1 here?
        # cl_vocabulary = pd.DataFrame()
        # print "cl {0}".format(cl)
        residual_1 = count_1[condition == 0]
        residual_0 = count_0[condition == 0]
        # print "length of the residual_1 {0}".format(len(residual_1))
#        s = np.zeros(len(residual_1))
        s = v_log_ratio(residual_1, residual_0).reshape([len(residual_1), 1]) 
        whitened = whiten(s)
        codebook = kmeans(whitened, cl)[0]
        code = vq(whitened, codebook)[0]
        # print "length of code {0}".format(len(code))
        s1 = pd.Series(data = vocabulary_t[condition == 0]) # .astype(str)
        s2 = pd.Series(data = code)
        cl_vocabulary = pd.DataFrame.from_dict({"cat_feature_input": s1, "cluster_id": s2})

        #print cl_vocabulary.axes

        cl_p = np.zeros(cl, dtype = float)
        # print cl_p, len(cl_p)
        
        for i in range(cl):
            # print i
            c1 = residual_1[code == i]
            c0 = residual_0[code == i]
            cl_p[i] = log_ratio(sum(c1), sum(c0))
            # print "Hey"
    
    d = np.zeros(len(input))
    d[pd.isnull(input)] = p[pd.isnull(vocabulary)]
    
    for i in range(len(vocabulary)):
        d[input == vocabulary[i]] = p[i]
    vocabulary = vocabulary.astype(str)

    if 'cl_vocabulary' in locals():
        print "cl_vocabulary in locals()"
        for i in range(len(cl_vocabulary)):
            d[input == cl_vocabulary.loc[i, "cat_feature_input"]] = cl_p[cl_vocabulary.loc[i, "cluster_id"]]
        #print cl_vocabulary.axes
        cl_vocabulary.loc[:, "cat_feature_input"] = cl_vocabulary["cat_feature_input"].astype(str)
        # print cl_vocabulary["cat_feature_input"].apply(type)
    
        output = dict(zip(["d", "vocabulary", "cl_vocabulary", "p", "cl_p"], [d, vocabulary, cl_vocabulary, p, cl_p]))
    else:
        output = dict(zip(["d", "vocabulary", "p"], [d, vocabulary, p]))

    #print output
    return output