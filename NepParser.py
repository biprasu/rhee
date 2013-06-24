#encoding=UTF8
import ply.yacc as yacc
from NepInterpreter import interpret
from sys import argv,exit

start = "N"

precedence = (
    ('left', 'IDENTIFIER'),
    ('left', 'EQ'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'POWER'),
    )

def p_N(p):
    'N : element NEWLINE N'
    p[0] = [p[1]] + p[3]
def p_N_lastone(p):
    'N : element'
    p[0] = [p[1]]
def p_N_empty(p):
    'N : '
    p[0] = []



def p_element_stmt(p):
    'element : stmt'
    p[0] = p[1]

def p_stmt_assign(p):
    'stmt : IDENTIFIER ASSIGNMENT exp'
    p[0] = ("assignment"+"_"+str(p.lineno(2)), p[1], [p[3]])


#Pravesh added these

def p_stmt_break(p):
    'stmt : BAHIRA'
    p[0] = ("break"+"_"+str(p.lineno(1)),)

def p_stmt_continue(p):
    'stmt : ARKO'
    p[0] = ("continue"+"_"+str(p.lineno(1)),)

def p_stmt_filewritewithnewline(p):
    'stmt : IDENTIFIER MA dynamString LEKHA SEMICOLON'
    p[0] = ("assignment"+"_"+str(p.lineno(1)),"temp",[("functionCall"+"_"+str(p.lineno(1)), u"__फाइललेख__",[p[1],p[3]])])

def p_stmt_filewrite(p):
    'stmt : IDENTIFIER MA dynamString LEKHA'
    p[0] = ("assignment"+"_"+str(p.lineno(1)),"temp", [("functionCall"+"_"+str(p.lineno(1)), u"__फाइललेखलाइन__",[p[1],p[3]])])

def p_stmt_fileread(p):
    'stmt : IDENTIFIER BATA IDENTIFIER LEU'
    p[0] = ("assignment"+"_"+str(p.lineno(1)),p[3], [("functionCall"+"_"+str(p.lineno(1)), u"__फाइलपढ__",[p[1]])])

def p_stmt_fileclose(p):
    'stmt : IDENTIFIER BANDAGARA'
    p[0] = ("assignment"+"_"+str(p.lineno(1)),"temp", [("functionCall"+"_"+str(p.lineno(1)), u"__बन्दगर__", [p[1]])])

def p_stmt_graphicshow(p):
    'stmt : IDENTIFIER DEKHAU'
    p[0] = ("assignment"+"_"+str(p.lineno(1)),"temp", [("functionCall"+"_"+str(p.lineno(1)), u"__देखाउ__", [p[1]])])

def p_stmt_graphichide(p):
    'stmt : IDENTIFIER LUKAU'
    p[0] = ("assignment"+"_"+str(p.lineno(1)),"temp", [("functionCall"+"_"+str(p.lineno(1)), u"__लुकाउ__", [p[1]])])

def p_stmt_graphicupdate(p):
    'stmt : IDENTIFIER BANAU'
    p[0] = ("assignment"+"_"+str(p.lineno(1)),"temp", [("functionCall"+"_"+str(p.lineno(1)), u"__बनाउ__", [p[1]])])

def p_stmt_graphiclear(p):
    'stmt : IDENTIFIER METAU'
    p[0] = ("assignment"+"_"+str(p.lineno(1)),"temp", [("functionCall"+"_"+str(p.lineno(1)), u"__मेटाउ__", [p[1]])])

# single rule to draw all graphics
def p_stmt_graphicdraw(p):
    'stmt : IDENTIFIER MA IDENTIFIER KORA variableexp '
    p[0] = ("assignment"+"_"+str(p.lineno(1)),"temp", [("functionCall"+"_"+str(p.lineno(1)), u"__कोर__", [p[1],p[3]]+p[5])])

# def p_stmt_println(p):
#     'stmt : dynamString COMMA LEKHA'
#     p[0] = ("println", p[1])

def p_stmt_withoutCommaNewline(p):
    'stmt : dynamString LEKHA'
    p[0] = ("println"+"_"+str(p.lineno(2)), p[1])

# def p_stmt_print(p):
#     'stmt : dynamString COMMA LEKHA SEMICOLON'
#     p[0] = ("print", p[1])

