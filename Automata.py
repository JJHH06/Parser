# Created by: José Hurtarte
# Created on: 25/02/2023
# Last modified on: 19/03/2023
# Description: Automata module and class


from graphviz import Digraph
import copy

class Automata:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states
        self.current_simulation_state = -1

    def state_move(self, state, symbol):
        return [transition[1] for transition in self.transitions if transition[0] == (state, symbol)]
    
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


def dfa_simulation(automata: Automata, input_string: str):
    current_state = automata.initial_state
    for symbol in input_string:
        next_state = automata.state_move(current_state, symbol)
        if len(next_state) == 0:
            return False
        current_state = next_state[0]
    return current_state in automata.final_states
    

def clean_transitions(automata):
    ignored_chars = ['|', '(', ')', '*', '+', '?']
    new_transitions = []
    new_alphabet = set()
    for transition in automata.transitions:
        if len(transition[0][1])==2 and transition[0][1][0] == '\\' and transition[0][1][1] in ignored_chars:
            new_transitions.append(((transition[0][0], transition[0][1][1]), transition[1]))
        else:
            new_transitions.append(transition)
    for token in automata.alphabet:
        if len(token)== 2 and token[0] == '\\' and token[1] in ignored_chars:
            new_alphabet.add(token[1])
        else:
            new_alphabet.add(token)
    automata.alphabet = new_alphabet
    automata.transitions = new_transitions

def simplification_automata(automata: Automata):
    new_automata = copy.deepcopy(automata)
    prev_equivalent_states = []
    not_final_states = {state for state in new_automata.states if state not in new_automata.final_states}
    if len(not_final_states) != 0:
        prev_equivalent_states.append(not_final_states)
    prev_equivalent_states.append(set(new_automata.final_states))
    has_minimization_converged = False
    while not has_minimization_converged:
        new_equivalent_states = []
        simplified_global_transitions = []

        for i in range(len(prev_equivalent_states)):
            decomposed_states = []
            decomposed_states_transitions = []
            # cada indice j es un estado de uno de los conjuntos de estados equivalentes previos
            for j in prev_equivalent_states[i]:
                char_transitions = set()
                for token in new_automata.alphabet:
                    state_transition = new_automata.state_move(j, token)
                    if len(state_transition) != 0:
                        if len(state_transition)>1:
                            raise Exception("Automata no determinista")
                        state_moved_to  = state_transition[0] #esto nos dice en el automata pasado en donde es que se mueve
                        index_in_prev_equivalent_states = [k for k, my_set in enumerate(prev_equivalent_states) if state_moved_to in my_set][0] #esto nos dice en los equivalentes a que posicion se mueve
                        char_transitions.add(((i, token), index_in_prev_equivalent_states))
                if char_transitions not in decomposed_states_transitions:
                    decomposed_states_transitions.append(char_transitions)
                    decomposed_states.append({j})
                else:
                    decomposed_states[decomposed_states_transitions.index(char_transitions)].add(j)
            new_equivalent_states.extend(decomposed_states)
            simplified_global_transitions.extend(decomposed_states_transitions)
            

        has_minimization_converged = prev_equivalent_states == new_equivalent_states
        prev_equivalent_states = new_equivalent_states.copy()
        
    
    final_states = []
    simplified_states = []
    for index, state in enumerate(prev_equivalent_states):
        simplified_states.append(index)
        for final_state in new_automata.final_states:
            if final_state in state:
                final_states.append(index)
                break
    initial_state = [k for k, my_set in enumerate(prev_equivalent_states) if new_automata.initial_state in my_set][0]

    return Automata(simplified_states, new_automata.alphabet, [item for sublist in simplified_global_transitions for item in sublist], initial_state, final_states)


def nfa_simulation(automata: Automata, input_string: str):
    current_states = automata.epsilon_closure(automata.initial_state)
    for symbol in input_string:
        next_states = []
        for state in current_states:
            next_states.extend(automata.state_move(state, symbol))
        current_states = []
        for state in next_states:
            current_states.extend(automata.epsilon_closure(state))
    return any([state in automata.final_states for state in current_states])

def dfa_simulation(automata: Automata, input_string: str):
    current_state = automata.initial_state
    for symbol in input_string:
        next_state = automata.state_move(current_state, symbol)
        if len(next_state) == 0:
            return False
        current_state = next_state[0]
    return current_state in automata.final_states
    
