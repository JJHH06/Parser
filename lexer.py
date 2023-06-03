# Created by: José Hurtarte
# Created on: 20/02/2023
# Last modified on: 23/04/2023
# Description: Lexer for an infix regular expression

import sys
from graphviz import Digraph
import re

from Automata import *
from ExtendedAutomata import *
from ExpressionTree import *


# cleans the input from whitespaces
# TODO: Modify to do this but with classes?
# Note, Legacy, not using this anymore
def clean_input(user_input):
    user_input = user_input.replace(' ','')
    
    return user_input


def neutralize_forbidden_characters(user_input):
    result = []
    symbols = ['|','*','+','?']
    for i in user_input:
        if i in symbols:
            result.append('\\' + i)
        else:
            result.append(i)
    return result

# TODO: Modify to do this but with classes?
def format_input(user_input):
    symbols = ['|','*','+','?']
    result = []
    for i in range(len(user_input)):
        if (i != 0):
            #fist case we check if the previous character is a token and current character is a opening parenthesis
            if (user_input[i-1] not in symbols and user_input[i-1] != '('  and user_input[i] == '('):
                result.append('•')
                result.append(user_input[i])
            #second case we check if the previous character is a * or + or ? and current character is a token
            elif (user_input[i-1] in symbols[1:] and user_input[i] not in symbols and user_input[i] != ')'):
                result.append('•')
                result.append(user_input[i])
            #third case we check if the previous character is a closing parenthesis and current character is a token
            elif (user_input[i-1] == ')' and user_input[i] not in symbols and user_input[i] != '(' and user_input[i] != ')'):
                result.append('•')
                result.append(user_input[i])
            #last check if previous character is not a symbol and not a parenthesis and current character is not a symbol and not a parenthesi
            elif (user_input[i-1] not in symbols and user_input[i-1] != '(' and user_input[i-1] != ')' and user_input[i] not in symbols and user_input[i] != '(' and user_input[i] != ')'):
                result.append('•')
                result.append(user_input[i])
            else:
                result.append(user_input[i])
        else:
            result.append(user_input[i])
    return result


def validate_input_naive(user_input):
    if len(user_input) == 0:
        print('Invalid input: Empty input')
        return False

    if '.' in user_input:
        print('Invalid input: . is a reserved character')
        return False

    if '||' in user_input:
        print('Invalid input: Two or more consecutive |')
        return False

    if user_input.startswith(('*', '+', '?', '|', '.')):
        print('Invalid input: Symbols at start are not a valid operation')
        return False

    if user_input.endswith(('|', '.')):
        print('Invalid input: Symbol at end not valid')
        return False

    for i in range(len(user_input)):
        if user_input[i:i+2] == '()':
            print('Invalid input: Empty parenthesis')
            return False

        if user_input[i] == '(' and (i+1 == len(user_input) or user_input[i+1] in '+*?|.'):
            print('Invalid input: Operators after open parenthesis are not a valid operation')
            return False

        if user_input[i] in '|.' and (i == 0 or user_input[i-1] in '|(' or i+1 == len(user_input) or user_input[i+1] in '|)'):
            print('Invalid input: {} not valid'.format(user_input[i]))
            return False
    parenthesis_count = 0
    for i in range(len(user_input)):
        if (user_input[i] == '('):
            parenthesis_count += 1
        elif (user_input[i] == ')'):
            parenthesis_count -= 1
        if (parenthesis_count < 0):
            print('Invalid input: Mismatched parenthesis, cannot close a parenthesis that was not opened, error at position: {}'.format(i))
            return False
    if (parenthesis_count != 0):
        print('Invalid input: Parenthesis mismatch error, close all parenthesis to fix it')
        return False
    return True

def read_yalex_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        file_content = file.read()
        file.close()
    return file_content
    

#TODO: Remove for future versions
def remove_text_between_braces(text):
    result = ''
    skip = False
    escape = False
    for char in text:
        if escape:
            if char == 'n':
                result += '\n'
            elif char == 't':
                result += '\t'
            elif char == 's':
                result += ' '
            else:
                result += '\\' + char
            escape = False
        elif char == '\\':
            escape = True
        # elif char == '{':
        #     skip = True
        # elif char == '}':
        #     skip = False
        elif not skip:
            result += char
    return result
