# -*- coding: utf-8 -*-
#!/usr/bin/python

from regex import *
from automata import *

def afd_minimo(archivo_regex, archivo_automata):

	regpars = parse_regex(archivo_regex)
	automata = armar_automata(regpars)
	automata = automata.remover_transiciones_lambda()
	automata = automata.determinizar_automata()
	escribir_archivo(automata, archivo_automata)

	return automata


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

# http://www.cs.odu.edu/~toida/nerzic/390teched/regular/fa/min-fa.html
def minimizar_afd(automata):
	s1 = automata.finales
	s2 = [estado for estado in automata.estados if estado not in s1]
	partition = [s1, s2]

	transitions = transitions_group(automata)
	new_partition = particionar(partition, transitions)

	while not (new_partition == partition):
		new_partition = particionar(partition)

	partition = eliminar_estados_trampa(new_partition)


def particionar (subconjunto, transitions):
	resultado = []

	for elemento in subconjunto:
		i = 0
		encontrado = false
		while (i < len(subconjunto)) and (not encontrado):
			encontrado = (elemento, subconjunto[i]) in transitions

def escribir_archivo(automata, filename):
	f = open(filename, 'w')

	for i in range(0, len(automata.estados)):
		if i < len(automata.estados)-1 :
			f.write('q')
			f.write(str(automata.estados[i]))
			f.write('\t')
		if i == len(automata.estados)-1 :
			f.write('q')
			f.write(str(automata.estados[i]))

	f.write('\n')

	for i in range(0, len(automata.alfabeto)):
		if (i < len(automata.alfabeto)-1) and (automata.alfabeto[i] != 'lambda') :
			f.write(str(automata.alfabeto[i]))
			f.write('\t')
		if (i == len(automata.alfabeto)-1) and (automata.alfabeto[i] != 'lambda') :
			f.write(str(automata.alfabeto[i]))

	f.write('\n')

	f.write('q')
	f.write(str(automata.estado_inicial))

	f.write('\n')

	for i in range(0, len(automata.estados_finales)):
		if i < len(automata.estados_finales)-1 :
			f.write('q')
			f.write(str(automata.estados_finales[i]))
			f.write('\t')
		if i == len(automata.estados_finales)-1 :
			f.write('q')
			f.write(str(automata.estados_finales[i]))

	f.write('\n')

	for i in range(0, len(automata.transiciones)):
		if i < len(automata.transiciones)-1 :
			f.write('q')
			f.write(str(automata.transiciones[i][0]))
			f.write('\t')
			f.write(str(automata.transiciones[i][1]))
			f.write('\t')
			f.write('q')
			f.write(str(automata.transiciones[i][2]))
			f.write('\n')
		if i == len(automata.transiciones)-1 :
			f.write('q')
			f.write(str(automata.transiciones[i][0]))
			f.write('\t')
			f.write(str(automata.transiciones[i][1]))
			f.write('\t')
			f.write('q')
			f.write(str(automata.transiciones[i][2]))

	f.close()

	return 0


