# -*- coding: utf-8 -*-
#!/usr/bin/python

import sys
import os

def armar_automata(regpars):

        if regpars.nombre == 'OPT':
                automata0 = Automata([0],['lambda'], 0, [0], [])
                automataF = Automata([0],['lambda'], 0, [0], [])
                automataM1 = Automata([0,1],['lambda'], 0, [1], [[0,'lambda',1]])
                automataM1 = armarConcat(automata0, 'lambda', automataM1)  #agregar transición final 0 con inicial
                automataM1 = armarConcat(automataM1, 'lambda', automataF)
                automataM2 = armar_automata(regpars.argumentos[0])
                automataM1 = armarOr(automataM1, 'lambda', automataM2)

        if regpars.nombre == 'CONCAT':
                cant_arg = len(regpars.argumentos)
                automataM1 = armar_automata(regpars.argumentos[0])

                for i in range(1,cant_arg):
                        automataM2 = armar_automata(regpars.argumentos[i])
                        automataM1 = armarConcat(automataM1, 'lambda', automataM2) #agregar transición final M1 con iinicial M2

        if regpars.nombre == 'OR':
                cant_arg = len(regpars.argumentos)
                automataM1 = armar_automata(regpars.argumentos[0])

                automata0 = Automata([0],['lambda'], 0, [0], [])
                automataF = Automata([0],['lambda'], 0, [0], [])

                automataM1 = armarConcat(automata0, 'lambda', automataM1)  #agregar transición final 0 con inicial
                automataM1 = armarConcat(automataM1, 'lambda', automataF)

                for i in range(1,cant_arg):
                        automataM2 = armar_automata(regpars.argumentos[i])
                        automataM1 = armarOr(automataM1, 'lambda', automataM2) #agregar transicion desde estado inicial M1 con inicialM2

        if (regpars.nombre == 'STAR') or (regpars.nombre == 'PLUS'):
                automata0 = Automata([0],['lambda'], 0, [0], [])
                automataF = Automata([0],['lambda'], 0, [0], [])
                automataM1 = armar_automata(regpars.argumentos[0])
                automataM1 = armarPlus(automata0, automataM1, automataF)

                if (regpars.nombre == 'STAR'):
                        estado_final_M1 = automataM1.estados_finales[0] #Se que siempre es único por definición de Plus del algoritmo Thompson
                        estado_inicial_M1 = automataM1.estado_inicial
                        automataM1.transiciones.append([estado_inicial_M1, 'lambda',estado_final_M1])

        if regpars.nombre == 'simbolo':
                automataM1 = Automata([0,1],['lambda',regpars.valor], 0, [1], [[0,regpars.valor,1]])

        return automataM1

def armarConcat(automata1, lamb, automata2):
        automata2 = renombrarAutomata(automata1, automata2)
        estados_finales_A1 = automata1.estados_finales
        estado_inicial_A2 = automata2.estado_inicial

        automata1 = unirAutomatas(automata1,automata2, 'CONCAT')        
        for i in range(0,len(estados_finales_A1)):
                automata1.transiciones.append([estados_finales_A1[i], lamb,estado_inicial_A2])

        return automata1

def armarOr(automata1, lamb, automata2):

        automata2 = renombrarAutomata(automata1, automata2)

        estado_inicial_A1 = automata1.estado_inicial
        estado_final_A1 = automata1.estados_finales[0] #Se que siempre es único por definición de Or del algoritmo Thompson
        estado_inicial_A2 = automata2.estado_inicial
        estados_finales_A2 = automata2.estados_finales

        automata1 = unirAutomatas(automata1,automata2, 'OR')

        automata1.transiciones.append([estado_inicial_A1, lamb,estado_inicial_A2])

        for i in range(0,len(estados_finales_A2)):
                automata1.transiciones.append([estados_finales_A2[i], lamb,estado_final_A1])

        return automata1

def armarPlus(automata0, automataM1, automataF):

        estado_inicial_M1 = automataM1.estado_inicial
        estados_finales_M1 = automataM1.estados_finales
        for i in range(0,len(estados_finales_M1)):
                automataM1.transiciones.append([estados_finales_M1[i], 'lambda',estado_inicial_M1])

        automataM1 = armarConcat(automata0, 'lambda', automataM1)
        automataM1 = armarConcat(automataM1, 'lambda', automataF)

        return automataM1

