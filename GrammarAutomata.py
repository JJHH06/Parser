import copy
from Automata import Automata


def production_linealization(standard_production):
    dereferenced_production = copy.deepcopy(standard_production)
    new_production = []
    new_production.extend(dereferenced_production[0])
    for prod_element in dereferenced_production[1]:
        new_production.extend(prod_element)
    new_production.append(dereferenced_production[2])
    return tuple(copy.deepcopy(new_production)) #TODO: check if deepcopy here is necessary

# params:
#   - item: a list of the form [non_terminal, [element0, element1...], index]
#   - productions: list of productions in item format but index is always -1
def grammar_closure(item_list: list, input_productions: list):
    productions = copy.deepcopy(input_productions)
    items = copy.deepcopy(item_list)
    linealized_items = [production_linealization(k) for k in items]
    i = 0
    while i < len(items):
        if items[i][2] < len(items[i][1]) and items[i][1][items[i][2]][0] == 'NON_TERMINAL':
            for l in productions:
                if l[0] == items[i][1][items[i][2]] and production_linealization(l) not in linealized_items:
                    items.append([l[0],copy.deepcopy(l[1]),0]) #check if needed
                    linealized_items.append(production_linealization(l))
        i += 1
    return copy.deepcopy(items)

# goto without the closure
def grammar_goto( items, symbol ):
    items = copy.deepcopy(items)
    movable_items = [n for n in items if n[2] < len(n[1])]
    goto_items = [i for i in movable_items if i[1][i[2]] == symbol]
    moved_items = [[j[0], copy.deepcopy(j[1]), j[2]+1] for j in goto_items]
    return copy.deepcopy(moved_items)

def item_list_in_equivalent_states(equivalent_states, item_list):
    temptative_list = [t for t in equivalent_states if len(t) == len(item_list)]
    if len(temptative_list) == 0:
        return False
    for n in temptative_list:
        is_equivalent = True
        for i in item_list:
            if i not in n:
                is_equivalent = False
                break
        if is_equivalent:
            return True
    return False

        

def grammar_subset_construction(productions, alphabet):
    #CONVENCION
    #primer indice referencia a la posicion de la posicion de la produccion
    #segundo item a la posicion del elemento dentro de la produccion

    # Production structure:
    # NON TERMINAL, [ELEMENT1, ELEMENT2, ...],-1
    #ELEMENT has the following structure (TYPE, VALUE)

    # no terminales son: NON_TERMINAL
    # terminales son: TOKEN

    acceptance_production = copy.deepcopy(productions[0])
    acceptance_production[2] = 1



    init_trans = copy.deepcopy(productions[0])
    init_trans[2] = 0
    init_closure = grammar_closure([init_trans], productions)

    equivalent_states = [init_closure]

    equivalent_states_linealization = [set([production_linealization(k) for k in init_closure])]

    equivalent_transitions = []


    i = 0
    while i < len(equivalent_states):
        for symbol in alphabet:
            next_states = []
            next_states.extend(grammar_goto(equivalent_states[i], symbol))
        #next_states = set(next_states)
            if len(next_states) == 0:
                continue

            temp_next_states = [] #estados a los que se llega con epsilon y move

            temp_next_states.extend(grammar_closure(next_states, productions))
            next_states = copy.deepcopy(temp_next_states) #en teoria aca ya tendriamos el estado equivalente


            # #verificamos si es un estado atrapante
            # print('\nEstado tentativo')
            # for x in next_states:
            #     print(x[0], '->', [j[1] for j in x[1]])

            if len(next_states) !=0:
                #if next_states not in equivalent_states:

                #print('Sera aceptado como nuevo:', item_list_in_equivalent_states(equivalent_states, next_states))
                
                linealized_production = set([production_linealization(x) for x in next_states])
                if linealized_production not in equivalent_states_linealization:
                    equivalent_states.append(copy.deepcopy(next_states))
                    equivalent_states_linealization.append(linealized_production)
                equivalent_transitions.append(((equivalent_states_linealization.index(set([production_linealization(y) for y in equivalent_states[i]])), symbol[1]), equivalent_states_linealization.index(linealized_production)))
                #new_alphabet.add(symbol[1])
        i += 1
    
    lineal_accept_prod = production_linealization(acceptance_production)
    final_state_index = -1
    for n in range(len(equivalent_states_linealization)):
        if lineal_accept_prod in equivalent_states_linealization[n]:
            final_state_index = n
            break
    
    return equivalent_states, Automata([i for i in range(len(equivalent_states))], set([i[1] for i in alphabet]), equivalent_transitions, 0, [final_state_index])

