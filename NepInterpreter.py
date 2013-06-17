import re

environment = (None,{})
map_num = {u'\u0966':0, u'\u0967':1, u'\u0968':2, u'\u0969':3,
            u'\u096a':4, u'\u096b':5, u'\u096c':6, u'\u096d':7,
            u'\u096e':8 ,u'\u096f':9
            }

def get_key_from_value(my_dict, v):
    for key,value in my_dict.items():
        if value == v:
            return key
    return None

def to_ascii(num):
    ascii = ''
    for char in num:
                ascii += (char == '-') and '-' or ((char=='.') and '.' or str(map_num[char]))
    return float(ascii)

def to_unicode(num):
    unic = u''
    for char in str(num):
        unic += (char == '-' ) and '-' or ((char=='.') and '.' or get_key_from_value(map_num, int(char)))
    return unic


def interpret(trees,env = environment):
    for tree in trees:
        stmttype = tree[0]
        if stmttype == 'string':
            return tree[1]
        elif stmttype == 'number':
            return tree[1]
        elif stmttype == 'identifier':
            return env[1][tree[1]]
        elif stmttype == 'parenthesis':
            return interpret(tree[1])
        elif stmttype == 'positive':
            return interpret(tree[1])
        elif stmttype == 'negative':
            return get_key_from_value(map_num, not map_num[interpret(tree[1])])       
        elif stmttype == 'println' or stmttype == 'print':
            for data in tree[1]:
                print interpret(data),
            print
        elif stmttype == 'assignment':
            env[1][tree[1]] = interpret(tree[2])
            #print env
        elif stmttype == 'increment':
            pass
        elif stmttype == 'binop':
            operator = tree[1]
            if operator == u'\u0935\u093e':
                return get_key_from_value(map_num, map_num[interpret(tree[2])] or map_num[interpret(tree[3])])

            left_value = to_ascii(interpret(tree[2]))
            right_value = to_ascii(interpret(tree[3]))

            if operator == '^':
                num = left_value**right_value
            elif operator == '+':
                num = left_value + right_value
            elif operator == '-':
                num = left_value - right_value
            elif operator == '*':
                num = left_value * right_value     
            elif operator == '/':
                num = left_value / right_value                            
            elif operator == '<':
                num = left_value < right_value 
                return (left_value < right_value) and u'\u0967' or u'\u0966'
            elif operator == '>':
                num = left_value > right_value
                return (left_value > right_value) and u'\u0967' or u'\u0966'
            elif operator == '<=':
                num = left_value <= right_value 
                return (left_value <= right_value) and u'\u0967' or u'\u0966'
            elif operator == '>=':
                num = left_value >= right_value  
                return (left_value >= right_value) and u'\u0967' or u'\u0966'                
            elif operator == '==':
                return (left_value == right_value) and u'\u0967' or u'\u0966'
            elif operator == '!=':
                return (left_value != right_value) and u'\u0967' or u'\u0966'   
                         
            return to_unicode(num)

        elif stmttype == 'whileloop':
            while map_num[interpret(tree[1])]:
                interpret(tree[2])

        elif stmttype == 'ifelse':
            interpret(tree[1])
        elif stmttype == 'yedi':
            if map_num[interpret(tree[1])]:
                interpret(tree[2])
                return
        elif stmttype == 'elseif':
            if map_num[interpret(tree[1])]:
                interpret(tree[2])
                return
        elif stmttype == 'else':
            interpret(tree[1])

        elif stmttype == 'conditionalbinop':
            operator = tree[1]
            if operator == u'\u0930':
                return get_key_from_value(map_num, map_num[interpret(tree[2])] and map_num[interpret(tree[3])])
            elif operator == u'\u0935\u093e':
                return get_key_from_value(map_num, map_num[interpret(tree[2])] or map_num[interpret(tree[3])])

        elif stmttype == 'forloop':
            env[1][tree[1]] = interpret(tree[2])

            start = int(to_ascii(interpret(tree[2])))
            end = int(to_ascii(interpret(tree[3])))
            inc = int(to_ascii(interpret(tree[5])))
            temp = start

            inc = (tree[4]== u'-') and -1*inc or 1*inc
            for i in range(start, end, inc):
                interpret(tree[6])
                temp += inc
                env[1][tree[1]] = to_unicode(temp)

        elif stmttype == 'conditional':
            return map_num[interpret(tree[1])] and interpret(tree[2]) or interpret(tree[3])