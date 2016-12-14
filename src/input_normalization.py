__author__ = 'Jonathan Rubin'

import os
import sys

def run(contbeds,expbeds):
    bedgraphs = list()
    for i in range(len(contbeds)):
        control = contbeds[i]
        experiment = expbeds[i]
        print "Control file: ", control
        print "Experimental file: ", experiment
        filepath = '/'.join(control.split('/')[:-1]) + '/'
        filename = experiment.split('/')[-1]
        os.system("bedtools unionbedg -i " + control  + " " + experiment + " > " + filepath + filename + "_union.BedGraph")
        outfile = open(filepath + filename + "_norm.BedGraph",'w')
        with open(filepath + filename + "_union.BedGraph") as F:
            for line in F:
                line = line.strip().split()
                outfile.write('\t'.join(line[:-2]))
                c = float(line[-2])
                e = float(line[-1])
                v = c-e
                if v < 0:
                    v = 0
                outfile.write('\t' + str(v) + '\n')
        bedgraphs.append(filepath + filename + "_norm.BedGraph")
    return bedgraphs
