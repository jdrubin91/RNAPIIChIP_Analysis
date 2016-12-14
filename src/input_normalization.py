__author__ = 'Jonathan Rubin'

import os
import sys

def run(contbeds,expbeds):
    bedgraphs = list()
    for i in range(len(contbeds)):
        control = contbeds[i]
        experiment = expbeds[i]
        filepath = '/'.join(control.split('/')[:-1]) + '/'
        filename = experiment.split('/')[-1]
        os.system("bedtools unionbedg -i " + control  + " " + experiment + " > " + filepath + filename + "_norm.BedGraph")
        bedgraphs.append(filepath + filename + "_norm.BedGraph")
    return bedgraphs
