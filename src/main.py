__author__ = 'Jonathan Rubin'


#REQUIREMENTS:
#FSTITCH(https://github.com/azofeifa/FStitch): change Fstitch directory below
#Training file: Create from FStitch readme, change directory below


# This Python Repository takes as input RNAPII ChIP-Seq data (with input controls) and does the following:

# 1. Run FSTITCH (https://github.com/azofeifa/FStitch) to determine ON/OFF regions of the genome.
# 2. Merge ON regions from all replicates and treated/untreated
# 3. Count FPKM of merged ON regions for all replicates (subtract appropriate FPKM from input regions)
# 4. Generate FPKM counts for all ON regions (averaged over replicates)
# 5. Run regions through DE-Seq
# 6. Filter regions from Ref-Seq annotated genes
# 7. Run MEME to get motifs
# 8. Run Tomtom to get TFs

import fstitch

#Return parent directory
def parent_dir(directory):
    pathlist = directory.split('/')
    newdir = '/'.join(pathlist[0:len(pathlist)-1])
    
    return newdir

#Src directory
srcdir = os.path.dirname(os.path.realpath(__file__))

#Fstitch bed file directory
fstitchbed = parent_dir(srcdir) + '/fstitch_bed/'


#User-defined Input:
#=========================================================================================================
#Training file directory
trainingdir = parent_dir(srcdir) + '/training_files/'

#Fstitch directory
fstitchdir = parent_dir(srcdir) + '/FStitch/src/FStitch'

#BedGraph files
bedgraphs = ['/scratch/Shares/dowell/Pelish_RNAPII/bowtie/sortedbam/genomecoveragebed/fortdf/SRR1768126.fastq.bowtie2.sorted.BedGraph.reflected.sorted.BedGraph.mp.BedGraph', \
            '/scratch/Shares/dowell/Pelish_RNAPII/bowtie/sortedbam/genomecoveragebed/fortdf/SRR1768127.fastq.bowtie2.sorted.BedGraph.reflected.sorted.BedGraph.mp.BedGraph', \
            '/scratch/Shares/dowell/Pelish_RNAPII/bowtie/sortedbam/genomecoveragebed/fortdf/SRR1768128.fastq.bowtie2.sorted.BedGraph.reflected.sorted.BedGraph.mp.BedGraph', \
            '/scratch/Shares/dowell/Pelish_RNAPII/bowtie/sortedbam/genomecoveragebed/fortdf/SRR1768129.fastq.bowtie2.sorted.BedGraph.reflected.sorted.BedGraph.mp.BedGraph', \
            '/scratch/Shares/dowell/Pelish_RNAPII/bowtie/sortedbam/genomecoveragebed/fortdf/SRR1768130.fastq.bowtie2.sorted.BedGraph.reflected.sorted.BedGraph.mp.BedGraph', \
            '/scratch/Shares/dowell/Pelish_RNAPII/bowtie/sortedbam/genomecoveragebed/fortdf/SRR1768131.fastq.bowtie2.sorted.BedGraph.reflected.sorted.BedGraph.mp.BedGraph', \
            '/scratch/Shares/dowell/Pelish_RNAPII/bowtie/sortedbam/genomecoveragebed/fortdf/SRR1768132.fastq.bowtie2.sorted.BedGraph.reflected.sorted.BedGraph.mp.BedGraph', \
            '/scratch/Shares/dowell/Pelish_RNAPII/bowtie/sortedbam/genomecoveragebed/fortdf/SRR1768133.fastq.bowtie2.sorted.BedGraph.reflected.sorted.BedGraph.mp.BedGraph']
#=========================================================================================================

def run():
    fstitch(fstitchdir,trainingdir,bedgraphs,fstitchbed)


