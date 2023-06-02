import sys
from ExtendedAutomata import *
import copy
import os
from Scanner import *
from Automata import Automata, draw_automata
from GrammarAutomata import *



def build_goto_table(tokens:list(), automata:Automata, states_len:int) -> list():
    goto_table = [{i:None for i in tokens } for _ in range(states_len)]
    
    for transition in automata.transitions:
        for non_terminal in tokens:
            if transition[0][1] == non_terminal:
                goto_table[transition[0][0]][non_terminal] = transition[1]
                continue
    return goto_table

def build_action_table_shift(tokens:list(), automata:Automata, states_len:int) -> list():
    extended_tokens = copy.deepcopy(tokens)+['$']
    action_table = [{i:None for i in extended_tokens } for _ in range(states_len)]
    action_table[automata.final_states[0]]['$'] = ('accept', None)
    for transition in automata.transitions:
        for terminal in tokens:
            if transition[0][1] == terminal:
                action_table[transition[0][0]][terminal] = ('shift', transition[1])
                continue
    return action_table


def main():
    extended_automata = ExtendedAutomata([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], {' ', 'p', 'c', 'x', 'H', 'a', 'e', 'y', 'r', ';', '\t', 'C', 'u', 'Z', 'E', 'O', 'w', 'j', 'L', '\n', 'n', 'm', 'g', 'R', 'N', 'S', 'A', 'o', 'G', 'M', 'd', 'B', 'f', 'J', 'K', 'k', 'P', 'X', 'i', 'v', 's', 'U', 'b', 'Y', 'F', 'T', '%', ':', 'l', 'h', 'q', 'W', 'I', 'V', 't', 'D', '|', 'z', 'Q'}, [((0, ' '), 1), ((0, 'p'), 2), ((0, 'c'), 2), ((0, 'x'), 2), ((0, 'H'), 3), ((0, 'a'), 2), ((0, 'e'), 2), ((0, 'y'), 2), ((0, 'r'), 2), ((0, ';'), 4), ((0, '\t'), 1), ((0, 'C'), 3), ((0, 'u'), 2), ((0, 'Z'), 3), ((0, 'E'), 3), ((0, 'O'), 3), ((0, 'w'), 2), ((0, 'j'), 2), ((0, 'L'), 3), ((0, '\n'), 1), ((0, 'n'), 2), ((0, 'm'), 2), ((0, 'g'), 2), ((0, 'R'), 3), ((0, 'N'), 3), ((0, 'S'), 3), ((0, 'A'), 3), ((0, 'o'), 2), ((0, 'G'), 3), ((0, 'M'), 3), ((0, 'd'), 2), ((0, 'B'), 3), ((0, 'f'), 2), ((0, 'J'), 3), ((0, 'K'), 3), ((0, 'k'), 2), ((0, 'P'), 3), ((0, 'X'), 3), ((0, 'i'), 2), ((0, 'v'), 2), ((0, 's'), 2), ((0, 'U'), 3), ((0, '|'), 5), ((0, 'b'), 2), ((0, 'Y'), 3), ((0, 'F'), 3), ((0, 'T'), 3), ((0, '%'), 6), ((0, ':'), 7), ((0, 'l'), 2), ((0, 'h'), 2), ((0, 'q'), 2), ((0, 'W'), 3), ((0, 'I'), 3), ((0, 't'), 2), ((0, 'V'), 3), ((0, 'D'), 3), ((0, 'z'), 2), ((0, 'Q'), 3), ((1, ' '), 1), ((1, '\t'), 1), ((1, '\n'), 1), ((2, 'p'), 2), ((2, 'c'), 2), ((2, 'x'), 2), ((2, 'a'), 2), ((2, 'e'), 2), ((2, 'y'), 2), ((2, 'r'), 2), ((2, 'u'), 2), ((2, 'w'), 2), ((2, 'j'), 2), ((2, 'n'), 2), ((2, 'm'), 2), ((2, 'g'), 2), ((2, 'o'), 2), ((2, 'd'), 2), ((2, 'f'), 2), ((2, 'k'), 2), ((2, 'i'), 2), ((2, 'v'), 2), ((2, 's'), 2), ((2, 'b'), 2), ((2, 'l'), 2), ((2, 'h'), 2), ((2, 'q'), 2), ((2, 't'), 2), ((2, 'z'), 2), ((3, 'H'), 3), ((3, 'C'), 3), ((3, 'Z'), 3), ((3, 'E'), 3), ((3, 'O'), 3), ((3, 'L'), 3), ((3, 'R'), 3), ((3, 'N'), 3), ((3, 'S'), 3), ((3, 'A'), 3), ((3, 'G'), 3), ((3, 'M'), 3), ((3, 'B'), 3), ((3, 'J'), 3), ((3, 'K'), 3), ((3, 'P'), 3), ((3, 'X'), 3), ((3, 'U'), 3), ((3, 'Y'), 3), ((3, 'F'), 3), ((3, 'T'), 3), ((3, 'W'), 3), ((3, 'I'), 3), ((3, 'V'), 3), ((3, 'D'), 3), ((3, 'Q'), 3), ((6, 't'), 8), ((8, 'o'), 9), ((9, 'k'), 10), ((10, 'e'), 11), ((11, 'n'), 12)], 0, [1, 2, 3, 4, 5, 7, 12], [0, 1, 2, 6, 4, 5, 3])
    # ruta_archivo = sys.argv[1]
    ruta_archivo = "slr-1.yalp"
    file_content = read_file(ruta_archivo)
    file_tokens = file_simulation(extended_automata, clean_comments(file_content))
    productions = []

    # NON TERMINAL, [ELEMENT1, ELEMENT2, ...],-1
    current_production = [None, [], -1]

    #ELEMENT has the following structure (TYPE, VALUE)

    is_declaring_tokens = False
    is_delcaring_productions = True
    terminals = []
    non_terminals = []
    
    for token in file_tokens:

        if token[0] == 'TOKEN_DECLARATION':
            is_declaring_tokens = True
        elif token[0] == 'TOKEN':
            if is_declaring_tokens:
                if token not in terminals:
                    terminals.append(token)
            else:
                # IF FOUND IN PRODUCTION
                current_production[1].append(token)
        elif token[0] == 'NON_TERMINAL':
            if is_delcaring_productions:
                current_production[0] = token
                if token not in non_terminals:
                    non_terminals.append(token)
            else:
                # IF inside production
                current_production[1].append(token)
                if token not in non_terminals:
                    non_terminals.append(token)

        elif token[0] == 'PROD_ARROW':
            is_declaring_tokens = False
            is_delcaring_productions = False #este tiene que cambiar con el EOP
        elif token[0] == 'OR':
            # IF inside production
            productions.append(current_production)
            current_production = [current_production[0], [], -1]
        elif token[0] == 'EOP':
            # IF inside production
            productions.append(current_production)
            current_production = [None, [], -1]
            is_delcaring_productions = True
    #Now before we conclude we need to augment the grammar

    #Initial non terminal
    prime_init_exp = (productions[0][0][0], productions[0][0][1]+"_PRIME")

    #Pending to solve
    #non_terminals.add(prime_init_exp)

    #added new production at start
    productions = [[prime_init_exp, [copy.deepcopy(productions[0][0])], -1]] + copy.deepcopy(productions)



    print("\nPRODUCTIONS:")
    for production in productions:
        print(production[0][1], '->', [n[1] for n in production[1]])

    print("\nTERMINALS:")
    print(terminals)

    print("\nNON TERMINALS:")
    print(non_terminals)

    alphabet = non_terminals + terminals
    alphabet = copy.deepcopy(alphabet)


    #CONVENCION
    #primer indice referencia a la posicion de la posicion de la produccion
    #segundo item a la posicion del elemento dentro de la produccion

    # Production structure:
    # NON TERMINAL, [ELEMENT1, ELEMENT2, ...],-1
    #ELEMENT has the following structure (TYPE, VALUE)

    # no terminales son: NON_TERMINAL
    # terminales son: TOKEN



    
    equival_states, slr_automata = grammar_subset_construction(productions, alphabet)

    # for every state in equivalent states print its productions 
    # for state in range(len(equival_states)):
    #     print("\nSTATE: ", state)
    #     for production in equival_states[state]:
    #         print(production[0][1], '->', [n[1] for n in production[1]], production[2])

    file_name = os.path.basename(ruta_archivo)
    with open("./lab_outputs/"+file_name+".legend.txt", 'w') as file:
        for state in range(len(equival_states)):
            file.write("\nSTATE: {}\n".format(state))
            for production in equival_states[state]:
                file.write("{} -> {} {}\n".format(production[0][1], [n[1] for n in production[1]], production[2]))

    draw_automata(slr_automata, "./lab_outputs/"+file_name+".automata", file_name)
    #CONVENCION
    #primer indice referencia a la posicion de la posicion de la produccion
    #segundo item a la posicion del elemento dentro de la produccion

    # Production structure:
    # NON TERMINAL, [ELEMENT1, ELEMENT2, ...],-1
    #ELEMENT has the following structure (TYPE, VALUE)

    # no terminales son: NON_TERMINAL
    # terminales son: TOKEN

    # build a dictionary of the productions
    # equival_states

    STATES_LEN = len(equival_states)
    non_terminals_tokens = [n[1] for n in non_terminals] 
    terminals_tokens = [t[1] for t in terminals]
    
    goto_table = build_goto_table(non_terminals_tokens,slr_automata, len(equival_states))
    action_table = build_action_table_shift(terminals_tokens, slr_automata, len(equival_states))
    print('\nTable: ')
    for ac in action_table:
        print(ac)














if __name__ == "__main__":
    main()