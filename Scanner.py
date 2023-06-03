from ReturnTypes import *

import sys
from ExtendedAutomata import *


extended_automata = ExtendedAutomata([0, 1, 2, 3, 4, 5, 6], {'F', 'Z', 'X', 'N', 'b', 'l', '9', 'c', 'H', '\t', 'p', 'u', 'y', 'A', '7', '*', 'n', 'M', '+', 'J', 'q', 'S', 'e', 'h', '0', 'V', 'g', 'j', '1', '8', 'W', 'R', 'k', 'B', 'v', 't', ' ', 'f', ')', '(', '6', '4', 's', 'L', 'P', 'Y', 'x', '2', '\n', '3', 'i', 'm', 'o', 'G', 'w', 'E', 'T', '5', 'r', 'z', 'I', 'a', 'd', 'Q', 'U', 'O', 'K', 'D', 'C'}, [((0, 'F'), 1), ((0, 'Z'), 1), ((0, 'N'), 1), ((0, 'X'), 1), ((0, 'b'), 1), ((0, 'l'), 1), ((0, '*'), 2), ((0, 'c'), 1), ((0, 'H'), 1), ((0, '\t'), 3), ((0, 'p'), 1), ((0, 'u'), 1), ((0, 'y'), 1), ((0, 'A'), 1), ((0, '+'), 4), ((0, 'M'), 1), ((0, 'n'), 1), ((0, 'J'), 1), ((0, 'S'), 1), ((0, 'e'), 1), ((0, 'h'), 1), ((0, 'q'), 1), ((0, 'V'), 1), ((0, 'g'), 1), ((0, 'j'), 1), ((0, 'W'), 1), ((0, 'R'), 1), ((0, 'k'), 1), ((0, 'B'), 1), ((0, 'v'), 1), ((0, 't'), 1), ((0, ' '), 3), ((0, 'f'), 1), ((0, 's'), 1), ((0, 'L'), 1), ((0, 'P'), 1), ((0, 'Y'), 1), ((0, 'x'), 1), ((0, '\n'), 3), ((0, 'i'), 1), ((0, 'm'), 1), ((0, 'o'), 1), ((0, 'G'), 1), ((0, 'w'), 1), ((0, '('), 5), ((0, 'E'), 1), ((0, 'T'), 1), ((0, ')'), 6), ((0, 'r'), 1), ((0, 'z'), 1), ((0, 'I'), 1), ((0, 'a'), 1), ((0, 'd'), 1), ((0, 'Q'), 1), ((0, 'U'), 1), ((0, 'O'), 1), ((0, 'K'), 1), ((0, 'D'), 1), ((0, 'C'), 1), ((1, 'F'), 1), ((1, 'Z'), 1), ((1, 'N'), 1), ((1, 'X'), 1), ((1, 'b'), 1), ((1, 'l'), 1), ((1, '9'), 1), ((1, 'c'), 1), ((1, 'H'), 1), ((1, 'p'), 1), ((1, 'u'), 1), ((1, 'y'), 1), ((1, 'A'), 1), ((1, '7'), 1), ((1, 'M'), 1), ((1, 'n'), 1), ((1, 'J'), 1), ((1, 'S'), 1), ((1, 'e'), 1), ((1, 'h'), 1), ((1, 'q'), 1), ((1, 'V'), 1), ((1, 'g'), 1), ((1, '0'), 1), ((1, 'j'), 1), ((1, '1'), 1), ((1, '8'), 1), ((1, 'W'), 1), ((1, 'R'), 1), ((1, 'k'), 1), ((1, 'B'), 1), ((1, 'v'), 1), ((1, 't'), 1), ((1, 'f'), 1), ((1, '6'), 1), ((1, '4'), 1), ((1, 's'), 1), ((1, 'L'), 1), ((1, 'P'), 1), ((1, 'Y'), 1), ((1, 'x'), 1), ((1, '2'), 1), ((1, '3'), 1), ((1, 'i'), 1), ((1, 'm'), 1), ((1, 'o'), 1), ((1, 'G'), 1), ((1, 'w'), 1), ((1, 'E'), 1), ((1, 'T'), 1), ((1, '5'), 1), ((1, 'r'), 1), ((1, 'z'), 1), ((1, 'I'), 1), ((1, 'a'), 1), ((1, 'd'), 1), ((1, 'Q'), 1), ((1, 'U'), 1), ((1, 'O'), 1), ((1, 'K'), 1), ((1, 'D'), 1), ((1, 'C'), 1), ((3, '\t'), 3), ((3, ' '), 3), ((3, '\n'), 3)], 0, [1, 2, 3, 4, 5, 6], [1, 3, 0, 2, 4, 5])


def pepe():
    print('pepe')


def match_automata_returns(recognized_type, i):
    if recognized_type is None:
        raise Exception('No type recognized at position', i)
    
    elif recognized_type == 0:
        pass
    elif recognized_type == 1:
         return ID 
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


    

    

      