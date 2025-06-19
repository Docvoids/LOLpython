import re
from collections import namedtuple
from .errors import LexerError

Token = namedtuple('Token', ['type', 'value', 'line', 'column'])

class Lexer:
    def __init__(self, code: str):
        self.code = code
        self.line = 1
        self.column = 1
        self.pos = 0

    def _get_token(self, token_specs):
        # Пропускаємо пробіли та нові рядки
        self.code = self.code.lstrip()
        self.pos = len(self.code) - len(self.code.lstrip())

        for token_type, pattern in token_specs:
            regex = re.compile(pattern)
            match = regex.match(self.code, self.pos)
            if match:
                value = match.group(0)
                token = Token(token_type, value, self.line, self.column)
                self.pos = match.end(0)
                return token
        return None

    def tokenize(self) -> list[Token]:
        tokens = []
        token_specs = [
            ('HAI', r'HAI 1\.2'),
            ('KTHXBYE', r'KTHXBYE'),
        ]

        while self.pos < len(self.code):
            # Проста логіка пропуску пробілів для початку
            if self.code[self.pos].isspace():
                if self.code[self.pos] == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.pos += 1
                continue

            token = self._get_token(token_specs)
            if token is None:
                raise LexerError(f"Unexpected character '{self.code[self.pos]}' at line {self.line}, column {self.column}")
            
            tokens.append(token)
            self.pos = token.value.__len__() # Дуже спрощено

        tokens.append(Token('EOF', 'EOF', self.line, self.column))
        return tokens
