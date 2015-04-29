# -*- coding: utf-8 -*- 
#!/usr/bin/python


def equivalentes(archivo_automata1, archivo_automata2):
    automata1 = parsear_automata(archivo_automata1)
	automata2 = parsear_automata(archivo_automata2)
    automata3 = interseccion(automata1,automata2.complemento())
    automata4 = interseccion(automata2,automata1.complemento())
    if len(automata3.transiciones) == 0 and len(automata4.transiciones) == 0: #falta ver si el estado inicial y final tienen que ser distintos
		return True
    return False
