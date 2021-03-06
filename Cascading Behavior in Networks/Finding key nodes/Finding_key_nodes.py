# Finding key nodes in the graph

import networkx as nx 
import matplotlib.pyplot as plt 

# Function to set the initial behavior preference for each node as B 
def set_all_to_B(G):
	for i in G.nodes():
		G.node[i]['behavior'] = 'B'

# Function to set behavior preference for two nodes (initial adopters) as A
def set_to_A(G, initial_adopters):
	for i in initial_adopters:
		G.node[i]['behavior'] = 'A'

# Function to find out neighbors of a node who have adopted a particular behavior
def find_neigh(node, behavior, G):
	behavior_neigh_count = 0
	for i in G.neighbors(node):
		if G.node[i]['behavior'] == behavior:
			behavior_neigh_count += 1
	return behavior_neigh_count

# Function to calculate the final behavior adopted by each node
def recalculate_behaviors(G):
	behavior_dict = {}
	a = 9 # Payoff associated with A
	b = 5 # Payoff associated with B
	for i in G.nodes():
		num_A = find_neigh(i, 'A', G)
		num_B = find_neigh(i, 'B', G)
		payoff_A = a * num_A
		payoff_B = b * num_B
		if payoff_A >= payoff_B:
			behavior_dict[i] = 'A'
		else:
			behavior_dict[i] = 'B'
	return behavior_dict

# Function to update the value of the node attribute 'behavior'
def reset_node_attributes(G, behavior_dict):
	for each in behavior_dict:
		G.node[each]['behavior'] = behavior_dict[each]

# Function that returns value 1 when every node has adopted the "behavior" passed in arg
def terminate_1(behavior, G): 
	flag = 1 # variable containing the value to be returned
	for i in G.nodes():
		if G.node[i]['behavior'] != behavior:
			flag = 0
			break
	return flag 

# Function to determine whether all the nodes have adopted the same behavior
def terminate(G, count):
	flag1 = terminate_1('A', G) # Tells whether all the nodes have adopted the behavior 'A' or not
	flag2 = terminate_1('B', G) # Tells whether all the nodes have adopted the behavior 'B' or not
	if (flag1 == 1 or flag2 == 1 or count >= 200):
		return 1 # All nodes have adopted the same behavior
	else:
		return 0 # Not all nodes have adopted the same behavior

# Function for printing the result ; whether cascade is complete or incomplete i.e., Fate of the cascade
def print_result(G, u, v, key_nodes_list):
	c = terminate_1('A', G)
	if c == 1: # Means all nodes have adopted behavior 'A'
		print "Cascade is complete."
		key_nodes_list.append([u,v])

	else: # Means not all nodes have adopted behavior 'A' and cascade couldn't complete
		print "Cascade is incomplete."

# Function to find key nodes in the graph
def find_key_nodes(G):
	key_nodes_list = []
	for u in G.nodes():
		for v in G.nodes():
			if u < v :
				print '\n', u,v, ':', 
				initial_adopters = [] # Selecting two nodes out of 10 who will decide to go with behavior 'A' instead of behavior 'B'
				initial_adopters.append(u)
				initial_adopters.append(v)
				set_all_to_B(G)  # Setting the initial preferred behavior for each node to be 'B'
				set_to_A(G, initial_adopters)  # Setting the preferred behavior of two selected nodes as behavior 'A' 
				flag = 0 # Indicator for whether all nodes have adopted same behavior.  VALUES : 0(No), 1(Yes) [Initially flag = 0]
				count = 0 # counter for running iterations of nodes weighing their behaviors
				while(1):
					flag = terminate(G, count) # Whether all the nodes have adopted the same behavior
					if flag == 1: # Cascade will not move further
						break # Get out of the while loop, because "fate of cascade" has been decided ;-)
					count += 1 # Since fate of the cascade is still undecided, increase the counter for running another iteration
					behavior_dict = recalculate_behaviors(G)  # Determing the preferred behavior for each node after weighing all of their choices
					reset_node_attributes(G, behavior_dict)  # Changing (from initail to final) the node attribute "behavior" associated with each node 

				# Coming out of the while loop means fate of cascade has been decided
				#visualize_graph(G) # Visualize the final state of the graph
				print_result(G,u,v, key_nodes_list)
	print "\nThe key nodes-pair in the graph is/are : ",
	if (len(key_nodes_list) == 0):
		print "None"
	else:
		for i in key_nodes_list:
			print i,


G = nx.erdos_renyi_graph(10,0.5)  # Creating a random graph with 10 nodes and probability p = 0.5
find_key_nodes(G)