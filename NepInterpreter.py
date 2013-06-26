#encoding=UTF8
import re
import sys
import traceback

from NepInterpreterLibrary import ArgumentError, BreakError,ContinueError, checklibrary, call
#from NepGUI import writetogui

errors ={
    'ZeroDivisionError': 'शुन्य ले भाग गरियो',
    'NameError' : 'नाम मिलेन',
    'IOError' : 'फाइलमा गल्ति भएको छ',
    'IndexError': 'संग्रह को अकं मिलेन',
    'KeyError' : 'कोशमा नाम मिलेन',
    'ArgumentError' : 'काम को आरगुमेन्ट मिलेन',
    'BreakError' :u'यहा राख्न पाइन्न',
    'ContinueError' : u'यहा राख्न पाइन्न',
    'NotANumber'    : 'दिईएको अर्गुमेन्त अङ्क होइन ',
}

environment = (None,{})
map_num = {u'\u0966':0, u'\u0967':1, u'\u0968':2, u'\u0969':3,
            u'\u096a':4, u'\u096b':5, u'\u096c':6, u'\u096d':7,
            u'\u096e':8 ,u'\u096f':9
            }

def listtostring(k):
    s = u"["
    for elements in k:
        s += elements
        s += u","
    s += "]"
    return s

def get_key_from_value(my_dict, v):
#    if not v in my_dict.values():
#        return None
    for key,value in my_dict.items():
        if value == v:
            return key
    return None

def to_ascii(num):

    if not ( isinstance(num,str) or isinstance(num,unicode)):
        return num

    ascii = ''
    for char in num:
        if char in map_num:
            ascii += (char == '-') and '-' or ((char=='.') and '.' or str(map_num[char]))
        else:
            return num
    if ascii.find('.') == -1:
        return int(ascii)
    else:
        return float(ascii)

def to_unicode(num):
    if num is None:
        raise NameError
    if not(isinstance(num,int) or isinstance(num,float) ):
        return num
    unic = u''

    for char in str(num):
        unic += (char == '-' ) and '-' or ((char=='.') and '.' or get_key_from_value(map_num, int(char)))
    return unic

def _type(data, env):
    dtype = data[0][0]
    dtype = dtype[:-2]
    if dtype != 'identifier':   return data[0][0]
    return type(env_lookup(data[0][1], env))==list and "list" or "number"

gui = None
def interpret(trees,env = environment,tb=None):
    global gui

    if tb:
        gui = tb
    if not env:
        env = environment
    for tree in trees:

        if not tree:
            continue
        stmttype,lineno = tree[0].split('_')
        lineno = int(lineno)

        try:
        #These two errors will be caught by the loops
            if stmttype == 'blankLine':
                pass
            elif stmttype == 'break':
                raise BreakError()
            elif stmttype == 'continue':
                raise ContinueError()
            elif stmttype == 'string':
                return tree[1]
            elif stmttype == 'sunya':
                return None
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
            elif stmttype == 'slicing':
                return env_lookup( tree[1],env)[(tree[2] and int(to_ascii(interpret(tree[2],env))) or 0):(tree[3] and int(to_ascii(interpret(tree[3],env))) or None)]
            elif stmttype == 'input':
                env_update(tree[1],gui.getInputData(),env)

            elif stmttype == 'println' or stmttype == 'print':
                for data in tree[1]:
                    a = interpret(data,env)
                    if a:
                        #print interpret(data, env),
                        result = interpret(data,env)
                        if isinstance(result,list):
                            result = listtostring(result)
                        gui.tc3.SetValue(gui.tc3.GetValue() + result)
                    else:
                        #print u"शुन्य",
                        gui.tc3.SetValue(gui.tc3.GetValue() + u"शुन्य")
                if stmttype == 'println':   gui.tc3.SetValue(gui.tc3.GetValue()+u"\n")
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

                if _type(tree[2], env) == 'list' and operator == '+' :
                    return interpret(tree[2], env) + interpret(tree[3], env)
                

                # if _type(tree[2] ,env) == 'string' and operator == '+':
                #     return interpret(tree[2], env) + interpret(tree[3], env)

                left_value = None if tree[2] == u"शुन्य" else to_ascii(interpret(tree[2], env))
                right_value = None if tree[2] == u"शुन्य" else to_ascii(interpret(tree[3], env))

                if operator == '^':
                    num = left_value**right_value
                elif operator == '+':
                    num = left_value + right_value
                elif operator == '-':
                    num = left_value - right_value
                elif operator == '*':
                    print left_value, right_value
                    num = left_value * right_value
                elif operator == '/':
                    num = left_value / right_value
                elif operator == '%':
                    num = left_value % right_value
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
                    try:
                        for items in tree[2]:
                            interpret([items], env)
                    except BreakError:
                        break
                    except ContinueError:
                        continue

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
                if operator == u'\u0930': #RA
                    return get_key_from_value(map_num, map_num[interpret(tree[2], env)] and map_num[interpret(tree[3], env)])
                elif operator == u'\u0935\u093e': #WA
                    return get_key_from_value(map_num, map_num[interpret(tree[2], env)] or map_num[interpret(tree[3], env)])

            elif stmttype == 'forloop':
                env_update(tree[1], interpret(tree[2], env), env)

                start = int(to_ascii(interpret(tree[2], env)))
                end = int(to_ascii(interpret(tree[3], env)))
                inc = int(to_ascii(interpret(tree[5], env)))
                temp = start

                inc = (tree[4]== u'-') and -1*inc or 1*inc
                for i in range(start, end, inc):
                    try:
                        for items in tree[6]:
                            type = items[0].split('_')[0]
                            if type == 'break':
                                raise BreakError()
                            elif type == 'continue':
                                raise ContinueError()
                            interpret([items], env)
                    except BreakError:
                        break
                    except ContinueError:
                        temp += inc
                        env_update(tree[1], to_unicode(temp), env)
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

                if env_exists(fname,env):
                    fvalue = env_lookup(fname,env)
                else:
                    fvalue = [None]
                #check local function
                if fvalue[0] == "function":
                    fparams = fvalue[1]
                    fbody = fvalue[2]
                    fenv = fvalue[3]
                    newenv = (fenv, {})
                    if len(fparams) != len(args):
                        raise ArgumentError()
                    else:
                        for i in range(len(args)):
                            argval = interpret(args[i], env)
                            (newenv[1])[fparams[i]] = argval
                    result = interpret(fbody,newenv)
                    return (result != None) and result or None

                elif checklibrary(tree):
                    return call (tree,env)
                else:
                    raise ArgumentError()

            elif stmttype == 'returnStmt':
                return [interpret(i, env) for i in tree[1]]
        except SystemExit:
            exit(-1)

        except Exception,e:
            if e.__class__.__name__ == "BreakError":
                raise BreakError()
            if e.__class__.__name__ == "ContinueError":
                raise ContinueError()

            #print traceback.format_exc()
            errormessage = to_unicode (lineno) + u" लाइनमा गल्ति भयो\n"
            errormessage += unicode(traceback.format_exc(),encoding="UTF8") + u"\n"
            #errorname = e.__class__.__name__
            #errormessage = errors.get(errorname)
            raise Exception(unicode(errormessage))





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


def env_exists(vname,env):
    if vname in env[1]:
        return True
    elif vname in environment[1]:
        return True
    else:
        return False
        #error


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
        raise NameError
        #error