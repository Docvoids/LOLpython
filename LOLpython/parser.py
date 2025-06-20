from . import ast_nodes as ast
from .errors import ParserError

class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.pos = 0

    def _current(self):
        return self.tokens[self.pos]

    def _advance(self):
        self.pos += 1
        return self.tokens[self.pos - 1]

    def _eat(self, token_type):
        token = self._current()
        if token.type == token_type:
            return self._advance()
        raise ParserError(f"Expected token {token_type} but got {token.type} at line {token.line}")

    def _consume_whitespace(self):
        while self._current().type in ('NEWLINE', 'COMMENT'):
            self._advance()

    def parse(self) -> ast.ProgramNode:
        self._eat('HAI')
        self._consume_whitespace()
        statements = self._parse_statement_list(('KTHXBYE',))
        self._eat('KTHXBYE')
        self._eat('EOF')
        return ast.ProgramNode(statements=statements)

    def _parse_statement_list(self, terminators: tuple):
        statements = []
        self._consume_whitespace()
        while self._current().type not in terminators + ('EOF',):
            statements.append(self._parse_statement())
            self._consume_whitespace()
        return statements

    def _parse_statement(self):
        token_type = self._current().type
        if token_type == 'I_HAS_A': return self._parse_var_decl()
        if token_type == 'VISIBLE': return self._parse_visible()
        if token_type == 'HOW_IZ_I': return self._parse_func_def()
        if token_type == 'FOUND_YR': return self._parse_return()
        
        expr = self._parse_expression()
        self._consume_whitespace()
        if self._current().type == 'R':
            self._eat('R')
            value = self._parse_expression()
            if not isinstance(expr, ast.IdentifierNode):
                raise ParserError("Invalid assignment target.")
            return ast.AssignmentNode(target=expr, expression=value)
        
        if isinstance(expr, ast.FuncCallNode):
            return expr

        raise ParserError(f"Invalid statement structure starting with {expr} at line {self._current().line}.")

    def _parse_expression(self):
        token_type = self._current().type
        if token_type in ('SUM_OF', 'DIFF_OF', 'PRODUKT_OF', 'QUOSHUNT_OF', 'BOTH_SAEM', 'DIFFRINT'):
            op_token = self._advance()
            left = self._parse_postfix_expression()
            self._eat('AN')
            right = self._parse_postfix_expression()
            return ast.BinaryOpNode(left=left, op=op_token.type, right=right)
        return self._parse_postfix_expression()

    def _parse_postfix_expression(self):
        expr = self._parse_primary()
        while True:
            if self._current().type == 'YR':
                expr = self._finish_call(expr)
            else:
                break
        return expr

    def _parse_primary(self):
        token = self._current()
        if token.type in ('NUMBR', 'YARN', 'TROOF'):
            return self._parse_literal()
        if token.type == 'IDENTIFIER':
            return ast.IdentifierNode(name=self._advance().value)
        raise ParserError(f"Unexpected token when parsing a primary expression: {token}")

    def _parse_var_decl(self):
        self._eat('I_HAS_A')
        name = self._eat('IDENTIFIER').value
        initializer = None
        if self._current().type == 'ITZ':
            self._eat('ITZ')
            initializer = self._parse_expression()
        return ast.VarDeclNode(name=name, initializer=initializer)

    def _parse_visible(self):
        self._eat('VISIBLE')
        expressions = [self._parse_expression()]
        terminators = ('NEWLINE', 'EOF', 'KTHXBYE', 'COMMENT', 'IF_U_SAY_SO')
        while self._current().type not in terminators:
            expressions.append(self._parse_expression())
        return ast.VisibleNode(expressions=expressions)

    def _parse_func_def(self):
        self._eat('HOW_IZ_I')
        name = self._eat('IDENTIFIER').value
        params = []
        if self._current().type == 'YR':
            self._eat('YR')
            params.append(ast.IdentifierNode(name=self._eat('IDENTIFIER').value))
            while self._current().type == 'AN':
                self._eat('AN')
                self._eat('YR')
                params.append(ast.IdentifierNode(name=self._eat('IDENTIFIER').value))
        self._consume_whitespace()
        body = self._parse_statement_list(('IF_U_SAY_SO',))
        self._eat('IF_U_SAY_SO')
        return ast.FuncDefNode(name=name, params=params, body=body)

    def _parse_return(self):
        self._eat('FOUND_YR')
        value = None
        terminators = ('NEWLINE', 'COMMENT', 'IF_U_SAY_SO')
        if self._current().type not in terminators:
            value = self._parse_expression()
        return ast.ReturnNode(value=value)

    def _finish_call(self, callee):
        args = []
        if self._current().type == 'YR':
            self._eat('YR')
            # Перевірка, чи є аргументи після YR
            if self._current().type not in ('NEWLINE', 'COMMENT', 'R', 'IF_U_SAY_SO', 'KTHXBYE'):
                args.append(self._parse_expression())
                while self._current().type == 'AN':
                    self._eat('AN')
                    self._eat('YR')
                    args.append(self._parse_expression())
        return ast.FuncCallNode(callee=callee, args=args)

    def _parse_literal(self):
        token = self._advance()
        if token.type == 'NUMBR':
            val = token.value
            return ast.LiteralNode(value=int(val) if '.' not in val else float(val))
        if token.type == 'YARN':
            return ast.LiteralNode(value=token.value[1:-1])
        if token.type == 'TROOF':
            return ast.LiteralNode(value=True if token.value == 'WIN' else False)
        raise ParserError(f"Invalid literal token: {token}")
