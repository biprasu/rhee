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
            return map_num[interpret(tree[1])]
        elif stmttype == 'negative':
            return not map_num[interpret(tree[1])]       
        elif stmttype == 'print':
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
            left_value = right_value = ''
            num = interpret(tree[2])
            for char in num:
                left_value += (char == '-') and '-' or ((char=='.') and '.' or str(map_num[char]))
            num = interpret(tree[3])
            for char in num:
                right_value += (char == '-') and '-' or ((char=='.') and '.' or  str(map_num[char]))
            left_value = float(left_value)
            right_value = float(right_value)

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
            result = u''
            for char in str(num):
                result += (char == '-' ) and '-' or ((char=='.') and '.' or get_key_from_value(map_num, int(char)))
            return result

        elif stmttype == 'whileloop':
            while interpret(tree[1]):
                interpret(tree[2])

