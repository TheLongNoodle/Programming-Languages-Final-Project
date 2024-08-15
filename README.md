# Python Compiler and Interpreter
By Omer Aley-Raz and Yuval Gendler

## Overview

This project implements a compiler and interpreter for a custom programming language. The language supports variable assignments, arithmetic operations, boolean expressions, function definitions (including recursion), lambda expressions, control flow (if, else), and printing of values. The language syntax is inspired by Python and JavaScript, featuring semicolon-terminated statements and braces for code blocks.

The project leverages **PLY (Python Lex-Yacc)** to handle lexical analysis and parsing, with a custom interpreter built to evaluate the resulting parse tree.

The project is separated to 2 folders: "Part A" and "Part B".

## Features

#### Variables:
- INTEGER
- BOOLEAN
- Named variables (`=`)
#### Arithmetic Operations (for INTEGERs):
 - Addition (`+`)
 - Subtraction (`-`)
 - Multiplication (`*`)
 - Division (`/`) (integer division)
 - Modulo (`%`)
#### Boolean Operations:
 - AND (`&&`)
 - OR (`||`)
 - NOT (`!`)
### Comparison Operations:
 - Equal to (`==`)
 - Not equal to (`!=`)
 - Greater than (`>`)
 - Less than (`<`)
 - Greater than or equal to (`>=`)
 - Less than or equal to (`<=`)
### Functions:
 - Named function definitions (`def`)
 - Anonymous functions and lambda expressions (`lambda`)
 - `if/else` statements
 - `print` and `break` statements
 - Support for function application
 - Support for recursive function calls
 - Support for a replacement for while loop.
 - REPL
 - Interpret from .lambda files
   (add as argument)


## Syntax Example
this is the Test.lambda file provided with the project, it has examples of the syntax for the language.
when running this test file, output should be ```True``` for all lines, so in this example it will print ```True``` 20 times. 

<details>
<summary>Test.lambda</summary>

\* bare in mind the the lambda files do NOT support comments at the moment!\
comments are added here only to provide context, this file will NOT run but the one provided with the program does not have comments and will run.


```
# Addition
print(2+5==7);

# Subtraction
print(2-5==-3);

# Negative numbers
print(-2+5==3);
print(2--5==7);

# Multiplication
print(2*5==10);

# Integer division
print(5/2==2);

# Modulus
print(5%2==1);

# Saving variables, equal
a = (1==1);
print(a);

# Less then
print(2<5);

# Less equal
print(2<=5);

# Greater then
print(5>2);

# Greater equal
print(5>=2);

# Not equal
print(2!=5);

# AND
print(true&&true);

# OR
print(true||false);

# NOT
print(!false);
print(false||!false);

# Lambda expression
print(lambda(a,b):{a*b;}(3,4) == 12);

# Unnamed function
print(lambda(a,b):{if(a>=b){return a;}return b;}(6,12) == 12);

# Named and recursive function
def fib(n) {
    if (n == 0) { return 0; }
    if (n == 1) { return 1; }
    return (lambda(a,b):{a+b;}(fib(n-1),fib(n-2)));
}
print(fib(10) == 55);
```
</details>

## BNF
```
<program> ::= <statements>

<statements> ::= <statements> <statement>
               | <statement>

<statement> ::= <assignment>
              | <function_definition>
              | <if_statement>
              | <return_statement>
              | <print_statement>
              | <expression> ";"

<assignment> ::= <ID> "=" <expression> ";"

<function_definition> ::= "def" <ID> "(" <function_args> ")" "{" <statements> "}"

<function_args> ::= <function_args> "," <ID>
                  | <ID>
                  | ε

<function_call> ::= <ID> "(" <function_call_args> ")"

<function_call_args> ::= <function_call_args> "," <expression>
                       | <expression>
                       | ε

<if_statement> ::= "if" "(" <expression> ")" "{" <statements> "}"
                 | "if" "(" <expression> ")" "{" <statements> "}" "else" "{" <statements> "}"

<return_statement> ::= "return" <expression> ";"

<lambda_expression> ::= "lambda" "(" <function_args> ")" ":" "{" <statements> "}" "(" <function_call_args> ")"

<print_statement> ::= "print" "(" <expression> ")" ";"

<expression> ::= <NUMBER>
               | <ID>
               | "true"
               | "false"
               | "(" <expression> ")"
               | <expression> "+" <expression>
               | <expression> "-" <expression>
               | <expression> "*" <expression>
               | <expression> "/" <expression>
               | <expression> "%" <expression>
               | <expression> ">" <expression>
               | <expression> "<" <expression>
               | <expression> ">=" <expression>
               | <expression> "<=" <expression>
               | <expression> "==" <expression>
               | <expression> "!=" <expression>
               | <expression> "&&" <expression>
               | <expression> "||" <expression>
               | "!" <expression>
               | "-" <expression>
               | <function_call>
               | <lambda_expression>

<empty> ::= ε

```