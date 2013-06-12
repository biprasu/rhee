#encoding=UTF8
import re
import ply.lex as lex
 
 
#tokens
tokens = ['STRING',
          'PLUS',
          'MINUS',
          'DIVIDE',
          'TIMES',
          'POWER',
          'LPARA',
          'RPARA',
          'LGPARA',
          'RGPARA',
          'GE',
          'LE',
          'EQ',
          'NE',
          'LT',
          'GT',
          'ASSIGNMENT',
          'COMMA',
          'SEMICOLON',
          'IDENTIFIER',
          'NUMBER',
          'NEWLINE',
    ]
 
reserved = {
    u'यदि' : 'YEDI',
    u'भए' : 'BHAE',
    u'नभए'  : 'NABHAE',
    u'लेख' : 'LEKHA',
    u'अथवा' : 'ATHAWA',
    u'लेउ' : 'LEU',
    u'दिय' : 'DIYE',
    u'सबै' : 'SABEI',
    u'देखि' : 'DEKHI',
    u'बैस' : 'BAISA',
    u'जब' : 'JABA',
    u'बज' : 'BAJA',
    u'सम्म' : 'SAMMA',
    u'छैन' : 'CHHAINA',
    u'छ' : 'CHHA',
    u'र'  : 'RA',
 
}
 
tokens = tokens + list(reserved.values())
 
 
 
#comment
def t_comment(token):
    ur'(//.*)|(?:/\*[^(\*/)]*\*/)'
    token.lexer.lineno += token.value.count('\n')
    pass
 
 
def t_NEWLINE(token):
    ur'\n+'
    token.lexer.lineno += token.value.count('\n')
    return token
 
 
#string
def t_STRING(token):
    ur'"[^"]*"'
    token.value = token.value[1:-1]
    return token
 
 
 
#mathematical symbols
t_PLUS = ur'\+'
t_MINUS = ur'\-'
t_DIVIDE = ur'/'
t_TIMES = ur'\*'
t_POWER = ur'\^'

#paranthesis
t_LPARA = ur'\('
t_RPARA = ur'\)'
 
t_LGPARA = ur'\['
t_RGPARA = ur'\]'
 
#logical
t_GE = ur'>='
t_LE = ur'<='
t_EQ = ur'=='
t_NE = ur'!='
t_GT = ur'>'
t_LT = ur'<'
 
#assignment
t_ASSIGNMENT = ur'='
t_COMMA = ur','
t_SEMICOLON = ur';'
 
#words
def t_IDENTIFIER(token):
    #down below is the entire devanagari script except numbers.
    ur'[\u0900-\u0965][\u0900-\u0965_०-९]*'
    token.type = reserved.get(token.value,'IDENTIFIER')    # Check for reserved words
    return token
 
def t_NUMBER(token):
    ur'[०-९]+(\.[०-९]+)?'
    return token
 
#ignore
t_ignore = u' \t'
#error
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# lexer = lex.lex()
# ip = unicode(open('inputfile.txt','r').read(),encoding="UTF8")
 
# lexer.input (ip)
 
 
# while True:
#     a = lexer.token()
#     if not a: break
#     if not a.type == 'NEWLINE':
#         print a.type, a.value
#     else:
#         print a.type
