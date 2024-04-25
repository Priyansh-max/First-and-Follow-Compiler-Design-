
# def non_terminalf(grammar): 
#     lst = []
#     for key , value in grammar.items():
#         lst.append(key)
        
#     return lst

# def rec_topdown(grammar , productions , str , i ,j, non_terminals):
#     if i == len(str):
#         return True
#     for production in productions:
#         for curr_nonterm in production:
#             if curr_nonterm in non_terminals:
#                 rec_topdown(grammar , grammar[curr_nonterm] , str , i , j+1 , non_terminals)
#             elif curr_nonterm == '~':
#                 continue
#             elif curr_nonterm not in non_terminals and curr_nonterm == str[i]:
#                 i = i + 1
#                 print(i)
#             else:
#                 print("Hi")
#                 return False
                           
# grammar = {
#     'S': ['A1S', '~'],
#     'A': ['01A', '11'],
# }
# non_terminals = non_terminalf(grammar)
# str = input("Enter a string to parse : ")
# ans = rec_topdown(grammar , 'S' , str , 0 ,0, non_terminals)
# ans = False
# for productions in grammar['S']:
#     ans = ans or rec_topdown(grammar , productions , str , 0 ,0, non_terminals)

# print(ans)

input_str = ""
idx = 0
error = False

def match(c):
    global idx, error
    if input_str[idx] == c:
        idx += 1
    else:
        error = True

def A():
    global idx, error
    if input_str[idx] == '0':
        match('0')
        match('1')
        A()
    elif input_str[idx] == '1':
        match('1')
        match('1')
    else:
        error = True

def S():
    global idx, error
    if input_str[idx] == '0' or input_str[idx] == '1':
        A()
        match('1')
        S()
    elif input_str[idx] == '~':
        match('~')
    else:
        error = True

input_str = "111~"

S()

if idx == len(input_str) and not error:
    print("Valid Expression")
else:
    print("Invalid Expression")

    