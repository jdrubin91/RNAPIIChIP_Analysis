__author__ = 'Jonathan Rubin'

import os
import pybedtools as pybt

def append(file1,file2):
    linelist = list()
    with open(file1) as F1:
        with open(file2)as F2:
            for line1 in F1:
                line2 = F2.readline()
                add = line2.strip().split()[-1]
                linelist.append(line1.strip() + '\t' + add + '\n')
    
    outfile = open(file1,'w')
    for line in linelist:
        outfile.write(line)

def add_header(file1,header):
    linelist = list()
    with open(file1) as F:
        for line in F:
            linelist.append(line)
            
    outfile = open(file1,'w')
    outfile.write(header + '\n')
    for line in linelist:
        outfile.write(line)

def run(onregions,bedgraphs,deseqdir):
    os.system("cat " + ' '.join(onregions) + " > " + deseqdir + "fstitch_allON_regions.bed")
    print "cat " + ' '.join(onregions) + " > " + deseqdir + "fstitch_allON_regions.bed"
    a = pybt.BedTool(deseqdir + "fstitch_allON_regions.bed").cut([0,1,2]).sort().merge()
    a.saveas(deseqdir + "counts.bed")
    header = list()
    for file1 in bedgraphs:
        header.append(file1.split('/')[-1])
        b = a.map(b=file1,c=4,o="sum")
        b.saveas(deseqdir + "temp.bed")
        append(deseqdir+"counts.bed",deseqdir+"temp.bed")

    add_header(deseqdir+"counts.bed",'\t'.join(header))


