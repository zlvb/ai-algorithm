#!/usr/bin/python
# -*- coding: UTF-8 -*-

import random,sys,cPickle,time,math
from datetime import datetime
#from multiprocessing import Pool
random.seed(datetime.now())

def initweightlayer(n):
    weightlayer = []
    for i in xrange(n*81):
        weightlayer.append(random.random())
    return weightlayer


def runnetwork(i, w, n):
    for idx in xrange(n-1):
        ws = idx * 81
        i.append([])
        for K in xrange(9):
            m = map(lambda x,y:x*y, i[idx], w[ws:ws+9])
            v = max(0, reduce(lambda x,y:x+y, m))
            i[idx+1].append(v)
            ws += 9

def printBoard(board):
    def R(o):
        return repr(o).replace('2', 'X').replace('1', 'O').replace('0', '_').replace(',', ' ').replace('(', '|').replace(')', '|')
    print(R((board[0], board[1], board[2])) + ' 0 1 2')
    print(R((board[3], board[4], board[5])) + ' 3 4 5')
    print(R((board[6], board[7], board[8])) + ' 6 7 8')
    print('-'*19)

def getmaxpos(output, empty):
    max = -99999999
    pos = -1
    for idx,v in enumerate(empty):
        if output[v] > max:
            max = output[v]
            pos = v
    #print(pos)
    empty.remove(pos)
    return pos
    
def check3(board, p1, p2, t):
    return board[p1] == board[p2] and board[p2] == t


wintable = {}
wintable[0] = ((1,2), (3,6), (4,8))
wintable[1] = ((0,2), (4,7))
wintable[2] = ((0,1), (5,8), (4,6))
wintable[3] = ((0,6), (4,5))
wintable[4] = ((1,7), (3,5), (0,8), (2,6))
wintable[5] = ((2,8), (3,4))
wintable[6] = ((0,3), (2,4), (7,8))
wintable[7] = ((1,4), (6,8))
wintable[8] = ((2,5), (6,7), (0,4))

def checkwin(b, pos, t):
    #print 'cur:', pos
    checks = wintable[pos]
    for pair in checks:
        if check3(b, pair[0], pair[1], t):
            return True
    return False

class Unit:
    def __init__(self, init = True):
        if init:
            self.weight = initweightlayer(layernum) 
        self.win = 0
        self.lose = 0
    def variation(self):
        for idx,v in enumerate(self.weight):
            if random.randint(0,3) == 0:
                if random.randint(0,1) == 1:
                    self.weight[idx] = v + random.random()
                else:
                    self.weight[idx] = v - random.random()

def mycmpwin(u1,u2):
    if u1.lose < u2.lose:
        return -1
    if u1.lose > u2.lose:
        return 1
    if u1.win > u2.win:
        return -1
    if u1.win < u2.win:
        return 1
    return 0

def pvecheck(empty, board, M, E):
    for pos in empty:
        board[pos] = M
        if checkwin(board, pos, M):
            empty.remove(pos)
            return pos
        board[pos] = 0
    for pos in empty:
        board[pos] = E
        if checkwin(board, pos, E):
            empty.remove(pos)
            board[pos] = M
            return pos
        board[pos] = 0
    return -1    
    
def hybrid(u1, u2, n):
    half = n * 81 / 2
    newU = Unit(False)
    newU.weight = u1.weight[0:half] + u2.weight[half:n*81]
    #print(newU.weight[80])
    newU.variation()
    return newU
           
if __name__ == '__main__':
    layernum = 20
    epoch = 100
    weightgroup = []
    for i in xrange(100):
        weightgroup.append(Unit())

    for E in xrange(epoch):     
        for unit in weightgroup:   
            for i in xrange(10):
                inputlayer = [[0,0,0,0,0,0,0,0,0,], ]
                empty = [0,1,2,3,4,5,6,7,8]
                while True:                       
                    runnetwork(inputlayer, unit.weight, layernum)
                    output = inputlayer[layernum - 1]
                    inputlayer = inputlayer[0:1]
                    pos = getmaxpos(output, empty)
                    inputlayer[0][pos] = 2
                    if checkwin(inputlayer[0], pos, 2):
                        unit.win += 1
                        break
                    if not empty:
                        break  
                    pos = pvecheck(empty, inputlayer[0], 1, 2)
                    if pos != -1:
                        unit.lose += 1
                        break
                    pos = random.randint(0, len(empty)-1)
                    idx = empty.pop(pos)
                    inputlayer[0][idx] = 1
                    if checkwin(inputlayer[0], pos, 1):
                        unit.lose += 1
                        break
                    if not empty:
                        break 
                #print('--------------------------')
            #sys.stdout.write('[ %d%% ] | Epoch:%d | Win: %d Lose: %d/100\n' % (E*100/epoch, E, unit.win, unit.lose))
        weightgroup = sorted(weightgroup, cmp = mycmpwin)
        count = len(weightgroup) / 2
        weightgroup = weightgroup[0:count]
        sys.stdout.write('[ %d%% ] | Epoch:%d Top(%d) | Win: %d Lose: %d/100\n' % (E*100/epoch,  E, count*2, weightgroup[0].win, weightgroup[0].lose))
        babies = []
        for i in xrange(count):
            weightgroup[i].win = 0
            weightgroup[i].lose = 0
        for i in xrange(count / 2):
            babies.append(hybrid(weightgroup[i], weightgroup[i+1], layernum))
            babies.append(hybrid(weightgroup[i], weightgroup[i+1], layernum))
        weightgroup += babies
            