def unirAutomatas(automata1, automata2, forma_de_union):

        automata1.estados = automata1.estados + automata2.estados
        automata1.alfabeto = list(set(automata1.alfabeto + automata2.alfabeto))

        if forma_de_union == 'CONCAT':
                automata1.estados_finales = automata2.estados_finales

        for i in (range(0,len(automata2.transiciones))):
                automata1.transiciones.append(automata2.transiciones[i])

        return automata1

def renombrarAutomata(automata1, automata2):

        for i in (range(0, len(automata2.estados))):
                if (automata2.estados[i] in automata1.estados):
                        nuevoEstado = buscarEstadoQueNoExista(automata1.estados, automata2.estados)
                        automata2.transiciones = renombrarTransiciones(automata2.transiciones, automata2.estados[i], nuevoEstado)

                        if (automata2.estados[i] == automata2.estado_inicial):
                                automata2.estado_inicial = nuevoEstado

                        for j in (range(0, len(automata2.estados_finales))):
                                if (automata2.estados[i] == automata2.estados_finales[j]):
                                        automata2.estados_finales[j] = nuevoEstado

                        automata2.estados[i] = nuevoEstado

        return automata2

def buscarEstadoQueNoExista(estados1, estados2):
	i = 0
	while ((i in estados1) or (i in estados2)):
		i = i + 1

	return i

def renombrarTransiciones(transiciones, estado, nuevoEstado):

	for i in (range(0, len(transiciones))):
		if (transiciones[i][0] == estado):
			transiciones[i][0] = nuevoEstado
		if (transiciones[i][2] == estado):
			transiciones[i][2] = nuevoEstado

	return transiciones

def interseccion(automata1, automata2):
	inicial1 = automata1.estado_inicial
	inicial2 = automata2.estado_inicial
	finales1 = automata1.estados_finales
	finales2 = automata2.estados_finales
	alfabeto = []
	for a1 in automata1.alfabeto:
		for a2 in automata2.alfabeto:
			if a1 == a2:
				alfabeto.append(a1)
	estados = []
	for e1 in automata1.estados:
		for e2 in automata2.estados:
			estados.append([e1,e2])
	transiciones = []
	for t1 in automata1.transiciones:
		for t2 in automata2.transiciones:
			if t1[1] == t2[1]:
				transiciones.append([[t1[0],t2[0]],t1[1],[t1[2],t2[2]]])
	inicial = [inicial1,inicial2]
	finales = []
	for f1 in finales1:
		for f2 in finales2:
			finales.append([f1,f2])

	a = Automata(estados, alfabeto, inicial, finales, transiciones)
	a.renombrar_estados()
	return a
	
def escribir_archivo(automata, filename):
	f = open(filename, 'w')

	for i in range(0, len(automata.estados)):
		if i < len(automata.estados)-1 :
			f.write('q')
			f.write(str(automata.estados[i]))
			f.write('\t')
		if i == len(automata.estados)-1 :
			f.write('q')
			f.write(str(automata.estados[i]))

	f.write('\n')

	for i in range(0, len(automata.alfabeto)):
		if (i < len(automata.alfabeto)-1) and (automata.alfabeto[i] != 'lambda') :
			f.write(str(automata.alfabeto[i]))
			f.write('\t')
		if (i == len(automata.alfabeto)-1) and (automata.alfabeto[i] != 'lambda') :
			f.write(str(automata.alfabeto[i]))

	f.write('\n')

	f.write('q')
	f.write(str(automata.estado_inicial))

	f.write('\n')

	for i in range(0, len(automata.estados_finales)):
		if i < len(automata.estados_finales)-1 :
			f.write('q')
			f.write(str(automata.estados_finales[i]))
			f.write('\t')
		if i == len(automata.estados_finales)-1 :
			f.write('q')
			f.write(str(automata.estados_finales[i]))

	f.write('\n')

	for i in range(0, len(automata.transiciones)):
		if i < len(automata.transiciones)-1 :
			f.write('q')
			f.write(str(automata.transiciones[i][0]))
			f.write('\t')
			f.write(str(automata.transiciones[i][1]))
			f.write('\t')
			f.write('q')
			f.write(str(automata.transiciones[i][2]))
			f.write('\n')
		if i == len(automata.transiciones)-1 :
			f.write('q')
			f.write(str(automata.transiciones[i][0]))
			f.write('\t')
			f.write(str(automata.transiciones[i][1]))
			f.write('\t')
			f.write('q')
			f.write(str(automata.transiciones[i][2]))

	f.close()

	return 0



