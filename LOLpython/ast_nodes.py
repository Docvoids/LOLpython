from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class ASTNode: pass

@dataclass
class ExpressionNode(ASTNode): pass

@dataclass
class LiteralNode(ExpressionNode):
    value: Any

@dataclass
class IdentifierNode(ExpressionNode):
    name: str

@dataclass
class StatementNode(ASTNode): pass

@dataclass
class ProgramNode(ASTNode):
    statements: List[StatementNode]

@dataclass
class VarDeclNode(StatementNode):
    name: str
    initializer: Optional[ExpressionNode]

@dataclass
class VisibleNode(StatementNode):
    expressions: List[ExpressionNode]
