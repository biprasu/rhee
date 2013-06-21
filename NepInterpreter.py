import re

environment = (None,{})
map_num = {u'\u0966':0, u'\u0967':1, u'\u0968':2, u'\u0969':3,
            u'\u096a':4, u'\u096b':5, u'\u096c':6, u'\u096d':7,
            u'\u096e':8 ,u'\u096f':9
            }

def get_key_from_value(my_dict, v):
#    if not v in my_dict.values():
#        return None
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

def type(data):
    return data[0][0]


def interpret(trees,env = environment):
    for tree in trees:
        stmttype,lineno = tree[0].split('_')
        lineno = int(lineno)
        if stmttype == 'string':
            return tree[1]
        elif stmttype == 'number':
            return tree[1]
        elif stmttype == 'identifier':
            return env_lookup(tree[1],env)
        elif stmttype == 'list':
            return [interpret(i,env) for i in tree[1]]
        elif stmttype == 'listItem':
            return env_lookup(tree[1], env)[int(to_ascii(interpret(tree[2], env)))]
        elif stmttype == 'parenthesis':
            return interpret(tree[1], env)
        elif stmttype == 'positive':
            return interpret(tree[1], env)
        elif stmttype == 'negative':
            return get_key_from_value(map_num, not map_num[interpret(tree[1], env)])       
        elif stmttype == 'println' or stmttype == 'print':
            for data in tree[1]:
                print interpret(data, env),
            if stmttype == 'println':   print
        elif stmttype == 'assignment':
            env_update(tree[1], interpret(tree[2],env), env)
            #print env
        elif stmttype == 'increment':
            pass
        elif stmttype == 'binop':
            operator = tree[1]
            if operator == u'\u0935\u093e':
                return get_key_from_value(map_num, map_num[interpret(tree[2], env)] or map_num[interpret(tree[3], env)])

#            if type(tree[2]) != type(tree[3]):
#                print 'error: type mismatch'
#                return

            if type(tree[2]) == 'list':
                return interpret(tree[2], env) + interpret(tree[3], env)

            left_value = to_ascii(interpret(tree[2], env))
            right_value = to_ascii(interpret(tree[3], env))

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
            while map_num[interpret(tree[1], env)]:
                interpret(tree[2], env)

        elif stmttype == 'ifelse':
            interpret(tree[1], env)
        elif stmttype == 'yedi':
            if map_num[interpret(tree[1], env)]:
                interpret(tree[2])
                return
        elif stmttype == 'elseif':
            if map_num[interpret(tree[1], env)]:
                interpret(tree[2], env)
                return
        elif stmttype == 'else':
            interpret(tree[1], env)

        elif stmttype == 'conditionalbinop':
            operator = tree[1]
            if operator == u'\u0930':
                return get_key_from_value(map_num, map_num[interpret(tree[2], env)] and map_num[interpret(tree[3], env)])
            elif operator == u'\u0935\u093e':
                return get_key_from_value(map_num, map_num[interpret(tree[2], env)] or map_num[interpret(tree[3], env)])

        elif stmttype == 'forloop':
            env_update(tree[1], interpret(tree[2], env), env) 

            start = int(to_ascii(interpret(tree[2], env)))
            end = int(to_ascii(interpret(tree[3], env)))
            inc = int(to_ascii(interpret(tree[5], env)))
            temp = start

            inc = (tree[4]== u'-') and -1*inc or 1*inc
            for i in range(start, end, inc):
                interpret(tree[6], env)
                temp += inc
                env_update(tree[1], to_unicode(temp), env)

        elif stmttype == 'conditional':
            return map_num[interpret(tree[1], env)] and interpret(tree[2], env) or interpret(tree[3], env)

        elif stmttype == 'listAssignment':
            env_update(tree[1], [interpret(i, env) for i in tree[2]], env)

        elif stmttype == 'functionDefination':
            fname = tree[1]
            fparams = tree[2]
            fbody = tree[3]
            fvalue = ("function", fparams, fbody, env)
            add_to_env(env, fname, fvalue)

        elif stmttype == 'functionCall':
            fname = tree[1]
            args = tree[2]
            fvalue = env_lookup(fname,env)
            #print fvalue
            if fvalue[0] == "function":
                fparams = fvalue[1]
                fbody = fvalue[2]
                fenv = fvalue[3]
                newenv = (fenv, {})
                if len(fparams) != len(args):
                    print "wrong number of args"
                    return
                else:
                    for i in range(len(args)):
                        argval = interpret(args[i], env)
                        (newenv[1])[fparams[i]] = argval 
                result = interpret(fbody,newenv)
                return (result != None) and result or None

        elif stmttype == 'returnStmt':
            return [interpret(i, env) for i in tree[1]]                                     



def add_to_env(env,vname,value):
    env[1][vname] = value

def env_update(vname,value,env):
    if vname in env[1]:
        (env[1])[vname] = value
    # elif not (env[0]== None):
    #     env_update(vname,value,env[0])
    elif vname in environment[1]:
        (environment[1])[vname] = value
    else:
        (env[1])[vname] = value

    

def env_lookup(vname, env):
    if vname in env[1]:
        return (env[1])[vname]
    # elif env[0] == None:
    #     return None
    # else:
    #     return env_lookup(vname, env[0])
    elif vname in environment[1]:
        return (environment[1])[vname]
    else:
        pass
        #error