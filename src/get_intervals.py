__author__ = 'Jonathan Rubin'

import os
import numpy as np
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

def subtract_files(file1,file2,outfilename):
    linelist = list()
    with open(file1) as F1:
        with open(file2) as F2:
            for line in F1:
                line2 = F2.readline()
                line = line.strip().split()
                linelist.append('\t'.join(line[:3]) + '\t')
                line2 = line2.strip().split()
                for i in range(3,len(line)):
                    val1 = int(line[i])
                    val2 = int(line2[i])
                    if val1-val2 > 0:
                        linelist.append(str(val1-val2)+'\t')
                    else:
                        linelist.append('0\t')
                linelist.append('\n')
    outfile = open(outfilename, 'w')
    for line in linelist:
        outfile.write(line)
    outfile.close()

def normalize_file(infile,outfile):
    sites = list()
    vals = list()
    with open(infile) as F:
        for line in F:
            line = line.strip().split()
            sites.append(line[:3])
            vals.append([float(x) for x in line[3:]])
    t = np.array(vals).T
    norm_factors = list()
    for i in range(len(t)):
        norm_factors.append(sum(t[i]))
    mean = np.mean(norm_factors)
    for j in range(len(norm_factors)):
        norm_factors[j] = norm_factors[j]/mean
    print norm_factors
    outfile = open(outfile,'w')
    for k in range(len(sites)):
        outfile.write('\t'.join(sites[k]))
        outfile.write('\t')
        for l in range(len(norm_factors)):
            outfile.write(str(norm_factors[l]*vals[k][l]) + '\t')
        outfile.write('\n')



                    

def run(onregions,expbeds,contbeds,deseqdir,conditions,norm):
    header = 'chr\tstart\tstop\t' + '\t'.join(conditions)
    os.system("cat " + ' '.join(onregions) + " > " + deseqdir + "fstitch_allON_regions.bed")
    a = pybt.BedTool(deseqdir + "fstitch_allON_regions.bed").cut([0,1,2]).sort().merge()
    a.saveas(deseqdir + "expcounts.bed")
    for file1 in expbeds:
        b = a.map(b=file1,c=4,o="sum",null="0")
        b.saveas(deseqdir + "temp.bed")
        append(deseqdir+"expcounts.bed",deseqdir+"temp.bed")
    if norm:
        a.saveas(deseqdir + "contcounts.bed")
        for file2 in contbeds:
            b = a.map(b=file2,c=4,o="sum",null="0")
            b.saveas(deseqdir + "temp.bed")
            append(deseqdir+"contcounts.bed",deseqdir+"temp.bed")
        subtract_files(deseqdir + "expcounts.bed",deseqdir + "contcounts.bed",deseqdir+"subcounts.bed")
        normalize_file(deseqdir+"subcounts.bed",deseqdir+"normcounts.bed")
        add_header(deseqdir+"normcounts.bed",header)
        return deseqdir+"normcounts.bed"
    else:
        normalize_file(deseqdir+"expcounts.bed",deseqdir+"normcounts.bed")
        add_header(deseqdir+"normcounts.bed",header)
        return deseqdir+"normcounts.bed"