def p_stmt_WOCommaSameline(p):
    'stmt : dynamString LEKHA SEMICOLON'
    p[0] = ("print"+"_"+str(p.lineno(2)), p[1])

def p_stmt_input(p):
    'stmt : IDENTIFIER LEU'
    p[0] = ("input"+"_"+str(p.lineno(2)), p[1])

def p_stmt_increment(p):
    'stmt : IDENTIFIER incrementsign ASSIGNMENT exp'
    p[0] = ("assignment"+"_"+str(p.lineno(1)), p[1], [("binop", p[2],[("identifier", p[1])],[p[4]])])

def p_stmt_ifcondition(p):
    'stmt : YEDI condition NEWLINE cmpdstmt optelse DIYE'
    p[0] = ("ifelse"+"_"+str(p.lineno(1)), [("yedi"+"_"+str(p.lineno(1)), p[2], p[4])] + p[5])

def p_stmt_for(p):
    'stmt : SABEI IDENTIFIER ASSIGNMENT exp DEKHI exp SEMICOLON sign exp NEWLINE cmpdstmt BAISA'
    p[0] = ("forloop"+"_"+str(p.lineno(1)), p[2], [p[4]], [p[6]], p[8], [p[9]], p[11])

def p_stmt_for1(p):
    'stmt : SABEI IDENTIFIER ASSIGNMENT exp DEKHI exp NEWLINE cmpdstmt BAISA'
    p[0] = ("forloop"+"_"+str(p.lineno(1)), p[2], [p[4]], [p[6]], u"+", [("number_"+str(p.lineno(1)),u'१' )], p[8])

def p_stmt_while(p):
    'stmt : JABA SAMMA whilecond NEWLINE cmpdstmt BAJA'
    p[0] = ("whileloop"+"_"+str(p.lineno(1)), p[3], p[5])

def p_stmt_list(p):
    'stmt : IDENTIFIER ASSIGNMENT LGPARA variableexp RGPARA'
    p[0] = ("listAssignment"+"_"+str(p.lineno(1)), p[1], p[4])

def p_stmt_function(p):
    'stmt : KAAM IDENTIFIER LPARA variableArgs RPARA NEWLINE cmpdstmt MAKA'
    p[0] = ('functionDefination'+"_"+str(p.lineno(1)), p[2], p[4], p[7])

def p_stmt_functionCall(p):
    'stmt : IDENTIFIER LPARA variableexp RPARA'
    p[0] = ("assignment"+"_"+str(p.lineno(1)),"temp", [("functionCall"+"_"+str(p.lineno(1)), p[1], p[3])])

def p_stmt_returnStatement(p):
    'stmt : exp PATHAU'
    p[0] = ('returnStmt'+"_"+str(p.lineno(2)), [p[1]])

def p_stmt_newline(p):
    'stmt : NEWLINE'
    pass

def p_variableArgs_arguments(p):
    'variableArgs : IDENTIFIER COMMA variableArgs'
    p[0] = [p[1]] + p[3]
def p_variableArgs_single(p):
    'variableArgs : IDENTIFIER'
    p[0] = [p[1]]
def p_variableArgs_empty(p):
    'variableArgs : '
    p[0] = []

def p_variableexp_more(p):
    'variableexp : exp COMMA variableexp'
    p[0] = [[p[1]]] + p[3]
def p_variableexp_one(p):
    'variableexp : exp'
    p[0] = [[p[1]]]
def p_variableexp_empty(p):
    'variableexp : '
    p[0] = []



def p_exp_equal(p):
    '''exp : exp EQ exp
            | exp LE exp
            | exp GE exp
            | exp NE exp
            | exp LT exp
            | exp GT exp
            | exp PLUS exp
            | exp MINUS exp
            | exp TIMES exp
            | exp DIVIDE exp
            | exp POWER exp
            | exp MODULUS exp
            | exp RA exp
            | exp WA exp
    '''
    p[0] = ("binop"+"_"+str(p.lineno(2)), p[2],[p[1]],[p[3]])

def p_exp_identifier(p):
    'exp : IDENTIFIER'
    p[0] = ("identifier"+"_"+str(p.lineno(1)), p[1])
def p_exp_string(p):
    'exp : STRING'
    p[0] = ("string"+"_"+str(p.lineno(1)), p[1])
def p_exp_number(p):
    'exp : NUMBER'
    p[0] = ("number"+"_"+str(p.lineno(1)), p[1])

