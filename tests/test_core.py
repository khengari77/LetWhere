import pytest
from letwhere.parser import main_parser
from letwhere.evaluator import evaluate, Environment
from pyparsec.Prim import run_parser

def eval_code(code):
    ast, err = run_parser(main_parser, code)
    assert err is None, f"Parse Error: {err}"
    return evaluate(ast, Environment())

def test_arithmetic():
    assert eval_code("1 + 2 * 3") == 7
    assert eval_code("(1 + 2) * 3") == 9

def test_recursion_factorial():
    code = r"""
    let fact = \n -> if n < 2 then 1 else n * fact (n-1)
    in fact 5
    """
    assert eval_code(code) == 120

def test_where_scope():
    code = r"""
    x + y where { x = 10; y = 5 }
    """
    assert eval_code(code) == 15

def test_shadowing():
    # Inner let should shadow outer let
    code = r"""
    let x = 10 in
        let x = 20 in x
    """
    assert eval_code(code) == 20
