from dataclasses import dataclass
from typing import List

@dataclass
class ASTNode: pass

@dataclass
class StatementNode(ASTNode): pass

@dataclass
class ProgramNode(ASTNode):
    statements: List[StatementNode]
