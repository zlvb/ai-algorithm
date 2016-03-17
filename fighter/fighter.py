# -*- coding: UTF-8 -*-
# 

import random,time,copy,sys,os,cPickle

ACT_TYPE = {None:0,'nor':1,'spl':2,'cur':3,'dfn':4}
ACT_MAP = {1:'nor',2:'spl',3:'cur',4:'dfn'}
SPL_MP = 20
CUR_MP = 40

CHAR = {'hp':'血', 'mp':'魔', 'last_act':'上次操作', 'max_hp':'血上限', 'nor':'普通攻击', 'spl':'技能', 'cur':'治疗', 'dfn':'防守'}

class Neuron:
    def __init__(self, arg=None):
        self.arg = arg

    def __call__(self, arg):
        result = 0
        i = 0
        for v in self.arg:
            result += v * arg[i]
            i += 1
        return result


GROUP_SIZE = 32
gine_length = 4

suitfunc = None

def _gg():
    k = random.randint(1,2)
    if k == 2:
        return -1 * random.random()
    else:
        return random.random()
       
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
                                    
def cross(g1,g2):
    r = random.randint(1,100)
    new_baby1=[]
    new_baby2=[]
    if r <= 70:
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
 
def init_group():
    group=[]
    for i in xrange(GROUP_SIZE):
        group.append(new_gene())
    return group

def roulette(group):
    s = random.randint(1,100) / 100.0
    t=0
    for g in group:
        t += g[gine_length]
        if t >= s:
            return g

def epoch(group):
    if not group:
        return init_group()
    else:
        group.sort(mycmp)
        k = len(group) / 2
        group = group[0:k]
        babies = []
        while len(babies) < k:
            p1 = roulette(group)
            p2 = roulette(group)
            if p1 and p2:
                b1,b2 = cross(p1,p2)
                babies.append(b1)
                babies.append(b2)
        return group + babies

    
def find_result(group):
    if group[0][gine_length] > 0.95:
        print '*************'        
        fd = open('fighter.save', 'wb+')
        cPickle.dump(group[0], fd)
        fd.close()
        return group[0]
            
def suit(gene):
    w = 0
    r = 200
    for i in xrange(r):
        if suitfunc(gene):
            w += 1.0
    gene[gine_length] = w/r
    sys.stdout.write('                              \r')
    sys.stdout.write('%d%%\r' % int(gene[gine_length]*100))

def select_act(role_computer, role_tester, gene=None, rd=False):    
    if rd:
        rk = random.choice(['nor','cur','spl','dfn'])
    
    else:
        act_nor = Neuron(gene[0])
        act_spl = Neuron(gene[1])
        act_cur = Neuron(gene[2])
        act_dfn = Neuron(gene[3])
        
        r1=[role_computer['atk'], role_computer['max_hp'], role_computer['hp'], role_computer['mp'], role_computer['dfn'], ACT_TYPE[role_computer['last_act']]]
        r2=[role_tester['atk'], role_tester['max_hp'], role_tester['hp'], role_tester['mp'], role_tester['dfn'], ACT_TYPE[role_tester['last_act']]]
        
        rk = 'nor'
        rv = 0
        act = {}
        act['nor'] = act_nor(r1+r2)
        act['spl'] = act_spl(r1+r2)
        act['cur'] = act_cur(r1+r2)
        
        for k,v in act.items():
            if v > rv:
                rk = k
                rv = v
        
    if rk == 'spl':
        if role_computer['mp'] < SPL_MP:
            rk = 'nor'
            
    if rk == 'cur':
        if role_computer['mp'] < CUR_MP:
            rk = 'nor'
    
    return rk

def calc_atkeff(role_computer, role_tester):
    dfnadd = 0
    if role_tester['last_act'] == 'dfn':
        dfnadd = role_tester['dfn']*2
    atkeff = (role_computer['atk'] - role_tester['dfn'] - dfnadd)*0.2
    if atkeff <= 0:
        atkeff = random.randint(1,2)
        
    baoji = random.randint(1,100)
    if baoji < 20:
        atkeff *= 1.2
    return atkeff    
        