def p_exp_minus(p):
    'exp : MINUS NUMBER'
    p[0] = ("number"+"_"+str(p.lineno(1)), "-"+p[2])

def p_exp_sunya(p):
    'exp : SUNYA'
    p[0] = ('sunya'+"_"+str(p.lineno(1)),)
def p_exp_list(p):
    'exp : LGPARA variableexp RGPARA'
    p[0] = ("list"+"_"+str(p.lineno(1)), p[2])
def p_exp_listitem(p):
    'exp : IDENTIFIER LGPARA exp RGPARA'
    p[0] = ("listItem"+"_"+str(p.lineno(1)), p[1], [p[3]])
def p_exp_paren(p):
    'exp : LPARA exp RPARA'
    p[0] = ("parenthesis"+"_"+str(p.lineno(1)), [p[2]])

def p_exp_slicing(p):
    'exp : IDENTIFIER LGPARA sliceexp COLON sliceexp RGPARA'
    p[0] = ("slicing"+"_"+str(p.lineno(1)), p[1], p[3], p[5])
def p_sliceexp_var(p):
    'sliceexp : exp'
    p[0] = [p[1]]
def p_sliceexp_empty(p):
    'sliceexp : '
    p[0] = []

def p_exp_conditional(p):               # second one is to be evaluated , third one is exp if true and fourth is if false
    'exp : LPARA exp RPARA QUESTION exp COLON exp'
    p[0] = ("conditional"+"_"+str(p.lineno(4)), [p[2]], [p[5]], [p[7]])

def p_exp_functionCall(p):
    'exp : IDENTIFIER LPARA variableexp RPARA'
    p[0] = ("functionCall"+"_"+str(p.lineno(1)), p[1], p[3])

def p_dynamString_ident(p):
    'dynamString : exp COMMA dynamString'
    p[0] = [[p[1]]] + p[3]
def p_dynamString_exp(p):
    'dynamString : exp'
    p[0] = [[p[1]]]

def p_condition_binop(p):
    '''condition : condition RA condition
                    | condition WA condition
    '''
    p[0] = [("conditionalbinop"+"_"+str(p.lineno(2)), p[2], p[1], p[3])]

def p_condition_positive(p):
    'condition : exp BHAE'
    p[0] = [("positive"+"_"+str(p.lineno(2)), [p[1]])]

def p_condition_neg(p):
    'condition : exp NABHAE'
    p[0] = [("negative"+"_"+str(p.lineno(2)), [p[1]])]

def p_cmpdstmt_stmt(p):
    'cmpdstmt : stmt NEWLINE cmpdstmt'
    p[0] = [p[1]] + p[3]
def p_cmpdstmt_empty(p):
    'cmpdstmt : '
    p[0] = []

def p_optelse_elseif(p):
    'optelse : ATHAWA condition NEWLINE cmpdstmt optelse'
    p[0] = [("elseif"+"_"+str(p.lineno(1)), p[2], p[4])] + p[5]
def p_optelse_else(p):
    'optelse : ATHAWA NEWLINE cmpdstmt'
    p[0] = [("else"+"_"+str(p.lineno(1)), p[3])]
def p_optelse_empty(p):
    'optelse : '
    p[0] = []

"""
om namah shivaya
"""

def p_sign(p):
    '''sign : PLUS
            | MINUS
    '''
    p[0] = p[1]
def p_incrementsign(p):
    '''incrementsign : sign
                        | TIMES
                        | DIVIDE
    '''
    p[0] = p[1]



def p_whilecond_normal(p):
    '''whilecond : whilecond RA whilecond
                    | whilecond WA whilecond
    '''
    p[0] = [("conditionalbinop"+"_"+str(p.lineno(2)), p[2], p[1], p[3])]

def p_whilecond_pos(p):
    'whilecond : exp CHHA'
    p[0] = [("positive"+"_" +str(p.lineno(2)), [p[1]])]
def p_whilecond_neg(p):
    'whilecond : exp CHHAINA'
    p[0] = [("negative"+"_" + str(p.lineno(2)), [p[1]])]


def p_error(p):
    #changed here
    print "Syntax Error: Near Token " + p.type
    print p.lineno
    exit(-1)




