import os
import sys
from automata import *
from regex import *
from ejercicio_a import *
from ejercicio_b import *
from ejercicio_c import *
from ejercicio_d import *
from ejercicio_e import *
from ejercicio_f import *

tests_correctamente = True

def test1():
	estados = [0, 1]
	alfabeto = ['a','b']
	finales = [1]
	inicial = 0
	transiciones = [ [0,'a',0],[0,'b',1],[1,'b',0] ]
	automata = Automata(estados, alfabeto, inicial, finales, transiciones)
	if not(automata.pertenece_al_lenguaje('ab')):
		sys.stderr.write('Fallo de la comprobacion si una cadena pertenece al lenguaje')
		tests_correctamente = False
	if automata.pertenece_al_lenguaje('a'):
		sys.stderr.write('Fallo de la comprobacion si una cadena pertenece al lenguaje')
		tests_correctamente = False

def test2():
	estados1 = [0, 1]
	alfabeto1 = ['a','b']
	finales1 = [1]
	inicial1 = 0
	transiciones1 = [ [0,'a',1],[0,'b',0],[1,'a',1],[1,'b',1] ]
	automata1 = Automata(estados1, alfabeto1, inicial1, finales1, transiciones1)
	
	estados2 = [0,1]
	alfabeto2 = ['a','b']
	finales2 = [1]
	inicial2 = 0
	transiciones2 = [ [0,'b',1],[0,'a',0],[1,'a',1],[1,'b',1] ]
	automata2 = Automata(estados2, alfabeto2, inicial2, finales2, transiciones2)
	
	automata3 = interseccion_automatas(automata1, automata2)
	
	if not(automata3.pertenece_al_lenguaje('ab') and automata1.pertenece_al_lenguaje('ab') and automata2.pertenece_al_lenguaje('ab')):
		sys.stderr.write('Fallo la interseccion')
		tests_correctamente = False
	if not(automata3.pertenece_al_lenguaje('bab')) and automata1.pertence_al_lenguaje('bab'):
		sys.stderr.write('Fallo la interseccion')
		tests_correctamente = False
		
def test3():
	estados1 = [0,1]
	alfabeto1 = ['a']
	finales1 = [1]
	estado_inicial1 = 0
	transiciones1 = [[0,'a',1],[1,'a',0]]
	automata1 = Automata(estados1, alfabeto1, estado_inicial1, finales1, transiciones1) #acepta cadenas impares de "a"
	
	automata2 = automata1.complemento()
	
	if automata2.pertenece_al_lenguaje('aaa') and not(automata1.pertenece_al_lenguaje('aaa')):
		sys.stderr.write('Fallo el complemento')
		tests_correctamente = False
	if not(automata2.pertenece_al_lenguaje('aa')) and automata1.pertenece_al_lenguaje('aa'):
		sys.stderr.write('Fallo el complemento')
		tests_correctamente = False

def test4():
	estados1 = [0,1,2,3,4]
	alfabeto1 = ['a','b']
	finales1 = [3]
	estado_inicial1 = 0
	transiciones1 = [[0,'a',1],[1,'b',3]]
	automata1 = Automata(estados1, alfabeto1, estado_inicial1, finales1, transiciones1)
	
	estados2 = [0,1,2,3,4]
	alfabeto2 = ['a','b']
	finales2 = [3]
	estado_inicial2 = 0
	transiciones2 = [[0,'a',1],[0,'b',2],[1,'b',3],[1,'a',2],[3,'a',2],[2,'a',4],[4,'b',2]]
	automata2 = Automata(estados2, alfabeto2, estado_inicial2, finales2, transiciones2)
	
	automata3 = interseccion_automatas(automata1,automata2.complemento())
	automata4 = interseccion_automatas(automata2,automata1.complemento())
	automata3 = minimizar_afd(automata3)
	automata4 = minimizar_afd(automata4)
	if len(automata3.transiciones) != 0 or len(automata4.transiciones) != 0:
		sys.stderr.write('Fallo la equivalencia')
		tests_correctamente = False

	estados5 = [0,1,2,3,4]
	alfabeto5 = ['a','b']
	finales5 = [3]
	estado_inicial5 = 0
	transiciones5 = [[0,'a',1],[1,'a',3]]
	automata5 = Automata(estados5, alfabeto5, estado_inicial5, finales5, transiciones5)
	
	automata6 = interseccion_automatas(automata1,automata5.complemento())
	automata7 = interseccion_automatas(automata5,automata1.complemento())
	automata6 = minimizar_afd(automata6)
	automata7 = minimizar_afd(automata7)
	if len(automata6.transiciones) == 0 and len(automata7.transiciones) == 0:
		sys.stderr.write('Fallo la equivalencia')
		tests_correctamente = False

test1()
test2()
test3()
test4()
if tests_correctamente:
  print "Los tests finalizaron correctamente"
