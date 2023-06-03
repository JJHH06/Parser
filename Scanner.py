from ReturnTypes import *

import sys
from ExtendedAutomata import *


extended_automata = ExtendedAutomata([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], {'0', 'E', '.', '1', '5', '7', '\n', '*', '8', '+', '2', '4', '3', '\t', '9', '6', ')', ' ', '-', '('}, [((0, '0'), 1), ((0, '+'), 2), ((0, '1'), 1), ((0, '5'), 1), ((0, '7'), 1), ((0, '\n'), 3), ((0, '8'), 1), ((0, '2'), 1), ((0, '4'), 1), ((0, '3'), 1), ((0, ')'), 4), ((0, '\t'), 3), ((0, '('), 5), ((0, '*'), 6), ((0, '9'), 1), ((0, '6'), 1), ((0, ' '), 3), ((1, '0'), 1), ((1, 'E'), 7), ((1, '.'), 8), ((1, '1'), 1), ((1, '5'), 1), ((1, '7'), 1), ((1, '8'), 1), ((1, '2'), 1), ((1, '4'), 1), ((1, '3'), 1), ((1, '9'), 1), ((1, '6'), 1), ((3, '\n'), 3), ((3, '\t'), 3), ((3, ' '), 3), ((7, '0'), 9), ((7, '+'), 10), ((7, '1'), 9), ((7, '5'), 9), ((7, '7'), 9), ((7, '8'), 9), ((7, '2'), 9), ((7, '4'), 9), ((7, '3'), 9), ((7, '9'), 9), ((7, '6'), 9), ((7, '-'), 10), ((8, '0'), 11), ((8, '1'), 11), ((8, '5'), 11), ((8, '7'), 11), ((8, '8'), 11), ((8, '2'), 11), ((8, '4'), 11), ((8, '3'), 11), ((8, '9'), 11), ((8, '6'), 11), ((9, '0'), 9), ((9, '1'), 9), ((9, '5'), 9), ((9, '7'), 9), ((9, '8'), 9), ((9, '2'), 9), ((9, '4'), 9), ((9, '3'), 9), ((9, '9'), 9), ((9, '6'), 9), ((10, '0'), 9), ((10, '1'), 9), ((10, '5'), 9), ((10, '7'), 9), ((10, '8'), 9), ((10, '2'), 9), ((10, '4'), 9), ((10, '3'), 9), ((10, '9'), 9), ((10, '6'), 9), ((11, '0'), 11), ((11, 'E'), 7), ((11, '1'), 11), ((11, '5'), 11), ((11, '7'), 11), ((11, '8'), 11), ((11, '2'), 11), ((11, '4'), 11), ((11, '3'), 11), ((11, '9'), 11), ((11, '6'), 11)], 0, [1, 2, 3, 4, 5, 6, 9, 11], [1, 2, 0, 5, 4, 3, 1, 1])


def debugPrint():
    print('xd')


def match_automata_returns(recognized_type, i):
    if recognized_type is None:
        raise Exception('No type recognized at position', i)
    
    elif recognized_type == 0:
         return WHITESPACE 
    elif recognized_type == 1:
         return NUMBER 
    elif recognized_type == 2:
         return PLUS 
    elif recognized_type == 3:
         return TIMES 
    elif recognized_type == 4:
         return LPAREN 
    elif recognized_type == 5:
         return RPAREN 



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


    

    

print('Finished file')