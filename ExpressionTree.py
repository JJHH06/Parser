# Created by: José Hurtarte
# Created on: 24/02/2023
# Last modified on: 19/03/2023
# Description: Automata module and class

from graphviz import Digraph

class Tree:
    def __init__(self, root, firstPos = None, lastPos = None, nullable = None):
        self.key = root
        self.leftChild = None
        self.rightChild = None
        self.firstPos = firstPos
        self.lastPos = lastPos
        self.nullable = nullable

#builds a tree based on the Tree class
# TODO: Modify to do this but with classes?
def build_tree(postfix_expression):
    unary_operators = ['*','+','?']
    binary_operators = ['|','•']
    stack = []
    for token in postfix_expression:
        # Checks if token is a valid operand
        if token not in unary_operators and token not in binary_operators:
            stack.append(Tree(token))
        # checks if token is a valid binary operator
        elif token in binary_operators:
            operator_tree = Tree(token)
            operator_tree.rightChild = stack.pop()
            operator_tree.leftChild = stack.pop()
            stack.append(operator_tree)
        # checks if token is a valid unary operator
        elif token in unary_operators:
            operator_tree = Tree(token)
            operator_tree.leftChild = stack.pop()
            stack.append(operator_tree)
    return stack.pop()

# Builds direct tree for construction of DFA, also builds followpos table
def build_direct_construction_tree(postfix_expression):
    
    unary_operators = ['*','+','?']
    binary_operators = ['|','•']
    stack = []
    leaf_positions = []
    followpos_table = []
    

    for token in postfix_expression:
        # Checks if token is a valid operand
        if token not in unary_operators and token not in binary_operators:
            #if token is epsilon, it is nullable
            if token == 'ε':
                stack.append(Tree(token, set(), set(), True))
            else:
                stack.append(Tree(token, {len(leaf_positions)}, {len(leaf_positions)}, False))
                #print(token, {len(leaf_positions)}, {len(leaf_positions)})
                leaf_positions.append(token)
                followpos_table.append(set())

        # checks if token is a valid binary operator
        elif token in binary_operators:
            operator_tree = Tree(token)
            operator_tree.rightChild = stack.pop()
            operator_tree.leftChild = stack.pop()

            if token == '|':
                operator_tree.nullable = operator_tree.leftChild.nullable or operator_tree.rightChild.nullable
                operator_tree.firstPos = operator_tree.leftChild.firstPos.union(operator_tree.rightChild.firstPos)
                operator_tree.lastPos = operator_tree.leftChild.lastPos.union(operator_tree.rightChild.lastPos)
            elif token == '•':
                operator_tree.nullable = operator_tree.leftChild.nullable and operator_tree.rightChild.nullable
                if operator_tree.leftChild.nullable:
                    operator_tree.firstPos = operator_tree.leftChild.firstPos.union(operator_tree.rightChild.firstPos)
                else:
                    operator_tree.firstPos = operator_tree.leftChild.firstPos.copy()
                if operator_tree.rightChild.nullable:
                    operator_tree.lastPos = operator_tree.leftChild.lastPos.union(operator_tree.rightChild.lastPos)
                else:
                    operator_tree.lastPos = operator_tree.rightChild.lastPos.copy()
                for i in operator_tree.leftChild.lastPos:
                    followpos_table[i] = followpos_table[i].union(operator_tree.rightChild.firstPos)
            #print(operator_tree.key, operator_tree.firstPos, operator_tree.lastPos)
            stack.append(operator_tree)
        # checks if token is a valid unary operator
        elif token in unary_operators:
            operator_tree = Tree(token)
            operator_tree.leftChild = stack.pop()
            if token == '*':
                operator_tree.nullable = True
                operator_tree.firstPos = operator_tree.leftChild.firstPos.copy()
                operator_tree.lastPos = operator_tree.leftChild.lastPos.copy()
                for i in operator_tree.lastPos:
                    followpos_table[i] = followpos_table[i].union(operator_tree.firstPos)
                
            elif token == '+':
                operator_tree.nullable = operator_tree.leftChild.nullable
                operator_tree.firstPos = operator_tree.leftChild.firstPos.copy()
                operator_tree.lastPos = operator_tree.leftChild.lastPos.copy()
                for i in operator_tree.lastPos:
                    followpos_table[i] = followpos_table[i].union(operator_tree.firstPos)
            elif token == '?':
                operator_tree.nullable = True
                operator_tree.firstPos = operator_tree.leftChild.firstPos.copy()
                operator_tree.lastPos = operator_tree.leftChild.lastPos.copy()
            #print(operator_tree.key, operator_tree.firstPos, operator_tree.lastPos)
            stack.append(operator_tree)
    resulting_tree =Tree('•')
    resulting_tree.leftChild = stack.pop()
    resulting_tree.rightChild = Tree('#', {len(leaf_positions)}, {len(leaf_positions)}, False)
    followpos_table.append(set())

    resulting_tree.nullable = resulting_tree.leftChild.nullable and resulting_tree.rightChild.nullable
    if resulting_tree.leftChild.nullable:
        resulting_tree.firstPos = resulting_tree.leftChild.firstPos.union(resulting_tree.rightChild.firstPos)
    else:
        resulting_tree.firstPos = resulting_tree.leftChild.firstPos.copy()
    if resulting_tree.rightChild.nullable:
        resulting_tree.lastPos = resulting_tree.leftChild.lastPos.union(resulting_tree.rightChild.lastPos)
    else:
        resulting_tree.lastPos = resulting_tree.rightChild.lastPos.copy()
    for i in resulting_tree.leftChild.lastPos:
        followpos_table[i] = followpos_table[i].union(resulting_tree.rightChild.firstPos)
    
    #print(resulting_tree.key, resulting_tree.firstPos, resulting_tree.lastPos)

    #print('\nfollowpos table')
    # for i in range(len(followpos_table)):
    #     print(i, followpos_table[i])
    return resulting_tree, followpos_table, leaf_positions


