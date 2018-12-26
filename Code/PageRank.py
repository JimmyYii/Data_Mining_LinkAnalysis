# Data Mining, Project3 - Link Analysis
# PageRank
# Chun-Yii Liu, N16064103
# 2018/12/24

import numpy as np
import pandas as pd
import time

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


def PageRank(allnodes, subgraph, df = 0.15):
	PR = {}
	PR[0] = {}

	# give initial value of each node
	for node in allnodes:
		PR[0][node] = 1/len(allnodes)

	t = 1
	error = 1
	while error > 1e-6 and  t < 1e3:	# condition of convergence or avoid not converge
		PR[t] = {}
		for node in subgraph:
			PR_sum = 0
			if subgraph[node].pa != None:
				for parent in subgraph[node].pa:
					outDegree = len(subgraph[parent].ch)
					PR_sum = PR_sum + PR[t-1][parent]/outDegree
			PR[t][node] = df/len(allnodes) + (1 - df)*PR_sum
			# df is the damping factor: random jumping probability
		del_PR = list(map(lambda x: abs(x[0]-x[1]), zip(list(PR[t].values()), list(PR[t-1].values()))))
		error = sum(i**2 for i in del_PR)**0.5
		print('Number of iteration:',t,', error:',error)
		t = t + 1
	return PR, t-1

def show_PR(PR,iteration):
    PR_descend = sorted(PR[iteration], key=PR[iteration].get, reverse=True)[:10]
    print("\nPageRank:")
    for key in PR_descend:
        print(key,": ",PR[iteration][key])

#-----------------------------------------------

graph = pd.read_csv('graph_2.txt',header=-1)
graph.columns = ['1st node', '2nd node']

allnodes, subgraph = graphProcess(graph)

start = time.time()
PageRank, N_iter = PageRank(allnodes, subgraph)
end = time.time()

print("Execution time:", end - start)
show_PR(PageRank, N_iter)
