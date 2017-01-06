__author__ = 'Jonathan Rubin'


#REQUIREMENTS:
#module load bedtools2_2.22.0
#FSTITCH(https://github.com/azofeifa/FStitch): change Fstitch directory below
#Training file: Create from FStitch readme, change directory below


# This Python Repository takes as input RNAPII ChIP-Seq data (with input controls) and does the following:

# 1. Run FSTITCH (https://github.com/azofeifa/FStitch) to determine ON/OFF regions of the genome.
# 2. Merge ON regions from all replicates and treated/untreated
# 3. Count FPKM of merged ON regions for all replicates
# 4. Generate FPKM counts for all ON regions
# 5. Run through DE-Seq
# 6. Filter regions from Ref-Seq annotated genes
# 7. Run MEME to get motifs
# 8. Run Tomtom to get TFs

import os
import fstitch
import input_normalization
import get_intervals
import deseq
import motif_enrichment

#Return parent directory
def parent_dir(directory):
    pathlist = directory.split('/')
    newdir = '/'.join(pathlist[0:len(pathlist)-1])
    
    return newdir

#Src directory
srcdir = os.path.dirname(os.path.realpath(__file__))

#Fstitch bed file directory
fstitchbed = parent_dir(srcdir) + '/fstitch_bed/'

#DE-Seq files directory
deseqdir = parent_dir(srcdir) + '/deseq_files/'

#Gene annotations file
geneannotations = parent_dir(srcdir) + '/RefSeqHG19.bed'

#User-defined Input:
#=========================================================================================================
#Training file directory
trainingdir = parent_dir(srcdir) + '/training_files/'

#Fstitch directory
fstitchdir = parent_dir(srcdir) + '/FStitch/src/FStitch'

#BedGraph files (if not using normalization module)
bedgraphs = []

#Normalize to control? - This module was under construction but is no longer functional. Normalization now happens
#after Fstitch (All FStitch regions get subtracted from input when counting reads over regions before DE-Seq)
normalize = False

#Control BedGraph files (order corresponds to expbeds) - Leave as empty list if you don't want to normalize to control (or have done so in some other way)
contbeds = ['/scratch/Shares/dowell/Pelish_RNAPII/bowtie/sortedbam/genomecoveragebed/fortdf/SRR1768126.fastq.bowtie2.sorted.BedGraph.reflected.sorted.BedGraph', \
            '/scratch/Shares/dowell/Pelish_RNAPII/bowtie/sortedbam/genomecoveragebed/fortdf/SRR1768127.fastq.bowtie2.sorted.BedGraph.reflected.sorted.BedGraph', \
            '/scratch/Shares/dowell/Pelish_RNAPII/bowtie/sortedbam/genomecoveragebed/fortdf/SRR1768130.fastq.bowtie2.sorted.BedGraph.reflected.sorted.BedGraph', \
            '/scratch/Shares/dowell/Pelish_RNAPII/bowtie/sortedbam/genomecoveragebed/fortdf/SRR1768131.fastq.bowtie2.sorted.BedGraph.reflected.sorted.BedGraph']

#Experimental BedGraph files (order corresponds to contbeds)
expbeds = ['/scratch/Shares/dowell/Pelish_RNAPII/bowtie/sortedbam/genomecoveragebed/fortdf/SRR1768128.fastq.bowtie2.sorted.BedGraph.reflected.sorted.BedGraph', \
            '/scratch/Shares/dowell/Pelish_RNAPII/bowtie/sortedbam/genomecoveragebed/fortdf/SRR1768129.fastq.bowtie2.sorted.BedGraph.reflected.sorted.BedGraph', \
            '/scratch/Shares/dowell/Pelish_RNAPII/bowtie/sortedbam/genomecoveragebed/fortdf/SRR1768132.fastq.bowtie2.sorted.BedGraph.reflected.sorted.BedGraph', \
            '/scratch/Shares/dowell/Pelish_RNAPII/bowtie/sortedbam/genomecoveragebed/fortdf/SRR1768133.fastq.bowtie2.sorted.BedGraph.reflected.sorted.BedGraph']

#Condition names: Assign a condition to your bedgraph files in the order that they appear in expbeds
conditions = ['DMSO','DMSO','CA','CA']

#Filter for gene annotations? (Only search unnanotated regions for motif hits?)
genefilter = False

norm = len(contbeds)>0
#=========================================================================================================

def run():
    if normalize:
        "Normalizing BedGraphs..."
        bedgraphs = input_normalization.run(contbeds,expbeds)
        "done"
    else:
        bedgraphs = expbeds
    "Running FStitch..."
    # onregions = fstitch.run(fstitchdir,trainingdir,expbeds,fstitchbed)
    onregions = [geneannotations]
    "done\nGetting Interval File..."
    counts = get_intervals.run(onregions,expbeds,contbeds,deseqdir,conditions,norm=True,geneannotations,genefilter)
    results = deseq.run(counts,conditions,deseqdir)
    motif_enrichment.run()