# Builds direct aumented
def build_direct_aumented_construction_tree(postfix_expression,leaf_positions = [], followpos_table = []):
    
    unary_operators = ['*','+','?']
    binary_operators = ['|','•']
    stack = []
    

    for token in postfix_expression:
        # Checks if token is a valid operand
        if token not in unary_operators and token not in binary_operators:
            #if token is epsilon, it is nullable
            if token == 'ε':
                stack.append(Tree(token, set(), set(), True))
            else:
                stack.append(Tree(token, {len(leaf_positions)}, {len(leaf_positions)}, False))
                #print(token, {len(leaf_positions)}, {len(leaf_positions)})
                leaf_positions.append(token)
                followpos_table.append(set())

        # checks if token is a valid binary operator
        elif token in binary_operators:
            operator_tree = Tree(token)
            operator_tree.rightChild = stack.pop()
            operator_tree.leftChild = stack.pop()

            if token == '|':
                operator_tree.nullable = operator_tree.leftChild.nullable or operator_tree.rightChild.nullable
                operator_tree.firstPos = operator_tree.leftChild.firstPos.union(operator_tree.rightChild.firstPos)
                operator_tree.lastPos = operator_tree.leftChild.lastPos.union(operator_tree.rightChild.lastPos)
            elif token == '•':
                operator_tree.nullable = operator_tree.leftChild.nullable and operator_tree.rightChild.nullable
                if operator_tree.leftChild.nullable:
                    operator_tree.firstPos = operator_tree.leftChild.firstPos.union(operator_tree.rightChild.firstPos)
                else:
                    operator_tree.firstPos = operator_tree.leftChild.firstPos.copy()
                if operator_tree.rightChild.nullable:
                    operator_tree.lastPos = operator_tree.leftChild.lastPos.union(operator_tree.rightChild.lastPos)
                else:
                    operator_tree.lastPos = operator_tree.rightChild.lastPos.copy()
                for i in operator_tree.leftChild.lastPos:
                    followpos_table[i] = followpos_table[i].union(operator_tree.rightChild.firstPos)
            #(operator_tree.key, operator_tree.firstPos, operator_tree.lastPos)
            stack.append(operator_tree)
        # checks if token is a valid unary operator
        elif token in unary_operators:
            operator_tree = Tree(token)
            operator_tree.leftChild = stack.pop()
            if token == '*':
                operator_tree.nullable = True
                operator_tree.firstPos = operator_tree.leftChild.firstPos.copy()
                operator_tree.lastPos = operator_tree.leftChild.lastPos.copy()
                for i in operator_tree.lastPos:
                    followpos_table[i] = followpos_table[i].union(operator_tree.firstPos)
                
            elif token == '+':
                operator_tree.nullable = operator_tree.leftChild.nullable
                operator_tree.firstPos = operator_tree.leftChild.firstPos.copy()
                operator_tree.lastPos = operator_tree.leftChild.lastPos.copy()
                for i in operator_tree.lastPos:
                    followpos_table[i] = followpos_table[i].union(operator_tree.firstPos)
            elif token == '?':
                operator_tree.nullable = True
                operator_tree.firstPos = operator_tree.leftChild.firstPos.copy()
                operator_tree.lastPos = operator_tree.leftChild.lastPos.copy()
            #print(operator_tree.key, operator_tree.firstPos, operator_tree.lastPos)
            stack.append(operator_tree)
    resulting_tree =Tree('•')
    resulting_tree.leftChild = stack.pop()
    resulting_tree.rightChild = Tree('#', {len(leaf_positions)}, {len(leaf_positions)}, False)
    followpos_table.append(set())
    leaf_positions.append('DELIMITATOR')

    resulting_tree.nullable = resulting_tree.leftChild.nullable and resulting_tree.rightChild.nullable
    if resulting_tree.leftChild.nullable:
        resulting_tree.firstPos = resulting_tree.leftChild.firstPos.union(resulting_tree.rightChild.firstPos)
    else:
        resulting_tree.firstPos = resulting_tree.leftChild.firstPos.copy()
    if resulting_tree.rightChild.nullable:
        resulting_tree.lastPos = resulting_tree.leftChild.lastPos.union(resulting_tree.rightChild.lastPos)
    else:
        resulting_tree.lastPos = resulting_tree.rightChild.lastPos.copy()
    for i in resulting_tree.leftChild.lastPos:
        followpos_table[i] = followpos_table[i].union(resulting_tree.rightChild.firstPos)
    
    #print(resulting_tree.key, resulting_tree.firstPos, resulting_tree.lastPos)

    #print('\nfollowpos table')
    # for i in range(len(followpos_table)):
    #     print(i, followpos_table[i])
    return resulting_tree, followpos_table, leaf_positions



