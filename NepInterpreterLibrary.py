#encoding=UTF8

import os
import codecs

import NepInterpreter as NI

def openfile(args,env):
    filename = NI.interpret(args[0],env)
    mode = NI.interpret(args[1],env)
    if mode == u'लेख्न':
        return codecs.open(filename,"w",encoding="UTF8")
    elif mode == u'पढ्न':
        if not os.path.exists(filename):
            raise IOError
            #return a generator, then we'll just do writes

        #return the file, but also save the generator so as to use it later
        file = codecs.open(filename,"r",encoding="UTF8")
        filename += u"generator"
        gen = (i for i in file.readlines())
        return file,gen

    elif mode == u'जोड्न':
        return codecs.open(filename,"a",encoding="UTF8")


def readfile(args,env):
    id = args[0]
    file,filegen = NI.env_lookup(id,env)
    try:
        a = filegen.next()
        return a[:-1]
    except StopIteration:
        return None


def writefile(args,env):
    id = args[0]
    file = NI.env_lookup(id,env)
    for items in args[1]:
        a = NI.interpret(items,env)
        file.write(a)
    return

def writefileln(args,env):
    id = args[0]
    file = NI.env_lookup(id,env)
    for items in args[1]:
        file.write(NI.interpret(items,env))
    file.write(u"\n")
    return

def closefile(args,env):
    id = args[0]
    file = NI.env_lookup(id,env)
    if (isinstance(file,tuple)):
        file[0].close()
    else:
        file.close()



function_names = {
    u'फाइलखोल' : openfile,
    u'बन्दगर' : closefile,
    u"फाइलपढ" : readfile,
    u"फाइललेख" : writefile,
    u"फाइललेखलाइन" : writefileln,
}


class ArgumentError(Exception):
    pass

def checklibrary(tree):
    fname = tree[1]
    if fname not in function_names:
        return False
    return True

def call(tree,env):
    fname = tree[1]
    args = tree[2]
    #call with args
    return function_names[fname](args,env)

