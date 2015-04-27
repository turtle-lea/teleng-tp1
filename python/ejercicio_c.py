# -*- coding: utf-8 -*- 
#!/usr/bin/python

from regex import *
from automata import *

def grafo(archivo_automata, archivo_dot):
	automata = afd_minimo(archivo_automata)

def print_transitions(group):
	print ("strict digraph {")
 	print ("rankdir=LR;")
 	print ("node [shape = none, label = \"\", width = 0, height = 0]; qd;")
 	print ("node [label=\"\N\", width = 0.5, height = 0.5];")
	print ("node [shape = doublecircle]; q1;")
	print ("node [shape = circle];")
	print ("qd -> q0")
	for transition, labels in group.iteritems():
		#transition == (orig, dest)
		#labels == (label1, label2, label3)
		orig_state = transition[0]
		dest_state = transition[1]
		
		print ("q" + orig_state + " -> " + "q" + dest_state, end = " ")
		print ("[label=\"", end = "")
		print (','.join(str(label) for label in labels, end = "")
		print ("\"]")
	print ("}")
		
		
	
def transitions_group(automata):
	group = {}
	for transition in automata.transitions:
		# key == (qi, qj)
		key = transition[0], transition[2]
		# value == [label1, label2, ...]
		value = []
		if key in group:
			value = group[key]
			if not(transition[1] in value):
				value.append(transition[1])
				
		group[key] = value
		
	return group