def deterministic_automata(automata: Automata):
    new_automata = copy.deepcopy(automata)
    equivalent_states = []

    initial_state = new_automata.epsilon_closure(new_automata.initial_state)
    equivalent_states.append(set(initial_state))
    equivalent_transitions = []

    deterministic_alphabet = new_automata.alphabet.copy()
    if 'ε' in deterministic_alphabet:
        deterministic_alphabet.remove('ε')

    for state in equivalent_states:
        for symbol in deterministic_alphabet:
            next_states = []
            for nfa_state in state:
                next_states.extend(new_automata.state_move(nfa_state, symbol))
            next_states = set(next_states)
            
            temp_next_states = []
            for nfa_state in next_states:
                temp_next_states.extend(new_automata.epsilon_closure(nfa_state))
            next_states = set(temp_next_states)

            if len(next_states) != 0:
                if next_states not in equivalent_states:
                    equivalent_states.append(next_states)
                equivalent_transitions.append(((equivalent_states.index(state), symbol), equivalent_states.index(next_states)))

    equivalent_final_states = []
    for i in range(len(equivalent_states)):
        for legacy_final_state in new_automata.final_states:
            if legacy_final_state in equivalent_states[i]:
                equivalent_final_states.append(i)
                break
    return Automata([i for i in range(len(equivalent_states))], deterministic_alphabet, equivalent_transitions, 0, equivalent_final_states)



def direct_construction(followpos_table, initial_state, final_states, alphabet_list):
    deterministic_alphabet  = set(alphabet_list)
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
    return Automata([i for i in range(len(equivalent_states))], deterministic_alphabet, direct_transitions, 0, equivalent_final_states)



# ensures that all the states are serial and no state is missing
def embellish_automata(automata):
    state_map = {prev_state: new_state for new_state, prev_state in enumerate(automata.states)}
    states = [state_map[state] for state in automata.states]
    initial_state = state_map[automata.initial_state]
    
    final_states = [state_map[state] for state in automata.final_states]
    initial_state_map = {initial_state: 0, 0: initial_state}
    final_state_map = {final_states[i-1]:len(states)-i for i in range(1, len(final_states)+1)}
    transitions = []
    for transition in automata.transitions:
        new_transition = ((state_map[transition[0][0]], transition[0][1]), state_map[transition[1]])
        if new_transition[0][0] in initial_state_map:
            new_transition = ((initial_state_map[new_transition[0][0]], new_transition[0][1]), new_transition[1])
        if new_transition[1] in initial_state_map:
            new_transition = (new_transition[0], initial_state_map[new_transition[1]])
        if new_transition[0][0] in final_state_map:
            new_transition = ((final_state_map[new_transition[0][0]], new_transition[0][1]), new_transition[1])
        if new_transition[1] in final_state_map:
            new_transition = (new_transition[0], final_state_map[new_transition[1]])
        transitions.append(new_transition)
    initial_state = initial_state_map[initial_state]
    return Automata(states, automata.alphabet, transitions, initial_state, final_states)

# draws the automata using graphviz
def draw_automata(automata, filename = 'NFA', title = ''):
    f = Digraph('finite_state_machine', format='png')
    f.attr(rankdir='LR')
    f.attr('node', shape='circle') #makes all nodes circles
    # inner_nodes is equal to all the nodes that are not the initial state or the final states
    inner_nodes = [state for state in automata.states if state not in automata.final_states and state != automata.initial_state]
    f.node('start_mark', shape='point', style='invis')
    f.node(str(automata.initial_state))
    f.edge('start_mark', str(automata.initial_state))
    for operand in automata.alphabet:
        next_states = [transition[1] for transition in automata.transitions if transition[0] == (automata.initial_state, operand)]
        for next_state in next_states:
            f.edge(str(automata.initial_state), str(next_state), label=repr(operand))
    for state in inner_nodes:
        f.node(str(state))
        for operand in automata.alphabet:
            next_states = [transition[1] for transition in automata.transitions if transition[0] == (state, operand)]
            for next_state in next_states:
                f.edge(str(state), str(next_state), label=repr(operand))
    for state in automata.final_states:
        f.node(str(state), shape='doublecircle')
        if state != automata.initial_state:
            for operand in automata.alphabet:
                next_states = [transition[1] for transition in automata.transitions if transition[0] == (state, operand)]
                for next_state in next_states:
                    f.edge(str(state), str(next_state), label=repr(operand))
    f.attr(label=title)
    f.render(filename, format='png')


