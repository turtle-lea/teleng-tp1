	# -*- coding: utf-8 -*-
#!/usr/bin/python

from regex import *
from automata import *

def afd_minimo(archivo_regex, archivo_automata):
        regpars = parse_regex(archivo_regex)
        automata = armar_automata(regpars)

        ### AFND ---> AFD
        automata = automata.determinizar_automata()
        automata = automata.minimizar_afd_2()
        #automata = minimizar_afd(automata)
        escribir_archivo(automata, archivo_automata)
        return 0

