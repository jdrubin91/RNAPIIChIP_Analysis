__author__ = 'Jonathan Rubin'

import pybedtools as pybt
import os

def run(intervalfile,motiffiles):
    a = pybt.BedTool(intervalfile).cut([0,1,2]).sort()
    for motiffile in os.listdir(motiffiles):
        b = pybt.BedTool(motiffile).cut([0,1,2]).sort()
        

