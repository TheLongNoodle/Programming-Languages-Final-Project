import ply.yacc as yacc
from Lexer import tokens  # Import tokens from the lexer module

# Define the precedence
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NE'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV', 'MOD'),
    ('right', 'NOT'),
    ('right', 'UMINUS'),
)

# Grammar rules
def p_program(p):
    """program : statements"""
    p[0] = p[1]

def p_statements(p):
    """statements : statements statement
                  | statement"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    """statement : assignment
                 | function_definition
                 | if_statement
                 | return_statement
                 | print_statement
                 | expression SEMICOLON"""
    p[0] = p[1]

def p_assignment(p):
    """assignment : ID ASSIGN expression SEMICOLON"""
    p[0] = ('assign', p[1], p[3])

def p_function_definition(p):
    """function_definition : DEF ID LPAREN function_args RPAREN LBRACE statements RBRACE"""
    p[0] = ('function_definition', p[2], p[4], p[7])

def p_function_args(p):
    """function_args : function_args COMMA ID
                     | ID
                     | empty"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_function_call(p):
    """function_call : ID LPAREN function_call_args RPAREN"""
    p[0] = ('function_call', p[1], p[3])

def p_function_call_args(p):
    """function_call_args : function_call_args COMMA expression
                          | expression
                          | empty"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_if_statement(p):
    """if_statement : IF LPAREN expression RPAREN LBRACE statements RBRACE
                    | IF LPAREN expression RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE"""
    if len(p) == 8:
        p[0] = ('if', p[3], p[6])
    else:
        p[0] = ('if_else', p[3], p[6], p[10])

def p_return_statement(p):
    """return_statement : RETURN expression SEMICOLON"""
    p[0] = ('return', p[2])

def p_lambda_expression(p):
    """lambda_expression : LAMBDA LPAREN function_args RPAREN COLON LBRACE statements RBRACE LPAREN function_call_args RPAREN"""
    p[0] = ('lambda', p[3], p[7], p[10])

def p_print_statement(p):
    """print_statement : PRINT LPAREN expression RPAREN SEMICOLON"""
    p[0] = ('print', p[3])

def p_expression(p):
    '''expression : NUMBER
                  | ID
                  | TRUE
                  | FALSE
                  | LPAREN expression RPAREN
                  | expression PLUS expression
                  | expression MINUS expression
                  | expression MULT expression
                  | expression DIV expression
                  | expression MOD expression
                  | expression GT expression
                  | expression LT expression
                  | expression GE expression
                  | expression LE expression
                  | expression EQ expression
                  | expression NE expression
                  | expression AND expression
                  | expression OR expression
                  | NOT expression %prec NOT
                  | MINUS expression %prec UMINUS
                  | function_call
                  | lambda_expression'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        # Handle negation
        if p[1] == '!':
            p[0] = ('not', p[2], p.lineno(1))
        else:
            p[0] = ('uminus', p[2], p.lineno(1))
    elif len(p) == 4:
        if p[1] == '(':
            p[0] = p[2]
        else:
            p[0] = (p[2], p[1], p[3])


def p_empty(p):
    """empty :"""
    p[0] = []

def p_error(p):
    print(f"Syntax error at '{p.value if p else 'EOF'}'")

# Build the parser
parser = yacc.yacc()
