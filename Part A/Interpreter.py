import traceback

from Lexer import lexer
from Parser import parser
import math

class Return(Exception):
    def __init__(self, result):
        self.result = result

class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.functions = {} if parent is None else parent.functions
        self.parent = parent

    def set(self, var, value):
        if var in self.variables:
            self.variables[var] = value
        else:
            # If no parent, create the variable in the current environment
            self.variables[var] = value

    def get(self, var):
        if var in self.variables:
            return self.variables[var]
        elif self.parent:
            return self.parent.get(var)
        else:
            raise RuntimeError(f"Variable '{var}' not found")

    def define_function(self, name, args, body):
        if self.parent:
            self.parent.define_function(name, args, body)
        else:
            self.functions[name] = (args, body)

    def call_function(self, name, arguments):
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

def interpret(source_code, env = global_env):
    lexer.input(source_code)
    parse_tree = parser.parse(lexer=lexer)
    #print(parse_tree) # Debug
    eval_statements(parse_tree, env)

def eval_statements(statements, env, end=False):
    result = None
    for statement in statements:
        result = eval_statement(statement, env)
        # try:
        #     result = eval_statement(statement, env)
        # except Return as e:
        #     result = e.result
        #     if isinstance(statement, (list, tuple)):
        #         if statement[0] != 'function_call':
        #             raise Return(result)
        #     else:
        #         return result
    return result

def eval_statement(statement, env):
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

def eval_expression(expr, env):
    if isinstance(expr, int):
        return expr
    elif isinstance(expr, bool):
        return expr
    elif isinstance(expr, str):
        return env.get(expr)
    elif isinstance(expr, tuple):
        op, *operands = expr
        # Handle function calls
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
                return e.result
        elif op in ('+', '-', '*', '/', '%'):
            return eval_binary_op(op, *map(lambda x: eval_expression(x, env), operands))
        elif op in ('==', '!=', '<', '<=', '>', '>='):
            return eval_comparison(op, *map(lambda x: eval_expression(x, env), operands))
        elif op in ('&&', '||'):
            return eval_logical_op(op, *map(lambda x: eval_expression(x, env), operands))
        elif op == 'not':
            return not eval_expression(operands[0], env)
        elif op == 'uminus':
            return -eval_expression(operands[0], env)
    else:
        raise RuntimeError(f"Unknown expression type: {expr}")

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
