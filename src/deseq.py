__author__ = 'Jonathan Rubin'

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import itertools
import numpy as np
from scipy import stats

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
    sites = list()
    with open(counts) as F:
        F.readline()
        for line in F:
            line = line.strip().split()
            site = ':'.join(line[:3])
            d[site] = [[]]
            for val in line[3:]:
                d[site][0].append(float(val))
            indexesi = conditionIndexes[0]
            indexesj = conditionIndexes[1]
            valuesi = [d[site][0][i] for i in indexesi]
            valuesj = [d[site][0][j] for j in indexesj]
            values = list()
            for r in itertools.product(valuesi, valuesj):
                if r[0] == 0 or r[1] == 0:
                    values.append(0.0)
                else:
                    values.append(np.log2(r[1]/r[0]))
            d[site].append(values)
            condition1mean = np.mean(valuesi)
            condition2mean = np.mean(valuesj)
            d[site].append(condition1mean)
            d[site].append(condition2mean)
            meanexpression = np.mean([condition1mean,condition2mean])
            if condition1mean == 0 or condition2mean == 0:
                foldchange = 0.0
            else:
                foldchange = np.log2(condition2mean/condition1mean)
            x.append(meanexpression) 
            d[site].append(meanexpression)
            y.append(foldchange)
            d[site].append(foldchange)
            sites.append(site)

    #d[chr:start:stop] = [[val1,val2,val3,val4,...,valn],[log2foldchangeiterations],condition1mean,condition2mean,meanexpression,log2foldchangemean]

    sigx = list()
    sigy = list()

    low = 10
    high = max(x)
    windows = int(np.log10(high))
    p = 0.01
    for i in range(windows):
        j = (10**i)+low
        k = 10**(i+1)+low if 10**(i+1)+low < high else high
        windowx = list()
        windowy = list()
        keys = list()
        for l in range(len(x)):
            if j < x[l] < k:
                keys.append(sites[l])
                windowx.append(x[l])
                windowy.append(y[l])
        if len(windowy) < 1:
            meany = 0.0
            sy = 0.0
        else:
            meany = np.mean(windowy)
            sy = np.std(windowy)/(len(windowy))**(1/2)
        for key in keys:
            replist = d[key][1]
            meanrep = np.mean(replist)
            srep = np.std(replist)/(len(replist))**(1/2)
            Z = (meany-meanrep)/((sy)**2 + (srep)**2)**(1/2)
            pval = min(stats.norm.cdf(Z),1-stats.norm.cdf(Z))
            # pval = stats.ks_2samp(replist,windowy)[1]
            d[key].append(pval)
            if pval < p:
                sigx.append(d[key][-3])
                sigy.append(d[key][-2])

    #d[chr:start:stop] = [[val1,val2,val3,val4,...,valn],[log2foldchangeiterations],condition1mean,condition2mean,meanexpression,log2foldchangemean,pval]




    F = plt.figure() 
    ax = F.add_subplot(111)
    plt.xscale('log')
    plt.scatter(x,y,c='b',edgecolor="",s=14)
    plt.scatter(sigx,sigy,c='r',edgecolor="",s=14)
    plt.title(conditionNames[1] + ' vs. ' + conditionNames[0])
    plt.ylabel("log2(" + conditionNames[1] + "/" + conditionNames[0] + ")")
    plt.xlabel("Mean Expression")
    plt.savefig(deseqdir + 'MA_plot.png')


            

                
            




            

    