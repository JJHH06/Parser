import sys
from ExtendedAutomata import *
import copy
import os
from YaprScanner import yapr_file_simulation
from Automata import Automata, draw_automata
from GrammarAutomata import *
import pandas as pd



def clean_yapr_comments(raw_input):
    clean_string = ''
    can_append = True
    i = 0
    while i < len(raw_input):
        if raw_input[i] == '/':
            if (i+1 < len(raw_input) and raw_input[i+1] == '*'):
                can_append = False
                i += 2  # skip over the comment start
                continue
        elif raw_input[i] == '*':
            if (i+1 < len(raw_input) and raw_input[i+1] == '/'):
                can_append = True
                i += 2  # skip over the comment end
                continue
        if can_append:
            clean_string += raw_input[i]
            i += 1
        else:
            i += 1
    return clean_string


def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def simulationTable(automata:Automata, input_simbols:list(), productions:list(), action_table:list(), goto_table: list()):
    stack = [automata.initial_state]
    symbols = []
    input = input_simbols+ [('TOKEN', '$')]
    action = None

    stack_list = [ copy.deepcopy(stack)]
    symbols_list = [ copy.deepcopy(symbols)]
    input_list = [ copy.deepcopy(input)]
    action_list = [ copy.deepcopy(action)]

    i = 0
    while True:
        s = stack[-1] # numero de estado al tope del stack
        a = input[0] # primer simbolo de la entrada
        if a[1] not in action_table[s].keys():
            print('REJECTED yapr and yalex files mismatch')
            break
        elif action_table[s][a[1]] is None:
            print('REJECTED')
            break
        elif action_table[s][a[1]][0] == 'shift':
            action = action_table[s][a[1]]
            stack.append(action_table[s][a[1]][1])
            symbols.append(input.pop(0))
            #agregar a historial
            stack_list.append(copy.deepcopy(stack))
            symbols_list.append(copy.deepcopy(symbols))
            input_list.append(copy.deepcopy(input))
            action_list.append(copy.deepcopy(action))
        elif action_table[s][a[1]][0] == 'reduce':
            r = len(productions[action_table[s][a[1]][1]][1]) #productions[[s][a[1]][1]][0] es el que debo agregar
            for _ in range(r):
                stack.pop()
                symbols.pop()
            stack.append(goto_table[stack[-1]][productions[action_table[s][a[1]][1]][0][1]]) #creo xd verificar
            symbols.append(productions[action_table[s][a[1]][1]][0][0])
            #agregar a historial
            stack_list.append(copy.deepcopy(stack))
            symbols_list.append(copy.deepcopy(symbols))
            input_list.append(copy.deepcopy(input))
            action_list.append(copy.deepcopy(action))
        elif action_table[s][a[1]][0] == 'accept':
            print('ACCEPT')
            break
        else:
            print('REJECTED')
            break




def calculate_follow(non_terminal:tuple, productions:list, follow_table:dict, first_table:dict):
    if follow_table[non_terminal[1]] is not None:
        return follow_table[non_terminal[1]]
    else:
        follow_table[non_terminal[1]] = set()
        for production in productions:
            if non_terminal in production[1]:
                index = production[1].index(non_terminal)
                if index == len(production[1])-1:
                    if production[0] != non_terminal:
                        follow_table[non_terminal[1]] = follow_table[non_terminal[1]].union(calculate_follow(production[0], productions, follow_table, first_table))
                else:
                    follow_table[non_terminal[1]] = follow_table[non_terminal[1]].union(calculate_first(production[1][index+1], productions, first_table))
        return follow_table[non_terminal[1]]



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


def calculate_first(grammar_symbol, productions, first_table):
    if grammar_symbol[0] == 'TOKEN':
        return set([grammar_symbol[1]])
    elif grammar_symbol[0] == 'NON_TERMINAL':
        if first_table[grammar_symbol[1]] is not None:
            return first_table[grammar_symbol[1]]
        else:
            first_table[grammar_symbol[1]] = set()
            for production in productions:
                if production[0][1] == grammar_symbol[1]:
                    first_table[grammar_symbol[1]] = first_table[grammar_symbol[1]].union(calculate_first(production[1][0], productions, first_table))
            return first_table[grammar_symbol[1]]
    elif grammar_symbol[0] == 'EPSILON':
        return set('ε')
    else:
        return set()
    
