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
        for token_type, pattern in token_specs:
            regex = re.compile(pattern)
            match = regex.match(self.code, self.pos)
            if match:
                value = match.group(0)
                token = Token(token_type, value, self.line, self.column)
                self.pos = match.end(0)
                lines = value.split('\n')
                if len(lines) > 1:
                    self.line += len(lines) - 1
                    self.column = len(lines[-1]) + 1
                else:
                    self.column += len(value)
                return token
        return None

    def tokenize(self) -> list[Token]:
        tokens = []
        token_specs = [
            ('SKIP', r'[ \t]+'),
            ('NEWLINE', r'\n+'),
            ('COMMENT', r'BTW.*'),

            ('O_RLY', r'O RLY\?'),
            ('YA_RLY', r'YA RLY'),
            ('NO_WAI', r'NO WAI'),
            ('OIC', r'OIC'),

            ('HOW_IZ_I', r'HOW IZ I'),
            ('IF_U_SAY_SO', r'IF U SAY SO'),
            ('FOUND_YR', r'FOUND YR'),
            ('HOW_DUZ_I', r'HOW DUZ I'),
            ('YR', r'YR'),

            ('HAI', r'HAI 1\.2'),
            ('KTHXBYE', r'KTHXBYE'),
            ('KTHX', r'KTHX'),
            ('I_HAS_A', r'I HAS A'),
            ('ITZ', r'ITZ'),
            ('R', r'R'),
            ('SUM_OF', r'SUM OF'),
            ('DIFF_OF', r'DIFF OF'),
            ('PRODUKT_OF', r'PRODUKT OF'),
            ('QUOSHUNT_OF', r'QUOSHUNT OF'),
            ('BOTH_SAEM', r'BOTH SAEM'),
            ('DIFFRINT', r'DIFFRINT'),
            ('AN', r'AN'),
            ('VISIBLE', r'VISIBLE'),
            
            ('YARN', r'"[^"]*"'),
            ('NUMBR', r'-?\d+\.\d+|-?\d+'),
            ('TROOF', r'WIN|FAIL'),
            ('IDENTIFIER', r'[a-zA-Z][a-zA-Z0-9_]*'),
        ]

        while self.pos < len(self.code):
            token = self._get_token(token_specs)
            if token is None:
                raise LexerError(f"Unexpected character '{self.code[self.pos]}' at line {self.line}, column {self.column}")
            if token.type != 'SKIP':
                tokens.append(token)
        tokens.append(Token('EOF', 'EOF', self.line, self.column))
        return tokens
        
