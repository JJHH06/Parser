# Created by: José Hurtarte
# Created on: 23/04/2023
# Last modified on: 23/04/2023
# Description: Extended Automata module and class


from graphviz import Digraph
import copy

class ExtendedAutomata:
    def __init__(self, states, alphabet, transitions, initial_state, final_states, final_states_returns):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states
        self.current_simulation_state = -1
        self.final_states_returns = final_states_returns #deberia ser una lista que nos diga que debe retornar cada uno de los estados finales

    def state_move(self, state, symbol):
        return [transition[1] for transition in self.transitions if transition[0] == (state, symbol)]
    def stringify_constructor(self):
        return f"ExtendedAutomata({self.states}, {self.alphabet}, {self.transitions}, {self.initial_state}, {self.final_states}, {self.final_states_returns})"


    def single_state_move(self, state, symbol):
        for transition in self.transitions:
            if transition[0] == (state, symbol):
                self.current_simulation_state = transition[1]
                return transition[1]
        self.current_simulation_state = -1
        return -1
    def epsilon_closure(self, state):
        closure = [state]
        for closure_state in closure:
            
            for transition in self.transitions:
                if transition[0] == (closure_state, 'ε'):
                    if transition[1] not in closure:
                        closure.append(transition[1])
        return closure
    def reset_simulation(self):
        self.current_simulation_state = self.initial_state
    def simulate(self, symbol):
        if self.current_simulation_state == -1:
            return -1
        next_state = self.single_state_move(self.current_simulation_state, symbol)
        if next_state == -1:
            return -1
        if self.current_simulation_state in self.final_states:
            return 1
        if self.current_simulation_state not in self.final_states:
            return 0
    def get_return(self): #retorna el valor que debe retornar el automata en el estado actual, SOLO FUNCIONA SI EL ESTADO ACTUAL ES UN ESTADO FINAL
        return self.final_states_returns[self.final_states.index(self.current_simulation_state)]



# DIRECT CONSTRUCTION FOR AUTOMATAS WITH RETURNS
def direct_extended_construction(followpos_table, initial_state, final_states, alphabet_list):
    deterministic_alphabet  = set(alphabet_list)
    deterministic_alphabet.remove('DELIMITATOR')
    equivalent_states = [initial_state]
    leaf_positions = {character: [i for i in range(len(alphabet_list)) if alphabet_list[i] == character] for character in deterministic_alphabet}
    direct_transitions = []
    
    
    for state in equivalent_states:
        for symbol in deterministic_alphabet:
            next_states = []
            #cuales de esos son ese char
            next_states = set([nfa_state for nfa_state in state if nfa_state in leaf_positions[symbol]])
            
            temp_next_states = []
            #el followpos
            for nfa_state in next_states:
                temp_next_states.extend(followpos_table[nfa_state])
            next_states = set(temp_next_states)

            if len(next_states) != 0:
                if next_states not in equivalent_states:
                    equivalent_states.append(next_states)
                direct_transitions.append(((equivalent_states.index(state), symbol), equivalent_states.index(next_states)))

    equivalent_final_states = []
    for i in range(len(equivalent_states)):
        for legacy_final_state in final_states:
            if legacy_final_state in equivalent_states[i]:
                equivalent_final_states.append(i)
                break

    return_indexes = [ -1 for _ in range(len(equivalent_final_states))] #por si en dado caso el estado fuera irreconocible sabemos que ocurre

    for i in range(len(equivalent_final_states)):
        for j in reversed(range(len(final_states))):
            if final_states[j] in equivalent_states[equivalent_final_states[i]]:
                return_indexes[i] = j
                # no se le coloca break porque la prioridad es basado en el orden entonces si encuentra varios estados, debe asignar el que este mas cercano al inicio
                # de la lista de estados finales
    
    #TODO: ELIMINAR ESTE PRINT
    print("return_indexes: ", return_indexes)
    print("equivalent_final_states: ", equivalent_final_states)
                
    

    
    return ExtendedAutomata([i for i in range(len(equivalent_states))], deterministic_alphabet, direct_transitions, 0, equivalent_final_states, return_indexes)