# Shunting yard algorithm
# Based on the wikipedia pseudocode and from from the pseudocode from geeksforgeeks
def shunting_yard(user_input):
    precedence_table= {'|':1,'•':2,'*':3,'+':3,'?':3,'(':-1,')':-1}
    operators = ['|','*','+','?','•']
    output = []
    operator_stack = []
    for token in user_input:
        if token in operators:
            while (len(operator_stack)>0 and precedence_table[token] <= precedence_table[operator_stack[-1]]):
                output.append(operator_stack.pop())
            operator_stack.append(token)
        else:
            if token != '(' and token != ')':
                output.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while (len(operator_stack)>0 and operator_stack[-1] != '('):
                    output.append(operator_stack.pop())
                operator_stack.pop()
    while (len(operator_stack)>0):
        output.append(operator_stack.pop())
    return output


# postorder traversal of the tree for drawing
def postorder_traversal_draw(tree, digraph):
    if tree:
        if tree.leftChild:
            digraph.edge(str(id(tree)), str(id(tree.leftChild)))
            postorder_traversal_draw(tree.leftChild, digraph)
        if tree.rightChild:
            digraph.edge(str(id(tree)), str(id(tree.rightChild)))
            postorder_traversal_draw(tree.rightChild, digraph)
        node_label = r"'{}'".format(tree.key)
        digraph.node(str(id(tree)), node_label)
    else:
        return
