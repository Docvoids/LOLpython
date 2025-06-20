from . import ast_nodes as ast
from .errors import InterpreterError

class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.variables = {}

    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        return None

    def set(self, name, value):
        self.variables[name] = value

    def has(self, name):
        return name in self.variables

class Interpreter:
    def __init__(self):
        self.global_scope = Scope()
        self.current_scope = self.global_scope

    def interpret(self, node: ast.ASTNode):
        method_name = f'_visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self._generic_visit)
        return visitor(node)

    def _generic_visit(self, node):
        raise InterpreterError(f"No _visit_{type(node).__name__} method")

    def _visit_ProgramNode(self, node: ast.ProgramNode):
        for statement in node.statements:
            self.interpret(statement)

    def _visit_VarDeclNode(self, node: ast.VarDeclNode):
        if self.current_scope.has(node.name):
            raise InterpreterError(f"Variable '{node.name}' already declared.")
        value = None
        if node.initializer:
            value = self.interpret(node.initializer)
        self.current_scope.set(node.name, value)

    def _visit_VisibleNode(self, node: ast.VisibleNode):
        outputs = []
        for expr in node.expressions:
            val = self.interpret(expr)
            if val is None:
                outputs.append("NOOB")
            elif isinstance(val, bool):
                outputs.append("WIN" if val else "FAIL")
            else:
                outputs.append(str(val))
        print(" ".join(outputs))

    def _visit_LiteralNode(self, node: ast.LiteralNode):
        return node.value

    def _visit_IdentifierNode(self, node: ast.IdentifierNode):
        var_name = node.name
        value = self.current_scope.get(var_name)
        if value is None and not self.current_scope.has(var_name):
            raise InterpreterError(f"Undeclared variable '{var_name}'")
        return value
