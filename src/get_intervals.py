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
    outfile.close()

def add_header(file1,header):
    linelist = list()
    with open(file1) as F:
        for line in F:
            linelist.append(line)
            
    outfile = open(file1,'w')
    outfile.write(header + '\n')
    for line in linelist:
        outfile.write(line)

def subtract_files(file1,file2,outfilename,absolute=True):
    linelist = list()
    with open(file1) as F1:
        with open(file2) as F2:
            for line in F1:
                line2 = F2.readline()
                line = line.strip().split()
                linelist.append('\t'.join(line[:3]))
                line2 = line2.strip().split()
                for i in range(3,len(line[3:])):
                    val1 = float(line[i])
                    val2 = float(line2[i])
                    if absolute:
                        linelist.append(str(abs(val1-val2))+'\t')
                    else:
                        linelist.append(str(val1-val2)+'\t')
                linelist.append('\n')
    outfile = open(outfilename, 'w')
    for line in linelist:
        outfile.write(line)
    outfile.close()
                    

def run(onregions,expbeds,contbeds,deseqdir,names):
    os.system("cat " + ' '.join(onregions) + " > " + deseqdir + "fstitch_allON_regions.bed")
    print "cat " + ' '.join(onregions) + " > " + deseqdir + "fstitch_allON_regions.bed"
    a = pybt.BedTool(deseqdir + "fstitch_allON_regions.bed").cut([0,1,2]).sort().merge()
    a.saveas(deseqdir + "expcounts.bed")
    a.saveas(deseqdir + "contcounts.bed")
    header = list()
    for file1 in expbeds:
        b = a.map(b=file1,c=4,o="sum")
        b.saveas(deseqdir + "temp.bed")
        append(deseqdir+"expcounts.bed",deseqdir+"temp.bed")
    add_header(deseqdir+"expcounts.bed",'\t'.join(names))
    for file2 in contbeds:
        b = a.map(b=file2,c=4,o="sum")
        b.saveas(deseqdir + "temp.bed")
        append(deseqdir+"contcounts.bed",deseqdir+"temp.bed")
    add_header(deseqdir+"contcounts.bed",'\t'.join(names))
    subtract_files(deseqdir + "expcounts.bed",deseqdir + "contcounts.bed",deseqdir+"normcounts.bed")



