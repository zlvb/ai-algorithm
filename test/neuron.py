# -*- coding: UTF-8 -*-
# 


# 神经细胞
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