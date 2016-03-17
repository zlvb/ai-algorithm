# -*- coding: UTF-8 -*-
# 

import random,time,sys,os
import copy

scene = [
[1,1,1,1,1,1,1,1,1,1],
[1,0,0,1,0,0,0,0,0,1],
[1,0,1,0,0,1,1,1,1,1],
[1,0,1,0,0,0,1,0,0,1],
[1,0,0,0,0,0,1,0,0,1],
[1,0,0,0,0,0,0,0,0,1],
[1,0,1,0,1,0,1,0,1,1],
[1,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1]
]

width = len(scene[0])
height = len(scene)

start = (1,1)
end = (width-2,height-2)

up = [0,0]
down = [0,1]
left = [1,0]
right = [1,1]

gine_length = width*height*2 # 基因长度
group_size = gine_length*2 # 种群大小
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
	pos = copy.deepcopy(start)
	
	ig = 0
	while ig<gine_length:
		new_pos = []
		g = [gine[ig],gine[ig+1]]
		ig += 2
		if g == up:
			new_pos = [pos[0]-1, pos[1]]
		elif g == down:
			new_pos = [pos[0]+1, pos[1]]
		elif g == left:
			new_pos = [pos[0], pos[1]-1]
		elif g == right:
			new_pos = [pos[0], pos[1]+1]
			
		if scene[new_pos[1]][new_pos[0]] == 1:
			continue
		
		pos = new_pos
		if new_pos == end:
			break
			
	s = abs((end[0]-pos[0]) + (end[1]-pos[1]))
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
		new_baby1 = copy.deepcopy(p1)
		new_baby2 = copy.deepcopy(p2)
	
	return new_baby1,new_baby2

def display_scene(pos):
	for i,v in enumerate(scene):
		for j,k in enumerate(v):
			if i == pos[1] and j == pos[0]:
				sys.stdout.write('*')
			elif k==0:
				sys.stdout.write(' ')
			else:
				sys.stdout.write(str(k))
		sys.stdout.write('\n')
	
def show_scene(gine):
	pos = copy.deepcopy(start)
	ig = 0
	final_path=[]
	while ig<gine_length:
		new_pos = []
		g = [gine[ig],gine[ig+1]]
		ig += 2
		if g == up:
			new_pos = [pos[0]-1, pos[1]]
		elif g == down:
			new_pos = [pos[0]+1, pos[1]]
		elif g == left:
			new_pos = [pos[0], pos[1]-1]
		elif g == right:
			new_pos = [pos[0], pos[1]+1]
			
		if scene[new_pos[1]][new_pos[0]] == 1:
			continue
		
		pos = new_pos
		if len(final_path)>=3 and pos == final_path[len(final_path)-2]:
			del final_path[len(final_path)-1]
			continue
		else:
			final_path.append(new_pos)
		
	for p in final_path:
		display_scene(p)
		if p == end:
			break
		time.sleep(0.2)
		os.system('cls')


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
	
	global start
	global end
	while True:
		group = []
		while True:
			group = epoch(group)
			#show_group(group)
			r = find_result(group)
			if r:
				show_scene(r)
				break
		start,end = end,start
			
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
	print s
	
def show_group(group):
	print '-'*30
	for g in group:
		show_gine(g)
			