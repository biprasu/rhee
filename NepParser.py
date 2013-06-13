#encoding=UTF8
import ply.yacc as yacc

start = "N"

precedence = (
    ('left', 'IDENTIFIER'),
    ('left', 'EQ'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'POWER'),
    )

def p_N(p):
    'N : element N'
    p[0] = [p[1]] + p[2]
def p_N_empty(p):
    'N : '
    p[0] = []
def p_element_stmt(p):
    'element : stmt NEWLINE'
    p[0] = p[1]
def p_stmt_assign(p):
    'stmt : IDENTIFIER ASSIGNMENT exp'
    p[0] = ("assignment", p[1], [p[3]])

def p_stmt_print(p):
    'stmt : dynamString LEKHA'
    p[0] = ("print", p[1])

def p_stmt_input(p):
    'stmt : IDENTIFIER LEU'
    p[0] = ("input", p[1])

def p_stmt_increment(p):
    'stmt : IDENTIFIER incrementsign ASSIGNMENT exp'
    p[0] = ("increment", p[2], [p[4]])

def p_stmt_ifcondition(p):
    'stmt : YEDI condition NEWLINE cmpdstmt optelse DIYE'
    p[0] = ("ifelse", [("yedi", p[2], p[4])] + p[5])

def p_stmt_for(p):
    'stmt : SABEI IDENTIFIER ASSIGNMENT exp DEKHI exp SEMICOLON sign exp NEWLINE cmpdstmt BAISA'
    p[0] = ("forloop", p[2], [p[4]], [p[6]], p[8], [p[9]], p[11])

def p_stmt_while(p):
    'stmt : JABA SAMMA whilecond NEWLINE cmpdstmt BAJA'
    p[0] = ("whileloop", p[3], p[5])



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
    '''
    p[0] = ("binop", p[2],[p[1]],[p[3]])

def p_exp_identifier(p):
    'exp : IDENTIFIER'
    p[0] = ("identifier", p[1])
def p_exp_string(p):
    'exp : STRING'
    p[0] = ("string", p[1])
def p_exp_number(p):
    'exp : NUMBER'
    p[0] = ("number", p[1])
def p_exp_paren(p):
    'exp : LPARA exp RPARA'
    p[0] = ("parenthesis", [p[2]])

def p_dynamString_ident(p):
    'dynamString : exp COMMA dynamString'
    p[0] = [[p[1]]] + p[3]
def p_dynamString_exp(p):
    'dynamString : exp'
    p[0] = [[p[1]]]

def p_condition_binop(p):
    '''condition : condition RA condition
    '''
    p[0] = [("conditionalbinop", p[2], p[1], p[3])]

def p_condition_positive(p):
    'condition : exp BHAE'
    p[0] = [("positive", [p[1]])]

def p_condition_neg(p):
    'condition : exp NABHAE'
    p[0] = [("negative", [p[1]])]

def p_cmpdstmt_stmt(p):
    'cmpdstmt : stmt NEWLINE cmpdstmt'
    p[0] = [p[1]] + p[3]
def p_cmpdstmt_empty(p):
    'cmpdstmt : '
    p[0] = []

def p_optelse_elseif(p):
    'optelse : ATHAWA condition NEWLINE cmpdstmt optelse'
    p[0] = [("elseif", p[2], p[4])] + p[5]
def p_optelse_else(p):
    'optelse : ATHAWA NEWLINE cmpdstmt'
    p[0] = [("else", p[3])]
def p_optelse_empty(p):
    'optelse : '
    p[0] = []


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
    'whilecond : whilecond RA whilecond'
    p[0] = [("conditionalbinop", p[2], p[1], p[3])]

def p_whilecond_pos(p):
    'whilecond : exp CHHA'
    p[0] = [("positive", [p[1]])]
def p_whilecond_neg(p):
    'whilecond : exp CHHAINA'
    p[0] = [("negative", [p[1]])]


def p_error(p):
    tok = yacc.token()
    print "Syntax Error: Near Token " + str(tok)
    exit(1)




import ply.lex as lex
# import ply.yacc as yacc
import NepLexer
# import NepParser
from NepLexer import tokens
# from NepParser import * 
lexer = lex.lex(module=NepLexer)
parser = yacc.yacc()


ip = u'''क = १०.३२
ख = "नेपाल"
ख = क
ख = ( क )
ख = (क==२)
ख = (क!=२)
ख = (क>=२)
ख = (क<=२)
ख = (क>२)
ख = (क<२)
'''
ip = u'''ख = क - २ + (भ  * त) / ८ ^ २
'''
ip = u'''क लेख
क, " मा हामीले  २ हालेका छौँ " लेख
"ख मा ", ख, " छ" लेख
'''
# ip = u'''ख लेउ
# '''
# ip = u'''सबै ख = ३ देखि ५; -२
#      क लेउ
#      २^क लेख
# बैस
# '''
# ip = u'''जब सम्म क==१० छ र ख==२ छैन
# २^क लेख
# बज
# '''
# ip = u'''यदि  क == २ भए			
#     क = १०.३२
#     क = १०.३२
# अथवा क >= ३ भए र क == १० नभए
#     "क तिन भन्दा बेसि छ तर १० छैन" लेख
# अथवा
#     ख लेउ
#     "ख मा ", ख, " छ" लेख
# दिय
# '''
# ip = u'''क += १०.३२
# क -= १०.३२
# क *= १०.३२
# क /= १०.३२
# '''


# '''
# print tokenizer(ip)
ast = parser.parse(ip, lexer=lexer)
print ast
# print "done"

