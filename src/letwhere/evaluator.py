# LetWhere/evaluator.py
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Callable
from .ast_nodes import *

class Environment:
    def __init__(self, parent: Optional['Environment'] = None):
        self.values: Dict[str, Any] = {}
        self.parent = parent

    def get(self, name: str):
        if name in self.values:
            return self.values[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"Variable '{name}' not found.")

    def set(self, name: str, value: Any):
        self.values[name] = value

    def __repr__(self):
        return f"<Env keys={list(self.values.keys())} parent={self.parent is not None}>"

@dataclass
class Closure:
    params: List[str]
    body: Expr
    env: Environment

    def __repr__(self):
        return f"<Closure params={self.params}>"

def evaluate(node: Expr, env: Environment) -> Any:
    match node:
        case Literal(value):
            return value
            
        case Identifier(name):
            return env.get(name)
            
        case BinaryOp(left, op, right):
            l_val = evaluate(left, env)
            r_val = evaluate(right, env)
            
            if op == '+': return l_val + r_val
            if op == '-': return l_val - r_val
            if op == '*': return l_val * r_val
            if op == '/': return l_val // r_val # Integer division
            if op == '==': return l_val == r_val
            if op == '<': return l_val < r_val
            if op == '>': return l_val > r_val
            raise ValueError(f"Unknown operator {op}")

        case IfElse(cond, t_branch, f_branch):
            if evaluate(cond, env):
                return evaluate(t_branch, env)
            return evaluate(f_branch, env)

        case FunctionDef(params, body):
            # Capture current environment for closure
            return Closure(params, body, env)

        case FunctionCall(func_expr, arg_exprs):
            func = evaluate(func_expr, env)
            if not isinstance(func, Closure):
                raise TypeError(f"'{func}' is not a function")
            
            if len(arg_exprs) != len(func.params):
                raise TypeError(f"Expected {len(func.params)} args, got {len(arg_exprs)}")

            # Evaluate arguments in the *current* scope
            arg_values = [evaluate(arg, env) for arg in arg_exprs]

            # Create call scope:
            # Parent is the CLOSURE'S captured env (Lexical Scoping), not the caller's env.
            call_env = Environment(parent=func.env)
            for param, val in zip(func.params, arg_values):
                call_env.set(param, val)
            
            return evaluate(func.body, call_env)

        case Let(bindings, body):
            # Recursive scope: definitions can see each other and themselves
            new_env = Environment(parent=env)
            
            # First pass: evaluate bindings in the new_env
            # Note: For function definitions, they will capture new_env.
            # Since new_env is mutable, the reference works even if 'set' happens later.
            for b in bindings:
                val = evaluate(b.value, new_env)
                new_env.set(b.name, val)
                
            return evaluate(body, new_env)

        case Where(body, bindings):
            # Semantically identical to Let
            new_env = Environment(parent=env)
            for b in bindings:
                val = evaluate(b.value, new_env)
                new_env.set(b.name, val)
            return evaluate(body, new_env)

    raise ValueError(f"Unknown node type: {node}")