def do_spl(role_computer, role_tester):
    atkeff = calc_atkeff(role_computer,role_tester)
    role_tester['hp'] -= atkeff * 1.7
    role_computer['mp'] -= SPL_MP
    
def do_nor(role_computer, role_tester):
    atkeff = calc_atkeff(role_computer,role_tester)
    role_tester['hp'] -= atkeff
    
def do_cur(role_computer,role_tester):
    role_computer['hp'] += role_computer['max_hp'] * 0.5
    role_computer['mp'] -= CUR_MP
    if role_computer['hp'] > role_computer['max_hp']:
        role_computer['hp'] = role_computer['max_hp']
    
def do_dfn(role_computer,role_tester):
    pass
    
def do_action(role_computer, role_tester, act):
    if act == 'spl':
        do_spl(role_computer,role_tester)
            
    elif act == 'nor':        
        do_nor(role_computer,role_tester)
        
    elif act == 'cur':
        do_cur(role_computer,role_tester)
                
    elif act == 'dfn':
        do_dfn(role_computer,role_tester)
            
    role_computer['last_act'] = act


def begin_fight(gene, show=False, man=False):
    role_computer = {'atk':200, 'dfn':70, 'hp':200, 'mp':160, 'last_act':None, 'max_hp':200}
    role_tester = {'atk':200, 'dfn':70, 'hp':200, 'mp':160, 'last_act':None, 'max_hp':200}
    if show:
        show_role('电脑', role_computer)
        show_role('玩家', role_tester)
    r = random.randint(1,2)
    while True:    
        if role_computer['hp'] > 0 and role_tester['hp'] > 0:
            if man:
                while True:
                    act = int(raw_input('[1] 普通攻击\n[2] 技能（耗魔）\n[3] 治疗（耗魔）\n[4] 防御（减轻下次伤害）\n请输入：'))
                    act = ACT_MAP[act]                    
                    if act == 'spl':
                        if role_tester['mp'] < SPL_MP:
                            print ('mp < %d, retry:' % SPL_MP)
                            continue
                    elif act == 'cur':
                        if role_tester['mp'] < CUR_MP:
                            print ('mp < %d, retry:' % CUR_MP)
                            continue
                    break
            else:
                act = select_act(role_tester, role_computer, None, True)
            do_action(role_tester,role_computer,act)
            if show:
                os.system('cls')
                print '玩家发动',CHAR[role_tester['last_act']], '结果如下'                
                show_role('电脑', role_computer)
                show_role('玩家', role_tester)
                print '-----------'
                time.sleep(2)
        else:
            break
    
        if role_computer['hp'] > 0 and role_tester['hp'] > 0:
            act = select_act(role_computer, role_tester, gene)
            do_action(role_computer,role_tester,act)
            if show:
                print '电脑发动',CHAR[role_computer['last_act']], '结果如下'
                show_role('电脑', role_computer)
                show_role('玩家', role_tester)
                print '-----------'
        else:
            break                    
    if role_computer['hp'] > 0:
        return True
    return False    
    
def begin():    
    global suitfunc
    suitfunc = begin_fight
    try:         
        fd = open('fighter.save')
        r = cPickle.load(fd)
        fd.close()
    except:
        group = []
        while True:
            group = epoch(group)
            r = find_result(group)
            if r:
                break
    os.system('cls')
    begin_fight(r,True,True)
def show_role(name, r):
    sys.stdout.write(name + ':')
    for k,v in r.items():
        if k in ('dfn', 'atk', 'last_act', 'max_hp'):
            continue
        sys.stdout.write('%s:%d '%(CHAR[k],int(v)))
    sys.stdout.write('\n')

if __name__ == '__main__':
    begin()