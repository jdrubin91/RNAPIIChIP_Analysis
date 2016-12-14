__author__ = 'Jonathan Rubin'

#Runs FStitch
#Requires a training set

import os

def run(fstitchdir,trainingdir,bedgraphs,fstitchbed):
    trainingfile = trainingdir + 'training_set_fixed.txt'
    for file1 in bedgraphs:
        filename = file1.split('/')[-1]
        os.system(fstitchdir + "train -i " + file1 + " -j " + trainingfile + " -o " + trainingdir + filename + "_parameters.out") 
        os.system(fstitchdir + "segment -i " + file1 + " -k " + trainingdir + filename + "_parameters.out" + " -o " + fstitchbed + filename + ".bed")



