# -*- coding: UTF-8 -*-
#

import random,sys,os,time

'''
0 石头
1 剪刀
2 布
'''

names = [u'石头',u'剪刀',u'布']

com_act = None
act_list = []
usr_next = None

def forecast():
	if usr_next == None:
		return random.randint(0,2)
	return usr_next
		
def com():
	u = forecast()
	if u == 0:
		return 2
	elif u == 1:
		return 0
	elif u == 2:
		return 1
	
def usr(t):	
	global usr_next
	
	qv = 0
	max = 0
	p = -1
	for i,x in enumerate(act_list):
		if x[0] != t:
			qv = x[1]
			x[1] = 0
		elif x[0] == t and i < len(act_list)-1:
			x[1] = qv + 1
			if max <= qv:
				max = qv
				p = i
				qv = 0
				#print t,max,p,qv,i
	
	if p != -1:
		#print '****',p
		usr_next = act_list[p+1][0]
		
	act_list.append([t,0])	
	last = len(act_list)-1

	while len(act_list) > 20:
		act_list.pop(0)
		
	'''
	for a in act_list:
		sys.stdout.write(str(a[0]) + ' ')
	print ''
	for a in act_list:
		sys.stdout.write(str(a[1]) + ' ')
	print ''
	'''

def checkwin(com, you):
	win = u'你赢了'
	lose = u'你输了'
	draw = u'平局'
	if com == you:
		return draw
	if com == 0 and you == 2:
		return win
	if com == 1 and you == 0:
		return win
	if com == 2 and you == 1:
		return win
	return lose
	
def begin():
	global com_act
	global act_list
	global usr_next
	
	com_act = None
	act_list = []
	usr_next = None
	while True:
		os.system('cls')
		com_next = com()
		print u'计算机打算下一次出：%s' % names[com_next]
		print u'0石头 1剪刀 2布 3结束 【请选择0,1,2,3】'
		while True:
			try:
				u = int(sys.stdin.readline(1))
				if u >= 3:
					return
				break
			except:
				pass
		usr(u)
		print u'计算机：%s 你：%s\t%s' % (names[com_next], names[u], checkwin(com_next,u))
		#print '='*10
		time.sleep(2)