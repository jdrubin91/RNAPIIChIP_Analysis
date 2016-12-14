import sys

file1 = sys.argv[1]
outfile = open(file1.split('.txt')[0]+'_fixed.txt','w')

with open(file1) as F:
	for line in F:
		line = line.split(':')
		chr = line[0]
		start = ''.join(line[1].split('-')[0].split(','))
		stop = ''.join(line[1].split('-')[1].split()[0].split(','))
		signal = line[1].split('-')[1].split()[1]
		outfile.write(chr+'\t'+start+'\t'+stop+'\t'+signal + '\n')
		