import ply.lex as lex
# import ply.yacc as yacc
import NepLexer
# import NepParser
from NepLexer import tokens
# from NepParser import * 
lexer = lex.lex(module=NepLexer)
parser = yacc.yacc()




#write input text here to override it
input = ""


ip = u'''क लेख
क, " मा हामीले  २ हालेका छौँ " लेख
"ख मा ", ख, " छ" लेख
'''
ip = u'''ख लेउ
'''
ip = u'''सबै ख = ३ देखि ५; -२
     क लेउ
     २^क लेख
बैस
'''
ip = u'''जब सम्म क==१० छ र ख==२ छैन
२^क लेख
बज
'''
ip = u'''यदि  क == २ भए			
    क = १०.३२
    क = १०.३२
अथवा क >= ३ भए र क == १० नभए
    "क तिन भन्दा बेसि छ तर १० छैन" लेख
अथवा
    ख लेउ
    "ख मा ", ख, " छ" लेख
दिय
'''
ip = u'''क += १०.३२
क = क + १०.३२
क -= १०.३२
क *= १०.३२
क /= १०.३२
'''
ip = u'''क = (क == २) ? २५: ५
'''
ip = u'''यदि  क == २ वा क == ३ भए
    क लेख
    क, " मा हामीले  २ हालेका छौँ " लेख
दिय
'''
ip = u'''यदि  क == २ भए वा क == ३ भए
    क लेख
    क, " मा हामीले  २ हालेका छौँ " लेख
दिय
'''
ip = u'''क = २
क लेख;
क लेख;
क, " मा हामीले  २ हालेका छौँ " लेख;
"२" लेख;
'''
ip = u'''क = [१, ०, ३, २,]
क लेख
क = [१, ०, ३, २,] + [१, ०, ३, २,]
क[१] लेख;
क = []
'''
ip = u'''काम रमाईलो ()
    क = []
    क[१०] लेख;
मका
रमाईलो ()
'''
ip = u'''काम रमाईलो (क, ख,)
    क = []
    क[१०] लेख;
    क पठाउ 
मका
रमाईलो (१०, म)
'''
ip = u'''काम रमाईलो (क, ख,)
    "क" लेख;
मका
क = रमाईलो (१०, म)
रमाईलो (१०, म) लेख;
'''
ip = u'''काम रमाईलो (क, ख,)
    "क" लेख;
मका
रमाईलो(१०,१०,१०)
म=१०
क = रमाईलो (१०, म)
रमाईलो (१०, म) लेख
'''

# ip = u'''क = १०.३२^"नेपाल"
# ख = "नेपाल"^१०
# ख = "नेपाल"*१०
# ख = "नेपाल"-१०  /* yestai yestai type mismatch haru ni aauna sakchan interpret garda check gara la bikram */
# ख = "नेपाल"+१०  
# ख = "नेपाल"/१०
# ख = ("नेपाल">=२)
# ख = [१, ०, ३, २,] ^ १० + 3 * "नेपाल"
# '''
# print tokenizer(ip)
ip = u'''क = "फाइलखोल"
म = क[:-१]
म लेख
'''

inpu =u'''क = "फाइलखोल"
क लेख
म = गन("फाइलखोल")
म लेख
म = टुक्राऊ("फाइलखोल", "इ")
म लेख
म = खोज("फाइलखोल", "इ")
म लेख
म = खोज("फाइलखोल", "इ", ०, १०)
म लेख
म = बद्ल("फाइलखोल", "इ", "ल")
म लेख
म = अङ्क("१०")
म लेख
म = खालीहताऊ("   फाइलखोल   ")
म लेख
म = गन(["फ", "ाइलखोल"])
म लेख
म = टुक्राऊ("फाइलखोल", "इ")
म लेख
म = खोज("फाइलखोल", "इ")

'''

ip = u'''क = १+०-३*२+१-३*२
क लेख
३%२ लेख
'''
#write a file name here to override it.
filename = ""

usage =\
"""
Usage: python NepParser.py filename
filename: .rhee File to interpret
"""

args = str(argv)
if not input:
    if filename:
        input = unicode(open(filename,"r").read(),'UTF8')
    elif len(argv) <2:
        print usage
        exit(-1)
    else:
        input = unicode(open(argv[1],"r").read(),"UTF8")


ast = parser.parse(input, lexer=lexer)
print ast

try:
#    pass
    interpret(ast)
except:
    pass

exit(0)
