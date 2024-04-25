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
    stack = []
    while True:
        if input_str[idx] == '0':
            match('0')
            match('1')
        elif input_str[idx] == '1':
            match('1')
            match('1')
        else:
            error = True
            break
        if input_str[idx] != '0':
            break

def S():
    global idx, error
    stack = []
    while True:
        if input_str[idx] == '0' or input_str[idx] == '1':
            A()
            match('1')
        elif input_str[idx] == '~':
            match('~')
            break
        else:
            error = True
            break

input_str = "111~"
S()

if idx == len(input_str) and not error:
    print("Valid Expression")
else:
    print("Invalid Expression")
