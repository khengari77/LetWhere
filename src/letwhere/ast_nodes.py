# LetWhere/ast_nodes.py
from dataclasses import dataclass
from typing import List, Union

@dataclass
class Node:
    pass

@dataclass
class Expr(Node):
    pass

@dataclass
class Literal(Expr):
    value: Union[int, bool]

@dataclass
class Identifier(Expr):
    name: str

@dataclass
class BinaryOp(Expr):
    left: Expr
    op: str
    right: Expr

@dataclass
class IfElse(Expr):
    cond: Expr
    true_branch: Expr
    false_branch: Expr

@dataclass
class FunctionDef(Expr):
    params: List[str]
    body: Expr

@dataclass
class FunctionCall(Expr):
    func: Expr
    args: List[Expr]

@dataclass
class Binding:
    name: str
    value: Expr

@dataclass
class Let(Expr):
    bindings: List[Binding]
    body: Expr

@dataclass
class Where(Expr):
    body: Expr
    bindings: List[Binding]
