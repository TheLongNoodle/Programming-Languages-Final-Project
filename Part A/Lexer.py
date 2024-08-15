import ply.lex as lex

# List of token names
tokens = [
    'NUMBER', 'ID', 'ASSIGN',                                               # Numbers and identifiers
    'PLUS', 'MINUS', 'MULT', 'DIV', 'MOD',                                  # Math op
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COMMA', 'SEMICOLON', 'COLON',  # Symbols
    'EQ', 'NE', 'LT', 'GT', 'LE', 'GE',                                     # Comparison
    'AND', 'OR', 'NOT', 'TRUE', 'FALSE',                                    # Binary op
    'IF', 'ELSE', 'DEF', 'RETURN', 'PRINT', 'LAMBDA'                        # Statements
]

# Regular expression rules for simple tokens
t_PLUS       = r'\+'
t_MINUS      = r'-'
t_MULT       = r'\*'
t_DIV        = r'/'
t_MOD        = r'%'
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_LBRACE     = r'\{'
t_RBRACE     = r'\}'
t_COMMA      = r','
t_SEMICOLON  = r';'
t_COLON      = r':'
t_ASSIGN     = r'='
t_EQ         = r'=='
t_NE         = r'!='
t_LT         = r'<'
t_GT         = r'>'
t_LE         = r'<='
t_GE         = r'>='
t_AND        = r'&&'
t_OR         = r'\|\|'
t_NOT        = r'!'

def t_TRUE(t):
    r"""true"""
    t.value = True
    return t

def t_FALSE(t):
    r"""false"""
    t.value = False
    return t

def t_IF(t):
    r"""if"""
    return t

def t_ELSE(t):
    r"""else"""
    return t

def t_DEF(t):
    r"""def"""
    return t

def t_RETURN(t):
    r"""return"""
    return t

def t_PRINT(t):
    r"""print"""
    return t

def t_LAMBDA(t):
    r"""lambda"""
    return t

# Regular expression for identifiers
def t_ID(t):
    r"""[a-zA-Z_][a-zA-Z_0-9]*"""
    return t

# Regular expression for numbers
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = int(t.value) if '.' not in t.value else float(t.value)
    return t

# Ignored characters (spaces and tabs)
t_ignore = ' \t'

# Track line numbers
def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
