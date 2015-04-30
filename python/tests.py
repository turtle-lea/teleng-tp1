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

### Se parsea correctamente la regex archivos_regex/archivo_regex_1
def test1():
  os.system("./AFD.py -leng archivos_regex/archivo_regex_1 -aut archivos_automata/archivo_automata_1")
  os.system("sleep 0.1")

### Se parsea correctamente un automata
### Se obtiene un automata de la regex archivos_regex/archivo_regex_1 que soporta cadenas del lenguaje
def test2():
  archivo_automata_1 = open('archivos_automata/archivo_automata_1', 'r')
  automata = parsear_automata(archivo_automata_1)
  estados = [0,1,2,3,4,5,6]
  alfabeto = ['a','c', 'b', 'e', 'd', 'f']
  if automata.estados != estados or automata.alfabeto != alfabeto:
    sys.stderr.write('Fallo el parseo del automata en test 1')
    tests_correctamente = False
  if not(automata.pertenece_al_lenguaje('adef')):
    sys.stderr.write('No reconoce una cadena valida')
    tests_correctamente = False
  if not(automata.pertenece_al_lenguaje('babadedef')):
    sys.stderr.write('No reconoce una cadena valida')
    tests_correctamente = False
  if automata.pertenece_al_lenguaje('abcf'):
    sys.stderr.write('Reconoce una cadena NO valida')
    tests_correctamente = False
  if automata.pertenece_al_lenguaje('abcf'):
    sys.stderr.write('Reconoce una cadena NO valida')
    tests_correctamente = False

### Se escribe un archivo dot correspondiente al automata
### El archivo dot puede ser rendereado correctamente y guardado como imagen
def test3():
  x = 3


test1()
test2()
if tests_correctamente:
  print "Los tests finalizaron correctamente"
