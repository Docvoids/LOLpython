from . import ast_nodes as ast
from .errors import InterpreterError


class ReturnSignal(Exception):
    def __init__(self, value): self.value = value


class LOLInstance:
    def __init__(self, class_def: ast.ClassDefNode):
        self.class_def = class_def
        self.fields = {}

    def __str__(self):
        return f"[instance of {self.class_def.name}]"


class LOLCallable:
    def __init__(self, func_def: ast.FuncDefNode, instance=None):
        self.func_def = func_def
        self.instance = instance

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

    def has(self, name):
        return name in self.variables


class Interpreter:
    def __init__(self):
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.current_instance = None

    def interpret(self, node: ast.ASTNode):
        method_name = f'_visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self._generic_visit)
        return visitor(node)

    def _evaluate_and_call(self, node):
        value = self.interpret(node)
        if isinstance(value, LOLCallable):
            if not value.func_def.params:
                return self._execute_function(value.func_def, [], instance=value.instance)
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
        elif isinstance(target, ast.MemberAccessNode):
            obj = self.interpret(target.object)
            if not isinstance(obj, LOLInstance):
                raise InterpreterError("Can only assign to properties of an instance.")
            obj.fields[target.member.name] = value
        elif isinstance(target, ast.BukkitAccessNode):
            bukkit_obj = self._evaluate_and_call(target.bukkit)
            if not isinstance(bukkit_obj, list):
                raise InterpreterError("Can only perform indexed assignment on a BUKKIT.")
            index = self._evaluate_and_call(target.index)
            if not isinstance(index, int):
                raise InterpreterError("BUKKIT index must be a NUMBR.")
            while len(bukkit_obj) <= index:
                bukkit_obj.append(None)
            bukkit_obj[index] = value
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
            if val is None:
                outputs.append("NOOB")
            elif isinstance(val, bool):
                outputs.append("WIN" if val else "FAIL")
            elif isinstance(val, LOLInstance):
                outputs.append(str(val))
            elif isinstance(val, list):
                outputs.append(f"[BUKKIT of {len(val)} items]")
            else:
                outputs.append(str(val))
        print(" ".join(outputs))

    def _visit_BinaryOpNode(self, node: ast.BinaryOpNode):
        left_val = self._evaluate_and_call(node.left)
        right_val = self._evaluate_and_call(node.right)
        if node.op in ('SUM_OF', 'DIFF_OF', 'PRODUKT_OF', 'QUOSHUNT_OF'):
            if not isinstance(left_val, (int, float)) or not isinstance(right_val, (int, float)):
                raise InterpreterError(
                    f"Arithmetic operations require NUMBRs, but got {type(left_val)} and {type(right_val)}"
                )
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
            raise InterpreterError(f"'{name}' is not a function or method.")
        return self._execute_function(callee.func_def, node.args, instance=callee.instance)

    def _visit_FuncDefNode(self, node: ast.FuncDefNode):
        self.current_scope.set(node.name, node)

    def _visit_ClassDefNode(self, node: ast.ClassDefNode):
        self.current_scope.set(node.name, node)

    def _visit_IfNode(self, node: ast.IfNode):
        condition_val = self._evaluate_and_call(node.condition)
        is_true = condition_val not in (False, None)
        if is_true:
            for stmt in node.if_block:
                self.interpret(stmt)
        elif node.else_block is not None:
            for stmt in node.else_block:
                self.interpret(stmt)

    def _visit_BukkitNode(self, node: ast.BukkitNode):
        return []

    def _visit_BukkitAccessNode(self, node: ast.BukkitAccessNode):
        bukkit_obj = self._evaluate_and_call(node.bukkit)
        if not isinstance(bukkit_obj, list):
            raise InterpreterError("Can only perform indexed access on a BUKKIT.")
        index = self._evaluate_and_call(node.index)
        if not isinstance(index, int):
            raise InterpreterError("BUKKIT index must be a NUMBR.")
        if 0 <= index < len(bukkit_obj):
            return bukkit_obj[index]
        return None

    def _visit_MaekNode(self, node: ast.MaekNode):
        target_val = self._evaluate_and_call(node.target)
        if node.target_type.upper() == 'NUMBR':
            if isinstance(target_val, list):
                return len(target_val)
        raise InterpreterError(f"Cannot MAEK {type(target_val)} A {node.target_type}")

    def _execute_function(self, func_def: ast.FuncDefNode, args: list, instance=None):
        if len(args) != len(func_def.params):
            raise InterpreterError(
                f"Function '{func_def.name}' expected {len(func_def.params)} arguments, but got {len(args)}."
            )

        previous_scope, previous_instance = self.current_scope, self.current_instance
        parent_scope = self.global_scope if instance is None else previous_scope
        call_scope = Scope(parent=parent_scope)
        self.current_scope, self.current_instance = call_scope, instance

        for param, arg_expr in zip(func_def.params, args):
            arg_value = self._interpret_in_scope(arg_expr, previous_scope, previous_instance)
            self.current_scope.set(param.name, arg_value)

        return_value = None
        try:
            for stmt in func_def.body:
                self.interpret(stmt)
        except ReturnSignal as ret:
            return_value = ret.value

        self.current_scope, self.current_instance = previous_scope, previous_instance
        return return_value

    def _interpret_in_scope(self, node, scope, instance):
        original_scope, original_instance = self.current_scope, self.current_instance
        self.current_scope, self.current_instance = scope, instance
        result = self._evaluate_and_call(node)
        self.current_scope, self.current_instance = original_scope, original_instance
        return result

    def _visit_LiteralNode(self, node: ast.LiteralNode):
        return node.value

    def _visit_IdentifierNode(self, node: ast.IdentifierNode):
        var_name = node.name
        value = self.current_scope.get(var_name)
        if isinstance(value, ast.FuncDefNode):
            return LOLCallable(value)
        if value is None and not self.current_scope.has(var_name):
            raise InterpreterError(f"Undeclared variable '{var_name}'")
        return value

    def _visit_NewInstanceNode(self, node: ast.NewInstanceNode):
        class_name = node.class_name.name
        class_def = self.current_scope.get(class_name)
        if not isinstance(class_def, ast.ClassDefNode):
            raise InterpreterError(f"'{class_name}' is not a class.")
        instance = LOLInstance(class_def)
        for prop in class_def.properties:
            value = self.interpret(prop.initializer) if prop.initializer else None
            instance.fields[prop.name] = value
        return instance

    def _visit_MemberAccessNode(self, node: ast.MemberAccessNode):
        obj = self.interpret(node.object)
        if not isinstance(obj, LOLInstance):
            raise InterpreterError("Can only access properties or methods on an instance.")
        member_name = node.member.name
        for method in obj.class_def.methods:
            if method.name == member_name:
                return LOLCallable(method, instance=obj)
        if member_name in obj.fields:
            return obj.fields[member_name]
        raise InterpreterError(f"Instance of '{obj.class_def.name}' has no property or method named '{member_name}'.")

    def _visit_MeNode(self, node: ast.MeNode):
        if self.current_instance is None:
            raise InterpreterError("'ME' can only be used inside a method.")
        return self.current_instance
