# LetWhere/parser.py
from pyparsec.Parsec import Parsec
from pyparsec.Token import TokenParser, LanguageDef
from pyparsec.Prim import pure, lazy, run_parser, try_parse
from pyparsec.Char import one_of, alpha_num, char, letter
from pyparsec.Combinators import sep_by, many1, option_maybe
from pyparsec.Expr import build_expression_parser, Infix, Prefix, Assoc # <--- Added Prefix

from .ast_nodes import *

# 1. Lexer Configuration
def_lang = LanguageDef(
    comment_line="--",
    ident_start=letter(),
    ident_letter=alpha_num() | char('_'),
    reserved_names=[
        "let", "in", "where", "if", "then", "else", 
        "True", "False"
    ],
    reserved_op_names=["+", "-", "*", "/", "=", "==", "<", ">", "\\", "->", ";"],
    op_start=one_of("+-*/=<>;\\-"),
    op_letter=one_of("+-*/=<>;\\->")
)

lexer = TokenParser(def_lang)

parens = lexer.parens
braces = lexer.braces
reserved = lexer.reserved
reserved_op = lexer.reserved_op
identifier = lexer.identifier
integer = lexer.integer
natural = lexer.natural
white_space = lexer.white_space

# 2. Forward Declarations
def expr_wrapper():
    return expression()

# 3. Atoms
def literal():
    return (reserved("True") >> pure(Literal(True))) | \
           (reserved("False") >> pure(Literal(False))) | \
           natural.map(Literal)

def variable():
    return try_parse(identifier.map(Identifier))

def atom():
    return parens(lazy(expr_wrapper)) | literal() | variable()

# 4. Application
def application_term():
    def fold_app(atoms):
        head = atoms[0]
        rest = atoms[1:]
        curr = head
        for arg in rest:
            curr = FunctionCall(curr, [arg])
        return curr

    return many1(atom()).map(fold_app)

# 5. Arithmetic
def make_binary(op_str):
    def op(left, right):
        return BinaryOp(left, op_str, right)
    return op

def make_neg():
    # Helper to convert -x to (0 - x)
    def op(val):
        return BinaryOp(Literal(0), "-", val)
    return op

op_table = [
    # Prefix negation (e.g., -5, -(x+y))
    [Prefix(reserved_op("-") >> pure(make_neg()))],
    [Infix(reserved_op("*") >> pure(make_binary("*")), Assoc.LEFT),
     Infix(reserved_op("/") >> pure(make_binary("/")), Assoc.LEFT)],
    [Infix(reserved_op("+") >> pure(make_binary("+")), Assoc.LEFT),
     Infix(reserved_op("-") >> pure(make_binary("-")), Assoc.LEFT)],
    [Infix(reserved_op("==") >> pure(make_binary("==")), Assoc.LEFT),
     Infix(reserved_op("<") >> pure(make_binary("<")), Assoc.LEFT),
     Infix(reserved_op(">") >> pure(make_binary(">")), Assoc.LEFT)],
]

def arithmetic_expr():
    return build_expression_parser(op_table, application_term())

# 6. Structure Parsers
def lambda_def():
    # Helper to transform \x y z -> body INTO \x -> \y -> \z -> body
    def make_curried(params, body):
        curr = body
        # Iterate backwards to wrap body: \z -> body, then \y -> (\z -> body)...
        for p in reversed(params):
            curr = FunctionDef([p], curr)
        return curr

    return (reserved_op("\\") >> 
            many1(identifier).bind(lambda params:
            reserved_op("->") >>
            lazy(expr_wrapper).map(lambda body: 
            make_curried(params, body))))

def if_expr():
    return (reserved("if") >> lazy(expr_wrapper).bind(lambda cond:
            reserved("then") >> lazy(expr_wrapper).bind(lambda tr:
            reserved("else") >> lazy(expr_wrapper).map(lambda fl:
            IfElse(cond, tr, fl)))))

def binding():
    return identifier.bind(lambda name:
           reserved_op("=") >>
           lazy(expr_wrapper).map(lambda val:
           Binding(name, val)))

def let_expr():
    return (reserved("let") >> 
            sep_by(binding(), reserved_op(";")).bind(lambda binds:
            reserved("in") >> 
            lazy(expr_wrapper).map(lambda body:
            Let(binds, body))))

# 7. Core Term
def core_term():
    return lambda_def() | if_expr() | let_expr() | arithmetic_expr()

# 8. Top Level Expression
def expression():
    def attach_where(term_node, where_part):
        if where_part is None:
            return term_node
        return Where(term_node, where_part)

    where_clause = reserved("where") >> braces(sep_by(binding(), reserved_op(";")))

    return core_term().bind(lambda term:
           option_maybe(where_clause).map(lambda w:
           attach_where(term, w)))

main_parser = white_space >> expression()
