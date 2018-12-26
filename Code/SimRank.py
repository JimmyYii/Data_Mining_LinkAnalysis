# Data Mining, Project3 - Link Analysis
# SimRank
# Chun-Yii Liu, N16064103
# 2018/12/24

import numpy as np
import pandas as pd
import itertools
import time
np.set_printoptions(threshold=np.nan)	# To display whole matrix of 

class link:
	def __init__(self, name):
		self.node = name
		self.ch = None
		self.pa = None
		#print(self.node)

	def add_ch(self, ch_list):
		self.ch = ch_list
		#print(self.ch)

	def add_pa(self, pa_list):
		self.pa = pa_list
		#print(self.pa)


def graphProcess(graph):
	allnodes = []
	subgraph = {}

	for node in graph['1st node']:
		if node not in allnodes:
			allnodes.append(node)
			subgraph[node] = link(node)
			subgraph[node].add_ch(list(graph['2nd node'][graph['1st node']==node]))	#?

	for node in graph['2nd node']:
		if node not in allnodes:
			allnodes.append(node)
			subgraph[node] = link(node)
		subgraph[node].add_pa(list(graph['1st node'][graph['2nd node']==node]))	#why out of 'if'

	return allnodes, subgraph


def SimRank(allnodes, subgraph, C=0.5, iteration=100):
	sim = np.identity(len(allnodes))
	for N_iter in range(iteration):
		sim_old = np.copy(sim)
		for a, b in itertools.product(allnodes,allnodes):
			#print(a,b)
			if a == b or subgraph[a].pa == None or subgraph[b].pa == None:
				continue	# S(a,a) = 1, and S(a,b) = 0 if a or b has no parent
			sum_Sab = 0
			for pa_a in subgraph[a].pa:
				for pa_b in subgraph[b].pa:
					sum_Sab = sum_Sab + sim_old[pa_a-1][pa_b-1]
			sim[a-1][b-1] = sum_Sab*C/(len(subgraph[a].pa)*len(subgraph[b].pa))

	return sim

#-----------------------------------------------

graph = pd.read_csv('graph_3.txt',header=-1)
graph.columns = ['1st node', '2nd node']

allnodes, subgraph = graphProcess(graph)

start = time.time()
sim = SimRank(allnodes, subgraph)
end = time.time()

print("Execution time:", end - start)
print(sim)