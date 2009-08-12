# -*- coding: UTF-8 -*-
# 

import random,time,copy,sys,os
from neuron import Neuron
import ga

ACT_TYPE = {None:0,'nor':1,'spl':2,'cur':3,'dfn':4}

SPL_MP = 19
CUR_MP = 20

CHAR = {'atk':'攻击力', 'dfn':'防御力', 'hp':'血', 'mp':'魔', 'last_act':'上次操作', 'max_hp':'血上限', 'nor':'普通攻击', 'spl':'必杀攻击', 'cur':'治疗', 'dfn':'防守'}


def select_act(role1, role2, gene=None, rd=False):
	
	if rd:
		#rk = random.choice(['nor','spl','cur','dfn'])
		rk = random.choice(['nor','cur'])
	
	else:
		act_nor = Neuron(gene[0])
		act_spl = Neuron(gene[1])
		act_cur = Neuron(gene[2])
		act_dfn = Neuron(gene[3])
		
		r1=[role1['atk'], role1['dfn'], role1['max_hp'], role1['hp'], role1['mp'], ACT_TYPE[role1['last_act']]]
		r2=[role2['atk'], role2['dfn'], role2['max_hp'], role2['hp'], role2['mp'], ACT_TYPE[role2['last_act']]]
		
		
		'''nor = int(act_nor(r1+r2))
		spl = int(act_spl(r1+r2))
		cur = int(act_cur(r1+r2))
		dfn = int(act_dfn(r1+r2))
		
		if nor <= 0:
			nor = 1
		if spl <= 0:
			spl = 1
		if cur <= 0:
			cur = 1
		if dfn <= 0:
			dfn = 1
		
		act = []
		act += ['nor'] * nor
		act += ['spl'] * spl
		act += ['cur'] * cur
		act += ['dfn'] * dfn
		#if act:
			#rk = random.choice(act)
		#else:
		rk = random.choice(['nor','spl','cur','dfn'])'''
		
		rk = 'nor'
		rv = 0
		act = {}
		act['nor'] = act_nor(r1+r2)
		#act['spl'] = act_spl(r1+r2)
		act['cur'] = act_cur(r1+r2)
		#act['dfn'] = act_dfn(r1+r2)
		
		for k,v in act.items():
			if v > rv:
				rk = k
				rv = v
		
	if rk == 'spl':
		if role1['last_act'] == 'spl':
			rk = random.choice(['nor','cur','dfn'])
		if role1['mp'] < SPL_MP:
			rk = 'nor'
			
	if rk == 'cur':
		if role1['mp'] < CUR_MP or role1['hp'] == role1['max_hp']:
			#k = random.randint(1,2)
			#if k == 1:
				#rk = 'dfn'
			#else:
			rk = 'nor'
	
	return rk

def calc_atkeff(role1, role2):
	dfnadd = 0
	if role2['last_act'] == 'dfn':
		dfnadd = role2['dfn']*0.75
	atkeff = (role1['atk'] - role2['dfn'] - dfnadd)*0.2
	if atkeff <= 0:
		atkeff = random.randint(1,2)
		
	baoji = random.randint(1,100)
	if baoji < 20:
		atkeff *= 1.2
	return atkeff	
		
def do_spl(role1, role2):
	atkeff = calc_atkeff(role1,role2)
	role2['hp'] -= atkeff * 1.5
	role1['mp'] -= SPL_MP
	
def do_nor(role1, role2):
	atkeff = calc_atkeff(role1,role2)
	role2['hp'] -= atkeff
	
def do_cur(role1,role2):
	role1['hp'] += role1['max_hp'] * 0.3
	role1['mp'] -= CUR_MP
	if role1['hp'] > role1['max_hp']:
		role1['hp'] = role1['max_hp']
	
def do_dfn(role1,role2):
	pass
	
def do_action(role1, role2, act):
	if act == 'spl':
		do_spl(role1,role2)
			
	elif act == 'nor':		
		do_nor(role1,role2)
		
	elif act == 'cur':
		do_cur(role1,role2)
				
	elif act == 'dfn':
		do_dfn(role1,role2)
			
	role1['last_act'] = act


def begin_fight(gene, show=False, man=False):
	role1 = {'atk':200, 'dfn':70, 'hp':200, 'mp':160, 'last_act':None, 'max_hp':200}
	role2 = {'atk':200, 'dfn':70, 'hp':200, 'mp':160, 'last_act':None, 'max_hp':200}
	
	r = random.randint(1,2)
	while True:
	
		if role1['hp'] > 0 and role2['hp'] > 0:
			if man:
				while True:
					act = sys.stdin.readline()
					act = act[:-1]
					if act == 'spl':
						if role2['mp'] < SPL_MP:
							print role2['mp'] , SPL_MP
							continue
					elif act == 'cur':
						if role2['mp'] < CUR_MP:
							continue
					break
				os.system('cls')
			else:
				act = select_act(role2, role1, None, True)
			do_action(role2,role1,act)
			if show:
				print '玩家',CHAR[role2['last_act']]
				show_role(role1)
				show_role(role2)
				print '-----------'
		else:
			break
	
		if role1['hp'] > 0 and role2['hp'] > 0:
			act = select_act(role1, role2, gene)
			do_action(role1,role2,act)
			if show:
				print '电脑',CHAR[role1['last_act']]
				show_role(role1)
				show_role(role2)
				print '-----------'
		else:
			break
				
	if role1['hp'] > 0:
		return True
	return False	
	
def begin():
	ga.suitfunc = begin_fight
	group = []
	while True:
		group = ga.epoch(group)
		r = ga.find_result(group)
		if r:
			print r
			begin_fight(r,True)
			print '**********'
			begin_fight(r,True,True)
			return
		#time.sleep(0.5)

def show_role(r):
	for k,v in r.items():
		sys.stdout.write('%s:%s\t'%(CHAR[k],v))
		
	print ''