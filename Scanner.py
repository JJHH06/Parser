
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
