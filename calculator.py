import ast
import operator

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

def evaluate(expr):
    def _eval(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        elif isinstance(node, ast.BinOp):
            op_fn = OPERATORS.get(type(node.op))  # type: ignore[call-overload, arg-type]
            if op_fn is None:
                raise ValueError(f"Unsupported operator: {node.op}")
            left, right = _eval(node.left), _eval(node.right)
            if isinstance(node.op, ast.Div) and right == 0:
                raise ValueError("Cannot divide by zero.")
            return op_fn(left, right)
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return operator.neg(_eval(node.operand))
        else:
            raise ValueError("Invalid expression.")

    tree = ast.parse(expr, mode='eval')
    return _eval(tree.body)

def main():
    print("=== Calculator ===")
    print("Operators: + - * / **  Grouping: ( )")
    print("Enter 'q' to quit, 'h' to view history\n")

    history = []

    while True:
        expr = input("Enter expression (e.g. (3+4)*2): ").strip()
        if expr.lower() == 'q':
            break
        if expr.lower() == 'h':
            if not history:
                print("No history yet.\n")
            else:
                print("=== Recent History ===")
                for entry in history:
                    print(f"  {entry}")
                print()
            continue

        try:
            result = evaluate(expr)
            print(f"Result: {result}\n")
            history.append(f"{expr} = {result}")
            if len(history) > 5:
                history.pop(0)
        except (ValueError, SyntaxError, TypeError) as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    main()