def clean_yalex_comments(raw_input):
    clean_string = ''
    can_append = True
    for i in range(len(raw_input)):
        if raw_input[i] == '(':
            if (i+1 < len(raw_input) and raw_input[i+1] == '*'):
                can_append = False
        elif raw_input[i] == ')':
            if (i-1 >= 0 and raw_input[i-1] == '*'):
                can_append = True
                continue
        if can_append:
            clean_string += raw_input[i]
    return remove_text_between_braces(clean_string)


# Note: this is under the supposition that the inputs are ascii chars
def char_range_set(char1, char2):
    pos1 = ord(char1)
    pos2 = ord(char2)
    # Swap if chars in disorder
    if pos1 > pos2: 
        pos1, pos2 = pos2, pos1
    return [chr(pos) for pos in range(pos1, pos2 + 1)]

def concat_with_or(my_list):
    result = '('
    if len(my_list) > 0:
        result += my_list[0]
        for i in range(1, len(my_list)):
            result += '|' + my_list[i]
    return result+')'

def concat_list_with_symbol(my_list, symbol = '|'):
    result = ['(']
    if len(my_list) > 0:
        result.append(my_list[0])
        for i in range(1, len(my_list)):
            result.append(symbol)
            result.append(my_list[i])
    result.append(')')
    return result



def build_direct_det_automaton(user_input):
    user_input = format_input(user_input)
    output = shunting_yard(user_input)
    #print('Postfix: ',output)
    # Direct construction tree
    tree, followpos, char_list = build_direct_construction_tree(output)
    # digraph = Digraph(graph_attr={'dpi': str(200)})
    # postorder_traversal_draw(tree, digraph)
    # digraph.render('expression_tree', format='png')
    
    #Direct construction deterministic automata
    det_automata = direct_construction(followpos, tree.firstPos, tree.lastPos, char_list)
    clean_transitions(det_automata)
    #draw_automata(det_automata, 'DFA', 'Direct construction DFA: '+''.join(user_input))
    return det_automata

def build_direct_extended_automaton(regex_list) -> ExtendedAutomata:
    # primero para cada una de las expresiones se formatean para concat
    formated_regex_list = [format_input(regex) for regex in regex_list]
    # segundo para cada una se hace el shunting yard
    output_list = [shunting_yard(regex) for regex in formated_regex_list]
    # Luego se construyen los arboles de cada expresion, pero se guardan en una lista de arboles
    tree_list = []
    leaf_positions_list = []
    followpos_list = []

    for j in range(len(output_list)):
        tree, followpos_list, leaf_positions_list = build_direct_aumented_construction_tree(output_list[j],leaf_positions_list, followpos_list)
        tree_list.append(copy.deepcopy(tree))
        # digraph = Digraph(graph_attr={'dpi': str(200)})
        # postorder_traversal_draw(tree, digraph)
        # digraph.render('expression_tree_'+str(j), format='png')
    initial_state = set()
    final_states = []

    # Una vez el arbol, calculamos la posicion inicial y las posiciones finales
    for element in tree_list:
        initial_state.update(element.firstPos)
        final_states.append(list(element.lastPos)[0])
    
    # print('Initial state: ', initial_state)
    # print('Final states: ', final_states)

    #las posiciones finales deben ser un listado de enteros para que en base a la posicion se pueda ver su return

    # Luego se construye el automata
    extended_automata = direct_extended_construction(followpos_list, initial_state, final_states, leaf_positions_list)
    #esto limpia transiciones que pueden tener algunos simbolos prohibidos
    clean_transitions(extended_automata)
    draw_automata(extended_automata, 'DFA', 'Direct construction DFA: slr-1.yal')
    return extended_automata



def concatenate_strings(string_list):
    result = ""
    for string in string_list:
        result += string
    return result

def build_tree_from_infix(user_input):
    user_input = format_input(user_input)
    output = shunting_yard(user_input)
    #print('Postfix: ',output)
    # Direct construction tree
    tree = build_tree(output)
    digraph = Digraph(graph_attr={'dpi': str(200)})
    postorder_traversal_draw(tree, digraph)
    digraph.render('expression_tree', format='png')
    return tree

