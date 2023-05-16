from ReturnTypes import *

import sys
from ExtendedAutomata import *



def clean_comments(raw_input):
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
    


def match_automata_returns(recognized_type, i):
    if recognized_type is None:
        raise Exception('No type recognized at position', i)
    
    elif recognized_type == 0:
        pass
    elif recognized_type == 1:
         return 'NON_TERMINAL' 
    elif recognized_type == 2:
         return 'TOKEN' 
    elif recognized_type == 3:
         return 'TOKEN_DECLARATION' 
    elif recognized_type == 4:
         return 'OR' 
    elif recognized_type == 5:
         return 'PROD_ARROW' 
    elif recognized_type == 6:
         return 'EOP' 



def file_simulation(extended_automata, test_string):
    recognized_tokens = []
    test_string = test_string + ''
    current_sim_status = 0
    first_recognized_pos = 0
    last_accepted_pos = 0
    reconized_type = None
    extended_automata.reset_simulation()
    FILE_SIZE = len(test_string)
    i = 0
    while i < FILE_SIZE:
        current_sim_status = extended_automata.simulate(test_string[i])
        if current_sim_status == 1:
            last_accepted_pos = i
            reconized_type = extended_automata.get_return()
        elif current_sim_status == -1:
            token = match_automata_returns(reconized_type, i)
            if token is not None:
                recognized_tokens.append((token, test_string[first_recognized_pos:last_accepted_pos+1]))
            if test_string[i] == '':
                break
            extended_automata.reset_simulation()
            first_recognized_pos = i
            last_accepted_pos = i
            reconized_type = None
            continue
        i += 1
    return recognized_tokens



# params:
#   - item: a list of the form [non_terminal, [element0, element1...], index]
#   - productions: list of productions in item format but index is always -1
def grammar_closure(item_list: list, productions):
    items = item_list.copy()
    i = 0
    while i < len(items):
        if items[i][2] < len(items[i][1]) and items[i][1][items[i][2]][0] == 'NON_TERMINAL':
            items = items + [[j[0],j[1],0] for j in productions if j[0] == items[i][1][items[i][2]] and [j[0],j[1],0] not in items]
        i += 1
    return items

# goto without the closure
def grammar_goto( items, symbol ):
    movable_items = [n for n in items if n[2] < len(n[1])]
    goto_items = [i for i in movable_items if i[1][i[2]] == symbol]
    moved_items = [[j[0], j[1], j[2]+1] for j in goto_items]
    return moved_items


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

    #
    #TODO: comment debug
    print(file_tokens)

    is_declaring_tokens = False
    is_delcaring_productions = True
    terminals = set()
    non_terminals = set()
    for token in file_tokens:

        if token[0] == 'TOKEN_DECLARATION':
            is_declaring_tokens = True
        elif token[0] == 'TOKEN':
            if is_declaring_tokens:
                terminals.add(token)
            else:
                # IF FOUND IN PRODUCTION
                current_production[1].append(token)
        elif token[0] == 'NON_TERMINAL':
            if is_delcaring_productions:
                current_production[0] = token
                non_terminals.add(token)
            else:
                # IF inside production
                current_production[1].append(token)
                non_terminals.add(token)

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
    productions = [[prime_init_exp, [productions[0][0]], -1]] + productions



    print("\nPRODUCTIONS:")
    for production in productions:
        print(production[0][1], '->', [n[1] for n in production[1]])

    print("\nTERMINALS:")
    print(terminals)

    print("\nNON TERMINALS:")
    print(non_terminals)


    #CONVENCION
    #primer indice referencia a la posicion de la posicion de la produccion
    #segundo item a la posicion del elemento dentro de la produccion

    # Production structure:
    # NON TERMINAL, [ELEMENT1, ELEMENT2, ...],-1
    #ELEMENT has the following structure (TYPE, VALUE)

    # no terminales son: NON_TERMINAL
    # terminales son: TOKEN

    init_trans = productions[0].copy()
    init_trans[2] = 0
    init_closure = grammar_closure([init_trans], productions)

    print("\nINITIAL CLOSURE xd:")
    for production in init_closure:
        print(production[0][1], '->', [n[1] for n in production[1]], production[2])

    E_goto = grammar_goto(init_closure, ('NON_TERMINAL', 'expression'))
    print("\nINITIAL GOTO:")
    for production in E_goto:
        print(production[0][1], '->', [n[1] for n in production[1]], production[2])


def grammar_goto( items, symbol ):
    movable_items = [n for n in items if n[2] < len(n[1])]
    goto_items = [i for i in movable_items if i[1][i[2]] == symbol]
    moved_items = [[j[0], j[1], j[2]+1] for j in goto_items]
    return moved_items





if __name__ == "__main__":
    main()