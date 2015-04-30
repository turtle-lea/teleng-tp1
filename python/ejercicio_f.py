# -*- coding: utf-8 -*- 
#!/usr/bin/python

from automata import *

def equivalentes(archivo_automata1, archivo_automata2):
	automata1 = parsear_automata(archivo_automata1)
	automata2 = parsear_automata(archivo_automata2)
	automata3 = interseccion_automatas(automata1,automata2.complemento())
	automata4 = interseccion_automatas(automata2,automata1.complemento())
	if len(automata3.transiciones) == 0 and len(automata4.transiciones) == 0: #falta ver si el estado inicial y final tienen que ser distintos
		print True
	else:
		print False
	return 0
