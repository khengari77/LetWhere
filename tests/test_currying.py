# tests/test_currying.py
import pytest
from letwhere.parser import main_parser
from letwhere.evaluator import evaluate, Environment
from pyparsec.Prim import run_parser

def eval_code(code):
    ast, err = run_parser(main_parser, code)
    assert err is None, f"Parse Error: {err}"
    return evaluate(ast, Environment())

def test_multi_arg_definition():
    # Should automatically curry: \x y -> ... becomes \x -> \y -> ...
    code = "(\\x y -> x + y) 10 20"
    assert eval_code(code) == 30

def test_partial_application():
    # Define a 2-arg function, supply 1 arg, store the resulting closure, then call it.
    code = """
    let add = \\x y -> x + y in
    let add_five = add 5 in
    add_five 10
    """
    assert eval_code(code) == 15

def test_higher_order_functions():
    # Passing a function (double) into another function (apply)
    code = """
    let apply = \\f x -> f x;
        double = \\n -> n * 2
    in apply double 10
    """
    assert eval_code(code) == 20

def test_church_pairs():
    # The logic from examples/04_cons_pairs.lw
    code = """
    let mk_pair = \\x y s -> s x y;
        fst = \\p -> p (\\x y -> x);
        snd = \\p -> p (\\x y -> y)
    in
        let p = mk_pair 10 20 in
        (fst p) + (snd p)
    """
    assert eval_code(code) == 30

def test_ackermann_logic():
    # Small scale Ackermann to prove deep recursion + multi-args works
    # ack 2 1 -> 5
    code = """
    let ack = \\m n ->
        if m == 0 then n + 1
        else if n == 0 then ack (m - 1) 1
        else ack (m - 1) (ack m (n - 1))
    in ack 2 1
    """
    assert eval_code(code) == 5
