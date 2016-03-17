# -*- coding: UTF-8 -*-
# 

import random,time,copy,sys,os

GROUP_SIZE = 32
gine_length = 4


suitfunc = None

# 初始化一个基因
def _gg():
	k = random.randint(1,2)
	if k == 2:
		return -1 * random.random()
	else:
		return random.random()

# 产生新的染色体		
def new_gene():
	g = [
	[_gg(), _gg(), _gg(), _gg(), _gg(), _gg(), _gg(), _gg(), _gg(), _gg(), _gg(), _gg()],
	[_gg(), _gg(), _gg(), _gg(), _gg(), _gg(), _gg(), _gg(), _gg(), _gg(), _gg(), _gg()],
	[_gg(), _gg(), _gg(), _gg(), _gg(), _gg(), _gg(), _gg(), _gg(), _gg(), _gg(), _gg()],
	[_gg(), _gg(), _gg(), _gg(), _gg(), _gg(), _gg(), _gg(), _gg(), _gg(), _gg(), _gg()],
	0
	]
	suit(g)
	return g
	
# 变异	
def mutate(gene):
	for r in gene:
		if not isinstance(r, list):
			continue
		for i in xrange(len(r)):
			k = random.randint(1,100)
			if k < 10:
				k = random.randint(1,2)
				if k == 1:
					r[i] += 0.01
				else:
					r[i] -= 0.01
					
# 杂交					
def cross(g1,g2):
	r = random.randint(1,100)
	new_baby1=[]
	new_baby2=[]
	if r <= 70:
		'''temp_baby1 = []
		temp_baby2 = []
		for i in xrange(gine_length):
			new_row1=[]
			new_row2=[]
			row1 = g1[i]
			row2 = g2[i]
			p = random.randrange(len(row1))
			new_row1 += row1[:p]
			new_row1 += row2[p:]
			new_row2 += row2[:p]
			new_row2 += row1[p:]
		
			temp_baby1.append(row1)
			temp_baby2.append(row2)
			
		temp_baby1.append(0)
		temp_baby2.append(0)'''
		# #############################
		temp_baby1 = g1
		temp_baby2 = g2
		# #############################
		
		pos = random.randrange(len(temp_baby1))
		new_baby1 += temp_baby1[:pos]
		new_baby1 += temp_baby2[pos:]
		new_baby2 += temp_baby2[:pos]
		new_baby2 += temp_baby1[pos:]
		mutate(new_baby1)
		mutate(new_baby2)
		suit(new_baby1)
		suit(new_baby2)
	else:
		new_baby1 = copy.deepcopy(g1)
		new_baby2 = copy.deepcopy(g2)
	
	return new_baby1,new_baby2

def mycmp(p1,p2):
    return -cmp(p1[gine_length],p2[gine_length])

# 初始化一个种群	
def init_group():
	group=[]
	for i in xrange(GROUP_SIZE):
		group.append(new_gene())
	return group

# 找出一个父母	
def roulette(group):
	s = random.randint(1,100) / 100.0
	t=0
	for g in group:
		t += g[gine_length]
		if t >= s:
			return g

def epoch(group):
	new_group=[]
	if not group:
		new_group = init_group()
	else:
		new_group.append(group[0])
		new_group.append(group[1])
		new_baby = 2
		k = len(group)
		while new_baby < k:
			p1 = roulette(group)
			p2 = roulette(group)
			if p1 and p2:
				b1,b2 = cross(p1,p2)
				new_group.append(b1)
				new_group.append(b2)
				new_baby += 2
	
	new_group.sort(mycmp)
	
	#print new_group[0][gine_length]
	
	return new_group
	
def find_result(group):
	for g in group:
		if g[gine_length] > 0.95:
			#print '*************'
			print g[gine_length]
			return g

			
def suit(gene):
	w = 0
	r = 200
	for i in xrange(r):
		if suitfunc(gene):
			w += 1.0
	print w/r
	gene[gine_length] = w/r
			