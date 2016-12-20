__author__ = 'Jonathan Rubin'

import numpy as np

def run(counts,conditions):
    d = dict()
    conditionNames = list()
    conditionIndexes = list()
    for i in range(len(conditions)):
        condition = conditions[i]
        if condition not in conditionNames:
            conditionNames.append(condition)
            conditionIndexes.append([i])
        else:
            conditionIndexes[conditionNames.index(condition)].append(i)
    if len(conditionNames) > 2:
        print "Error: More than two conditions. All replicates should be labeled the same."
    with open(counts) as F:
        F.readline()
        for line in F:
            line = line.strip().split()
            site = ':'.join(line[:3])
            d[site] = list()
            for val in line[3:]:
                #d[chr:start:stop] = [val1,val2,val3,val4,...,valn,condition1mean,var1,condition2mean,var2,meanexpression,meandifference]
                d[site].append(float(val))
            for indexlist in conditionIndexes:
                values = list()
                for i in indexlist:
                    values.append(d[site][i])
                d[site].append(np.mean(values))
                d[site].append(np.var(values))
            d[site].append(np.mean([d[site][-4],d[site][-2]]))
            d[site].append(d[site][-5]-d[site][-3])
    print d
            

                
            




            

    