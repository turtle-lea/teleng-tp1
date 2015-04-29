from ejercicio_a import *

def test1():
    transiciones = []
    transiciones.append([1, 'a', 3])
    transiciones.append([1, 'b', 2])
    transiciones.append([2, 'a', 4])
    transiciones.append([2, 'b', 1])
    transiciones.append([3, 'a', 5])
    transiciones.append([3, 'b', 4])
    transiciones.append([4, 'a', 4])
    transiciones.append([4, 'b', 4])
    transiciones.append([5, 'a', 3])
    transiciones.append([5, 'b', 2])
    alfabeto = ["a", "b"]
    estados = [1,2,3,4,5]
    estados_finales = [1,5]
    estado_inicial = 1

    automat = Automata (estados, alfabeto, estado_inicial, estados_finales, transiciones)
    min_afd = minimizar_afd(automat)

    #dicctest = transitions_by_state_and_label(automat.transiciones)
    #print (dicctest[(3, 'b')])
    
    print (min_afd.estados)
    print (min_afd.alfabeto)
    print (min_afd.estado_inicial)
    print (min_afd.estados_finales)
    print (min_afd.transiciones)

def test2():
    transiciones = []
    alfabeto = []
    estados = [1]
    estados_finales = [1]
    estado_inicial = 1
    automat = Automata (estados, alfabeto, estado_inicial, estados_finales, transiciones)
    min_afd = minimizar_afd(automat)
    print (min_afd.estados)
    print (min_afd.alfabeto)
    print (min_afd.estado_inicial)
    print (min_afd.estados_finales)
    print (min_afd.transiciones)

def test3():
    transiciones = []
    transiciones.append([1, 'a', 2])
    transiciones.append([2, 'b', 3])
    transiciones.append([3, 'c', 4])
    transiciones.append([4, 'd', 5])
    alfabeto = ["a", "b", "c", "d"]
    estados = [1,2,3,4,5]
    estados_finales = [5]
    estado_inicial = 1

    automat = Automata (estados, alfabeto, estado_inicial, estados_finales, transiciones)
    min_afd = minimizar_afd(automat)

    #dicctest = transitions_by_state_and_label(automat.transiciones)
    #print (dicctest[(3, 'b')])
    
    print (min_afd.estados)
    print (min_afd.alfabeto)
    print (min_afd.estado_inicial)
    print (min_afd.estados_finales)
    print (min_afd.transiciones)

def test4():
    transiciones = []
    transiciones.append([1, 'a', 2])
    transiciones.append([1, 'b', 3])
    transiciones.append([2, 'a', 2])
    transiciones.append([2, 'b', 4])
    transiciones.append([3, 'a', 3])
    transiciones.append([3, 'b', 3])
    transiciones.append([4, 'a', 6])
    transiciones.append([4, 'b', 3])
    transiciones.append([5, 'a', 5])
    transiciones.append([5, 'b', 3])
    transiciones.append([6, 'a', 5])
    transiciones.append([6, 'b', 4])
    alfabeto = ["a", "b"]
    estados = [1,2,3,4,5,6]
    estados_finales = [1,2,4,5,6]
    estado_inicial = 1

    automat = Automata (estados, alfabeto, estado_inicial, estados_finales, transiciones)
    min_afd = minimizar_afd(automat)

    #dicctest = transitions_by_state_and_label(automat.transiciones)
    #print (dicctest[(3, 'b')])
    
    print (min_afd.estados)
    print (min_afd.alfabeto)
    print (min_afd.estado_inicial)
    print (min_afd.estados_finales)
    print (min_afd.transiciones)

def test5():
    transiciones = []
    transiciones.append([0, '0', 1])
    transiciones.append([0, '1', 0])
    transiciones.append([1, '0', 0])
    transiciones.append([1, '1', 1])
    transiciones.append([2, '1', 0])
    transiciones.append([2, '0', 1])
    alfabeto = ["0", "1"]
    estados = [0,1,2]
    estados_finales = [1]
    estado_inicial = 0

    automat = Automata (estados, alfabeto, estado_inicial, estados_finales, transiciones)
    min_afd = minimizar_afd(automat)

    #dicctest = transitions_by_state_and_label(automat.transiciones)
    #print (dicctest[(3, 'b')])
    
    print (min_afd.estados)
    print (min_afd.alfabeto)
    print (min_afd.estado_inicial)
    print (min_afd.estados_finales)
    print (min_afd.transiciones)

def test6():
    transiciones = []
    transiciones.append([1, 'a', 2])
    transiciones.append([2, 'b', 3])
    transiciones.append([3, 'c', 4])
    transiciones.append([4, 'd', 4])
    transiciones.append([5, 'e', 6])
    transiciones.append([6, 'f', 7])
    transiciones.append([7, 'g', 8])
    alfabeto = ["a", "b", "c", "d", "e", "f", "g"]
    estados = [1,2,3,4,5,6,7,8]
    estados_finales = [4, 8]
    estado_inicial = 1

    automat = Automata (estados, alfabeto, estado_inicial, estados_finales, transiciones)
    min_afd = minimizar_afd(automat)

    #dicctest = transitions_by_state_and_label(automat.transiciones)
    #print (dicctest[(3, 'b')])
    transitions = transitions_by_state_and_label(automat)
    #print (transitions)
    #print (n_recheable(1, 5, alfabeto, transitions, len(estados)))
    print (min_afd.estados)
    print (min_afd.alfabeto)
    print (min_afd.estado_inicial)
    print (min_afd.estados_finales)
    print (min_afd.transiciones)

