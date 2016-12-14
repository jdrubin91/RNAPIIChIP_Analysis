__author__ = 'Jonathan Rubin'


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

#Training file directory
trainingfile = parent_dir(srcdir) + '/training_files/training_set_fixed.txt'

def run():
    fstitch(trainingfile)