def get_production_index(production, productions):
    for i in range(len(productions)):
        if productions[i][0] == production[0] and productions[i][1] == production[1]:
            return i
    return None


def calculate_reduce_table(action_table:list, equivalent_states:list, productions:list, follow_table:set):
    for x in range(len(equivalent_states)):
        for item in equivalent_states[x]:
            if item[2] == len(item[1]): #significa que el puntito esta apuntando afuera de la produccion
                to_state = get_production_index(item, productions)
                for terminal in follow_table[item[0][1]]:
                    if action_table[x][terminal] is not None:
                        if action_table[x][terminal][0] == 'shift':
                            print('ERROR: Shift-Reduce conflict:')
                            print(action_table[x][terminal])
                            print(('reduce', to_state))
                            exit()
                        elif action_table[x][terminal] != ('accept', None):
                            action_table[x][terminal] = ('reduce', to_state)
                    else:
                        action_table[x][terminal] = ('reduce', to_state)
            
    return action_table



def main():
    yapr_file_path = "lab-f.yalp" #TODO: remove this line
    yalex_file_path = 'lab-f.yal'# TODO: remove this line
    input_file_path = 'test.txt' # TODO: remove this line
    #check if arguments are more than 1 if not exit and print error
    # if len(sys.argv) < 2:
    #     print('Error: No input file')
    #     exit()
    


    

    extended_automata = ExtendedAutomata([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], {' ', 'p', 'c', 'x', 'H', 'a', 'e', 'y', 'r', ';', '\t', 'C', 'u', 'Z', 'E', 'O', 'w', 'j', 'L', '\n', 'n', 'm', 'g', 'R', 'N', 'S', 'A', 'o', 'G', 'M', 'd', 'B', 'f', 'J', 'K', 'k', 'P', 'X', 'i', 'v', 's', 'U', 'b', 'Y', 'F', 'T', '%', ':', 'l', 'h', 'q', 'W', 'I', 'V', 't', 'D', '|', 'z', 'Q'}, [((0, ' '), 1), ((0, 'p'), 2), ((0, 'c'), 2), ((0, 'x'), 2), ((0, 'H'), 3), ((0, 'a'), 2), ((0, 'e'), 2), ((0, 'y'), 2), ((0, 'r'), 2), ((0, ';'), 4), ((0, '\t'), 1), ((0, 'C'), 3), ((0, 'u'), 2), ((0, 'Z'), 3), ((0, 'E'), 3), ((0, 'O'), 3), ((0, 'w'), 2), ((0, 'j'), 2), ((0, 'L'), 3), ((0, '\n'), 1), ((0, 'n'), 2), ((0, 'm'), 2), ((0, 'g'), 2), ((0, 'R'), 3), ((0, 'N'), 3), ((0, 'S'), 3), ((0, 'A'), 3), ((0, 'o'), 2), ((0, 'G'), 3), ((0, 'M'), 3), ((0, 'd'), 2), ((0, 'B'), 3), ((0, 'f'), 2), ((0, 'J'), 3), ((0, 'K'), 3), ((0, 'k'), 2), ((0, 'P'), 3), ((0, 'X'), 3), ((0, 'i'), 2), ((0, 'v'), 2), ((0, 's'), 2), ((0, 'U'), 3), ((0, '|'), 5), ((0, 'b'), 2), ((0, 'Y'), 3), ((0, 'F'), 3), ((0, 'T'), 3), ((0, '%'), 6), ((0, ':'), 7), ((0, 'l'), 2), ((0, 'h'), 2), ((0, 'q'), 2), ((0, 'W'), 3), ((0, 'I'), 3), ((0, 't'), 2), ((0, 'V'), 3), ((0, 'D'), 3), ((0, 'z'), 2), ((0, 'Q'), 3), ((1, ' '), 1), ((1, '\t'), 1), ((1, '\n'), 1), ((2, 'p'), 2), ((2, 'c'), 2), ((2, 'x'), 2), ((2, 'a'), 2), ((2, 'e'), 2), ((2, 'y'), 2), ((2, 'r'), 2), ((2, 'u'), 2), ((2, 'w'), 2), ((2, 'j'), 2), ((2, 'n'), 2), ((2, 'm'), 2), ((2, 'g'), 2), ((2, 'o'), 2), ((2, 'd'), 2), ((2, 'f'), 2), ((2, 'k'), 2), ((2, 'i'), 2), ((2, 'v'), 2), ((2, 's'), 2), ((2, 'b'), 2), ((2, 'l'), 2), ((2, 'h'), 2), ((2, 'q'), 2), ((2, 't'), 2), ((2, 'z'), 2), ((3, 'H'), 3), ((3, 'C'), 3), ((3, 'Z'), 3), ((3, 'E'), 3), ((3, 'O'), 3), ((3, 'L'), 3), ((3, 'R'), 3), ((3, 'N'), 3), ((3, 'S'), 3), ((3, 'A'), 3), ((3, 'G'), 3), ((3, 'M'), 3), ((3, 'B'), 3), ((3, 'J'), 3), ((3, 'K'), 3), ((3, 'P'), 3), ((3, 'X'), 3), ((3, 'U'), 3), ((3, 'Y'), 3), ((3, 'F'), 3), ((3, 'T'), 3), ((3, 'W'), 3), ((3, 'I'), 3), ((3, 'V'), 3), ((3, 'D'), 3), ((3, 'Q'), 3), ((6, 't'), 8), ((8, 'o'), 9), ((9, 'k'), 10), ((10, 'e'), 11), ((11, 'n'), 12)], 0, [1, 2, 3, 4, 5, 7, 12], [0, 1, 2, 6, 4, 5, 3])
    #yapr_file_path = sys.argv[1]
    
    file_content = read_file(yapr_file_path)
    file_tokens = yapr_file_simulation(extended_automata, clean_yapr_comments(file_content))
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

    # print("\nTERMINALS:")
    # print(terminals)

    # print("\nNON TERMINALS:")
    # print(non_terminals)

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

    file_name = os.path.basename(yapr_file_path)
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


    initial_non_terminal = productions[0][0][1]

    # calculo de FIRST
    first_table = { initial_non_terminal: None}
    for n in non_terminals_tokens:
        first_table[n] = None
    
    # el simbolo inicial no tiene first
    first_table[initial_non_terminal] = set()

    for non_terminal_key in non_terminals_tokens:
        calculate_first(('NON_TERMINAL', non_terminal_key), productions, first_table)
    
    # print('\nTable:')
    # print(first_table)

    # calculo de FOLLOW
    follow_table = { initial_non_terminal: set(['$'])}
    for n in non_terminals_tokens:
        follow_table[n] = None

    for non_terminal_key in non_terminals_tokens:
        calculate_follow(('NON_TERMINAL', non_terminal_key), productions, follow_table, first_table)

    # print('\nFollow Table:')
    # print(follow_table)

    # calculo de ACTION con reduce
    # print('\nAction Table:')
    calculate_reduce_table(action_table, equival_states, productions, follow_table)

    # for i in range(len(action_table)):
    #     print(action_table[i])

    
    #para la impresion de la tabla
    joined_parsing_table = pd.concat([pd.DataFrame(action_table), pd.DataFrame(goto_table)], axis=1,keys=['ACTION', 'GOTO'])
    joined_parsing_table.to_csv("./lab_outputs/"+file_name+".parsing_table.csv")

    print('\nParsing Table:')
    print(joined_parsing_table)

    print('\nLexer Scanning:')

    from lexer import Lexer

    #yalex_file_path = sys.argv[2]
    Lexer(read_file(yalex_file_path))

    from Scanner import file_simulation, extended_automata

    test_string = read_file(input_file_path)
    tokenized_yalex_input = file_simulation( extended_automata, test_string)
    print(tokenized_yalex_input)
    parser_token_format = [('TOKEN', n[0]) for n in tokenized_yalex_input]
    
    print('\nParsing shift-reduce simulation:')
    simulationTable(slr_automata, parser_token_format, productions, action_table, goto_table)














if __name__ == "__main__":
    main()