def parsear_automata(filename):
	with open(filename,'r') as f:
		lines = f.readlines()

		#Leo los estados
		estados = lines[0].split()
		estados = [int(e[1:len(e)]) for e in estados]

		#Leo el alfabeto
		alfabeto = lines[1].split()

		#Leo el estado inicial
		estado_inicial = (lines[2].split())[0]
		estado_inicial = int(estado_inicial[1:len(estado_inicial)])
		if not(estado_inicial in estados):
			sys.stderr.write("El estado inicial no pertenece a los estados\n")

		#Leo los estados finales
		estados_finales = lines[3].split()
		estados_finales = [int(e[1:len(e)]) for e in estados_finales]
		for e in estados_finales:
			if not(e in estados):
				sys.stderr.write("El estado final '%s' no pertenece a los estados\n" % str(e))

		#Leo las transiciones
		transiciones = []
		for i in range(4,len(lines)):
			t = lines[i].split()
			t[0] = int((t[0])[1:len(t[0])])
			t[2] = int((t[2])[1:len(t[2])])
			if (not(t[0] in estados) or not(t[1] in alfabeto) or not(t[2] in estados)):
				sys.stderr.write("Transicion invalida de automata\n")
			transiciones.append(t)

		return Automata(estados,alfabeto,estado_inicial,estados_finales,transiciones)