# operand thomspon automata
def operand_automata(subexpression, current_state):
    states = [current_state, current_state+1]
    alphabet = {subexpression}
    initial_state = current_state
    final_states = [current_state+1]
    transitions = [((current_state, subexpression), current_state+1)]
    return Automata(states, alphabet, transitions, initial_state, final_states)

def or_automata(right_automata, left_automata, current_state):
    # union of the states of the two automata
    states = left_automata.states + right_automata.states
    states.extend([current_state, current_state+1])
    initial_state = current_state
    final_states = [current_state+1]
    # union of the alphabet of the two automata
    alphabet = left_automata.alphabet.union(right_automata.alphabet)
    alphabet.add('ε')
    # union of the transitions of the two automata
    transitions = left_automata.transitions + right_automata.transitions
    # add transitions to the new initial state
    transitions.append(((current_state, 'ε'), left_automata.initial_state))
    transitions.append(((current_state, 'ε'), right_automata.initial_state))
    # add transitions from the final states of the two automata to the new final state
    for state in left_automata.final_states:
        transitions.append(((state, 'ε'), current_state+1))
    for state in right_automata.final_states:
        transitions.append(((state, 'ε'), current_state+1))
    return Automata(states, alphabet, transitions, initial_state, final_states)

def concatenation_automata(right_automata, left_automata):
    # union of the states of the two automata
    states = [x for x in left_automata.states if x not in left_automata.final_states] + right_automata.states

    initial_state = left_automata.initial_state
    final_states = right_automata.final_states
    alphabet = left_automata.alphabet.union(right_automata.alphabet)
    transitions = left_automata.transitions + right_automata.transitions

    for i in range(len(transitions)):
        if transitions[i][1] in left_automata.final_states:
            transitions[i] = ((transitions[i][0][0], transitions[i][0][1]), right_automata.initial_state)
    return Automata(states, alphabet, transitions, initial_state, final_states)

def kleene_automata(automata, current_state):
    states = automata.states
    states.extend([current_state, current_state+1])
    initial_state = current_state
    final_states = [current_state+1]
    alphabet = automata.alphabet
    alphabet.add('ε')
    transitions = automata.transitions
    # transition the final states of the automata to the initial state
    for state in automata.final_states:
        transitions.append(((state, 'ε'), automata.initial_state))
    # transition from the initial state to the initial state of the automata
    transitions.append(((current_state, 'ε'), automata.initial_state))
    # transition from the final states of the automata to the final state
    for state in automata.final_states:
        transitions.append(((state, 'ε'), current_state+1))
    # transition from the initial state to the final state
    transitions.append(((current_state, 'ε'), current_state+1))
    return Automata(states, alphabet, transitions, initial_state, final_states)

def question_automata(automata, current_state):
    epsilon_automata = operand_automata('ε', current_state)
    return or_automata(epsilon_automata, automata, current_state+2)

def automata_state_change(automata):
    automata_copy = copy.deepcopy(automata)
    state_offset = max(automata.states)+1
    automata_copy.states = [state + state_offset for state in automata_copy.states]
    automata_copy.initial_state += state_offset
    automata_copy.final_states = [state + state_offset for state in automata_copy.final_states]
    automata_copy.transitions = [((transition[0][0] + state_offset, transition[0][1]), transition[1] + state_offset) for transition in automata_copy.transitions]
    return automata_copy, state_offset

def positive_closure_automata(automata, current_state):
    automata_copy, state_offset = automata_state_change(automata)
    return concatenation_automata(kleene_automata(automata_copy, current_state+state_offset), automata), state_offset+2

def build_automata(postfix_expression):
    unary_operators = ['*','+','?']
    binary_operators = ['|','.']
    stack = []
    next_state = 0
    for token in postfix_expression:
        # Checks if token is a valid operand
        if token not in unary_operators and token not in binary_operators:
            stack.append(operand_automata(token, next_state))
            next_state += 2
        #else checks which operator is it
        elif token == '|':
            stack.append(or_automata(stack.pop(), stack.pop(), next_state))
            next_state += 2
        elif token == '.':
            stack.append(concatenation_automata(stack.pop(), stack.pop()))
        elif token == '*':
            stack.append(kleene_automata(stack.pop(), next_state))
            next_state += 2
        elif token == '?':
            stack.append(question_automata(stack.pop(), next_state))
            next_state += 4
        elif token == '+':
            plus_closure_element, state_offset = positive_closure_automata(stack.pop(), next_state)
            stack.append(plus_closure_element)
            next_state += state_offset
    return stack.pop()

