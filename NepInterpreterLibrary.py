#encoding=UTF8

import os
import codecs
from Tkinter import *
import NepInterpreter as NI


class ArgumentError(Exception):
    pass

class BreakError(Exception):
    pass

class ContinueError(Exception):
    pass

to_col = {

    u"रातो" : "red",
    u"हरियो" : "green",
    u"निलो" : "blue",
    u"खैरो" : "brown",
    u"सुन्तला" : "orange",
    u"कालो" : "black",
    u"सेतो" : "white",
    u"पहेलो" : "yellow",
    u"प्याजि" : "purple",
    u"रानि" : "pink",
}

keyboard_keys = []

def keyboardhandler(event):
    global keyboard_keys
    keyboard_keys.append(event.keycode)
    return


def keyboardgetkeys(args,env):
    if args:
        raise ArgumentError()
    global keyboard_keys
    if keyboard_keys:
        return NI.to_unicode (keyboard_keys.pop(0))
    else:
        return NI.to_unicode(0)



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


def initgraphics(args,env):
    root = Tk()
    if len(args) < 3:
        raise ArgumentError()

    name = NI.interpret(args[0],env)
    name = name.encode('UTF8')
    height = int(NI.to_ascii(NI.interpret(args[1],env)))
    width = int(NI.to_ascii(NI.interpret(args[2],env)))
    root.title(name)
    root.configure(height=height, width=width)  #set width and height
    root.resizable(0,0)                         #disable resizing
    canvas = Canvas(root,width=width,height=height)
    canvas.pack(fill='both')

    #hide the windows
    root.withdraw()
    root.bind("<Key>",keyboardhandler)
    return root,canvas


def hidegraphics(args,env):
    if len(args) != 1:
        raise ArgumentError()
    root,canvas = NI.env_lookup(args[0],env)
    root.withdraw()
    return

def showgraphics(args,env):
    if len(args) != 1:
        raise ArgumentError()
    root,canvas = NI.env_lookup(args[0],env)
    root.deiconify()
    root.update()
    return

def cleargraphics(args,env):
    if len(args) != 1:
        raise ArgumentError()
    root,canvas = NI.env_lookup(args[0],env)
    canvas.delete(ALL)
    root.update()
    return

def updategraphics(args,env):
    if len(args) != 1:
        raise ArgumentError()
    root,canvas = NI.env_lookup(args[0],env)
    root.update()
    return


def drawgraphics(args,env):
    interpreted_args = [NI.env_lookup(args[0],env)]
    args = args[1:] #discard the root/canvas info
    for arg in args:
        if isinstance(arg,tuple) or isinstance(arg,list):
            interpreted_args.append(NI.interpret(arg))
        else:
            interpreted_args.append(arg)
    if interpreted_args[1] == u"गोलो":
        drawcircle(interpreted_args)
    elif interpreted_args[1] == u"कोठा":
        drawrectangle(interpreted_args)
    elif interpreted_args[1] == u"लाइन":
        drawline(interpreted_args)
    elif interpreted_args[1] == u"डट":
        drawpoint(interpreted_args)
    elif interpreted_args[1] == u"शब्द":
        drawtext(interpreted_args)
    return


def drawpoint(args):
    if len(args)<4 or len(args) > 6:
        raise ArgumentError()
    c1 = int(NI.to_ascii(args[2]))
    c2 = int(NI.to_ascii(args[3]))
    width = int(NI.to_ascii(args[4])) if args[4] else None
    outline = to_col[args[5]] if args[5] else None
    root,canvas = args[0]
    canvas.create_rectangle(c1,c2,c1,c2,width=width,outline=outline)
    root.update()
    return

def drawtext(args):
    if len(args)<5 or len(args) > 7:
        raise ArgumentError()
    c1 = int(NI.to_ascii(args[2]))
    c2 = int(NI.to_ascii(args[3]))
    text = args[4].encode("UTF8")
    size = int(NI.to_ascii(args[5])) if args[5] else None
    color = to_col[args[6]] if args[6] else None
    font = "a " + str(size) if size is not None else "0 "
    root,canvas = args[0]
    canvas.create_text(c1,c2,text=text,font=font,fill=color,anchor="nw")
    root.update()
    return

def drawline(args):
    'requires the canvas, 4 coords compulsory and width and foreground color optional'
    if len(args) < 6 or len(args) > 8:
        raise ArgumentError()
    root,canvas = args[0]
    c1 = int(NI.to_ascii(args[2]))
    c2 = int(NI.to_ascii(args[3]))
    c3 = int(NI.to_ascii(args[4]))
    c4 = int(NI.to_ascii(args[5]))
    width = int(NI.to_ascii(args[6])) if args[6] else None
    fill = to_col[args[7]] if args[7] else None
    canvas.create_line(c1,c2,c3,c4,width=width,fill=fill)
    canvas.update()
    return



def drawcircle(args):
    'requres canvas, 2 coords, radius compulsory; width, outline, fill optional'
    if len(args) < 5 or len(args) > 8:
        raise ArgumentError()
    root,canvas = args[0]
    x = int(NI.to_ascii(args[2]))
    y = int(NI.to_ascii(args[3]))
    r = int(NI.to_ascii(args[4]))
    width = int(NI.to_ascii(args[5]))
    outline = to_col[args[6]] if args[6] else None
    fill = to_col[args[7]] if args[7] else None
    canvas.create_oval(x-r,y-r,x+r,y+r,width=width,fill=fill,outline=outline)
    canvas.update()
    return

def drawrectangle(args):
    'requires the canvas, 4 coords compulsory and width and foreground color optional'
    if len(args) < 6 or len(args) > 9:
        raise ArgumentError()
    root,canvas = args[0]
    c1 = int(NI.to_ascii(args[2]))
    c2 = int(NI.to_ascii(args[3]))
    c3 = int(NI.to_ascii(args[4]))
    c4 = int(NI.to_ascii(args[5]))
    width = int(NI.to_ascii(args[6])) if args[6] else None
    outline = to_col[args[7]] if args[7] else None
    fill = to_col[args[8]] if args[8] else None
    canvas.create_rectangle(c1,c2,c3,c4,width=width,fill=fill,outline=outline)
    canvas.update()
    return





function_names = {
    u'फाइलखोल' : openfile,
    u'__बन्दगर__' : closefile,
    u"__फाइलपढ__" : readfile,
    u"__फाइललेख__" : writefile,
    u"__फाइललेखलाइन__" : writefileln,
    u"चित्र" : initgraphics,
    u"__देखाउ__" : showgraphics,
    u"__लुकाउ__" : hidegraphics,
    u"__बनाउ__" : updategraphics,
    u"__मेटाउ__" : cleargraphics,
    u"__कोर__" : drawgraphics,
    u"बटन" : keyboardgetkeys,
}


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