class Automata:
  def __init__(self, estados, alfabeto, estado_inicial, estados_finales, transiciones):
    self.estados = estados
    self.alfabeto = alfabeto
    self.estado_inicial = estado_inicial
    self.estados_finales = estados_finales
    self.transiciones = transiciones

  ##### Metodos auxiliares para transformar AFND-lambda en AFND

  def clausura(self, estado, simbolo):
  	resto_transiciones = list(self.transiciones)
  	if simbolo == 'lambda':
  		clausura = [estado]
  	else:
  		clausura = []
  	return self.clausura_aux(estado,simbolo,resto_transiciones,clausura)

  def clausura_aux(self, estado, simbolo, resto_transiciones, clausura):
    resto_transiciones_copy = list(resto_transiciones)
    resto_transiciones = [t for t in resto_transiciones if (t[0] == estado) and (t[1] == simbolo)]
    for t in resto_transiciones:
      resto_transiciones_copy.remove(t)
      clausura = self.clausura_aux(t[2], simbolo, resto_transiciones_copy, clausura)
      if not (t[2] in clausura):
        clausura.append(t[2])
      resto_transiciones_copy.append(t)
    return clausura

  #La idea para calcular las nuevas transiciones es la siguiente:
  #Dado un estado q y un símbolo de transición s
  #Primero calculo la clausura lambda de q
  #Para cada uno de los elementos de la clausura obtengo la clausura tomando la transición s
  #Sobre cada uno de estos elementos, obtengo la clausura lambda nuevamente
  #Finalmente, creo una transición del estilo (q,s,e) por cada uno de estos elementos
  def remover_transiciones_lambda(self):
    clausura_lambda_inicial = self.clausura_lambda(self.estado_inicial)
    intersection = [x for x in clausura_lambda_inicial if x in self.estados_finales]
    finales = list(self.estados_finales)
    if len(intersection) > 0 and not(self.estado_inicial in self.estados_finales):
      finales.append(self.estado_inicial)

    nuevas_transiciones = []
    for q in self.estados:
      for s in self.alfabeto:
        if s != 'lambda':
          clausura_lambda_q = self.clausura_lambda(q)
          for e in clausura_lambda_q:
            estados_alcanzables_por_transicion = self.delta_nd(e,s)
            clausura_lambda_estados_alcanzables = [self.clausura_lambda(x) for x in estados_alcanzables_por_transicion ]
            clausura_lambda_estados_alcanzables = [x for sublist in clausura_lambda_estados_alcanzables for x in sublist]
            clausura_lambda_estados_alcanzables = set(clausura_lambda_estados_alcanzables)
            for estado_clausura in clausura_lambda_estados_alcanzables:
              nueva_t = [q, s, estado_clausura]
              if not(nueva_t in nuevas_transiciones):
                nuevas_transiciones.append(nueva_t)

    alfabeto = list(self.alfabeto)
    if 'lambda' in alfabeto:
    	alfabeto.remove('lambda')
    return Automata(self.estados, alfabeto, self.estado_inicial, finales, nuevas_transiciones)

  ##### Metodos auxiliar para transformar un AFND en AFD

  def clausura_lambda(self,estado):
    return self.clausura(estado,'lambda')

  def delta_nd(self,estado,simbolo):
  	return sorted([t[2] for t in self.transiciones if (t[0] ==
  	 estado and t[1] == simbolo)])

  def delta_nd_conjunto(self,conjunto_estados,simbolo):
  	es = [self.delta_nd(e,simbolo) for e in conjunto_estados]
  	es = [e for sublist in es for e in sublist]
  	return list(set(es))

  def transiciones_de_estado(self, estado):
  	return [t[1] for t in self.transiciones if t[0] == estado]

  def transiciones_de_conjunto(self,conjunto_estados):
  	es = [self.transiciones_de_estado(e) for e in conjunto_estados]
  	es = [e for sublist in es for e in sublist]
  	es = list(set(es))
  	return es

  def renombrar_estados(self):
  	nombre_actual = 0
  	for i in range(0, len(self.estados)):
  		e = self.estados[i]
  		nombre_viejo = e
  		if self.estado_inicial == e:
  			self.estado_inicial = nombre_actual
  		if e in self.estados_finales:
  			self.estados_finales.remove(e)
  			self.estados_finales.append(nombre_actual)
  		for j in range(0, len(self.transiciones)):
  			t = self.transiciones[j]
  			nueva_t = list(t)
  			if nueva_t[0] == nombre_viejo:
  				nueva_t[0] = nombre_actual
  			if nueva_t[2] == nombre_viejo:
  				nueva_t[2] = nombre_actual
  			if t != nueva_t:
  				self.transiciones[j] = nueva_t
  		self.estados[i] = nombre_actual
  		nombre_actual += 1

  def determinizar_automata(self):
  	inicial = [self.estado_inicial]
  	faltan_agregar = [inicial]
  	transiciones = []
  	estados = []
  	while len(faltan_agregar) > 0:
  		es = faltan_agregar.pop()
  		estados.append(es)
  		ts = self.transiciones_de_conjunto(es)
  		for t in ts:
  			estado = self.delta_nd_conjunto(es,t)
  			transiciones.append([es,t,estado])
  			if not(estado in estados) and not(estado in faltan_agregar):
  				faltan_agregar.append(estado)
  	fs = set(self.estados_finales)
  	finales = [e for e in estados if len(fs.intersection(set(e))) > 0]
  	a = Automata(estados, self.alfabeto, inicial, finales, transiciones)
  	a.renombrar_estados()
  	return a

  def crear_estado_trampa(self):
        return max(self.estados)+1

  def completar_transiciones(self,estado_trampa):
        estados = self.estados + [estado_trampa]
        transiciones_agregadas = []
        for e in estados:
            for s in self.alfabeto:
                if len([t for t in self.transiciones if (t[0] == e) and (t[1] == s) ]) == 0:
                    transiciones_agregadas.append([e,s,estado_trampa])
        return transiciones_agregadas


  def complemento(self):
        estado_trampa = self.crear_estado_trampa()
        transiciones_a_agregar = self.completar_transiciones(estado_trampa)
        nuevos_finales = set(self.estados+[estado_trampa]) - set(self.estados_finales)
        nuevos_finales = list(nuevos_finales)
        return Automata(self.estados+[estado_trampa], self.alfabeto, self.estado_inicial, nuevos_finales, self.transiciones+transiciones_a_agregar)

def pertenece_al_lenguaje_automata(self, cadena):
	recorrer_automata  = self.estado_inicial
	i = 0
	j = 0
	while (i < len(cadena)) and (j < len(self.transiciones)):
		if (self.transiciones[j][0] == recorrer_automata) and (self.transiciones[j][1] == cadena[i]):
			i=i+1
			recorrer_automata = self.transiciones[j][2]
			j=-1
		j=j+1

	if i == len(cadena):
		if recorrer_automata in self.estados_finales:
			return True

	return False
