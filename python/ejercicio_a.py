# -*- coding: utf-8 -*- 
#!/usr/bin/python

from regex import parse_regex
from automata import armar_automata

def afd_minimo(archivo_regex, archivo_automata):
	
	regpars = parse_regex(archivo_regex)
	automata = armar_automata(regpars)
	
	return automata
