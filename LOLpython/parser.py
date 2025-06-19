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

    def parse(self) -> ast.ProgramNode:
        self._eat('HAI')
        statements = [] # Поки що завжди порожній список
        self._eat('KTHXBYE')
        self._eat('EOF')
        return ast.ProgramNode(statements=statements)
