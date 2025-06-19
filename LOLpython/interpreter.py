from . import ast_nodes as ast
from .errors import InterpreterError

class Interpreter:
    def __init__(self):
        pass

    def interpret(self, node: ast.ASTNode):
        method_name = f'_visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self._generic_visit)
        return visitor(node)

    def _generic_visit(self, node):
        raise InterpreterError(f"No _visit_{type(node).__name__} method")

    def _visit_ProgramNode(self, node: ast.ProgramNode):
        # Поки що нічого не робимо
        return None
