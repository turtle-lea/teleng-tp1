# -*- coding: utf-8 -*- 
#!/usr/bin/python

from automata import *

def complemento(archivo_automata1, archivo_automata):
	automata1 = parsear_automata(archivo_automata1)
	automata2 = automata1.complemento()
	escribir_archivo(automata2,archivo_automata)
	return 0
