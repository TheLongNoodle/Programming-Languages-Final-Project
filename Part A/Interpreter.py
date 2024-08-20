import traceback

from Lexer import lexer
from Parser import parser
import math

##################### Return Signal
class Return(Exception):
    def __init__(self, result):
        self.result = result

##################### Environment object
class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.functions = {} if parent is None else parent.functions
        self.parent = parent

    def set(self, var, value):                      # Save variable to environment
        if var in self.variables:
            self.variables[var] = value
        else:
            # If no parent, create the variable in the current environment
            self.variables[var] = value

    def get(self, var):                             # Get variable from environment
        if var in self.variables:
            return self.variables[var]
        elif self.parent:
            return self.parent.get(var)
        else:
            raise RuntimeError(f"Variable '{var}' not found")

    def define_function(self, name, args, body):    # Save function to environment
        if self.parent:
            self.parent.define_function(name, args, body)
        else:
            self.functions[name] = (args, body)

    def call_function(self, name, arguments):       # Call function from environment using given arguments
        if name in self.functions:
            args, body = self.functions[name]
            if len(arguments) != len(args):
                raise RuntimeError("Incorrect number of arguments")
            local_env = Environment(parent=self)
            for arg, value in zip(args, arguments):
                local_env.set(arg, value)
            return eval_statements(body, local_env)
        elif self.parent:
            return self.parent.call_function(name, arguments)
        else:
            raise RuntimeError(f"Function '{name}' not defined")

global_env = Environment()

##################### Main interpreter
def interpret(source_code, env = global_env): # The main interpreter
    lexer.input(source_code)
    parse_tree = parser.parse(lexer=lexer)
    # print(parse_tree) # Debug
    eval_statements(parse_tree, env)

##################### statement interpreter
def eval_statements(statements, env, end=False):
    result = None
    for statement in statements:
        result = eval_statement(statement, env)
    return result

def eval_statement(statement, env):         # Determine statement type
    # Basically, it checks for the type in statement[0], if it finds a recognised name it separates
    # the values after it accordingly and evaluate it as such, otherwise it's probably an expression so
    # it initiates eval_expression
    try:
        if statement[0] == 'assign':
            _, var, expr = statement
            value = eval_expression(expr, env)
            env.set(var, value)
        elif statement[0] == 'function_definition':
            _, name, args, body = statement
            env.define_function(name, args, body)
        elif statement[0] == 'function_call':
            _, name, args = statement
            arguments = [eval_expression(arg, env) for arg in args]
            try:
                return env.call_function(name, arguments)
            except Return as e:
                return e.result
        elif statement[0] == 'if':
            _, condition, body = statement
            if eval_expression(condition, env):
                eval_statements(body, env)
        elif statement[0] == 'if_else':
            _, condition, body_true, body_false = statement
            if eval_expression(condition, env):
                eval_statements(body_true, env)
            else:
                eval_statements(body_false, env)
        elif statement[0] == 'print':
            _, expr = statement
            try:
                print(eval_statement(expr, env))
            except Return as e:
                print(e.result)
        elif statement[0] == 'return':
            _, expr = statement
            raise Return (eval_expression(expr, env))
        elif statement[0] == 'lambda':
            _, args, body, arguments = statement
            env.define_function('lambda', args, body)
            arguments = [eval_statement(arg, env) for arg in arguments]
            try:
                return env.call_function('lambda', arguments)
            except Return as e:
                    return e.result
        else:
            return eval_expression(statement, env)
    except TypeError as e:
        return eval_expression(statement, env)

##################### Expression interpreter
def eval_expression(expr, env):                     # Checking if INT, BOOL or Variable
    if isinstance(expr, int):
        return expr
    elif isinstance(expr, bool):
        return expr
    elif isinstance(expr, str):
        return env.get(expr)
    elif isinstance(expr, tuple):                   # Checking if function call or lambda expression
        op, *operands = expr                        # separate tokens to evaluate operation
        if op == 'function_call':
            function_name, args = operands
            arguments = [eval_expression(arg, env) for arg in args]
            try:
                return env.call_function(function_name, arguments)
            except Return as e:
                return e.result
        if op == 'lambda':
            env.define_function('lambda', operands[0], operands[1])
            arguments = [eval_statement(arg, env) for arg in operands[2]]
            try:
                return env.call_function('lambda', arguments)
            except Return as e:
                return e.result                     # If not lambda or func call, determine operation
        elif op in ('+', '-', '*', '/', '%'):       # Binary operation
            return eval_binary_op(op, *map(lambda x: eval_expression(x, env), operands))
        elif op in ('==', '!=', '<', '<=', '>', '>='):
            return eval_comparison(op, *map(lambda x: eval_expression(x, env), operands))
        elif op in ('&&', '||'):
            return eval_logical_op(op, *map(lambda x: eval_expression(x, env), operands))
        elif op == 'not':                           # Unary operation
            return not eval_expression(operands[0], env)
        elif op == 'uminus':
            return -eval_expression(operands[0], env)
    else:
        raise RuntimeError(f"Unknown expression type: {expr}")

##################### Operations
def eval_binary_op(op, left, right):
    if op == '+':
        return left + right
    elif op == '-':
        return left - right
    elif op == '*':
        return left * right
    elif op == '/':
        return math.floor(left / right)
    elif op == '%':
        return left % right

def eval_comparison(op, left, right):
    if op == '==':
        return left == right
    elif op == '!=':
        return left != right
    elif op == '<':
        return left < right
    elif op == '<=':
        return left <= right
    elif op == '>':
        return left > right
    elif op == '>=':
        return left >= right

def eval_logical_op(op, left, right):
    if op == '&&':
        return left and right
    elif op == '||':
        return left or right

# NOTE!!! In this language, lambda expressions and unnamed functions are saved as a temporary copy function in the
# environment under the proprietary name 'lambda'.
