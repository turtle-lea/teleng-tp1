# -*- coding: utf-8 -*-
#!/usr/bin/python

from regex import *
from automata import *

def afd_minimo(archivo_regex, archivo_automata):

	regpars = parse_regex(archivo_regex)
	automata = armar_automata(regpars)
	automata = automata.remover_transiciones_lambda()
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
	
	
def nueva_particion (partition, transitions):
	
def particionar (subconjunto, transitions):
	resultado = []
	
	for elemento in subconjunto:
		i = 0
		encontrado = false
		while (i < len(subconjunto)) and (not encontrado):
			encontrado = (elemento, subconjunto[i]) in transitions
		
		if ( 
	



def escribir_archivo(automata, filename):
	f = open(filename, 'w')

	for i in range(0, len(automata.estados)):
		if i < len(automata.estados)-1 :
			f.write('q')
			f.write(str(automata.estados[i]))
			f.write(' ')
		if i == len(automata.estados)-1 :
			f.write('q')
			f.write(str(automata.estados[i]))

	f.write('\n')

	for i in range(0, len(automata.alfabeto)):
		if (i < len(automata.alfabeto)-1) and (automata.alfabeto[i] != 'lambda') :
			f.write(str(automata.alfabeto[i]))
			f.write(' ')
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
			f.write(' ')
		if i == len(automata.estados_finales)-1 :
			f.write('q')
			f.write(str(automata.estados_finales[i]))

	f.write('\n')

	for i in range(0, len(automata.transiciones)):
		if i < len(automata.transiciones)-1 :
			f.write('q')
			f.write(str(automata.transiciones[i][0]))
			f.write(' ')
			f.write(str(automata.transiciones[i][1]))
			f.write(' ')
			f.write('q')
			f.write(str(automata.transiciones[i][2]))
			f.write('\n')
		if i == len(automata.transiciones)-1 :
			f.write('q')
			f.write(str(automata.transiciones[i][0]))
			f.write(' ')
			f.write(str(automata.transiciones[i][1]))
			f.write(' ')
			f.write('q')
			f.write(str(automata.transiciones[i][2]))

	f.close()

	return 0

def armar_automata(regpars):

	if regpars.nombre == 'CONCAT':

		cant_arg = len(regpars.argumentos)
		automataM1 = armar_automata(regpars.argumentos[0])

		for i in range(1,cant_arg):

			automataM2 = armar_automata(regpars.argumentos[i])
			automataM1 = armarConcat(automataM1, 'lambda', automataM2) #agregar transición final M1 con iinicial M2

	if regpars.nombre == 'OR':

		cant_arg = len(regpars.argumentos)
		automataM1 = armar_automata(regpars.argumentos[0])

		automata0 = Automata([0],['lambda'], 0, [0], [])
		automataF = Automata([0],['lambda'], 0, [0], [])

		automataM1 = armarConcat(automata0, 'lambda', automataM1)  #agregar transición final 0 con inicial
		automataM1 = armarConcat(automataM1, 'lambda', automataF)

		for i in range(1,cant_arg):

			automataM2 = armar_automata(regpars.argumentos[i])
			automataM1 = armarOr(automataM1, 'lambda', automataM2) #agregar transicion desde estado inicial M1 con inicialM2

	if (regpars.nombre == 'STAR') or (regpars.nombre == 'PLUS'):

		automata0 = Automata([0],['lambda'], 0, [0], [])
		automataF = Automata([0],['lambda'], 0, [0], [])
		automataM1 = armar_automata(regpars.argumentos[0])

		automataM1 = armarPlus(automata0, automataM1, automataF)

		if (regpars.nombre == 'STAR'):

			estado_final_M1 = automataM1.estados_finales[0] #Se que siempre es único por definición de Plus del algoritmo Thompson
			estado_inicial_M1 = automataM1.estado_inicial

			automataM1.transiciones.append([estado_inicial_M1, 'lambda',estado_final_M1])

	if regpars.nombre == 'simbolo':

		automataM1 = Automata([0,1],['lambda',regpars.valor], 0, [1], [[0,regpars.valor,1]])

	return automataM1

def armarConcat(automata1, lamb, automata2):

	automata2 = renombrarAutomata(automata1, automata2)

	estados_finales_A1 = automata1.estados_finales
	estado_inicial_A2 = automata2.estado_inicial

	automata1 = unirAutomatas(automata1,automata2, 'CONCAT')

	for i in range(0,len(estados_finales_A1)):
		automata1.transiciones.append([estados_finales_A1[i], lamb,estado_inicial_A2])

	return automata1

def armarOr(automata1, lamb, automata2):

	automata2 = renombrarAutomata(automata1, automata2)

	estado_inicial_A1 = automata1.estado_inicial
	estado_final_A1 = automata1.estados_finales[0] #Se que siempre es único por definición de Or del algoritmo Thompson
	estado_inicial_A2 = automata2.estado_inicial
	estados_finales_A2 = automata2.estados_finales

	automata1 = unirAutomatas(automata1,automata2, 'OR')

	automata1.transiciones.append([estado_inicial_A1, lamb,estado_inicial_A2])

	for i in range(0,len(estados_finales_A2)):
		automata1.transiciones.append([estados_finales_A2[i], lamb,estado_final_A1])

	return automata1

def armarPlus(automata0, automataM1, automataF):

	estado_inicial_M1 = automataM1.estado_inicial
	estados_finales_M1 = automataM1.estados_finales
	for i in range(0,len(estados_finales_M1)):
		automataM1.transiciones.append([estados_finales_M1[i], 'lambda',estado_inicial_M1])

	automataM1 = armarConcat(automata0, 'lambda', automataM1)
	automataM1 = armarConcat(automataM1, 'lambda', automataF)

	return automataM1

def unirAutomatas(automata1, automata2, forma_de_union):

	automata1.estados = automata1.estados + automata2.estados
	automata1.alfabeto = list(set(automata1.alfabeto + automata2.alfabeto))

	if forma_de_union == 'CONCAT':
		automata1.estados_finales = automata2.estados_finales

	for i in (range(0,len(automata2.transiciones))):
		automata1.transiciones.append(automata2.transiciones[i])

	return automata1

def renombrarAutomata(automata1, automata2):

	for i in (range(0, len(automata2.estados))):

		if (automata2.estados[i] in automata1.estados):

			nuevoEstado = buscarEstadoQueNoExista(automata1.estados, automata2.estados)
			automata2.transiciones = renombrarTransiciones(automata2.transiciones, automata2.estados[i], nuevoEstado)

			if (automata2.estados[i] == automata2.estado_inicial):
				automata2.estado_inicial = nuevoEstado

			for j in (range(0, len(automata2.estados_finales))):

				if (automata2.estados[i] == automata2.estados_finales[j]):
					automata2.estados_finales[j] = nuevoEstado

			automata2.estados[i] = nuevoEstado

	return automata2

def buscarEstadoQueNoExista(estados1, estados2):
	i = 0
	while ((i in estados1) or (i in estados2)):
		i = i + 1

	return i

def renombrarTransiciones(transiciones, estado, nuevoEstado):

	for i in (range(0, len(transiciones))):
		if (transiciones[i][0] == estado):
			transiciones[i][0] = nuevoEstado
		if (transiciones[i][2] == estado):
			transiciones[i][2] = nuevoEstado

	return transiciones
