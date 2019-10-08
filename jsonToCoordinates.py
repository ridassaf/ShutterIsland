import json
import sys
import os
import random

def keyword(w):
	if 'mobile' in w or 'phage' in w or 'translocase' in w or 'protease' in w or 'terminase' in w or 'terminase' in w or 'resolvase' in w  or 'transpos' in w  or 'recombin' in w  or 'integrase' in w:
		return True
	return False

def valid(f):
	if f is not None and  len(f) > 0 and f[0] is not None and len(f[0]) > 1 and f[0][1] is not None  and 'blast' not in f[0][1].lower() and 'PGF' in f[0][1]:
		return True
	return False

 

height = 300
width = 300

colors = ["vlred", "lred", "dred", "vlblue", "lblue", "dblue", "vlgreen", "lgreen", "dgreen", "lyellow", "dyellow", "lorange", "orange", "gold", "lgrey", "dgrey", "vdgrey", "lbrown", "dbrown", "purple", "maroon", "salmon", "magneta", "magneta4"]

random.shuffle(colors)

###
p2p = {}
p2p_file = open('../manualpegtopgf.tab', 'r')
for row in p2p_file:
	cols = row.strip().split('\t')
	if len(cols[0]) > 0 and len(cols[1]) > 0:
		p2p[cols[0]] = cols[1]
p2p_file.close()
p2p_file = open('../pegtopgf.tab', 'r')
for row in p2p_file:
	cols = row.strip().split('\t')
	if len(cols[0]) > 0 and len(cols[1]) > 0:
		p2p[cols[0]] = cols[1]
p2p_file.close()

out = open('Coords/xyc.txt', 'w')
for filename in os.listdir(sys.argv[1]):
	if filename[0] == '.' or os.stat(sys.argv[1] + '/' + filename).st_size == 0 or 'json' not in filename.lower():
		continue

	with open(sys.argv[1] + '/' + filename,'r') as ff:
		data = json.load(ff)
	ff.close()
	if data['result'] is None:
		continue
	num_genomes = len(data['result'][0])
	num_pegs = len(data['result'][0][0]['features']) - 1
	if num_pegs == 0:
		continue

	per_peg = width / num_pegs - 10 #10 for the arrow

	### Get maximum size ### and assign color #########
	max_size = 0
	count = 0
	colormap = {}
	r = data['result'][0][0] #only the query genome
	for f in r['features']:
		if f['type'] == 'blast':
			continue

		size = f['size'] 
		if size > max_size:
			max_size = size

		if f['function'] is not None and keyword(f['function'].lower()):
			continue
		elif 'rna' in f['type'].lower():
			continue

		# skip assigning color to pin peg or some functionality peg:
		if f['fid'] in p2p: 
			pgf = p2p[f['fid']]
			if pgf not in colormap and count < 24:
				colormap[pgf] = colors[count]
				count += 1
	###################################################

	g_count = -1
	ppwa = width / num_pegs
	center = 0
	out.write('>'+filename+'\n')
	for r in data['result'][0]:
		g_count += 1
		blast = r['pinned_peg']
		if r['pinned_peg_strand'] == '+':
			features = sorted(r['features'], key=lambda k: k['fid'])
		elif r['pinned_peg_strand'] == '-':
			features = sorted(r['features'], key=lambda k: k['fid'], reverse=True)
		cc = 0
		for f in features:
			if len(f['attributes']) > 0 or f['fid'] in p2p:
				cc += 1
				if f['fid'] == blast:
					break
		if g_count == 0:
			center = cc

		p_count = center - cc # increase offset to center anchor
		for f in features:
			# check if peg has known pgf 
			if f['type'] == 'blast':
				continue
			if f['fid'] in p2p: 
				pgf = p2p[f['fid']] 
			elif valid(f['attributes']):
				pgf = f['attributes'][0][0]
			else:
				continue
						
			# assign color to peg 
			c = ''
			if f['fid'] == blast:
				c = 'red' # color of the anchor
			elif phage(f['function']):
				c = 'blue'
			elif mobile(f['function']):
				c = 'green'
			elif rna(f['function'].lower()):
				c = 'yellow' 
			elif pgf in colormap:
				c = colormap[pgf]
			else:
				c = 'black'
				
			# assign size and location 	
			size = min(f['size'], max_size)
			l = round(float(size)/max_size*per_peg) 
			xoffset = p_count * ppwa
			p_count += 1
			
			margin = (per_peg - l)/ 2.0
			strand = f['strand']
			yoffset = g_count * 15

			points = []
			if strand == '+':
				x1 = xoffset + margin
				y1 = yoffset + 5
				out.write(c+'\n')
				out.write(str(x1) + '\t' + str(y1) + '\n')
				out.write(str(x1 + l) + '\t'+ str(y1) + '\n')
				out.write(str(x1 + l) + '\t'+ str(y1 - 2.5) + '\n')#arrow up
				out.write(str(x1 + l + 10) + '\t' +str( y1 + 2.5) + '\n') #arrow forward
				out.write(str(x1 + l) + '\t' +str( y1 + 7.5) + '\n') #arrow down
				out.write(str(x1 + l) + '\t' +str( y1 + 5) + '\n') #arrow up
				out.write(str(x1) + '\t' +str( y1 + 5) + '\n')

			elif strand == '-':
				x1 = xoffset + 10 + margin
				y1 = yoffset + 5
				out.write(c+'\n')
				out.write(str(x1) + '\t' +str( y1) + '\n')
				out.write(str(x1) + '\t' +str( y1 - 2.5) + '\n')#arrow up
				out.write(str(x1 - 10) + '\t'+ str( y1 + 2.5) + '\n') #arrow backward
				out.write(str(x1) + '\t' +str( y1 + 7.5) + '\n') #arrow downward
				out.write(str(x1) + '\t' +str( y1 + 5) + '\n') #arrow up
				out.write(str(x1 + l) + '\t' +str( y1 + 5) + '\n')
				out.write(str(x1 + l) + '\t' +str( y1) + '\n')
out.close()
