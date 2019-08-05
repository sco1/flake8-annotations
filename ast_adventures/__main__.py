import ast

from ast_adventures import FunctionVisitor


with open("test.py", "r") as f:
    tree = ast.parse(f.read())

function_metadata = FunctionVisitor()
function_metadata.visit(tree)

with open("./test_output.txt", "w") as f:
    for fun in function_metadata.definitions:
        f.write(f"{fun}\n")
