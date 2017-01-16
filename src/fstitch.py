__author__ = 'Jonathan Rubin'

#Runs FStitch
#Requires a training set

import os

def run(fstitchdir,trainingdir,bedgraphs,fstitchbed):
    trainingfile = trainingdir + 'training_set_fixed.txt'
    newbedgraphs = list()
    for file1 in bedgraphs:
        filename = file1.split('/')[-1]
        os.system(fstitchdir + " train -i " + file1 + " -j " + trainingfile + " -o " + trainingdir + filename + "_parameters.out") 
        os.system(fstitchdir + " segment -i " + file1 + " -k " + trainingdir + filename + "_parameters.out" + " -o " + fstitchbed + filename + ".bed")
        outfile = open(fstitchbed + filename + "_ON.bed",'w')
        with open(fstitchbed + filename + ".bed") as F:
            for line in F:
                if 'ON' in line:
                    outfile.write(line)
        newbedgraphs.append(fstitchbed + filename + "_ON.bed")
    return newbedgraphs