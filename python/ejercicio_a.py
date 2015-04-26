# -*- coding: utf-8 -*- 
#!/usr/bin/python


def afd_minimo(archivo_regex, archivo_automata):
    raise NotImplementedError


class Automata:
  def __init__(self, estados, alfabeto, estado_inicial, estados_finales, transiciones):
    self.estados = estados
    self.alfabeto = alfabeto
    self.estado_inicial = estado_inicial
    self.estados_finales = estados_finales
    self.transiciones = transiciones
