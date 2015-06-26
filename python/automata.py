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

def interseccion_automatas(automata1, automata2):
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
	a = a.determinizar_automata() # elimina estados inalcanzables o sobrantes
	a = a.minimizar_afd()
	return a

def escribir_archivo(automata, f):
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
			if str(automata.alfabeto[i]) == '\t':
				f.write('\\t')
			else:
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
			if str(automata.transiciones[i][1]) == '\t':
				f.write('\\t')
			else:
				f.write(str(automata.transiciones[i][1]))
			f.write('\t')
			f.write('q')
			f.write(str(automata.transiciones[i][2]))
			f.write('\n')
		if i == len(automata.transiciones)-1 :
			f.write('q')
			f.write(str(automata.transiciones[i][0]))
			f.write('\t')
			if str(automata.transiciones[i][1]) == '\t':
				f.write('\\t')
			else:
				f.write(str(automata.transiciones[i][1]))
			f.write('\t')
			f.write('q')
			f.write(str(automata.transiciones[i][2]))

	f.close()

	return 0



def parsear_automata(f):
	lines = f.readlines()

	#Leo los estados
	estados = lines[0].split()
	estados = [int(e[1:len(e)]) for e in estados]

	#Leo el alfabeto
	alfabeto = lines[1].split()
	for i in range(0,len(alfabeto)):
		if alfabeto[i] == "\\t":
			alfabeto[i] = "\t"

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
		if t[1] == "\\t":
			t[1] = "\t"
		if (not(t[0] in estados) or not(t[2] in estados)):
			sys.stderr.write("Transicion invalida de automata\n")
		transiciones.append(t)

	f.close()
	return Automata(estados,alfabeto,estado_inicial,estados_finales,transiciones)


