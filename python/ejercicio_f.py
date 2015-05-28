# -*- coding: utf-8 -*- 
#!/usr/bin/python

from automata import *

def equivalentes(archivo_automata1, archivo_automata2):
	automata1 = parsear_automata(archivo_automata1)
	automata2 = parsear_automata(archivo_automata2)
	
	union_alfabeto = list(set(automata1.alfabeto + automata2.alfabeto))
	
	automata1.alfabeto = union_alfabeto
	automata2.alfabeto = union_alfabeto
	
	automata3 = interseccion_automatas(automata1,automata2.complemento())
	automata4 = interseccion_automatas(automata2,automata1.complemento())
	automata3 = minimizar_afd(automata3)
	automata4 = minimizar_afd(automata4)
	if len(automata3.transiciones) == 0 and len(automata4.transiciones) == 0:
		print True
	else:
		print False
	return 0
