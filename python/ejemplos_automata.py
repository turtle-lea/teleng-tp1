# -*- coding: utf-8 -*-
#!/usr/bin/python

import automata
from automata import *

transiciones1 = [[0,'lambda',1],[0,'a',2],[0,'lambda',3], [1,'lambda',4], [3,'lambda',4]]
estados = [0,1,2,3,4]
finales = []
alfabeto = ['lambda','a']
inicial = 0

transiciones2 = [[0,'lambda',1], [1,'lambda',2],[2,'lambda',0]]
transiciones3 = []
finales4 = [2]
transiciones4 = [[0,'lambda',1],[1,'lambda',2],[2,'lambda',0]]

alfabeto5 = ['a','lambda']
finales5 = [2,3,4]
transiciones5 = [[0,'lambda',1],[1,'a',2],[1,'a',3],[1,'a',4], [2,'lambda',3], [2,'lambda',4], [3,'lambda',2], [3, 'lambda', 4], [4, 'lambda',2], [4,'lambda',3]]

automata1 = Automata(estados,alfabeto5,inicial,finales,transiciones1)
automata2 = Automata(estados,alfabeto,inicial,finales,transiciones2)
automata3 = Automata(estados,alfabeto,inicial,finales,transiciones3)
automata4 = Automata(estados,alfabeto,inicial,finales4,transiciones4)
automata5 = Automata(estados,alfabeto,inicial,finales5,transiciones5)
automata6 = automata5.remover_transiciones_lambda()
automata7 = automata6.determinizar_automata()

estados29 = [0,1,2]
alfabeto29 = ['a','b']
finales29 = [2]
inicial29 = 0
transiciones29 = [[0,'a',0],[0,'b',0],[0,'a',1],[1,'b',2]]
automata29 = Automata(estados29, alfabeto29, inicial29, finales29, transiciones29)
