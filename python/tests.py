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

####################################### TESTS DE INTEGRACION (ejercicios a,b y c) #############################

os.system("mkdir -p archivos_automata")
os.system("mkdir -p archivos_dot")
os.system("mkdir -p images")

### Se parsea correctamente la regex archivos_regex/archivo_regex_1 ((a|b|c)*(de)+f)
def test1():
  os.system("./AFD.py -leng archivos_regex/archivo_regex_1 -aut archivos_automata/archivo_automata_1")
  os.system("sleep 0.1")

### Se parsea correctamente un automata
### Se obtiene un automata de la regex archivos_regex/archivo_regex_1 que soporta cadenas del lenguaje
def test2():
  global tests_correctamente
  archivo_automata_1 = open('archivos_automata/archivo_automata_1', 'r')
  automata = parsear_automata(archivo_automata_1)
  alfabeto = ['a','c', 'b', 'e', 'd', 'f']
  if automata.alfabeto != alfabeto:
    sys.stderr.write('Fallo el parseo del automata en test 1\n')
    tests_correctamente = False
  if not(automata.pertenece_al_lenguaje('adef')):
    sys.stderr.write('No reconoce una cadena valida\n')
    tests_correctamente = False
  if not(automata.pertenece_al_lenguaje('babadedef')):
    sys.stderr.write('No reconoce una cadena valida\n')
    tests_correctamente = False
  if automata.pertenece_al_lenguaje('abcf'):
    sys.stderr.write('Reconoce una cadena NO valida\n')
    tests_correctamente = False
  if automata.pertenece_al_lenguaje('abcf\n'):
    sys.stderr.write('Reconoce una cadena NO valida\n')
    tests_correctamente = False

### Se escribe un archivo dot correspondiente al automata
### El archivo dot puede ser rendereado correctamente y guardado como imagen
def test3():
  os.system("./AFD.py -aut archivos_automata/archivo_automata_1 -dot archivos_dot/archivo_dot_1")
  os.system("sleep 0.1")
  os.system("dot -Tpng archivos_dot/archivo_dot_1 -o images/imagen_1")


### Tests 4,5 y 6 son analogos a 1, 2 y 3 pero con archivos_regex/archivo_regex_2 : (-ABC)?(0|1)+\t*

def test4():
  os.system("./AFD.py -leng archivos_regex/archivo_regex_2 -aut archivos_automata/archivo_automata_2")
  os.system("sleep 0.1")

def test5():
  global tests_correctamente
  archivo_automata_2 = open('archivos_automata/archivo_automata_2', 'r')
  automata = parsear_automata(archivo_automata_2)
  #estados_finales = [0,1,2]
  #if automata.estado_inicial != 3 or automata.estados_finales != estados_finales:
    #tests_correctamente = False
    #sys.stderr.write('Fallo el parseo del automata en test 2\n')
  if not(automata.pertenece_al_lenguaje('010101')):
    sys.stderr.write('No reconoce una cadena valida\n')
    tests_correctamente = False
  if not(automata.pertenece_al_lenguaje('-ABC0\t\t')):
    sys.stderr.write('No reconoce una cadena valida\n')
    tests_correctamente = False
  if automata.pertenece_al_lenguaje('AB01'):
    sys.stderr.write('Reconoce una cadena NO valida')
    tests_correctamente = False
  if automata.pertenece_al_lenguaje('01ABC'):
    sys.stderr.write('Reconoce una cadena NO valida')
    tests_correctamente = False

def test6():
  os.system("./AFD.py -aut archivos_automata/archivo_automata_2 -dot archivos_dot/archivo_dot_2")
  os.system("sleep 0.1")
  os.system("dot -Tpng archivos_dot/archivo_dot_2 -o images/imagen_2")

### Tests 7: Ejemplo 1 de la seccion 4.3 del enunciado: ac*(bf*)?

def test7():
  os.system("./AFD.py -leng archivos_regex/archivo_regex_3 -aut archivos_automata/archivo_automata_3")
  os.system("sleep 0.1")
  os.system("./AFD.py -aut archivos_automata/archivo_automata_3 -dot archivos_dot/archivo_dot_3")
  os.system("sleep 0.1")
  os.system("dot -Tpng archivos_dot/archivo_dot_3 -o images/imagen_3")

### Tests 8: Ejemplo 2 de la seccion 4.3 del enunciado: (a*(ba*b)?(ccc)*

def test8():
  os.system("./AFD.py -leng archivos_regex/archivo_regex_4 -aut archivos_automata/archivo_automata_4")
  os.system("sleep 0.1")
  os.system("./AFD.py -aut archivos_automata/archivo_automata_4 -dot archivos_dot/archivo_dot_4")
  os.system("sleep 0.1")
  os.system("dot -Tpng archivos_dot/archivo_dot_4 -o images/imagen_4")

### Tests 9: Ejemplo de la seccion 5 del enunciado: (a|b)(a|b)*

def test9():
  os.system("./AFD.py -leng archivos_regex/archivo_regex_5 -aut archivos_automata/archivo_automata_5")
  os.system("sleep 0.1")
  os.system("./AFD.py -aut archivos_automata/archivo_automata_5 -dot archivos_dot/archivo_dot_5")
  os.system("sleep 0.1")
  os.system("dot -Tpng archivos_dot/archivo_dot_5 -o images/imagen_5")

def test9_bis():
  os.system("./AFD.py -leng archivos_regex/archivo_regex_6 -aut archivos_automata/archivo_automata_6")
  os.system("sleep 0.1")
  os.system("./AFD.py -aut archivos_automata/archivo_automata_6 -dot archivos_dot/archivo_dot_6")
  os.system("sleep 0.1")
  os.system("dot -Tpng archivos_dot/archivo_dot_6 -o images/imagen_6")

def test9_bis_bis():
  os.system("./AFD.py -leng archivos_regex/archivo_regex_7 -aut archivos_automata/archivo_automata_7")
  os.system("sleep 0.1")
  os.system("./AFD.py -aut archivos_automata/archivo_automata_7 -dot archivos_dot/archivo_dot_7")
  os.system("sleep 0.1")
  os.system("dot -Tpng archivos_dot/archivo_dot_7 -o images/imagen_7")



################################## TESTS DE FUNCIONALIDAD (d,e y f) ####################################

def test10():
  global tests_correctamente
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

def test11():
  global tests_correctamente
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

def test12():
  global tests_correctamente
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

test1()
test2()
test3()
test4()
test5()
test6()
test7()
test8()
test9()
test9_bis()
test9_bis_bis()
test10()
test11()
test12()

if tests_correctamente:
  print "Los tests finalizaron correctamente"
