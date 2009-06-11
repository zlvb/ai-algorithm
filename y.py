# -*- coding: UTF-8 -*-
# 

import random,time
from copy import copy

scene = [
[0,0,1,0,0],
[0,1,1,0,1],
[0,1,0,0,0],
[0,0,0,1,0],
[0,0,0,1,0],
[0,0,0,1,0],
[0,0,0,1,0],
]

width = len(scene[0])
height = len(scene)

start = (0,0)
end = (width-1,height-1)

up = [0,0]
down = [0,1]
left = [1,0]
right = [1,1]

gine_length = width*height*2 # 基因长度
group_size = gine_length*20 # 种群大小
mutate_rate = 0.01 # 变异率

def new_gine():
	gine=[]
	for i in xrange(gine_length):
		gine += [random.randrange(2)]
	gine.append(0)
	suit(gine)
	return gine
		
def init_group():
	group = []	
	for i in xrange(group_size):
		group.append(new_gine())
	
	return group
	
def mutate(gine): # 变异
	for i in xrange(gine_length):
		r = random.randint(1, 1/mutate_rate)
		if r == 1:
			gine[i] ^= 1
			
def suit(gine): # 评价适应性
	pos = copy(start)
	
	ig = 0
	while ig<gine_length:
		new_pos = []
		g = [gine[ig],gine[ig+1]]
		ig += 2
		if g == up:
			new_pos = [pos[0], pos[1]-1]
		elif g == down:
			new_pos = [pos[0], pos[1]+1]
		elif g == left:
			new_pos = [pos[0]-1, pos[1]]
		elif g == right:
			new_pos = [pos[0]+1, pos[1]]
			
		if new_pos[0] < 0 or new_pos[0]	> width-1 or new_pos[1] < 0 or new_pos[1] > height - 1:
			continue

		if scene[new_pos[1]][new_pos[0]] == 1:
			continue
		
		pos = new_pos
		if new_pos == end:
			break
			
	s = (width-pos[0]-1) + (height-pos[1]-1)
	gine[gine_length] = 1.0 / (s+1)
		
	return s
		

def roulette(group): # 找出一个父母
	s = 1.0/(random.randrange(width+height)+1)
	t=0
	for g in group:
		t += g[gine_length]
		if t >= s:
			return g

def cross(p1,p2): # 杂交
	r = random.randint(1,100)
	new_baby1=[]
	new_baby2=[]
	if r <= 70:
		pos = random.randrange(gine_length)
		new_baby1 += p1[:pos]
		new_baby1 += p2[pos:]
		new_baby2 += p2[:pos]
		new_baby2 += p1[pos:]
		mutate(new_baby1)
		mutate(new_baby2)
		suit(new_baby1)
		suit(new_baby2)
	else:
		new_baby1 = copy(p1)
		new_baby2 = copy(p2)
	
	return new_baby1,new_baby2
	
def show_scene(gine):
	answer = copy(scene)
	ig = 0
	while ig<gine_length:
		new_pos = []
		g = [gine[ig],gine[ig+1]]
		ig += 2
		if g == up:
			new_pos = [pos[0], pos[1]-1]
		elif g == down:
			new_pos = [pos[0], pos[1]+1]
		elif g == left:
			new_pos = [pos[0]-1, pos[1]]
		elif g == right:
			new_pos = [pos[0]+1, pos[1]]
			
		if new_pos[0] < 0 or new_pos[0]	> width-1 or new_pos[1] < 0 or new_pos[1] > height - 1:
			continue

		if scene[new_pos[1]][new_pos[0]] == 1:
			continue
		
		pos = new_pos
		answer[pos[0]][pos[1]] = '*'
		if new_pos == end:
			break

def find_result(group):
	for g in group:
		if g[gine_length] >= 1:
			return g

def mycmp(p1,p2):
    return -cmp(p1[gine_length],p2[gine_length])
			
def epoch(group):
	new_group=[]
	if not group:
		new_group = init_group()
	else:	
		new_baby = 0
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
	return new_group
			
def begin():
	group = []
	while True:
		group = epoch(group)
		show_group(group)
		r = find_result(group)
		if r:
			return r
		time.sleep(0.5)
			
			
def show_gine(gine):
	ig = 0
	s=''
	while ig < gine_length:
		g = [gine[ig],gine[ig+1]]
		if g == up:
			s += 'up\t'
		elif g == down:
			s += 'down\t'
		elif g == left:
			s += 'left\t'
		elif g == right:
			s += 'right\t'			
		ig += 2
	s+=str(gine[gine_length])
	#print gine_length
	#print gine
	print s
	
def show_group(group):
	print '-'*30
	for g in group:
		show_gine(g)
			