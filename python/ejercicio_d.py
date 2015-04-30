# -*- coding: utf-8 -*- 
#!/usr/bin/python

from automata import *

def interseccion(archivo_automata1, archivo_automata2, archivo_automata):
	automata1 = parsear_automata(archivo_automata1)
	automata2 = parsear_automata(archivo_automata2)
	automata3 = interseccion_automatas(automata1,automata2)
	escribir_archivo(automata3,archivo_automata)
	return 0
