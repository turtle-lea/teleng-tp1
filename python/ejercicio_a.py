# -*- coding: utf-8 -*- 
#!/usr/bin/python

from regex import parse_regex
from automata import armar_automata

def afd_minimo(archivo_regex, archivo_automata):
	
	regpars = parse_regex(archivo_regex)
	automata = armar_automata(regpars)
	escribir_archivo(automata, archivo_automata)
	
	return automata

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
