# -*- coding: utf-8 -*- 
#!/usr/bin/python

from automata import *

def pertenece_al_lenguaje(archivo_automata, cadena):
	automata = parsear_automata(archivo_automata)
	print automata.pertenece_al_lenguaje(cadena)
	return 0
