# Data Mining, Project3 - Link Analysis
# HITS
# Chun-Yii Liu, N16064103
# 2018/12/23

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


def HITS(allnodes, subgraph):
	a0 = {}
	h0 = {}
	# give initial value of each node
	for node in allnodes:
		a0[node] = 1
		h0[node] = 1

	a = {}
	h = {}
	a[0] = a0
	h[0] = h0
	#print(a,h)

	t = 1
	error = 1
	while error > 1e-6 and  t < 1e3:	# condition of convergence or avoid not converge
		a[t] = {}
		h[t] = {}
		for node in allnodes:
			sum_a = 0
			sum_h = 0
			if subgraph[node].pa != None:
				for item in subgraph[node].pa:
					#print(item)
					sum_h = sum_h + h[t-1][item]
				a[t][node] = sum_h
			if subgraph[node].ch != None:
				for item in subgraph[node].ch:
					#print(item)
					sum_a = sum_a + a[t-1][item]
				h[t][node] = sum_a
		
		# normalization
		for node in a[t]:
			a[t][node] = a[t][node]/sum(a[t].values())
		for node in h[t]:
			h[t][node] = h[t][node]/sum(h[t].values())

		# do ||a_t - a_t-1|| + ||h_t - h_t-1||
		v_a = list(map(lambda x: abs(x[0]-x[1]), zip(list(a[t].values()), list(a[t-1].values()))))
		v_h = list(map(lambda x: abs(x[0]-x[1]), zip(list(h[t].values()), list(h[t-1].values()))))
		del_a = sum(i**2 for i in v_a)**0.5
		del_h = sum(i**2 for i in v_h)**0.5
		error = del_a + del_h
		print('Number of iteration:',t,', error:', error)
		t = t + 1

	return a, h, t-1


def show_AuthHub(auth,hub,iteration):
    a_descend = sorted(auth[iteration], key=auth[iteration].get, reverse=True)[:10]
    h_descend = sorted(hub[iteration], key=hub[iteration].get, reverse=True)[:10]
    print("\nAuthority:")
    for key in a_descend:
        print(key,": ",auth[iteration][key])

    print("\nHub:")
    for key in h_descend:
        print(key,": ",hub[iteration][key])

#-----------------------------------------------

graph = pd.read_csv('graph_1.txt',header=-1)
graph.columns = ['1st node', '2nd node']

allnodes, subgraph = graphProcess(graph)

start = time.time()
authority, hub, N_iter = HITS(allnodes, subgraph)
end = time.time()

print("Execution time:", end - start)
show_AuthHub(authority, hub, N_iter)