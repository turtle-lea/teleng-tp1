	# -*- coding: utf-8 -*-
#!/usr/bin/python

from regex import *
from automata import *

def afd_minimo(archivo_regex, archivo_automata):
        regpars = parse_regex(archivo_regex)
        automata = armar_automata(regpars)
        ### AFND-lambda ---> AFND
        automata = automata.remover_transiciones_lambda()
        ### AFND ---> AFD
        automata = automata.determinizar_automata()
        automata = minimizar_afd(automata)
        escribir_archivo(automata, archivo_automata)
        return 0


#automata debe ser deterministico
def transitions_by_state_and_label(automata):
        group = {}
        for transition in automata.transiciones:
                #key = (origin_state, label)
                key = transition[0], transition[1]
                #value = dest_state (deterministic automat goes to one state)
                value = transition[2]
                group[key] = value

        return group

# http://www.cs.odu.edu/~toida/nerzic/390teched/regular/fa/min-fa.html
def minimizar_afd(automata):
        #transitions = {(1, "a"): 3, (1, "b"): 2, (2, "a"): 4, (2, "b"): 1, (3, "a"): 5, (3, "b"): 4, (4, "a"): 4, (4, "b"): 4, (5, "a"): 3, (5, "b"): 2}
        #alphabet = ["a", "b"]
        #partition = [[1, 5], [2, 3, 4]]
        transitions = transitions_by_state_and_label(automata)
        s1 = [state for state in automata.estados_finales]
        s2 = [state for state in automata.estados if state not in s1]
        partition = [s1, s2]
        new_partition = nueva_particion(partition, automata.alfabeto, transitions)
        while not (new_partition == partition):
                #print(partition)
                #print(new_partition)
                partition = new_partition
                new_partition = nueva_particion(partition, automata.alfabeto, transitions)


        #Delete "trap" states and unreachable states from the new partition
        partition = []
        for subset in new_partition:
                #print (subset)
                new_subset = eliminate_death_states(subset, automata.alfabeto, transitions, automata.estados_finales)
                #print (new_subset)
                new_subset = eliminate_unreachable_and_cyclic_states(automata.estado_inicial, new_subset, automata.alfabeto, transitions, automata.estados, automata.estados_finales)
                #print (new_subset)

                if len(new_subset) > 0:
                        partition.append(new_subset)


        #Generate the reduce automat transitions
        transitions_dicc = partition_transitions(partition, automata.alfabeto, transitions)
        new_transitions = []
        new_states = []
        for key, value in transitions_dicc.items():
                #transition == (orig, dest)
                #labels == (label1, label2, label3)
                orig_state = key[0]
                label = key[1]
                dest_state = value
                new_transitions.append([orig_state, label, dest_state])
                if not(orig_state in new_states):
                    new_states.append(orig_state)
                if not(dest_state in new_states):
                    new_states.append(dest_state)
        new_states.sort()

        #Generate min-automat init state
        new_init_state = representative_set(partition, automata.estado_inicial)

        #Generate min-automat final states
        new_final_states = []
        #print("automata.estados_finales" + str(automata.estados_finales))
        for final in automata.estados_finales:
            new_final = representative_set(partition, final)
            if not(new_final == -1) and not(new_final in new_final_states):
                new_final_states.append(new_final)


        min_afd = Automata(new_states, automata.alfabeto, new_init_state, new_final_states, new_transitions)
        return min_afd



def nueva_particion (partition, alphabet, transitions):
    #print(partition)
    new_partition = partition
    for symbol in alphabet:
        #print ("symbol: " + str(symbol))
        condition1 = True
        while condition1:
            partition = new_partition
            index = 0
            condition2 = (index < len(partition))

            while condition2:
                subset = partition[index]
                prefix_partition = partition[0:index]
                suffix_partition = partition[index+1:len(partition)]
                disjoint_subset  = disjoin(prefix_partition, subset, suffix_partition, symbol, transitions)
                index += 1
                condition2 = ([subset] == disjoint_subset and index < len(partition))

            new_partition = prefix_partition + disjoint_subset + suffix_partition
            condition1 = not (new_partition == partition)
            #print("partition: " + str(partition))
            #print("new_partition: " + str(new_partition))



    return new_partition