class Automata:
  def __init__(self, estados, alfabeto, estado_inicial, estados_finales, transiciones):
    self.estados = estados
    self.alfabeto = alfabeto
    self.estado_inicial = estado_inicial
    self.estados_finales = estados_finales
    self.transiciones = transiciones

  ##### Metodos auxiliares para transformar AFND-lambda en AFND

  def obtener_identificador(self, map_identificador_estado, conjunto_clausura):
    identificador = -1
    for i in map_identificador_estado:
      if map_identificador_estado[i] == conjunto_clausura:
        identificador = i
    return identificador

  def determinizar_automata(self):
    identificador = 0
    map_identificador_estado = {}
    t = {}
    estado_inicial = self.clausura_lambda(self.estado_inicial)
    cola_conjunto_clausuras = [estado_inicial]

    while len(cola_conjunto_clausuras) > 0:
      estado_actual = cola_conjunto_clausuras.pop(0)
      map_identificador_estado[identificador] = estado_actual
      t[identificador] = {}
      for symbol in self.alfabeto:
        if symbol != 'lambda':
          conjunto_clausura = self.delta_nd_conjunto(estado_actual, symbol)
          conjunto_clausura2 = []
          for cc in conjunto_clausura:
            conjunto_clausura2 = conjunto_clausura2 + self.clausura_lambda(cc)
          conjunto_clausura = set(conjunto_clausura + conjunto_clausura2)

          t[identificador][symbol] = conjunto_clausura
          if self.obtener_identificador(map_identificador_estado, conjunto_clausura) == (-1) and conjunto_clausura not in cola_conjunto_clausuras:
            cola_conjunto_clausuras.append(conjunto_clausura)
      identificador += 1

    estado_inicial = self.obtener_identificador(map_identificador_estado, estado_inicial)
    estados = []
    transiciones = []
    estados_finales = []
    for identificador in t.keys():
      estados.append(identificador)
      estado = map_identificador_estado[identificador]
      if len(set(estado).intersection(self.estados_finales)) > 0:
        estados_finales.append(identificador)
      for simbolo in t[identificador].keys():
        destino = t[identificador][simbolo]
        idDestino = self.obtener_identificador(map_identificador_estado, destino)
        transiciones.append([identificador,simbolo,idDestino])

    alfabeto = []
    for a in self.alfabeto:
      if a != 'lambda':
        alfabeto.append(a)

    a = Automata(estados, alfabeto, estado_inicial, estados_finales, transiciones)
    return a

  def particionPertenece(self, estado, particion_clases):
    for p in particion_clases:
      if estado in p:
        particion = p
    return particion

  def armar_automata_minimo(self, particion_clases):
    tablas = {}
    for p in particion_clases:
      t = {}
      for e1 in p:
        t[e1]={}
        for simbolo in self.alfabeto:
          e2 = self.destino(e1, simbolo)
          p2 = self.particionPertenece(e2,particion_clases)
          t[e1][simbolo] = p2
      tablas[p] = t
    estados = []
    estados_finales = []
    transiciones = []
    for p in particion_clases:
      estados.append(p)
      if(self.estado_inicial in p):
        estado_inicial = p
      if(len([e for e in p if (e in self.estados_finales)]) != 0):
        estados_finales.append(p)
    for k in tablas:
      e = tablas[k].keys()[0]
      for simbolo in self.alfabeto:
        transiciones.append([k,simbolo,tablas[k][e][simbolo]])

    a = Automata(estados, self.alfabeto, estado_inicial, estados_finales, transiciones)
    a.renombrar_estados()
    return a

  def minimizar_afd(self):
    finales = frozenset(self.estados_finales)
    no_finales = frozenset([e for e in self.estados if (e not in self.estados_finales)])
    particion_clases = set([no_finales, finales])
    nueva_particion_clases = self.nueva_particion(particion_clases)
    while(particion_clases != nueva_particion_clases):
      particion_clases = nueva_particion_clases
      nueva_particion_clases = self.nueva_particion(particion_clases)
    a = self.armar_automata_minimo(particion_clases)
    return a

  def destino(self, origen, label):
    return [t[2] for t in self.transiciones if (t[0] == origen) and (t[1] == label)][0]

  def clase_que_contiene(self, estado, particion_clases):
    res = set([])
    for clase in particion_clases:
      if estado in clase:
        res = clase
    return res

  def no_pertenece_a_ninguna(self, estado, particion_clases):
    return len(self.clase_que_contiene(estado, particion_clases)) == 0

  def nueva_particion(self, particion_clases):
    nueva_particion = set([])
    for clase in particion_clases:
      t = {}
      for estado in clase:
        t[estado] = {}
        for simbolo in self.alfabeto:
          e2 = self.destino(estado, simbolo)
          c_e2 = self.clase_que_contiene(e2, particion_clases)
          t[estado][simbolo] = c_e2
      for e1 in t:
        if self.no_pertenece_a_ninguna(e1, nueva_particion):
          nueva_clase = set([e1])
          for e2 in t:
            if (t[e1] == t[e2]):
              nueva_clase.add(e2)
          nueva_particion.add(frozenset(nueva_clase))
    return nueva_particion

  def clausura_lambda(self, estado):
    ### Todo estado pertenece a su clausura lambda ###
  	clausura = [estado]
  	return self.clausura_aux(estado, self.transiciones,clausura)

  def clausura_aux(self, estado, resto_transiciones, clausura):
    resto_transiciones_copy = list(resto_transiciones)
    resto_transiciones = [t for t in resto_transiciones if (t[0] == estado) and (t[1] == 'lambda')]
    for t in resto_transiciones:
      resto_transiciones_copy.remove(t)
      clausura = self.clausura_aux(t[2], resto_transiciones_copy, clausura)
      if not (t[2] in clausura):
        clausura.append(t[2])
      resto_transiciones_copy.append(t)
    return clausura

  ### Funcion delta definida para automatas no deterministicos
  ### delta : Q x Sigma -> [Q]
  ### Dado un estado y un simbolo, delta(q,s) devuelve el conjunto
  ### de estados alcanzables tomando la transicion s desde q
  def delta_nd(self,estado,simbolo):
  	return sorted([t[2] for t in self.transiciones if (t[0] ==
  	 estado and t[1] == simbolo)])

  ### Funcion delta generalizada para un conjunto de estados en automatas no deterministicos
  ### delta_nd_conjunto : [Q] x Sigma -> [Q]. delta_conjunto(qs,s)
  ### Devuelve el conjunto de estados alcanzables tomando la transicion s desde todos los q
  ### pertenecientes a qs
  def delta_nd_conjunto(self,conjunto_estados,simbolo):
  	es = [self.delta_nd(e,simbolo) for e in conjunto_estados]
  	es = [e for sublist in es for e in sublist]
  	return list(set(es))

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
        a = Automata(self.estados+[estado_trampa], self.alfabeto, self.estado_inicial, nuevos_finales, self.transiciones+transiciones_a_agregar)
        a = a.determinizar_automata()
        a = a.minimizar_afd()
        return a

  def pertenece_al_lenguaje(self, cadena):
    recorrer_automata  = self.estado_inicial
    i = 0
    j = 0

    #Aceptamos cadena vacia
    if len(cadena) == 0 and self.estado_inicial in self.estados_finales:
		return True

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
