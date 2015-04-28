#  -*- coding: utf-8 -*-
#!/usr/bin/python

def parse_regex(filename):
  f = open(filename, 'r')
  x = parse_regex_aux(f)
  f.close()
  return x

def parse_regex_aux(f):
  l = f.readline()
  if '{' in l:
    operacion = l[l.find("{")+1:l.find("}")]
    argumentos = []
    if (operacion == 'CONCAT') or (operacion == 'OR'):
      cant_argumentos = l[l.find("}")+1]
      cant_argumentos = int(cant_argumentos)
      for i in range(0, cant_argumentos):
        argumentos.append(parse_regex_aux(f))
    else:
      argumentos.append(parse_regex_aux(f))
    return Regex(operacion, '', argumentos)
  else:
    line = l.replace("\t", "")
    simbolo = line[0]
    if simbolo[0] == "\\" and line[1] == 't':
      simbolo = "\t"
    return Regex('simbolo', simbolo, [])

def reducir_argumentos(regex):
  if len(regex.argumentos) < 2:
    return regex
  else:
    a = reducir_argumentos(regex.argumentos.pop(0))
    b = reducir_argumentos(regex.argumentos.pop(0))
    r = Regex(regex.nombre, '', [a,b])
    regex.argumentos.insert(0,r)
    return regex

class Regex:
  def __init__(self, nombre, valor, argumentos ):
    self.nombre = nombre
    self.valor = valor
    self.argumentos = argumentos
