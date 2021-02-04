import numpy
import scipy.cluster.hierarchy as hcluster
import sys

# Read the gene numbers (using peg numbering) that were predicted as islands
data = numpy.zeros(shape=(1000,1))
input = open('islands.txt','r')
index = 0
for row in input:
	data[index] = int(row.strip())
	index += 1
input.close()


# Cluster the separate gene predictions into full islands
thresh = 8
clusters = hcluster.fclusterdata(data, thresh, criterion="distance")

# The code below reads in the genome.PATRIC.cds.tab file, and write the contig and coordinates of islands found
output = []
headers= []
for i in range(len(clusters)):
	c = [int(data[j][0]) for j in range(len(clusters)) if clusters[j] == clusters[i] and data[j] != 0]
	if len(c) >= 3 and c not in output:
		output.append(c)
		headers.append((c[0],c[len(c)-1]))

for h in headers:
	print str(h[0]) + '\t' + str(h[1])

input = open(sys.argv[1],'r') # genome file name .patric.cds.tab
line = 0
for row in input:
	columns = row.strip().split('\t')
	if line > 0:
		output = open(columns[0] + '.islands', 'a')
	for h in headers:
		if line == h[0]:
			output.write(columns[0] + '\t' + columns[2] + '\t' + columns[9] + '\t')
		if line == h[1]:
			output.write(columns[10] + '\n')
	line += 1
input.close()
output.close()
