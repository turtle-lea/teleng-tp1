# -*- coding: utf-8 -*-
#!/usr/bin/python

from regex import *
from automata import *
from ejemplos_automata import *

def grafo(archivo_automata, archivo_dot):
	automata = parsear_automata(archivo_automata)
	escribir_archivo_dot(archivo_dot, automata)

def transiciones_agrupadas(automata):
	group = {}
	for t in automata.transiciones:
		# key == (qi, qj)
		key = str(t[0])+','+str(t[2])
		# value == [label1, label2, ...]
		value = []
		if not(key in group.keys()):
			group[key] = value
		value = group[key]
		if not(t[1] in value):
			value.append(t[1])
			group[key] = value
	assert len([ t for e in group.keys() for t in group[e]]) == len(automata.transiciones)
	return group

def escribir_archivo(archivo_dot, automata):
	f = open(archivo_dot,'w')
	f.write("strict digraph {\n")
	f.write("\t rankdir=LR\n")
	f.write("\t node [shape = none, label = \" \", width = 0, height = 0]; qd;\n")
	f.write("\t node [label = \"\\N\", width = 0.5, height = 0.5];\n")
	for e in automata.estados_finales:
		f.write("\t node [shape = doublecircle]; q" + str(e) + ";\n")
	f.write("\t node [shape = circle];\n")

	### Escribo las transiciones
	ts = transiciones_agrupadas(automata)
	for k in ts.keys():
		origen_destino = k.split(',')
		value = ts[k]
		value_text = ', '.join(str(x) for x in value)
		label_text = "[label = \"" + value_text + "\"]"
		f.write("\t q" + str(origen_destino[0]) + " -> q" + str(origen_destino[1]) + " " + label_text + "\n")

	f.write("\t qd -> q"+ str(automata.estado_inicial) + "\n")
	f.write("}")
