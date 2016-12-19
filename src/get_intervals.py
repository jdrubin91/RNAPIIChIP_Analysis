__author__ = 'Jonathan Rubin'

import os

def run(bedgraphs,deseqdir):
    os.system("cat " + ' '.join(bedgraphs) + " > " + deseqdir + "fstitch_allON_regions.bed")
    os.system("sort -k1,1 -k2,2n fstitch_allON_regions.bed > fstitch_allON_regions.sorted.bed")
    os.system("bedtools merge -i " + deseqdir + "fstitch_allON_regions.sorted.bed > " + deseqdir + "fstitch_allON_regions.sorted.merged.bed")

