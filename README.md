# LetWhere

LetWhere is a Turing-complete, functional programming language designed as a reference implementation for the **PyParsec** library. It demonstrates advanced parsing concepts including recursive grammar, operator precedence, lexical scoping, and automatic currying.

## Features

*   **Haskell-style Syntax**: Clean, minimalist syntax using `let`, `in`, and `where` bindings.
*   **Turing Complete**: Supports deep recursion and high-order functions (proven via the Ackermann function).
*   **Automatic Currying**: All multi-argument functions are automatically transformed into nested single-argument closures.
*   **Operator Precedence**: Correct mathematical order of operations (e.g., multiplication binds tighter than addition, function application binds tighter than math).
*   **Lexical Scoping**: Closures capture their definition environment.

## Installation

This project is managed using `uv`.

1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/LetWhere.git
    cd LetWhere
    ```

2.  Sync dependencies and install the project in editable mode:
    ```bash
    uv sync
    uv pip install -e .
    ```

## Usage

### The REPL
Start the interactive shell by running the command without arguments:

```bash
uv run letwhere
```

### Execute a File
Run a source file (`.lw` extension recommended):

```bash
uv run letwhere examples/01_factorial.lw
```

### Direct Evaluation
Evaluate a single expression from the command line:

```bash
uv run letwhere -e "(\x -> x * 2) 21"
```

## Language Guide

### 1. Variables and Bindings
Variables are immutable. You can define them using `let` (prefix) or `where` (postfix).

**Let-style:**
```haskell
let x = 10;
    y = 20
in x + y
```

**Where-style:**
```haskell
x + y
where {
    x = 10;
    y = 20
}
```

### 2. Functions
Functions are first-class citizens. Multi-argument functions are supported via currying.

```haskell
-- Definition
let add = \x y -> x + y in

-- Application
add 10 20
```

### 3. Control Flow
Standard `if-then-else` constructs.

```haskell
if x < 10 then 100 else 200
```

### 4. Comments
Use `--` for single-line comments.

```haskell
-- This is a comment
let x = 1 in x
```

## Examples

Check the `examples/` directory for demonstrations of the language's power:

*   `01_factorial.lw`: Basic recursion.
*   `02_fibonacci.lw`: Tree recursion with `where` blocks.
*   `03_turing_ackermann.lw`: Proof of Turing completeness (deep recursion).
*   `04_cons_pairs.lw`: Implementation of data structures (pairs) using pure functions (Church encoding).

## Development

To run the test suite:

```bash
uv run pytest tests
```
