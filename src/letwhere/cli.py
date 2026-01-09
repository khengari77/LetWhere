import sys
import argparse
from pathlib import Path
from pyparsec.Prim import run_parser
from .parser import main_parser
from .evaluator import evaluate, Environment

def run_source(source_code: str, env: Environment, filename="<stdin>"):
    """Parses and evaluates a string of source code."""
    # Strip whitespace to ignore empty inputs
    if not source_code.strip():
        return

    ast, err = run_parser(main_parser, source_code)

    if err:
        print(f"Syntax Error in {filename}:")
        print(err)
        return

    try:
        result = evaluate(ast, env)
        print(f"=> {result}")
    except Exception as e:
        print(f"Runtime Error: {e}")

def repl():
    """Read-Eval-Print Loop."""
    print("LetWhere v0.1.0")
    print("Type 'exit' to quit, or enter code.")
    
    env = Environment()
    
    while True:
        try:
            text = input("lw> ")
            if text.strip() in ["exit", "quit"]:
                break
            run_source(text, env)
        except KeyboardInterrupt:
            print("\nExiting.")
            break
        except EOFError:
            break

def run_file(filepath: str):
    """Reads a file and executes it."""
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)
        
    source = path.read_text()
    env = Environment()
    run_source(source, env, filename=filepath)

def main():
    parser = argparse.ArgumentParser(description="The LetWhere Programming Language")
    parser.add_argument("file", nargs="?", help="The .lw file to execute")
    parser.add_argument("-e", "--eval", help="Evaluate a string of code directly")
    
    args = parser.parse_args()

    if args.eval:
        run_source(args.eval, Environment())
    elif args.file:
        run_file(args.file)
    else:
        repl()

if __name__ == "__main__":
    main()
