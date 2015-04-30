import os
import sys
from automata import *
from regex import *
from ejercicio_a import *
from ejercicio_b import *
from ejercicio_c import *
from ejercicio_d import *


def test1():
  os.system("./AFD.py -leng archivos_regex/archivo_regex_1 -aut archivos_automata/archivo_automata_1")
  os.system("sleep 0.1")
  archivo_automata_1 = open('archivos_automata/archivo_automata_1', 'r')
  automata = parsear_automata(archivo_automata_1)
  estados = [0,1,2,3,4,5,6]
  alfabeto = ['a','c', 'b', 'e', 'd', 'f']
  if automata.estados != estados or automata.alfabeto != alfabeto:
    sys.stderr.write('Fallo el parseo del automata en test 1')


test1()
print "Los tests finalizaron correctamente"