def clean_infix_set(user_input):
    # TODO: FOR ERRORS ADD FORBIDDEN SIMBOLS VALIDATION
    result = []
    for char in user_input:
        if char != '(' and char != ')' and char != '|':
            result.append(char)
    return concat_list_with_symbol(result)

def transform_regex_to_set(user_input):
    result = set()
    for char in user_input:
        if char != '(' and char != ')' and char != '|':
            result.add(char)
    return result

def set_difference(set1, set2):
    obj1 = transform_regex_to_set(set1)
    obj2 = transform_regex_to_set(set2)
    return concat_list_with_symbol(list(obj1 - obj2))

def create_file(file_content, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(file_content)
    #print(f'File {file_name} created successfully')

def generate_executable_file_content(extended_automata, code_segments,  header_text, footer_text):
    file_content = str()

    file_content += header_text + '\n\n'# uso del header

    code_class_generation ='''import sys
from ExtendedAutomata import *


extended_automata = '''+ extended_automata.stringify_constructor() + '\n\n'
    file_content += code_class_generation
    #a este punto ya tenemos el header y el constructor de la clase
    #ahora necesitamos una funcion para leer archivo y una forma de tomar la ruta desde consola

    get_console_input = '''
def debugPrint():
    print('xd')

'''
    file_content = file_content + get_console_input

    #ahora necesitamos simular el automata con el archivo

    file_simulation = '''

def file_simulation(extended_automata, test_string):
    recognized_tokens = []
    test_string = test_string + '\x1a'
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
            if test_string[i] == '\x1a':
                break
            extended_automata.reset_simulation()
            first_recognized_pos = i
            last_accepted_pos = i
            reconized_type = None
            continue
        i += 1
    return recognized_tokens


    '''

    # now we need to match the automata returns with the tokens
    match_automata_returns = '''
def match_automata_returns(recognized_type, i):
    if recognized_type is None:
        raise Exception('No type recognized at position', i)
    '''
    for i in range(len(code_segments)):
        match_automata_returns += f'''
    elif recognized_type == {str(i)}:
        {code_segments[i] if code_segments[i] != '' else 'pass'}'''
        
    match_automata_returns += '\n\n'

    file_content +=  match_automata_returns + file_simulation

    file_content +='''

    '''

    file_content += '\n\n' + footer_text
    return file_content
    




# Main function
def Lexer(file_raw_content:str):
    file_content = clean_yalex_comments(file_raw_content)
    

    let_ident = list('let')
    separator_ident = list('(\n|\t| )+')
    id_ident = list('(' + concat_with_or(char_range_set('a','z'))+'|'+concat_with_or(char_range_set('A','Z'))+'|'+concat_with_or(char_range_set('0','9'))+'|_)+')
    equal_ident = list('=')
    open_set_ident = list('[')
    close_set_ident = list(']')
    open_parenthesis_ident = ['\\(']
    close_parenthesis_ident = ['\\)']
    #char_ident = ["'","("]+list('('+concat_with_or(char_range_set('a','z'))+'|'+concat_with_or(char_range_set('A','Z'))+'|'+concat_with_or(char_range_set('0','9'))+'|_)|'+'(\n|\t| )'+'|')+operators_ident +[")","'"]
    #string_ident = ['"',"(","("]+list('('+concat_with_or(char_range_set('a','z'))+'|'+concat_with_or(char_range_set('A','Z'))+'|'+concat_with_or(char_range_set('0','9'))+'|_)|'+'(\n|\t| )'+'|')+operators_ident +[")",'+',")",'"']
    operators_ident = ['(','\\*','|','\\+','|', '\\?','|','\\|', '|','\\(','|','\\)','|','^','|','#',')']

    char_ident = list(concat_with_or(char_range_set('a','z'))+'|'+concat_with_or(char_range_set('A','Z'))+'|'+concat_with_or(char_range_set('0','9'))+'|'+'(\n|\t| )'+'|')+operators_ident
    string_ident = list(concat_with_or(char_range_set('a','z'))+'|'+concat_with_or(char_range_set('A','Z'))+'|'+concat_with_or(char_range_set('0','9'))+'|'+'(\n|\t| )'+'|')+operators_ident
    
    char_ascii_complement = concat_with_or(char_range_set(chr(33), chr(38))) +'|'+ concat_with_or(char_range_set(chr(44), chr(47)))+'|'+concat_with_or(char_range_set(chr(58), chr(62))) + '|('+chr(64) + ')|' + concat_with_or(char_range_set(chr(91), chr(96))) + '|(' + chr(123) + ')|' + concat_with_or(char_range_set(chr(125), chr(126)))
    string_ascii_complement ='('+chr(33) + ')|' + concat_with_or(char_range_set(chr(35), chr(39)))+ '|'+ concat_with_or(char_range_set(chr(44), chr(47)))+'|'+concat_with_or(char_range_set(chr(58), chr(62))) + '|('+chr(64) + ')|' + concat_with_or(char_range_set(chr(91), chr(96))) + '|(' + chr(123) + ')|' + concat_with_or(char_range_set(chr(125), chr(126)))
    

    anychar_regex = ['('] + char_ident + ['|'] +list(char_ascii_complement)+[')']
    char_ident = ["'",'('] + anychar_regex + [')',"'"]
    string_ident = ['"','(','('] + string_ident + ['|'] +list(string_ascii_complement)+[')','+',')','"']
    #Para el anychar
    


    anychar_ident = list('_')
    range_ident = ['('] + char_ident+[')','-','('] + char_ident+[')']
    rule_ident = list('rule')

    #para tener todos los caracteres ascii en string y char
    #char_ascii_complement = concat_with_or(char_range_set(chr(33), chr(38))) +'|'+ concat_with_or(char_range_set(chr(44), chr(47)))+'|'+concat_with_or(char_range_set(chr(58), chr(62))) + '|('+chr(64) + ')|' + concat_with_or(char_range_set(chr(91), chr(96))) + '|(' + chr(123) + ')|' + concat_with_or(char_range_set(chr(125), chr(126)))
    #string_ascii_complement ='('+chr(33) + ')|' + concat_with_or(char_range_set(chr(35), chr(39)))+ '|'+ concat_with_or(char_range_set(chr(44), chr(47)))+'|'+concat_with_or(char_range_set(chr(58), chr(62))) + '|('+chr(64) + ')|' + concat_with_or(char_range_set(chr(91), chr(96))) + '|(' + chr(123) + ')|' + concat_with_or(char_range_set(chr(125), chr(126)))
    
    # char_ident = char_ident +['|']+ list(char_ascii_complement)
    # string_ident = string_ident +['|']+ list(string_ascii_complement)

    disabledops_ident = ["'"] + operators_ident + ["'"]

    anychar_regex = anychar_regex + ['|','(', '\'', ')'] 
    anychar_regex = clean_infix_set(anychar_regex) #esto quita los parentesis anidados de un set

    code_segment_regex = ['{'] + set_difference(anychar_regex, list('({|})'))+ ['*','}']

    #print('code_segment_regex: ',''.join(code_segment_regex))

    # TODO: {id}



    let_automata = build_direct_det_automaton(let_ident)
    separator_automata = build_direct_det_automaton(separator_ident)
    id_automata = build_direct_det_automaton(id_ident)
    equal_automata = build_direct_det_automaton(equal_ident)
    open_set_automata = build_direct_det_automaton(open_set_ident)
    close_set_automata = build_direct_det_automaton(close_set_ident)
    open_parenthesis_automata = build_direct_det_automaton(open_parenthesis_ident)
    close_parenthesis_automata = build_direct_det_automaton(close_parenthesis_ident)
    operators_automata = build_direct_det_automaton(operators_ident)
    char_automata = build_direct_det_automaton(char_ident)
    string_automata = build_direct_det_automaton(string_ident)
    anychar_automata = build_direct_det_automaton(anychar_ident)
    range_automata = build_direct_det_automaton(range_ident)
    rule_automata = build_direct_det_automaton(rule_ident)
    disabledops_automata = build_direct_det_automaton(disabledops_ident)
    code_segment_automata = build_direct_det_automaton(code_segment_regex)

    #note: remember to reset simulation before even trying to simulate
    let_automata.reset_simulation()
    separator_automata.reset_simulation()
    id_automata.reset_simulation()
    equal_automata.reset_simulation()
    open_set_automata.reset_simulation()
    close_set_automata.reset_simulation()
    open_parenthesis_automata.reset_simulation()
    close_parenthesis_automata.reset_simulation()
    operators_automata.reset_simulation()
    char_automata.reset_simulation()
    string_automata.reset_simulation()
    anychar_automata.reset_simulation()
    range_automata.reset_simulation()
    rule_automata.reset_simulation()
    disabledops_automata.reset_simulation()
    code_segment_automata.reset_simulation()
    #print('AUTOMATAS GENERATED :)')
    

    
   

    #print('raw file_content', file_raw_content)
    #print('clean file_content', file_content)

    FILE_LENGTH = len(file_content)

    last_initial_pos = 0
    last_accepting_pos = 0

    # here we are going to be saving the types of the tokens, kinda like a return rule
    last_accepting_types = []

    # here we are going to be saving the tokens
    recognized_tokens = []

    current_pos = 0
    last_initial_pos = 0
    while (current_pos < FILE_LENGTH):
        #print('current_pos', current_pos, file_content[current_pos])
        accepting_types = []
        
        let_automata_sim_state = let_automata.simulate(file_content[current_pos])
        separator_automata_sim_state = separator_automata.simulate(file_content[current_pos])
        id_automata_sim_state = id_automata.simulate(file_content[current_pos])
        equal_automata_sim_state = equal_automata.simulate(file_content[current_pos])
        open_set_automata_sim_state = open_set_automata.simulate(file_content[current_pos])
        close_set_automata_sim_state = close_set_automata.simulate(file_content[current_pos])
        open_parenthesis_automata_sim_state = open_parenthesis_automata.simulate(file_content[current_pos])
        close_parenthesis_automata_sim_state = close_parenthesis_automata.simulate(file_content[current_pos])
        operators_automata_sim_state = operators_automata.simulate(file_content[current_pos])
        char_automata_sim_state = char_automata.simulate(file_content[current_pos])
        string_automata_sim_state = string_automata.simulate(file_content[current_pos])
        anychar_automata_sim_state = anychar_automata.simulate(file_content[current_pos])
        range_automata_sim_state = range_automata.simulate(file_content[current_pos])
        rule_automata_sim_state = rule_automata.simulate(file_content[current_pos])
        disabledops_automata_sim_state = disabledops_automata.simulate(file_content[current_pos])
        code_segment_automata_sim_state = code_segment_automata.simulate(file_content[current_pos])

        if separator_automata_sim_state == 1:
            if(current_pos+1<= FILE_LENGTH):
                last_initial_pos = current_pos+1
                last_accepting_pos = current_pos+1
                
        if separator_automata_sim_state == -1:
            if last_accepting_pos == current_pos:
                #reiniciar automatas y volver a simular
                let_automata.reset_simulation()
                separator_automata.reset_simulation()
                id_automata.reset_simulation()
                equal_automata.reset_simulation()
                open_set_automata.reset_simulation()
                close_set_automata.reset_simulation()
                open_parenthesis_automata.reset_simulation()
                close_parenthesis_automata.reset_simulation()
                operators_automata.reset_simulation()
                char_automata.reset_simulation()
                string_automata.reset_simulation()
                anychar_automata.reset_simulation()
                range_automata.reset_simulation()
                rule_automata.reset_simulation()
                disabledops_automata.reset_simulation()
                code_segment_automata.reset_simulation()

                #simular
                let_automata_sim_state = let_automata.simulate(file_content[current_pos])
                separator_automata_sim_state = separator_automata.simulate(file_content[current_pos])
                id_automata_sim_state = id_automata.simulate(file_content[current_pos])
                equal_automata_sim_state = equal_automata.simulate(file_content[current_pos])
                open_set_automata_sim_state = open_set_automata.simulate(file_content[current_pos])
                close_set_automata_sim_state = close_set_automata.simulate(file_content[current_pos])
                open_parenthesis_automata_sim_state = open_parenthesis_automata.simulate(file_content[current_pos])
                close_parenthesis_automata_sim_state = close_parenthesis_automata.simulate(file_content[current_pos])
                operators_automata_sim_state = operators_automata.simulate(file_content[current_pos])
                char_automata_sim_state = char_automata.simulate(file_content[current_pos])
                string_automata_sim_state = string_automata.simulate(file_content[current_pos])
                anychar_automata_sim_state = anychar_automata.simulate(file_content[current_pos])
                range_automata_sim_state = range_automata.simulate(file_content[current_pos])
                rule_automata_sim_state = rule_automata.simulate(file_content[current_pos])
                disabledops_automata_sim_state = disabledops_automata.simulate(file_content[current_pos])
                code_segment_automata_sim_state = code_segment_automata.simulate(file_content[current_pos])

        if let_automata_sim_state == 1:
            last_accepting_pos = current_pos
            accepting_types.append('LET')

        if rule_automata_sim_state == 1:
            last_accepting_pos = current_pos
            accepting_types.append('RULE')

        if anychar_automata_sim_state == 1:
            last_accepting_pos = current_pos
            accepting_types.append('ANYCHAR')
        
        if id_automata_sim_state == 1:
            last_accepting_pos = current_pos
            accepting_types.append('ID')
        
        if equal_automata_sim_state == 1:
            last_accepting_pos = current_pos
            accepting_types.append('EQUAL')

        if open_set_automata_sim_state == 1:
            last_accepting_pos = current_pos
            accepting_types.append('OPEN_SET')
        
        if close_set_automata_sim_state == 1:
            last_accepting_pos = current_pos
            accepting_types.append('CLOSE_SET')
        
        if open_parenthesis_automata_sim_state == 1:
            last_accepting_pos = current_pos
            accepting_types.append('OPEN_PARENTHESIS')
        
        if close_parenthesis_automata_sim_state == 1:
            last_accepting_pos = current_pos
            accepting_types.append('CLOSE_PARENTHESIS')
        
        if operators_automata_sim_state == 1:
            last_accepting_pos = current_pos
            accepting_types.append('OPERATOR')

        if disabledops_automata_sim_state == 1:
            last_accepting_pos = current_pos
            accepting_types.append('DISABLED_OPERATOR')
            
        if char_automata_sim_state == 1:
            last_accepting_pos = current_pos
            accepting_types.append('CHAR')
        
        if string_automata_sim_state == 1:
            last_accepting_pos = current_pos
            accepting_types.append('STRING')

        if range_automata_sim_state == 1:
            last_accepting_pos = current_pos
            accepting_types.append('RANGE')
        
        if code_segment_automata_sim_state == 1:
            last_accepting_pos = current_pos
            accepting_types.append('CODE_SEGMENT')

        if len(accepting_types) > 0:
            last_accepting_types = accepting_types.copy()

        if(let_automata_sim_state==-1)and (separator_automata_sim_state==-1) and (id_automata_sim_state==-1) and (equal_automata_sim_state==-1) and (open_set_automata_sim_state==-1) and (close_set_automata_sim_state==-1) and (open_parenthesis_automata_sim_state==-1) and (close_parenthesis_automata_sim_state==-1) and (operators_automata_sim_state==-1) and (char_automata_sim_state==-1) and (string_automata_sim_state==-1) and (anychar_automata_sim_state==-1) and (range_automata_sim_state==-1) and (code_segment_automata_sim_state == -1) and (rule_automata_sim_state == -1) and (disabledops_automata_sim_state == -1):
            # append token
            if len(last_accepting_types) != 0:
                recognized_tokens.append((file_content[last_initial_pos:last_accepting_pos+1], last_accepting_types[0]))
            else:
                raise Exception('Error: unrecognized token at position ' + str(last_initial_pos))
            last_accepting_types = []
            # reset automatas
            let_automata.reset_simulation()
            separator_automata.reset_simulation()
            id_automata.reset_simulation()
            equal_automata.reset_simulation()
            open_set_automata.reset_simulation()
            close_set_automata.reset_simulation()
            open_parenthesis_automata.reset_simulation()
            close_parenthesis_automata.reset_simulation()
            operators_automata.reset_simulation()
            char_automata.reset_simulation()
            string_automata.reset_simulation()
            anychar_automata.reset_simulation()
            range_automata.reset_simulation()
            rule_automata.reset_simulation()
            disabledops_automata.reset_simulation()
            code_segment_automata.reset_simulation()

            last_initial_pos = current_pos

        else:
            current_pos += 1
        
        if (current_pos == len(file_content) and separator_automata_sim_state !=1 ): #esto es valido cuando el string no termina con delims
            recognized_tokens.append((file_content[last_initial_pos:last_accepting_pos+1], last_accepting_types[0]))






    #print("Tokens reconocidos: ", recognized_tokens)

    let_declarations = {}
    rules = {}
    current_output = []
    current_id = str()
    is_declaring_id = False
    let_declaration = False
    set_bracket_count = 0
    is_first_to_arrive_set = False
    header_text = ''
    footer_text = ''
    header_done = False
    rule_list = []
    parenthesis_count = 0
    has_code_segment = False
    code_segments = []
    complement_operation = False
    difference_operation = False
    temp_difference_set = []

    for token in recognized_tokens:
        if token[1] == 'LET':
            if(len(current_output) > 0):
                let_declarations[current_id] = current_output
            current_output = []
            current_id = str()
            is_declaring_id = True
            let_declaration = True

        elif token[1] == 'RULE':
            if(len(current_output) > 0):
                let_declarations[current_id] = current_output
            current_output = []
            current_id = str()
            is_declaring_id = True
            let_declaration = False

        elif token[1] == 'ID':
            if is_declaring_id:
                current_id = token[0]
            else:
                if token[0] in let_declarations:
                    current_output = current_output + let_declarations[token[0]]
                else:
                    raise Exception('Error: undefined identifier ' + token[0])
        
        elif token[1] == 'CODE_SEGMENT':
            if not header_done:
                header_text = token[0][1:len(token[0])-1]
                header_done = True
            else:
                #en algun momento verificar de alguna manera si sobran los code segments
                #agregar codigo para los segmentos de codigo de rules en algun momento vamos a tener que verificar si hay un desfase en el ultimo verificando si el ultimo esta lleno
                pass
                has_code_segment = True
                code_segments.append(token[0][1:len(token[0])-1])



        elif token[1] == 'EQUAL':
            is_declaring_id = False
        
        elif token[1] == 'OPEN_PARENTHESIS':
            parenthesis_count += 1
            current_output.append('(')
        
        elif token[1] == 'CLOSE_PARENTHESIS':
            parenthesis_count -= 1
            current_output.append(')')
        
        elif token[1] == 'OPEN_SET':
            current_output.append('(')
            is_first_to_arrive_set = True
            set_bracket_count += 1
        elif token[1] == 'CLOSE_SET':
            current_output.append(')')
            set_bracket_count -= 1
        
        elif token[1] == 'OPERATOR':
            if (not let_declaration) and (token[0] == '|') and (parenthesis_count == 0): #TODO: para errores aqui se puede verificar
                rule_list.append(current_output)
                current_output = []
                if not has_code_segment:
                    code_segments.append('')
                has_code_segment = False
            else:
                if token[0] == '^':
                    #para errores verificar si no estamos dentro de un set asi se muere
                    complement_operation = True
                elif token[0] == '#':
                    difference_operation = True
                    # Aqui tenemos que recorrer el output hasta encontrar el ultimo set y retirarlo
                    if len(current_output) == 0:
                        raise Exception("Error: set Operator needs more than 1 set to work: ", token)
                    temp_set_count = 0
                    for i in range(len(current_output)-1, -1, -1):
                        if current_output[i] == ')':
                            temp_set_count += 1
                        elif current_output[i] == '(': #aqui se muere si no hay un set
                            temp_set_count -= 1
                        if temp_set_count == 0:
                            temp_difference_set = current_output[i:]
                            current_output = current_output[:i]
                            break
                        elif temp_set_count>1 or temp_set_count<0:
                            raise Exception("Error: Object to operate is not a set: ", token)                    
                else:
                    current_output.append(token[0])
        
        elif token[1] == 'DISABLED_OPERATOR':
            if set_bracket_count > 0:
                if is_first_to_arrive_set:
                    is_first_to_arrive_set = False
                    current_output.append('\\'+token[0][1])
                else:
                    current_output.append('|')
                    current_output.append('\\'+token[0][1])
            else:
                current_output.append('\\'+token[0][1])#Como es un char tambien y asumimos que todo esta bien, podemos asegurar que la posicion 1 es el char
        elif token[1] == 'CHAR':
            if set_bracket_count > 0:
                if is_first_to_arrive_set:
                    is_first_to_arrive_set = False
                else:
                    current_output.append('|')

                if complement_operation:
                    #agregar que hace el complemento
                    current_output = current_output + set_difference(anychar_regex, [token[0][1]])
                    complement_operation = False
                else:
                    current_output.append(token[0][1])
            else:
                current_output.append(token[0][1]) #Como es un char y asumimos que todo esta bien, podemos asegurar que la posicion 1 es el char
        elif token[1] == 'STRING':
            string_size = len(token[0])
            recognized_string = token[0][1:string_size-1]
            if set_bracket_count > 0:
                if is_first_to_arrive_set:
                    is_first_to_arrive_set = False
                else:
                    current_output.append('|')
                temp_current_string_output = []
                if complement_operation:
                    #current_output = current_output + set_difference(anychar_regex, neutralize_forbidden_characters(list(recognized_string)))
                    temp_current_string_output = set_difference(anychar_regex, neutralize_forbidden_characters(list(recognized_string)))
                    complement_operation = False
                else:
                    #current_output = current_output + concat_list_with_symbol(neutralize_forbidden_characters(list(recognized_string)))
                    temp_current_string_output = concat_list_with_symbol(neutralize_forbidden_characters(list(recognized_string)))
                #ahora faltaria hacer un current_output = current_output + temp_current_string_output
                if difference_operation:
                    current_output = current_output + set_difference(temp_difference_set, temp_current_string_output)
                    difference_operation = False
                else:
                    current_output = current_output + temp_current_string_output

            else:
                current_output.append('(')
                current_output = current_output + neutralize_forbidden_characters(list(recognized_string))
                current_output.append(')')

        elif token[1] == 'RANGE':
            range_size = len(token[0])
            character_range_list = concat_list_with_symbol(neutralize_forbidden_characters(char_range_set(token[0][1], token[0][range_size-2])))
            if set_bracket_count > 0:
                if is_first_to_arrive_set:
                    is_first_to_arrive_set = False
                else:
                    current_output.append('|')
                if complement_operation:
                    current_output = current_output + set_difference(anychar_regex, character_range_list)
                    complement_operation = False
                else:
                    current_output = current_output + character_range_list
            else:
                current_output = current_output + character_range_list
        elif token[1] == 'ANYCHAR':
            if set_bracket_count > 0:
                if is_first_to_arrive_set:
                    is_first_to_arrive_set = False
                    current_output = current_output + anychar_regex
                else:
                    current_output.append('|')
                    current_output = current_output + anychar_regex
            else:
                current_output = current_output + anychar_regex
    if set_bracket_count !=0:
        raise Exception("Error: Set brackets are not balanced")
    if parenthesis_count !=0:
        raise Exception("Error: Parenthesis are not balanced")
    
    # print('\n\nLET DECLARATIONS: ')
    # #iterate over let declarations and print them
    # for key in let_declarations:
    #     print(key, ':', concatenate_strings(let_declarations[key]))
    

    #print('\n\nRULE: ')
    rule_list.append(current_output)
    current_output = []

    footer_text = code_segments.pop()

    if len(code_segments) < len(rule_list):
        code_segments.append('')
    

    # for i in range(len(rule_list)):
    #     print('RULE', i, ':', concatenate_strings(rule_list[i]))
    #     print('CODE', i, ':', code_segments[i])
    #     print('\n')


    # print('\n\nHEADER: ', header_text)
    # print('\n\nFOOTER: ', footer_text)
    #print(current_id, ':', concatenate_strings(current_output))

    #resulting_rule_tree = build_tree_from_infix(current_output)
    extended_automata = build_direct_extended_automaton(rule_list)

    #print('\n\Constructor:\n', extended_automata.stringify_constructor())

    executable_file_content = generate_executable_file_content(extended_automata, code_segments, header_text, footer_text)
    create_file(executable_file_content, 'Scanner.py')


    print('\nFINISHED LEXER USE SUCCESFUL!')