def disjoin(prefix_set, subset, suffix_set, symbol, transitions):
    aux_partition = []
    states_by_representative = {}
    #print("====== INPUT ======")
    #print("symbol: " + symbol)
    #print("transitions: " + str(transitions))
    #print("prefix: " + str(prefix_set))
    #print("subset: " + str(subset))
    #print("suffix: " + str(suffix_set))
    for state in subset:
        option = 0
        representative_set_index = -1


        if (state, symbol) in transitions:
                while (option < 3) and representative_set_index == -1:
                    if option == 0:
                        #Check if representative set is in the prefix
                        representative_set_index = choose_representatives(prefix_set,  state, symbol, transitions)
                    elif option == 1:
                        #Check if representative set is in the suffix
                        representative_set_index = choose_representatives(suffix_set, state, symbol, transitions)
                    elif option == 2:
                        #Check if representative set is in the aux_partition (if not, must add a representative)
                        representative_set_index = choose_representatives(aux_partition, state, symbol, transitions)

                    if (representative_set_index == -1):
                        option += 1
        else:
                representative_set_index = -1


        if representative_set_index == -1:
            #No hay un subconjunto en el prefijo, el sufijo o la nueva particion de subset
            #que es representativo del elemento
            aux_partition.append([state])
            representative_set_index = len(aux_partition)

        #Id offset
        if option == 1:
            representative_set_index += len(prefix_set)
        elif option == 2:
            representative_set_index += len(prefix_set) + len(suffix_set)


        if not(representative_set_index in states_by_representative):
            states_by_representative[representative_set_index] = []

        states_by_representative[representative_set_index].append(state)

        #print("Option: " + str(option))
        #print("representative_set_index: " + str(representative_set_index))
        #print("states_by_representative: " + str(states_by_representative))
        sub_partition = []
        for index, states in states_by_representative.items():
            sub_partition.append(states)

    #print("====== OUTPUT ======")
    #print("prefix: " + str(prefix_set))
    #print("sub_partition: " + str(sub_partition))
    #print("suffix: " + str(suffix_set))
    return sub_partition


def is_in_subset(subset, alphabet, state, transitions):
	in_subset = True
	for symbol in alphabet:
		in_subset = in_subset and (transitions[(state, symbol)] in subset)

	return in_subset

def eliminate_death_states(subset, alphabet, transitions, terminal_states):
    result = []
    while len(subset) > 0:
        state = subset.pop(0)
        if not(is_death_state(state, alphabet, transitions, terminal_states)):
            result.append(state)

    return result

def eliminate_unreachable_and_cyclic_states(init_state, subset, alphabet, transitions, states, terminal_states):
    result = []
    while len(subset) > 0:
        state = subset.pop(0)
        if n_recheable(init_state, state, alphabet, transitions, len(states)):
            ##Si es alcanzable, me fijo si desde ese nodo puedo llegar a algun terminal
            for terminal in terminal_states:
                if n_recheable(state, terminal, alphabet, transitions, len(states)) and not (state in result):
                    result.append(state)
    return result


def is_death_state(state, alphabet, transitions, terminal_states):
    another_state = False
    for symbol in alphabet:
        if (state, symbol) in transitions:
            another_state = another_state or (transitions[(state, symbol)] != state)

    return not(another_state) and not(state in terminal_states)

def choose_representatives(partition, state, symbol, transitions):
    index = 0
    found = False
    while index < len(partition) and not(found):
        subset = partition[index]
        #Tomamos solo un elemento representativo
        representative = subset[0]
        #print(representative)
        #print(transitions)
        #print(state)
        #print(transitions[(state,symbol)])
        if (representative,symbol) in transitions:
            if not(transitions[(state,symbol)] == transitions[(representative,symbol)]):
                index += 1
            else:
                found = True
        else:
            index += 1
    if not(found):
        index = -1

    return index

#The representative of a disjoint set is the disjoint set index in the
#new partition
def representative_set(partition, state):
    index = 0
    found = False
    while index < len(partition) and not(found):
        subset = partition[index]
        if not(state in subset):
            index += 1
        else:
            found = True


    if not(found):
        index = -1

    return index


def partition_transitions(partition, alphabet, transitions):
    new_transitions = {}
    #print("transitions: " + str(transitions))
    #print("partition: " + str(partition))
    for subset in partition:
        #print(str(subset))
        for state in subset:
            #print(str(state))
            for symbol in alphabet:
                if (state, symbol) in transitions:
                    #Solo si existia originalmente la transicion
                    orig_state = representative_set(partition, state)
                    #print("state: " + str(state) + ", orig_state: " + str(orig_state))
                    #print("transitions: " + str(transitions))
                    #print("(state, symbol)" + str( (state, symbol) ) )
                    #print("transitions[(state, symbol)]" + str(transitions[(state, symbol)]))
                    dest_state = representative_set(partition, transitions[(state, symbol)])
                    if dest_state > -1:
                        #print("transitions[(state, symbol)]: " + str(transitions[(state, symbol)]) + ", dest_state: " + str(dest_state))
                        new_transitions[(orig_state, symbol)] = dest_state

    return new_transitions

def n_recheable(orig_state, dest_state, alphabet, transitions, n):
    recheable = (orig_state == dest_state)
    if n > 0:
        for symbol in alphabet:
            if (orig_state, symbol) in transitions:
                #print("(orig_state, symbol)" + str((orig_state, symbol)))
                next_state = transitions[(orig_state, symbol)]
                #print("next_state" + str(next_state))
                recheable = recheable or (n_recheable(next_state, dest_state, alphabet, transitions, n-1))
    return recheable
