import Interpreter
import sys
import traceback


def repl(prompt='REPL> '):                            # The REPL
    print("Welcome to the REPL! to exit, type 'exit'")
    while True:
        try:
            string = input(prompt)
            if string == 'exit':
                print("Bye!")
                sys.exit()
            Interpreter.interpret(string)
        except Exception as e:
            print(f"ERROR! {e}")
            #traceback.print_exception(type(e), e, e.__traceback__)     #debug

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if filename.endswith('.lambda'):
            try:
                with open(filename, 'r') as file:
                    code = file.read()
                    Interpreter.interpret(code)
            except FileNotFoundError:
                print(f"File '{filename}' not found.")
        else:
            print("Please provide a file with a '.lambda' extension.")
    else:
        print("lambda file not provided, initiating REPL...")
        repl()