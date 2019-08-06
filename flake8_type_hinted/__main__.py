import ast
from pathlib import Path

from flake8_type_hinted import FunctionVisitor

test_file = Path("./test.py")
with test_file.open("r") as f:
    tree = ast.parse(f.read())

function_metadata = FunctionVisitor()
function_metadata.visit(tree)

output_file = Path("./test_output.txt")
with output_file.open("w") as f:
    for fun in function_metadata.function_definitions:
        f.write(f"{fun}\n")
