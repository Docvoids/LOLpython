from . import ast_nodes as ast
from .errors import InterpreterError

class ReturnSignal(Exception):
    def __init__(self, value): self.value = value

class LOLCallable:
    def __init__(self, func_def: ast.FuncDefNode):
        self.func_def = func_def
    def __str__(self):
        return f"[callable {self.func_def.name}]"

class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.variables = {}
    def get(self, name):
        if name in self.variables: return self.variables[name]
        if self.parent: return self.parent.get(name)
        return None
    def set(self, name, value):
        self.variables[name] = value
    def has(self, name): return name in self.variables

class Interpreter:
    def __init__(self):
        self.global_scope = Scope()
        self.current_scope = self.global_scope

    def interpret(self, node: ast.ASTNode):
        method_name = f'_visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self._generic_visit)
        return visitor(node)

    def _evaluate_and_call(self, node):
        value = self.interpret(node)
        if isinstance(value, LOLCallable):
            if not value.func_def.params:
                return self._execute_function(value.func_def, [])
        return value

    def _generic_visit(self, node):
        raise InterpreterError(f"No _visit_{type(node).__name__} method")

    def _visit_ProgramNode(self, node: ast.ProgramNode):
        try:
            for statement in node.statements:
                self.interpret(statement)
        except ReturnSignal:
            raise InterpreterError("Return statement ('FOUND YR') outside of a function")

    def _visit_AssignmentNode(self, node: ast.AssignmentNode):
        value = self._evaluate_and_call(node.expression)
        target = node.target
        if isinstance(target, ast.IdentifierNode):
            var_name = target.name
            scope = self.current_scope
            while scope:
                if scope.has(var_name):
                    scope.set(var_name, value)
                    return
                scope = scope.parent
            raise InterpreterError(f"Undeclared variable '{var_name}'")
        else:
            raise InterpreterError("Invalid assignment target.")

    def _visit_VarDeclNode(self, node: ast.VarDeclNode):
        if self.current_scope.has(node.name):
            raise InterpreterError(f"Variable '{node.name}' already declared.")
        value = None
        if node.initializer:
            value = self._evaluate_and_call(node.initializer)
        self.current_scope.set(node.name, value)

    def _visit_VisibleNode(self, node: ast.VisibleNode):
        outputs = []
        for expr in node.expressions:
            val = self._evaluate_and_call(expr)
            if val is None: outputs.append("NOOB")
            elif isinstance(val, bool): outputs.append("WIN" if val else "FAIL")
            else: outputs.append(str(val))
        print(" ".join(outputs))

    def _visit_BinaryOpNode(self, node: ast.BinaryOpNode):
        left_val = self._evaluate_and_call(node.left)
        right_val = self._evaluate_and_call(node.right)
        if node.op in ('SUM_OF', 'DIFF_OF', 'PRODUKT_OF', 'QUOSHUNT_OF'):
            if not isinstance(left_val, (int, float)) or not isinstance(right_val, (int, float)):
                raise InterpreterError(f"Arithmetic operations require NUMBRs, but got {type(left_val)} and {type(right_val)}")
        if node.op == 'SUM_OF': return left_val + right_val
        if node.op == 'DIFF_OF': return left_val - right_val
        if node.op == 'PRODUKT_OF': return left_val * right_val
        if node.op == 'QUOSHUNT_OF':
            if right_val == 0: raise InterpreterError("Division by zero")
            return left_val / right_val
        if node.op == 'BOTH_SAEM': return left_val == right_val
        if node.op == 'DIFFRINT': return left_val != right_val
        raise InterpreterError(f"Unknown binary operator: {node.op}")

    def _visit_ReturnNode(self, node: ast.ReturnNode):
        value = self._evaluate_and_call(node.value) if node.value else None
        raise ReturnSignal(value)

    def _visit_FuncCallNode(self, node: ast.FuncCallNode):
        callee = self.interpret(node.callee)
        if not isinstance(callee, LOLCallable):
            name = getattr(node.callee, 'name', '[unknown]')
            raise InterpreterError(f"'{name}' is not a function.")
        return self._execute_function(callee.func_def, node.args)

    def _visit_FuncDefNode(self, node: ast.FuncDefNode):
        self.current_scope.set(node.name, LOLCallable(node))

    def _visit_IfNode(self, node: ast.IfNode):
        condition_val = self._evaluate_and_call(node.condition)
        is_true = condition_val not in (False, None)
        if is_true:
            for stmt in node.if_block:
                self.interpret(stmt)
        elif node.else_block is not None:
            for stmt in node.else_block:
                self.interpret(stmt)

    def _execute_function(self, func_def: ast.FuncDefNode, args: list):
        if len(args) != len(func_def.params):
            raise InterpreterError(f"Function '{func_def.name}' expected {len(func_def.params)} arguments, but got {len(args)}.")
        
        previous_scope = self.current_scope
        call_scope = Scope(parent=self.global_scope)
        self.current_scope = call_scope

        for param, arg_expr in zip(func_def.params, args):
            arg_value = self._interpret_in_scope(arg_expr, previous_scope)
            self.current_scope.set(param.name, arg_value)
        
        return_value = None
        try:
            for stmt in func_def.body:
                self.interpret(stmt)
        except ReturnSignal as ret:
            return_value = ret.value
        
        self.current_scope = previous_scope
        return return_value

    def _interpret_in_scope(self, node, scope):
        original_scope = self.current_scope
        self.current_scope = scope
        result = self._evaluate_and_call(node)
        self.current_scope = original_scope
        return result

    def _visit_LiteralNode(self, node: ast.LiteralNode):
        return node.value

    def _visit_IdentifierNode(self, node: ast.IdentifierNode):
        var_name = node.name
        value = self.current_scope.get(var_name)
        if value is None and not self.current_scope.has(var_name):
            raise InterpreterError(f"Undeclared variable '{var_name}'")
        return value
        
