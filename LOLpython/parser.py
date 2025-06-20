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
        if token_type == 'I_HAS_A':
            return self._parse_var_decl()
        if token_type == 'VISIBLE':
            return self._parse_visible()
        raise ParserError(f"Unexpected statement token: {self._current()}")

    def _parse_expression(self):
        token = self._current()
        if token.type in ('NUMBR', 'YARN', 'TROOF'):
            return self._parse_literal()
        if token.type == 'IDENTIFIER':
            return ast.IdentifierNode(name=self._advance().value)
        raise ParserError(f"Unexpected token when parsing an expression: {token}")

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
        # Поки що підтримуємо тільки один вираз
        return ast.VisibleNode(expressions=expressions)

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
