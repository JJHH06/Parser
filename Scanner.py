from ReturnTypes import *

import sys
from ExtendedAutomata import *


extended_automata = ExtendedAutomata([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], {'p', '%', 'v', ';', 'e', 'j', 'm', '\n', 'k', 'a', 'K', 'y', 'C', 'x', 'J', '\t', 'h', 's', 'D', 'M', 'Z', 'O', 'f', 'q', 'w', 'P', 'R', 'W', 'Y', 'S', 'r', 'g', 'd', 'V', '|', 'u', 'c', 'G', 'n', 'E', 'b', 'i', 'X', 'I', ' ', 'H', 't', 'B', 'F', 'L', 'U', 'N', 'l', 'o', 'z', ':', 'T', 'A', 'Q'}, [((0, 'p'), 1), ((0, '%'), 2), ((0, 'v'), 1), ((0, ';'), 3), ((0, 'e'), 1), ((0, 'j'), 1), ((0, '\n'), 4), ((0, 'k'), 1), ((0, 'a'), 1), ((0, 'K'), 5), ((0, 'y'), 1), ((0, 'C'), 5), ((0, 'x'), 1), ((0, 'h'), 1), ((0, '\t'), 4), ((0, 's'), 1), ((0, 'D'), 5), ((0, 'M'), 5), ((0, 'Z'), 5), ((0, 'O'), 5), ((0, 'f'), 1), ((0, 'q'), 1), ((0, 'w'), 1), ((0, 'P'), 5), ((0, 'R'), 5), ((0, 'W'), 5), ((0, 'Y'), 5), ((0, 'S'), 5), ((0, 'T'), 5), ((0, 'r'), 1), ((0, 'g'), 1), ((0, 'd'), 1), ((0, 'V'), 5), ((0, 'u'), 1), ((0, 'c'), 1), ((0, 'G'), 5), ((0, 'n'), 1), ((0, 'E'), 5), ((0, 'b'), 1), ((0, 'Q'), 5), ((0, 'i'), 1), ((0, 'X'), 5), ((0, 'I'), 5), ((0, ' '), 4), ((0, 'H'), 5), ((0, '|'), 6), ((0, 't'), 1), ((0, 'B'), 5), ((0, 'F'), 5), ((0, 'L'), 5), ((0, 'U'), 5), ((0, 'N'), 5), ((0, 'l'), 1), ((0, 'o'), 1), ((0, 'z'), 1), ((0, ':'), 7), ((0, 'm'), 1), ((0, 'A'), 5), ((0, 'J'), 5), ((1, 'p'), 1), ((1, 'v'), 1), ((1, 'e'), 1), ((1, 'j'), 1), ((1, 'k'), 1), ((1, 'a'), 1), ((1, 'y'), 1), ((1, 'x'), 1), ((1, 'h'), 1), ((1, 's'), 1), ((1, 'f'), 1), ((1, 'q'), 1), ((1, 'w'), 1), ((1, 'r'), 1), ((1, 'g'), 1), ((1, 'd'), 1), ((1, 'u'), 1), ((1, 'c'), 1), ((1, 'n'), 1), ((1, 'b'), 1), ((1, 'i'), 1), ((1, 't'), 1), ((1, 'l'), 1), ((1, 'o'), 1), ((1, 'z'), 1), ((1, 'm'), 1), ((2, 't'), 8), ((4, '\n'), 4), ((4, '\t'), 4), ((4, ' '), 4), ((5, 'K'), 5), ((5, 'C'), 5), ((5, 'D'), 5), ((5, 'M'), 5), ((5, 'Z'), 5), ((5, 'O'), 5), ((5, 'P'), 5), ((5, 'R'), 5), ((5, 'W'), 5), ((5, 'Y'), 5), ((5, 'S'), 5), ((5, 'T'), 5), ((5, 'V'), 5), ((5, 'G'), 5), ((5, 'E'), 5), ((5, 'Q'), 5), ((5, 'X'), 5), ((5, 'I'), 5), ((5, 'H'), 5), ((5, 'B'), 5), ((5, 'F'), 5), ((5, 'L'), 5), ((5, 'U'), 5), ((5, 'N'), 5), ((5, 'A'), 5), ((5, 'J'), 5), ((8, 'o'), 9), ((9, 'k'), 10), ((10, 'e'), 11), ((11, 'n'), 12)], 0, [1, 3, 4, 5, 6, 7, 12], [1, 6, 0, 2, 4, 5, 3])


def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    
ruta_archivo = sys.argv[1]

file_content = read_file(ruta_archivo)


def match_automata_returns(recognized_type, i):
    if recognized_type is None:
        raise Exception('No type recognized at position', i)
    
    elif recognized_type == 0:
        pass
    elif recognized_type == 1:
         return 'Non Terminal' 
    elif recognized_type == 2:
         return 'TOKEN' 
    elif recognized_type == 3:
         return 'TOKEN_DECLARATION' 
    elif recognized_type == 4:
         return 'TOKEN_DECLARATION' 
    elif recognized_type == 5:
         return 'PROD_ARROW' 
    elif recognized_type == 6:
         return 'EOP' 



def file_simulation(extended_automata, test_string):
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
                print(token, ':', test_string[first_recognized_pos:last_accepted_pos+1])
            if test_string[i] == '':
                break
            extended_automata.reset_simulation()
            first_recognized_pos = i
            last_accepted_pos = i
            reconized_type = None
            continue
        i += 1


    
file_simulation(extended_automata, file_content)
    

print('Finished file')