from collections import OrderedDict
from ordered_set import OrderedSet

#to check for non_terminal symbols

def non_terminalf(grammar): 
    lst = []
    for key , value in grammar.items():
        lst.append(key)
        
    return lst

#to calculate the first of a all the non-terminal in given grammar

def compute_first(grammar):
    first = {}
    lst = non_terminalf(grammar)
    print(lst)
    for non_terminal in grammar:
        first[non_terminal] = OrderedSet()
    print(first)
    while True:
        changes = False
        for non_terminal, productions in grammar.items():
            for production in productions:
                for i in production:
                    if i in lst:
                        first[non_terminal].add(i)
                    else:
                        first[non_terminal].add(i)
                        break                   
        break
    
    print(first)
    
    lst1 = non_terminalf(first)
    found = False
    for k , v in first.items():
        print(k)
        print(v)
        intersection = {'~'}
        for j in v:
            if j in lst1:
                intersection = intersection & first[j]
                
        print(intersection , "hiiiiii")
        for non_term in v:
            print(non_term)
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
    for non_terminal in grammar:
        follow[non_terminal] = set()
    follow[list(grammar.keys())[0]].add('$')  # Start symbol
    while True:
        changes = False
        for non_terminal, productions in grammar.items():
            for production in productions:
                for i, symbol in enumerate(production):
                    if symbol in grammar:
                        if i == len(production) - 1:
                            old_length = len(follow[symbol])
                            follow[symbol] |= follow[non_terminal]
                            if len(follow[symbol]) != old_length:
                                changes = True
                        else:
                            next_symbols = production[i + 1:]
                            epsilon_exists = True
                            for next_symbol in next_symbols:
                                if next_symbol not in first:
                                    epsilon_exists = False
                                    break
                                if '' not in first[next_symbol]:
                                    epsilon_exists = False
                                    break
                            if epsilon_exists:
                                old_length = len(follow[symbol])
                                follow[symbol] |= follow[non_terminal]
                                if len(follow[symbol]) != old_length:
                                    changes = True
                                follow[symbol] -= {''}
                            for next_symbol in next_symbols:
                                if next_symbol in first:
                                    if '' not in first[next_symbol]:
                                        old_length = len(follow[symbol])
                                        follow[symbol] |= first[next_symbol]
                                        if len(follow[symbol]) != old_length:
                                            changes = True
                                        break
        if not changes:
            break
    return follow


# Example grammar
grammar = {
    'S': ['A1S', '~'],
    'A': ['01A', '11'],
}

# grammar = {
#     'S': ['AB'],
#     'A': ['a','~'],
#     'B': ['b'],
# }


first = compute_first(grammar)

print(first)
print("FIRST sets:")
for non_terminal, first_set in first.items():
    print(non_terminal, ": ", set(first_set))

# follow = compute_follow(grammar, first)
# print("\nFOLLOW sets:")
# for non_terminal, follow_set in follow.items():
#     print(non_terminal, ": ", follow_set)
