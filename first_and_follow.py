from collections import OrderedDict
from ordered_set import OrderedSet
import pandas as pd

#to check for non_terminal symbols

def parse_csv_to_grammar(csv_file):
    grammar = {}

    df = pd.read_csv(csv_file, header=None, delim_whitespace=True)
    for index, row in df.items():
        for production in row[0:]:
            productions = []
            non_terminal = production[0]
            str = ""
            for i in production[1:]:
                if i == ',' or i == "":
                    continue
                else:
                    str = str + i
            if non_terminal in grammar.keys():
                grammar[non_terminal].append(str)
            else:
                productions.append(str)
                grammar[non_terminal] = productions

    return grammar

def non_terminalf(grammar): 
    lst = []
    for key , value in grammar.items():
        lst.append(key)
        
    return lst

#to calculate the first of a all the non-terminal in given grammar

def compute_first(grammar):
    first = {}
    lst = non_terminalf(grammar)
    for non_terminal in grammar:
        first[non_terminal] = OrderedSet()
    while True:
        for non_terminal, productions in grammar.items():
            for production in productions:
                for i in production:
                    if i in lst:
                        first[non_terminal].add(i)
                    else:
                        first[non_terminal].add(i)
                        break                   
        break
    
    lst1 = non_terminalf(first)
    found = False
    for k , v in first.items():
        print(k)
        print(v)
        intersection = {'~'}
        for j in v:
            if j in lst1:
                intersection = intersection & first[j]
                
        for non_term in v:
            if non_term in lst1:
                if '~' in intersection: #case to include epsilon only when it is present in both the non terminals
                    first[k] = first[k] - {non_term} | first[non_term]
                    print(first , "hi")
                else:
                    first[k] = first[k] - {non_term} | first[non_term] - '~'
                    found = True
                    break
        if found:
            first[k] -= lst1
            break         
    
    return first


def compute_follow(grammar, first):
    follow = {}
    lst = non_terminalf(grammar)
    for non_terminal in grammar:
        follow[non_terminal] = set()
    follow[list(grammar.keys())[0]].add('$')  # Start symbol
    
    while True:
        updated = False  # Flag to track if any changes were made in this iteration
        for non_terminal, productions in grammar.items():
            for production in productions:
                for i, symbol in enumerate(production):
                    if symbol in lst:
                        if i < len(production) - 1:
                            # If the current symbol is a non-terminal
                            next_symbol = production[i + 1]
                            if next_symbol in lst: # Case 1: If the next symbol is a non-terminal Add FIRST of next_symbol to FOLLOW of symbol
                                if '~' in first[next_symbol]:
                                    follow[symbol] |= first[next_symbol] - '~'
                                    follow[symbol].add(next_symbol)
                            else:
                                follow[symbol].add(next_symbol)
                        else:
                            # Case 2: If the current symbol is the last symbol in production
                            # Add FOLLOW[non_terminal] to FOLLOW[symbol]
                            follow[symbol] |= follow[non_terminal]

        if not updated:
            break
    
    #handling the case where follow of those non-terminal symbols which had epison in there first
    for k , v in follow.items():
        for non_terminal in v:
            if non_terminal in lst:
                follow[k] |= follow[non_terminal]
                follow[k] -= non_terminal
                   
    return follow

# ***************************************************************IMPLEMENTED LL(1) Parsing table********************************************************************

def generate_parsing_table(grammar, first, follow):
    non_terminals = list(grammar.keys())
    terminals = {'$'}
    for productions in grammar.values():
        for production in productions:
            for i in production:
                if i not in non_terminals and i != '~':
                    terminals.update(set(i))
                    
    print(terminals)
            

    parsing_table = pd.DataFrame(index=non_terminals , columns=terminals)

    for non_terminal, productions in grammar.items():
        for production in productions:
            for i in production:
                if(i in non_terminals):
                    if '~' in first[i]: #checking condition if epsilon is present in first(alpha)
                        for j in follow[non_terminal]: #if yes then using follow 
                            parsing_table.at[non_terminal,j] = production
                    else:
                        for k in first[i]: #if no then using first
                            parsing_table.at[non_terminal,k] = production 
                    break
                elif i == '~':
                    for j in follow[non_terminal]:
                            parsing_table.at[non_terminal,j] = production
                          
                else:
                    parsing_table.at[non_terminal,i] = production
                    

    return parsing_table

# Define your grammar here

""" S --> A1S
    S --> ~
    A --> 01A
    A --> 11
"""

csv_file = "grammar.csv"
grammar = parse_csv_to_grammar(csv_file)

print(grammar)


# grammar = {
#     'S': ['A1S', '~'],
#     'A': ['01A', '11'],
# }

# print(grammar)

# grammar = {
#     'S': ['aBDh'],
#     'B': ['cC'],
#     'C': ['bc', '~'],
#     'D': ['EF'],
#     'E': ['g', '~'],
#     'F': ['f', '~'],
# }



first = compute_first(grammar)

print("FIRST sets:")
for non_terminal, first_set in first.items():
    print(non_terminal, ": ", set(first_set))

follow = compute_follow(grammar, first)
print("\nFOLLOW sets:")
for non_terminal, follow_set in follow.items():
    print(non_terminal, ": ", set(follow_set))


parsing_table = generate_parsing_table(grammar, first, follow)
print("\nParsing Table:")
print(parsing_table)

