__author__ = 'Jonathan Rubin'

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def run(counts,conditions,deseqdir):
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
    x = list()
    y = list()
    with open(counts) as F:
        F.readline()
        for line in F:
            line = line.strip().split()
            site = ':'.join(line[:3])
            d[site] = list()
            for val in line[3:]:
                #d[chr:start:stop] = [val1,val2,val3,val4,...,valn,condition1mean,var1,condition2mean,var2,meanexpression,log2foldchange]
                d[site].append(float(val))
            for indexlist in conditionIndexes:
                values = list()
                for i in indexlist:
                    values.append(d[site][i])
                d[site].append(np.mean(values))
                d[site].append(np.var(values))
            meanexpression = np.mean([d[site][-4],d[site][-2]])
            if d[site][-4] == 0 or d[site][-2] == 0:
                foldchange = 0.0
            else:
                foldchange = np.log2(d[site][-4]/d[site][-2])
            x.append(meanexpression) 
            d[site].append(meanexpression)
            y.append(foldchange)
            d[site].append(foldchange)
    F = plt.figure() 
    ax = F.add_subplot(111)
    plt.scatter(x,y,c='b',edgecolor="",s=14)
    plt.savefig(deseqdir + 'MA_plot.png')
            

                
            




            

    